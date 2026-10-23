"""Web chat for recruiters (Streamlit). Run locally with `streamlit run app.py`.

Deliberately thin: all the logic lives in the tested `resumebot` package. Streamlit re-runs
this script on every message, so the models are built once (`st.cache_resource`) and shared
by every visitor, and the conversation on screen lives in `st.session_state`.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))  # lets the host import the package without installing it

import streamlit as st  # noqa: E402

from resumebot.answering import MAX_QUESTION_CHARS, Answerer, CachedAnswerer  # noqa: E402
from resumebot.chat import AI_ANSWERS_PER_DAY, Chat, PassageAnswerer, QuestionQuota, visitor_id  # noqa: E402
from resumebot.corpus import load_corpus  # noqa: E402
from resumebot.embeddings import FastEmbedEmbedder  # noqa: E402
from resumebot.llm import LLMConfigError, build_llm  # noqa: E402
from resumebot.presentation import format_answer  # noqa: E402
from resumebot.reranking import FastEmbedReranker  # noqa: E402
from resumebot.retrieval import Retriever  # noqa: E402

DESCRIPTION = f"""\
Ask about Kerry's experience, skills, education, projects, and writing.
Answers come only from Kerry's approved materials.
When something is not documented, the assistant says so instead of guessing.
Each visitor gets {AI_ANSWERS_PER_DAY} AI answers per day; after that, the chat shows the best-matching passages.
"""

# A line under each answer naming the model that wrote it (the fallback chain can switch models).
SHOW_MODEL = os.environ.get("SHOW_MODEL", "1") == "1"

EXAMPLES = [
    "What NLP work has Kerry done, and with what results?",
    "Has Kerry built a RAG system?",
    "What teaching or coaching experience does Kerry have?",
    "What degrees does Kerry hold?",
    "Has Kerry used Docker in a job?",
]


@st.cache_resource(show_spinner="Loading the materials...")
def build_chat():
    """Built once per server process and shared by every visitor."""
    retriever = Retriever(load_corpus(ROOT / "corpus" / "approved"), FastEmbedEmbedder(), reranker=FastEmbedReranker())
    try:
        llm = build_llm(os.environ.get("LLM_PROVIDER", "chain"))
    except LLMConfigError:  # no API key set (e.g. before the host's secrets are added): passages only
        llm = None
    # Repeated questions (such as the examples) are answered from memory at no token cost.
    answerer = CachedAnswerer(Answerer(retriever, llm)) if llm else None
    # Three AI answers per visitor per day, then passages only (portfolio budget).
    return Chat(answerer, PassageAnswerer(retriever), QuestionQuota()), llm


def models_in_order(llm) -> str:
    """The models the app tries, primary first: "1. gpt-oss-120b (groq) · 2. ..."."""
    if llm is None:
        return "none configured, passages only"
    labels = [m.label for m in getattr(llm, "_llms", [llm])]  # a chain, or one provider
    return " · ".join(f"{i}. {lab.partition(':')[2]} ({lab.partition(':')[0]})" for i, lab in enumerate(labels, 1))


def reply(chat: Chat, question: str) -> str:
    # Each question is answered on its own; earlier turns are not sent to the model.
    visitor = visitor_id(st.context.ip_address, st.context.headers.get("X-Forwarded-For"))
    answer = chat.reply(question, visitor)
    shown = format_answer(answer, show_model=SHOW_MODEL)
    if answer.answered_by and not answer.from_cache:  # this answer used one of the visitor's AI answers
        shown += f"\n\n*{chat.remaining(visitor)} of {AI_ANSWERS_PER_DAY} AI answers left today.*"
    return shown


st.set_page_config(page_title="Ask about Kerry", page_icon="💬")
st.title("Ask about Kerry")
st.markdown(DESCRIPTION)
chat, llm = build_chat()
if SHOW_MODEL:
    st.caption(f"Models, tried in order: {models_in_order(llm)}")

if "messages" not in st.session_state:
    st.session_state.messages = []  # this tab's conversation, kept across Streamlit's re-runs

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

example = None
if not st.session_state.messages:
    st.caption("Try an example:")
    for text in EXAMPLES:
        if st.button(text, key=text):
            example = text

typed = st.chat_input(f"Ask about Kerry's background (max {MAX_QUESTION_CHARS} characters)", max_chars=MAX_QUESTION_CHARS)
question = typed or example
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer_text = reply(chat, question)
        st.markdown(answer_text)
    st.session_state.messages.append({"role": "assistant", "content": answer_text})
    if example:
        st.rerun()  # hide the example buttons now that the conversation has started
