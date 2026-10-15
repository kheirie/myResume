"""Find the chunks most similar to a question.

Every chunk is embedded once, when the Retriever is built. A search embeds the
question and ranks all chunks by cosine similarity: with unit-length vectors
that is a single matrix-vector product, so no vector database is needed for a
corpus this size.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from resumebot.corpus import Chunk
from resumebot.embeddings import Embedder


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float  # cosine similarity: higher is more similar


def text_for_embedding(chunk: Chunk) -> str:
    """The text we embed: title and heading give the chunk its context.

    "Kheirie built preprocessing pipelines..." alone does not say Sanofi;
    with the document title prepended, "What did Kheirie do at Sanofi?" can match it.
    """
    return f"{chunk.doc_title}\n{chunk.heading}\n{chunk.text}"


class Retriever:
    def __init__(self, chunks: list[Chunk], embedder: Embedder):
        if not chunks:
            raise ValueError("cannot build a retriever over an empty corpus")
        self.chunks = list(chunks)
        self._embedder = embedder
        self._matrix = embedder.embed_passages([text_for_embedding(c) for c in self.chunks])

    def search(self, query: str, k: int = 4) -> list[Hit]:
        """Return the k most similar chunks, best first."""
        if k < 1:
            raise ValueError("k must be at least 1")
        scores = self._matrix @ self._embedder.embed_query(query)
        top = np.argsort(-scores, kind="stable")[:k]
        return [Hit(self.chunks[i], float(scores[i])) for i in top]
