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
# Case-insensitive: "tell me about kheirie" skipped the overview route and retrieved trivia.
# "Kerry" is how the web chat names her (the pronunciation of Kheirie).
SUBJECT_NAME = re.compile(r"\b(?:(?:Kheirie|Kerry)(?:['\u2019]s)?|El Hariri)\b", re.IGNORECASE)


# Abstain without calling the LLM when the best chunk scores below this.
# A cheap, deterministic safety net; the LLM is the main judge of whether the
# retrieved chunks contain the answer. Golden set, 2026-10-15: answerable
# questions score 0.583 and up; off-topic ones 0.486-0.581. At 0.55 no
# answerable question is blocked and 3 of 4 off-topic questions stop here,
# including "earliest start date", which the 8B model answered with a made-up
# date (prompt v1/v2) when the threshold was 0.50. Kheirie's choice.
# Raised to 0.56 on 2026-10-17 (Kheirie's choice): section keywords lifted "earliest start date"
# to 0.551; at 0.56 no answerable question is blocked and 3 of 4 off-topic ones stop here.
ABSTAIN_BELOW = 0.56


def remove_subject_name(text: str) -> str:
    lines = SUBJECT_NAME.sub("", text).splitlines()
    return "\n".join(" ".join(line.split()) for line in lines).strip()


# Pronouns in a question always mean the candidate, so like the name they carry no
# information; in a short question they weigh a lot: "did she do RAG?" scored 0.543
# (below the threshold), "did do RAG?" 0.634 (2026-10-24). "he" is included because
# visitors may guess wrong. Questions only: the corpus never uses pronouns for her.
SUBJECT_PRONOUNS = re.compile(r"\b(?:she|her|hers|herself|he|him|his|himself)\b", re.IGNORECASE)


# A bare acronym gives a short question little to match: "did she do retrieval-augmented
# generation (RAG)?" scored 0.740 against 0.634 for "did she do RAG?" (2026-10-24). Only
# acronyms with one meaning in this corpus: CV (curriculum vitae or computer vision) and
# MA are left out. So are AI and LLM, which the corpus mostly writes as words the
# articles use: spelling them out pulled "What AI teaching ... experience" and "has she
# used LLMs?" toward the articles, and both missed their sections (2026-10-24).
ACRONYMS = {
    "CPI": "consumer price index",
    "DL": "deep learning",
    "EFL": "English as a foreign language",
    "ETL": "extract, transform, load",
    "EU": "European Union",
    "GenAI": "generative AI",
    "HR": "human resources",
    "L&D": "learning and development",
    "LSTM": "long short-term memory",
    "ML": "machine learning",
    "MLOps": "machine learning operations",
    "NLP": "natural language processing",
    "PMI": "purchasing managers' index",
    "R&D": "research and development",
    "RAG": "retrieval-augmented generation",
    "RMSE": "root mean squared error",
    "RNN": "recurrent neural network",
}
_ACRONYM = re.compile(
    r"(?<!\w)(" + "|".join(re.escape(a) for a in sorted(ACRONYMS, key=len, reverse=True)) + r")(s?)(?!\w)",
    re.IGNORECASE,
)
_ACRONYM_KEYS = {a.lower(): a for a in ACRONYMS}


def expand_acronyms(query: str) -> str:
    """ "RAG" becomes "retrieval-augmented generation (RAG)", unless the question spells it out."""

    def expand(match: re.Match) -> str:
        acronym, plural = _ACRONYM_KEYS[match.group(1).lower()], match.group(2)
        meaning = ACRONYMS[acronym]
        if meaning.lower() in query.lower():
            return match.group(0)
        return f"{meaning} ({acronym}{plural})"  # plural on the acronym only, not "memorys"

    return _ACRONYM.sub(expand, query)


def prepare_query(query: str) -> str:
    """The question as searched: without the candidate's name or pronouns, acronyms spelled out."""
    return expand_acronyms(" ".join(SUBJECT_PRONOUNS.sub("", remove_subject_name(query)).split()))


