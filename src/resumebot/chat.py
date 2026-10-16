"""The public chat's budget: three AI answers per visitor per day, then passages only.

Kheirie's choice for the portfolio site (2026-10-16). An AI answer costs API tokens,
so each visitor gets AI_ANSWERS_PER_DAY of them. After that, the chat shows the
passages from the approved corpus that best match the question, word for word:
free, instant, and unable to invent anything.

Only answers a model actually wrote use up the allowance. Cached answers (such as
the example questions), refusals and "not found" cost nothing, so they are free and
are served even after the limit.
"""

from __future__ import annotations

import hashlib
import secrets
import threading
from datetime import date
from typing import Callable, Protocol

from resumebot.answering import MAX_QUESTION_CHARS, NOT_FOUND, TOO_LONG, Answer
from resumebot.retrieval import SearchResult

AI_ANSWERS_PER_DAY = 3
PASSAGES_SHOWN = 2
PASSAGES_NOTE = (
    f"You have used today's {AI_ANSWERS_PER_DAY} AI answers. Here are the passages from "
    "Kheirie's approved materials that best match your question:"
)
UNAVAILABLE_NOTE = (
    "AI answers are not available right now. Here are the passages from Kheirie's approved "
    "materials that best match your question:"
)

# Visitors are recognized by a salted hash of their network address, never the address
# itself. The salt is new at every start, so the hashes mean nothing outside this process.
_SALT = secrets.token_bytes(16)


def visitor_id(client_host: str | None, forwarded_for: str | None) -> str:
    """A stable, anonymous key for one visitor.

    Behind a hosting proxy the real address is the first entry of X-Forwarded-For.
    """
    address = (forwarded_for or "").split(",")[0].strip() or client_host or "unknown"
    return hashlib.sha256(_SALT + address.encode()).hexdigest()[:16]


class QuestionQuota:
    """Counts AI answers per visitor; every count resets when the day changes."""

    def __init__(self, per_day: int = AI_ANSWERS_PER_DAY, clock: Callable[[], date] = date.today):
        self._per_day = per_day
        self._clock = clock
        self._day = clock()
        self._used: dict[str, int] = {}
        self._lock = threading.Lock()  # Gradio answers two chats at once

    def _roll_over(self) -> None:
        if self._clock() != self._day:
            self._day, self._used = self._clock(), {}  # also forgets yesterday's visitors

    def remaining(self, visitor: str) -> int:
        with self._lock:
            self._roll_over()
            return self._per_day - self._used.get(visitor, 0)

    def record(self, visitor: str) -> None:
        with self._lock:
            self._roll_over()
            self._used[visitor] = self._used.get(visitor, 0) + 1


class Searcher(Protocol):
    def search(self, query: str, k: int = 4) -> SearchResult: ...


class PassageAnswerer:
    """Answers with the best-matching corpus sections, word for word. No model is called."""

    def __init__(self, retriever: Searcher):
        self._retriever = retriever

    def ask(self, question: str, note: str = PASSAGES_NOTE) -> Answer:
        question = question.strip()
        if len(question) > MAX_QUESTION_CHARS:
            return Answer(TOO_LONG, False, [], "too_long")
        result = self._retriever.search(question, k=PASSAGES_SHOWN)
        if result.should_abstain:
            return Answer(NOT_FOUND, False, [], "abstained_retrieval")
        chunks = [hit.chunk for hit in result.hits[:PASSAGES_SHOWN]]
        passages = [f"**{c.heading}** ({c.doc_title})\n\n{c.text}" for c in chunks]
        return Answer("\n\n".join([note, *passages]), True, chunks, "passages")


class CachingAnswerer(Protocol):
    def lookup(self, question: str) -> Answer | None: ...
    def ask(self, question: str) -> Answer: ...


class Chat:
    """Decides, per question, between a cached answer, an AI answer and passages.

    Without an answerer (no API key configured), every question gets passages.
    """

    def __init__(self, answerer: CachingAnswerer | None, passages: PassageAnswerer, quota: QuestionQuota):
        self._answerer = answerer
        self._passages = passages
        self._quota = quota

    def remaining(self, visitor: str) -> int:
        return self._quota.remaining(visitor)

    def reply(self, question: str, visitor: str) -> Answer:
        if self._answerer is None:
            return self._passages.ask(question, UNAVAILABLE_NOTE)
        cached = self._answerer.lookup(question)
        if cached is not None:
            return cached  # free, so served even after the limit
        if self._quota.remaining(visitor) <= 0:
            return self._passages.ask(question)
        answer = self._answerer.ask(question)
        if answer.outcome == "llm_unavailable":
            return self._passages.ask(question, UNAVAILABLE_NOTE)  # every model busy: passages beat "try later"
        if answer.answered_by and not answer.from_cache:
            self._quota.record(visitor)
        return answer
