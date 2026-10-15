import re
import zlib

import numpy as np
import pytest

from resumebot.corpus import Chunk
from resumebot.embeddings import normalize
from resumebot.retrieval import Retriever, text_for_embedding


class FakeEmbedder:
    """Deterministic bag-of-words vectors: fast, offline, and easy to reason about.

    Uses zlib.crc32 rather than hash(): Python salts hash() per process,
    so it would give different vectors on every test run.
    """

    dims = 512

    def _vector(self, text: str) -> np.ndarray:
        v = np.zeros(self.dims, dtype=np.float32)
        for word in re.findall(r"\w+", text.lower()):
            v[zlib.crc32(word.encode()) % self.dims] += 1
        return v

    def embed_passages(self, texts):
        return normalize(np.stack([self._vector(t) for t in texts]))

    def embed_query(self, text):
        return normalize(self._vector(text)[None, :])[0]


def make_chunk(doc_id, heading, text, title="Demo Role, Demo Corp"):
    slug = heading.lower().replace(" ", "-")
    return Chunk(f"{doc_id}#{slug}", doc_id, title, heading, text, "cv", ("CV (2026)",))


CHUNKS = [
    make_chunk("exp-a", "Pipelines", "Kheirie built data pipelines in Python."),
    make_chunk("exp-b", "Teaching", "Kheirie taught mathematics to primary school students."),
    make_chunk("exp-c", "Sentiment", "Kheirie applied BERT sentiment analysis to tweets."),
]


@pytest.fixture
def retriever():
    return Retriever(CHUNKS, FakeEmbedder())


def test_normalize_gives_unit_length_and_leaves_zero_vectors_alone():
    out = normalize(np.array([[3.0, 4.0], [0.0, 0.0]]))
    assert np.allclose(out[0], [0.6, 0.8])
    assert np.allclose(out[1], [0.0, 0.0])  # no division by zero, no NaN


def test_best_match_comes_first(retriever):
    hits = retriever.search("BERT sentiment analysis", k=3)
    assert hits[0].chunk.id == "exp-c#sentiment"


def test_results_are_sorted_by_score_and_limited_to_k(retriever):
    hits = retriever.search("Kheirie", k=2)
    assert len(hits) == 2
    assert hits[0].score >= hits[1].score


def test_k_larger_than_corpus_returns_every_chunk(retriever):
    assert len(retriever.search("anything", k=10)) == len(CHUNKS)


def test_k_below_one_is_rejected(retriever):
    with pytest.raises(ValueError):
        retriever.search("anything", k=0)


def test_empty_corpus_is_rejected():
    with pytest.raises(ValueError):
        Retriever([], FakeEmbedder())


def test_title_and_heading_are_embedded_with_the_text():
    chunk = make_chunk("exp-s", "Pipelines", "Kheirie built pipelines.", title="NLP Data Scientist, Sanofi")
    assert text_for_embedding(chunk) == "NLP Data Scientist, Sanofi\nPipelines\nKheirie built pipelines."
    other = make_chunk("exp-o", "Pipelines", "Kheirie built pipelines.", title="Data Scientist, Other Corp")
    hits = Retriever([other, chunk], FakeEmbedder()).search("Sanofi", k=1)
    assert hits[0].chunk.id == "exp-s#pipelines"  # only the title mentions Sanofi
