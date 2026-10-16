import re
import zlib

import numpy as np
import pytest

from resumebot.corpus import Chunk
from resumebot.embeddings import normalize
from resumebot.retrieval import (
    ABSTAIN_BELOW,
    OVERVIEW_CHUNK_IDS,
    OVERVIEW_QUERY,
    Retriever,
    SearchResult,
    expand_overview_query,
    remove_subject_name,
    text_for_embedding,
)


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
    hits = retriever.search("BERT sentiment analysis", k=3).hits
    assert hits[0].chunk.id == "exp-c#sentiment"


def test_results_are_sorted_by_score_and_limited_to_k(retriever):
    hits = retriever.search("data pipelines", k=2).hits
    assert len(hits) == 2
    assert hits[0].score >= hits[1].score


def test_k_larger_than_corpus_returns_every_chunk(retriever):
    assert len(retriever.search("anything", k=10).hits) == len(CHUNKS)


def test_k_below_one_is_rejected(retriever):
    with pytest.raises(ValueError):
        retriever.search("anything", k=0)


def test_empty_corpus_is_rejected():
    with pytest.raises(ValueError):
        Retriever([], FakeEmbedder())


def test_title_and_heading_are_embedded_with_the_text():
    chunk = make_chunk("exp-s", "Pipelines", "Kheirie built pipelines.", title="NLP Data Scientist, Sanofi")
    assert text_for_embedding(chunk) == "NLP Data Scientist, Sanofi\nPipelines\nbuilt pipelines."
    other = make_chunk("exp-o", "Pipelines", "Kheirie built pipelines.", title="Data Scientist, Other Corp")
    hits = Retriever([other, chunk], FakeEmbedder()).search("Sanofi", k=1).hits
    assert hits[0].chunk.id == "exp-s#pipelines"  # only the title mentions Sanofi


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Has Kheirie built RAG systems?", "Has built RAG systems?"),
        ("What is Kheirie's salary?", "What is salary?"),
        ("Kheirie El Hariri", ""),
        ("No name here", "No name here"),
    ],
)
def test_remove_subject_name(text, expected):
    assert remove_subject_name(text) == expected


def test_name_alone_does_not_decide_ranking():
    named = make_chunk("exp-n", "Nationality", "Kheirie has French nationality.")
    relevant = make_chunk("exp-g", "Grant", "received a regional development grant.")
    hits = Retriever([named, relevant], FakeEmbedder()).search("Has Kheirie received a grant?", k=1).hits
    assert hits[0].chunk.id == "exp-g#grant"


class FakeReranker:
    """Scores a text by how often it contains one chosen word."""

    def __init__(self, favourite: str):
        self.favourite = favourite

    def score(self, query, texts):
        return [float(t.lower().count(self.favourite)) for t in texts]


def test_reranker_reorders_candidates_but_keeps_similarity_scores():
    plain = Retriever(CHUNKS, FakeEmbedder()).search("BERT sentiment analysis", k=3)
    reranked = Retriever(CHUNKS, FakeEmbedder(), reranker=FakeReranker("mathematics")).search(
        "BERT sentiment analysis", k=3
    )
    assert plain.hits[0].chunk.id == "exp-c#sentiment"
    assert reranked.hits[0].chunk.id == "exp-b#teaching"  # the reranker's choice wins the order
    by_id = {h.chunk.id: h.score for h in plain.hits}
    assert all(h.score == by_id[h.chunk.id] for h in reranked.hits)  # similarity is unchanged
    assert reranked.hits[0].rerank_score == 1.0


def test_top_similarity_ignores_the_reranker():
    plain = Retriever(CHUNKS, FakeEmbedder()).search("BERT sentiment analysis")
    reranked = Retriever(CHUNKS, FakeEmbedder(), reranker=FakeReranker("mathematics")).search(
        "BERT sentiment analysis"
    )
    assert reranked.top_similarity == plain.top_similarity


@pytest.mark.parametrize("similarity, abstain", [(ABSTAIN_BELOW - 0.01, True), (ABSTAIN_BELOW, False)])
def test_should_abstain_below_threshold(similarity, abstain):
    assert SearchResult(hits=[], top_similarity=similarity).should_abstain is abstain


@pytest.mark.parametrize(
    "question",
    ["Tell me about Kheirie", "Who is Kheirie?", "Tell me about Kheirie's background", "Kheirie"],
)
def test_questions_with_no_topic_become_an_overview_query(question):
    assert expand_overview_query(remove_subject_name(question)) == OVERVIEW_QUERY


@pytest.mark.parametrize(
    "question",
    ["What is Kheirie's background in NLP?", "Tell me about Kheirie's teaching", "MLflow?"],
)
def test_questions_with_a_topic_keep_their_own_words(question):
    cleaned = remove_subject_name(question)
    assert expand_overview_query(cleaned) == cleaned


def overview_corpus():
    profile = [make_chunk("about", h, f"{h} text.") for h in ("Professional summary", "Data science profile")]
    trivia = make_chunk("about", "Nationality", "has French nationality.")
    return [trivia, *profile, *CHUNKS]


def test_overview_question_pins_the_profile_sections_first(monkeypatch):
    import resumebot.retrieval as retrieval

    monkeypatch.setattr(retrieval, "OVERVIEW_CHUNK_IDS", ("about#professional-summary", "about#data-science-profile"))
    for reranker in (None, FakeReranker("nationality")):
        hits = Retriever(overview_corpus(), FakeEmbedder(), reranker=reranker).search("Who is Kheirie?", k=3).hits
        assert [h.chunk.id for h in hits[:2]] == ["about#professional-summary", "about#data-science-profile"]


def test_topic_question_is_not_pinned(monkeypatch):
    import resumebot.retrieval as retrieval

    monkeypatch.setattr(retrieval, "OVERVIEW_CHUNK_IDS", ("about#professional-summary",))
    hits = Retriever(overview_corpus(), FakeEmbedder()).search("BERT sentiment analysis", k=1).hits
    assert hits[0].chunk.id == "exp-c#sentiment"
