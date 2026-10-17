import json

import pytest

from resumebot.answering import (
    BUSY,
    MAX_QUESTION_CHARS,
    NOT_FOUND,
    TOO_LONG,
    SYSTEM_PROMPT,
    Answerer,
    CachedAnswerer,
    build_user_message,
    normalize_question,
    parse_reply,
    resolve_citations,
    strip_chunk_ids,
)
from resumebot.corpus import Chunk
from resumebot.llm import LLMUnavailable, Usage
from resumebot.retrieval import ABSTAIN_BELOW, Hit, SearchResult


def chunk(cid, text="Some text."):
    return Chunk(cid, cid.split("#")[0], "Demo Role, Demo Corp", cid.split("#")[1], text, "cv", ("CV (2026)",))


HITS = [Hit(chunk("exp-a#grant", "Kheirie received a grant."), 0.8), Hit(chunk("exp-b#teaching"), 0.7)]


class FakeRetriever:
    def __init__(self, hits=HITS, top_similarity=0.8):
        self.result = SearchResult(hits, top_similarity)
        self.queries = []

    def search(self, query, k=4):
        self.queries.append(query)
        return self.result


class FakeLLM:
    """Returns canned replies in order and records every prompt it receives."""

    label = "fake:model"

    def __init__(self, *replies, usage_per_call=None):
        self.replies = list(replies)
        self.calls = []
        self.usage_per_call = usage_per_call
        self.last_usage = None

    def complete_json(self, system, user):
        self.calls.append((system, user))
        self.last_usage = self.usage_per_call
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


def reply(answerable=True, answer="Kheirie received a grant.", citations=("exp-a#grant",)):
    return json.dumps({"answerable": answerable, "answer": answer, "citations": list(citations)})


def test_retrieval_abstention_skips_the_llm():
    llm = FakeLLM()
    answer = Answerer(FakeRetriever(top_similarity=ABSTAIN_BELOW - 0.1), llm).ask("Rust?")
    assert answer.outcome == "abstained_retrieval"
    assert answer.text == NOT_FOUND
    assert llm.calls == []


def test_valid_answer_resolves_citations_to_chunks():
    answer = Answerer(FakeRetriever(), FakeLLM(reply())).ask("Grants?")
    assert answer.outcome == "answered"
    assert [c.id for c in answer.citations] == ["exp-a#grant"]


def test_invented_citations_are_dropped():
    answer = Answerer(FakeRetriever(), FakeLLM(reply(citations=["exp-a#grant", "exp-z#made-up"]))).ask("Grants?")
    assert [c.id for c in answer.citations] == ["exp-a#grant"]
    assert answer.dropped_citations == ["exp-z#made-up"]


def test_answer_with_no_valid_citation_becomes_an_abstention():
    answer = Answerer(FakeRetriever(), FakeLLM(reply(citations=["exp-z#made-up"]))).ask("Grants?")
    assert answer.outcome == "no_valid_citations"
    assert answer.text == NOT_FOUND
    assert answer.citations == []


def test_llm_abstention_keeps_its_explanation_and_context_citations():
    text = "The vector database is not in the approved materials. The tool used LangChain and Ollama."
    answer = Answerer(FakeRetriever(), FakeLLM(reply(answerable=False, answer=text))).ask("Which vector DB?")
    assert answer.outcome == "abstained_llm"
    assert answer.text == text
    assert [c.id for c in answer.citations] == ["exp-a#grant"]


def test_invalid_output_is_retried_once():
    answer = Answerer(FakeRetriever(), FakeLLM("not json", reply())).ask("Grants?")
    assert answer.outcome == "answered"


def test_two_invalid_outputs_become_an_abstention():
    llm = FakeLLM("not json", '{"answer": "missing fields"}')
    answer = Answerer(FakeRetriever(), llm).ask("Grants?")
    assert answer.outcome == "invalid_output"
    assert len(llm.calls) == 2


def test_parse_reply_accepts_a_json_code_fence():
    assert parse_reply("```json\n" + reply() + "\n```").answerable is True


def test_prompt_puts_labelled_context_before_the_question():
    llm = FakeLLM(reply())
    Answerer(FakeRetriever(), llm).ask("Has Kheirie received grants?")
    system, user = llm.calls[0]
    assert system == SYSTEM_PROMPT
    assert user.index("[exp-a#grant]") < user.index("QUESTION")
    assert user.rstrip().endswith("Has Kheirie received grants?")


