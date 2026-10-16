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

from resumebot.answering import Answerer  # noqa: E402
from resumebot.corpus import load_corpus  # noqa: E402
from resumebot.embeddings import FastEmbedEmbedder  # noqa: E402
from resumebot.llm import build_llm  # noqa: E402
from resumebot.presentation import format_answer  # noqa: E402
from resumebot.reranking import FastEmbedReranker  # noqa: E402
from resumebot.retrieval import Retriever  # noqa: E402

DESCRIPTION = """\
Ask about Kheirie El Hariri's experience, skills, education, projects, and writing.
Answers come only from Kheirie's approved materials and list their sources.
When something is not documented, the assistant says so instead of guessing.
"""

EXAMPLES = [
    "What NLP work has Kheirie done, and with what results?",
    "Has Kheirie built a RAG system?",
    "What teaching or coaching experience does Kheirie have?",
    "What degrees does Kheirie hold?",
    "Has Kheirie used Docker in a job?",
]

retriever = Retriever(load_corpus(ROOT / "corpus" / "approved"), FastEmbedEmbedder(), reranker=FastEmbedReranker())
answerer = Answerer(retriever, build_llm(os.environ.get("LLM_PROVIDER", "chain")))


def respond(message: str, history: list) -> str:
    # Each question is answered on its own; earlier turns are not sent to the model.
    return format_answer(answerer.ask(message))


demo = gr.ChatInterface(
    fn=respond,
    title="Ask about Kheirie El Hariri",
    description=DESCRIPTION,
    examples=EXAMPLES,
    concurrency_limit=2,  # the free Groq tier allows only a few questions per minute
)

if __name__ == "__main__":
    demo.launch()
