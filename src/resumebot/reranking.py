"""Second-stage reranking with a cross-encoder.

A cross-encoder reads the question and a chunk together, so it judges
relevance more precisely than comparing two separately computed vectors,
but it must run once per chunk. So it only reorders the bi-encoder's top
candidates. On the golden set (2026-10-15) it raised hit@4 from 79% to 86%.
Its scores are not calibrated, so they are never used for abstention.
"""

from __future__ import annotations

from typing import Protocol

from resumebot.embeddings import default_cache_dir

DEFAULT_RERANKER = "Xenova/ms-marco-MiniLM-L-6-v2"


class Reranker(Protocol):
    def score(self, query: str, texts: list[str]) -> list[float]:
        """Return one relevance score per text: higher is more relevant."""
        ...


class FastEmbedReranker:
    def __init__(self, model_name: str = DEFAULT_RERANKER, cache_dir: str | None = None):
        from fastembed.rerank.cross_encoder import TextCrossEncoder

        self._model = TextCrossEncoder(model_name=model_name, cache_dir=cache_dir or default_cache_dir())

    def score(self, query: str, texts: list[str]) -> list[float]:
        return [float(s) for s in self._model.rerank(query, texts)]