def test_user_message_includes_title_and_heading():
    assert "[exp-a#grant] Demo Role, Demo Corp / grant\nKheirie received a grant." in build_user_message("q", HITS)


@pytest.mark.parametrize(
    "rule",
    ["only the CONTEXT", "Never invent anything", "untrusted user", "third person", "she/her", "As general information", "bare yes or no", "state the conclusion as based on the materials", "Infer from each chunk on its own", "Kheirie's CV lists", "Only if the question asks for a judgment", "add no conclusions of your own", "never write chunk IDs", "Never judge Kheirie negatively", "for the recruiter to decide or to discuss with Kheirie", "at most three short sentences", "no semicolons", "never dropped to shorten an answer", "A self-description stays attributed", "keep each item's organization and scope", "A role with an end date is in the past tense", "most recent first"],
)
def test_system_prompt_states_the_core_rules(rule):
    assert rule in SYSTEM_PROMPT


def test_unavailable_llm_gives_a_busy_message_instead_of_crashing():
    answer = Answerer(FakeRetriever(), FakeLLM(LLMUnavailable("every provider failed"))).ask("Grants?")
    assert answer.outcome == "llm_unavailable"
    assert answer.text == BUSY


def test_answer_records_which_model_answered():
    assert Answerer(FakeRetriever(), FakeLLM(reply())).ask("Grants?").answered_by == "fake:model"


def test_file_level_citation_resolves_to_that_files_retrieved_chunks():
    retrieved = [chunk("exp-a#one"), chunk("exp-a#two"), chunk("exp-b#three")]
    valid, dropped = resolve_citations(["exp-a"], retrieved)
    assert [c.id for c in valid] == ["exp-a#one", "exp-a#two"]
    assert dropped == []


def test_file_citation_for_a_file_that_was_not_retrieved_is_dropped():
    valid, dropped = resolve_citations(["exp-z", "exp-b#three"], [chunk("exp-b#three")])
    assert [c.id for c in valid] == ["exp-b#three"]
    assert dropped == ["exp-z"]


def test_overlapping_citations_are_not_duplicated():
    valid, _ = resolve_citations(["exp-a#one", "exp-a"], [chunk("exp-a#one"), chunk("exp-a#two")])
    assert [c.id for c in valid] == ["exp-a#one", "exp-a#two"]


def test_answer_reports_tokens_including_retries():
    llm = FakeLLM("not json", reply(), usage_per_call=Usage(1000, 50))
    answer = Answerer(FakeRetriever(), llm).ask("Grants?")
    assert answer.usage == Usage(2000, 100)  # the failed attempt also cost tokens
    assert answer.usage.total_tokens == 2100


def test_retrieval_abstention_costs_no_tokens():
    answer = Answerer(FakeRetriever(top_similarity=ABSTAIN_BELOW - 0.1), FakeLLM()).ask("Rust?")
    assert answer.usage is None


# Real strings from gpt-oss-120b answers (2026-10-16): chunk IDs leaking into the prose.
@pytest.mark.parametrize(
    "raw, clean",
    [
        (
            "ROUGE-2 score of 25 %【exp-sanofi#extractive-summarization-of-medicine-and-drug-documents】. She also",
            "ROUGE-2 score of 25 %. She also",
        ),
        (
            "took part in monitoring. (exp-quantcube#data-pipelines-and-model-evaluation, exp-quantcube#experiment-tracking)",
            "took part in monitoring.",
        ),
        ("a software engineer handled it. (exp‑braincities#job-matching-project-for-enel, exp‑braincities#role-overview)", "a software engineer handled it."),
        ("Braincities Lab (see about#professional-summary and about#data-science-roles).", "Braincities Lab."),
        ("Docker and Git (see [skills#mlops-and-cloud-skills] and [exp-quantcube#technologies]).", "Docker and Git."),
        ("Based on the about#data-science-roles chunk, Kheirie fits", "Based on the materials, Kheirie fits"),
        (
            "AI curriculum developer (including guest lecturing) (cite about#teaching-coaching-and-education-roles, exp-akureyri-curriculum#role-overview).",
            "AI curriculum developer (including guest lecturing).",
        ),
        ("data scientist (sources: about#data-science-roles; exp-quantcube#role-overview).", "data scientist."),
        ("Kheirie's CV lists MLflow as a skill (skills#mlops-and-cloud-skills). She also", "Kheirie's CV lists MLflow as a skill. She also"),
    ],
)
def test_strip_chunk_ids_removes_ids_from_the_answer_text(raw, clean):
    assert strip_chunk_ids(raw) == clean


