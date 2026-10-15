"""Find the chunks most relevant to a question.

Stage 1 (bi-encoder): every chunk is embedded once, when the Retriever is
built. A search embeds the question and ranks all chunks by cosine similarity:
with unit-length vectors that is one matrix-vector product, so no vector
database is needed for a corpus this size.

Stage 2 (optional cross-encoder): the top candidates are reordered by a
reranker. The abstention decision always uses the stage-1 similarity, because
reranker scores are not calibrated.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np

from resumebot.corpus import Chunk
from resumebot.embeddings import Embedder
from resumebot.reranking import Reranker


# Every chunk and almost every question mentions the candidate, so the name
# carries no information for ranking (like a word with zero IDF). Left in, it
# dominates short chunks: "Kheirie has French nationality." matched salary,
# grant, and supervision questions. Removing it raised hit@4 from 64% to 79%.
SUBJECT_NAME = re.compile(r"\b(?:Kheirie(?:'s)?|El Hariri)\b")


# Abstain without calling the LLM when the best chunk scores below this.
# A cheap, deterministic safety net; the LLM is the main judge of whether the
# retrieved chunks contain the answer. Golden set, 2026-10-15: answerable
# questions score 0.583 and up; off-topic ones 0.486-0.581. At 0.55 no
# answerable question is blocked and 3 of 4 off-topic questions stop here,
# including "earliest start date", which the 8B model answered with a made-up
# date (prompt v1/v2) when the threshold was 0.50. Kheirie's choice.
ABSTAIN_BELOW = 0.55


def remove_subject_name(text: str) -> str:
    lines = SUBJECT_NAME.sub("", text).splitlines()
    return "\n".join(" ".join(line.split()) for line in lines).strip()


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float  # cosine similarity with the question: higher is more similar
    rerank_score: float | None = None  # set when a reranker ordered the results


@dataclass(frozen=True)
class SearchResult:
    hits: list[Hit]
    top_similarity: float  # best cosine similarity over all chunks

    @property
    def should_abstain(self) -> bool:
        """True when nothing in the corpus is close enough to be worth an LLM call."""
        return self.top_similarity < ABSTAIN_BELOW


def text_for_embedding(chunk: Chunk) -> str:
    """The text we embed: title and heading give the chunk its context.

    The candidate's name is removed (see SUBJECT_NAME); the chunk itself is unchanged.

    "Kheirie built preprocessing pipelines..." alone does not say Sanofi;
    with the document title prepended, "What did Kheirie do at Sanofi?" can match it.
    """
    return remove_subject_name(f"{chunk.doc_title}\n{chunk.heading}\n{chunk.text}")


class Retriever:
    def __init__(
        self,
        chunks: list[Chunk],
        embedder: Embedder,
        reranker: Reranker | None = None,
        candidates: int = 20,
    ):
        if not chunks:
            raise ValueError("cannot build a retriever over an empty corpus")
        self.chunks = list(chunks)
        self._embedder = embedder
        self._reranker = reranker
        self._candidates = candidates
        self._matrix = embedder.embed_passages([text_for_embedding(c) for c in self.chunks])

    def search(self, query: str, k: int = 4) -> SearchResult:
        """Return the k most relevant chunks, best first."""
        if k < 1:
            raise ValueError("k must be at least 1")
        query = remove_subject_name(query)
        scores = self._matrix @ self._embedder.embed_query(query)
        order = np.argsort(-scores, kind="stable")
        top_similarity = float(scores[order[0]])

        if self._reranker is None:
            hits = [Hit(self.chunks[i], float(scores[i])) for i in order[:k]]
        else:
            candidates = order[: max(k, self._candidates)]
            rerank = self._reranker.score(query, [text_for_embedding(self.chunks[i]) for i in candidates])
            # sorted() is stable: on equal rerank scores the cosine order is kept.
            ranked = sorted(zip(candidates, rerank), key=lambda pair: -pair[1])[:k]
            hits = [Hit(self.chunks[i], float(scores[i]), float(r)) for i, r in ranked]
        return SearchResult(hits, top_similarity)
