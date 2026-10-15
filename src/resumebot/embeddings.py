"""Text embeddings for retrieval.

Retrieval depends on the small Embedder interface, not on a specific library,
so tests can use a fast deterministic fake and the model can change later.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol

import numpy as np

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"


class Embedder(Protocol):
    def embed_passages(self, texts: list[str]) -> np.ndarray:
        """Return one unit-length row per text, shape (len(texts), dims)."""
        ...

    def embed_query(self, text: str) -> np.ndarray:
        """Return one unit-length vector, shape (dims,)."""
        ...


def normalize(vectors: np.ndarray) -> np.ndarray:
    """Scale vectors to length 1 so that a dot product equals cosine similarity."""
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    return vectors / np.where(norms == 0, 1, norms)


def default_cache_dir() -> str:
    # fastembed defaults to /tmp, which WSL clears on restart.
    return os.environ.get("FASTEMBED_CACHE_PATH", str(Path.home() / ".cache" / "fastembed"))


class FastEmbedEmbedder:
    """BGE embeddings via fastembed (ONNX runtime, CPU, no PyTorch)."""

    def __init__(self, model_name: str = DEFAULT_MODEL, cache_dir: str | None = None):
        # Imported here, not at the top: it is slow to import and unit tests never need it.
        from fastembed import TextEmbedding

        self._model = TextEmbedding(model_name, cache_dir=cache_dir or default_cache_dir())

    def embed_passages(self, texts: list[str]) -> np.ndarray:
        vectors = np.array(list(self._model.passage_embed(texts)), dtype=np.float32)
        return normalize(vectors)

    def embed_query(self, text: str) -> np.ndarray:
        # BGE prefixes queries with a retrieval instruction; query_embed does that for us.
        vectors = np.array(list(self._model.query_embed(text)), dtype=np.float32)
        return normalize(vectors)[0]