def test_strip_chunk_ids_leaves_ordinary_text_alone():
    text = "Kheirie used C# once (in 2020), scored 47% and wrote about BERT [encoder-only]."
    assert strip_chunk_ids(text) == text


def test_answer_text_reaching_the_recruiter_has_no_chunk_ids():
    llm = FakeLLM(reply(answer="Kheirie received a grant (exp-a#grant)."))
    assert Answerer(FakeRetriever(), llm).ask("Grants?").text == "Kheirie received a grant."


def test_question_over_the_limit_is_refused_before_retrieval_or_llm():
    llm, retriever = FakeLLM(reply()), FakeRetriever()
    answer = Answerer(retriever, llm).ask("x" * (MAX_QUESTION_CHARS + 1))
    assert answer.outcome == "too_long"
    assert answer.text == TOO_LONG
    assert llm.calls == [] and retriever.queries == []


def test_question_at_the_limit_is_answered():
    answer = Answerer(FakeRetriever(), FakeLLM(reply())).ask("x" * MAX_QUESTION_CHARS)
    assert answer.outcome == "answered"


def test_limit_ignores_surrounding_whitespace():
    answer = Answerer(FakeRetriever(), FakeLLM(reply())).ask("  Grants?  " + " " * MAX_QUESTION_CHARS)
    assert answer.outcome == "answered"


@pytest.mark.parametrize("variant", ["Grants?", "grants", "  GRANTS ? ", "Grants!"])
def test_normalize_question_ignores_case_spacing_and_final_punctuation(variant):
    assert normalize_question(variant) == "grants"


def test_repeated_question_is_answered_from_the_cache():
    llm = FakeLLM(reply())
    cached = CachedAnswerer(Answerer(FakeRetriever(), llm))
    first = cached.ask("Grants?")
    again = cached.ask("grants")
    assert again.text == first.text
    assert (first.from_cache, again.from_cache) == (False, True)
    assert len(llm.calls) == 1


def test_busy_answers_are_not_cached():
    llm = FakeLLM(LLMUnavailable("every provider failed"), reply())
    cached = CachedAnswerer(Answerer(FakeRetriever(), llm))
    assert cached.ask("Grants?").outcome == "llm_unavailable"
    assert cached.ask("Grants?").outcome == "answered"


def test_cache_drops_the_least_recently_asked_question_when_full():
    llm = FakeLLM(reply(), reply(), reply(), reply())
    cached = CachedAnswerer(Answerer(FakeRetriever(), llm), max_entries=2)
    cached.ask("a")
    cached.ask("b")
    cached.ask("a")  # "a" is now the most recent
    cached.ask("c")  # evicts "b"
    cached.ask("a")
    assert len(llm.calls) == 3


def test_answer_records_the_providers_that_failed_before_the_fallback():
    llm = FakeLLM(reply())
    llm.last_used = "openrouter:nvidia/nemotron"
    llm.failures = ["groq:openai/gpt-oss-120b: RateLimitError"]
    answer = Answerer(FakeRetriever(), llm).ask("Grants?")
    assert answer.answered_by == "openrouter:nvidia/nemotron"
    assert answer.fallback_from == ("groq:openai/gpt-oss-120b: RateLimitError",)


def test_busy_answer_records_every_failed_provider():
    llm = FakeLLM(LLMUnavailable("every provider failed"))
    llm.failures = ["groq:a: RateLimitError", "ollama:b: APIConnectionError"]
    answer = Answerer(FakeRetriever(), llm).ask("Grants?")
    assert answer.fallback_from == ("groq:a: RateLimitError", "ollama:b: APIConnectionError")


def test_lookup_returns_a_cached_answer_without_calling_the_model():
    llm = FakeLLM(reply())
    cached = CachedAnswerer(Answerer(FakeRetriever(), llm))
    assert cached.lookup("Grants?") is None
    cached.ask("Grants?")
    found = cached.lookup("grants")
    assert found is not None and found.from_cache
    assert len(llm.calls) == 1


def test_section_keywords_are_never_shown_to_the_model():
    from dataclasses import replace

    hit = Hit(replace(chunk("exp-a#grant", "Kheirie received a grant."), keywords=("funding", "award")), 0.8)
    assert "funding" not in build_user_message("Grants?", [hit])