# "Tell me about Kheirie" minus the name is "Tell me about": nothing left to search
# for, so it matched chunks titled "About Kheirie" (nationality, pronunciation)
# instead of the professional summary. A question made only of these filler words
# is a request for an overview. It is routed rather than searched: the sections that
# answer it are known, so they are pinned first (no single query retrieved all three),
# and the remaining slots come from searching OVERVIEW_QUERY.
FILLER_WORDS = {
    "a", "about", "an", "background", "can", "describe", "do", "does", "give", "her", "introduce",
    "is", "know", "me", "more", "of", "overview", "please", "profile", "she", "something", "summarise", "summarize",
    "summary", "tell", "the", "us", "what", "who", "you",
}
OVERVIEW_CHUNK_IDS = (
    "about#professional-summary",
    "about#data-science-profile",
    "about#learning-and-development-profile",
)
OVERVIEW_QUERY = "professional summary and profile: data science, NLP and generative AI experience; education, teaching and course design background"


def is_overview_question(query: str) -> bool:
    """True for questions with no topic of their own, such as "Who is Kheirie?" (name already removed)."""
    return all(w in FILLER_WORDS for w in re.findall(r"[a-z]+", query.lower()))


# "can you give more details?" has no topic of its own: searched alone it scored 0.558 and
# was "not found"; asked together with the previous question it scored 0.764 (2026-10-24).
# A follow-up has one of these cue words and otherwise only filler. Without a cue, a
# topic-less question ("Who is she?") stays an overview question.
FOLLOW_UP_CUES = {
    "detail", "details", "elaborate", "else", "example", "examples", "expand", "explain", "further",
    "how", "it", "more", "specific", "specifics", "that", "this", "why",
}
FOLLOW_UP_FILLER = {"and", "any", "could", "go", "into", "on", "other", "provide", "say", "share", "some", "would"}


def is_follow_up_question(question: str) -> bool:
    """True for questions such as "Can you give more details?" that only make sense after another one."""
    words = re.findall(r"[a-z]+", prepare_query(question).lower())
    allowed = FILLER_WORDS | FOLLOW_UP_CUES | FOLLOW_UP_FILLER
    return any(w in FOLLOW_UP_CUES for w in words) and all(w in allowed for w in words)


def expand_overview_query(query: str) -> str:
    """Replace a question with no topic of its own by an overview query."""
    return OVERVIEW_QUERY if is_overview_question(query) else query


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
    Section keywords are appended for matching only; the LLM and passages never see them.
    """
    text = f"{chunk.doc_title}\n{chunk.heading}\n{chunk.text}"
    if chunk.keywords:
        text += "\nKeywords: " + ", ".join(chunk.keywords)
    return remove_subject_name(text)


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
        ids = [c.id for c in self.chunks]
        self._overview_indices = [ids.index(cid) for cid in OVERVIEW_CHUNK_IDS if cid in ids]

    def search(self, query: str, k: int = 4) -> SearchResult:
        """Return the k most relevant chunks, best first."""
        if k < 1:
            raise ValueError("k must be at least 1")
        query = prepare_query(query)
        overview = is_overview_question(query)
        if overview:
            query = OVERVIEW_QUERY
        scores = self._matrix @ self._embedder.embed_query(query)
        order = np.argsort(-scores, kind="stable")
        top_similarity = float(scores[order[0]])
        if overview:
            pinned = [i for i in self._overview_indices]
            order = np.array(pinned + [i for i in order if i not in pinned])
            if self._reranker is None or len(pinned) >= k:
                return SearchResult([Hit(self.chunks[i], float(scores[i])) for i in order[:k]], top_similarity)

        if self._reranker is None:
            return SearchResult([Hit(self.chunks[i], float(scores[i])) for i in order[:k]], top_similarity)

        fixed = [i for i in order[:k] if overview and i in self._overview_indices]  # pinned stay first
        candidates = [i for i in order[: max(k, self._candidates)] if i not in fixed]
        rerank = self._reranker.score(query, [text_for_embedding(self.chunks[i]) for i in candidates])
        # sorted() is stable: on equal rerank scores the cosine order is kept.
        ranked = sorted(zip(candidates, rerank), key=lambda pair: -pair[1])[: k - len(fixed)]
        hits = [Hit(self.chunks[i], float(scores[i])) for i in fixed]
        hits += [Hit(self.chunks[i], float(scores[i]), float(r)) for i, r in ranked]
        return SearchResult(hits, top_similarity)
