"""Web chat for recruiters (Gradio). Run locally with `python app.py`.

Deliberately thin: all the logic lives in the tested `resumebot` package. The
retriever and the LLM are built once at startup and shared by every chat.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))  # lets Hugging Face Spaces import the package without installing it

import gradio as gr  # noqa: E402

from resumebot.answering import MAX_QUESTION_CHARS, Answerer, CachedAnswerer  # noqa: E402
from resumebot.chat import AI_ANSWERS_PER_DAY, Chat, PassageAnswerer, QuestionQuota, visitor_id  # noqa: E402
from resumebot.corpus import load_corpus  # noqa: E402
from resumebot.embeddings import FastEmbedEmbedder  # noqa: E402
from resumebot.llm import LLMConfigError, build_llm  # noqa: E402
from resumebot.presentation import format_answer  # noqa: E402
from resumebot.reranking import FastEmbedReranker  # noqa: E402
from resumebot.retrieval import Retriever  # noqa: E402

DESCRIPTION = f"""\
Ask about Kheirie El Hariri's experience, skills, education, projects, and writing.
Answers come only from Kheirie's approved materials.
When something is not documented, the assistant says so instead of guessing.
Each visitor gets {AI_ANSWERS_PER_DAY} AI answers per day; after that, the chat shows the best-matching passages.
"""

# A line under each answer naming the model that wrote it (the fallback chain can switch models).
SHOW_MODEL = os.environ.get("SHOW_MODEL", "1") == "1"

EXAMPLES = [
    "What NLP work has Kheirie done, and with what results?",
    "Has Kheirie built a RAG system?",
    "What teaching or coaching experience does Kheirie have?",
    "What degrees does Kheirie hold?",
    "Has Kheirie used Docker in a job?",
]

retriever = Retriever(load_corpus(ROOT / "corpus" / "approved"), FastEmbedEmbedder(), reranker=FastEmbedReranker())
# Repeated questions (such as the examples below) are answered from memory at no token cost.
try:
    llm = build_llm(os.environ.get("LLM_PROVIDER", "chain"))
except LLMConfigError:  # no API key set (e.g. a new Space before its secrets): passages only
    llm = None
answerer = CachedAnswerer(Answerer(retriever, llm)) if llm else None
# Three AI answers per visitor per day, then passages only (portfolio budget).
chat = Chat(answerer, PassageAnswerer(retriever), QuestionQuota())


def models_in_order() -> str:
    """The models the app tries, primary first: "1. gpt-oss-120b (groq) · 2. ..."."""
    if llm is None:
        return "none configured, passages only"
    labels = [m.label for m in getattr(llm, "_llms", [llm])]  # a chain, or one provider
    return " · ".join(f"{i}. {lab.partition(':')[2]} ({lab.partition(':')[0]})" for i, lab in enumerate(labels, 1))


def respond(message: str, history: list, request: gr.Request) -> str:
    # Each question is answered on its own; earlier turns are not sent to the model.
    visitor = visitor_id(request.client.host if request.client else None, request.headers.get("x-forwarded-for"))
    answer = chat.reply(message, visitor)
    shown = format_answer(answer, show_model=SHOW_MODEL)
    if answer.answered_by and not answer.from_cache:  # this answer used one of the visitor's AI answers
        shown += f"\n\n*{chat.remaining(visitor)} of {AI_ANSWERS_PER_DAY} AI answers left today.*"
    return shown


demo = gr.ChatInterface(
    fn=respond,
    title="Ask about Kheirie El Hariri",
    description=DESCRIPTION + (f"\n\n*Models, tried in order: {models_in_order()}*" if SHOW_MODEL else ""),
    examples=EXAMPLES,
    textbox=gr.Textbox(
        placeholder=f"Ask about Kheirie's background (max {MAX_QUESTION_CHARS} characters)",
        max_length=MAX_QUESTION_CHARS,
    ),
    concurrency_limit=2,  # the free Groq tier allows only a few questions per minute
)

if __name__ == "__main__":
    demo.launch()
