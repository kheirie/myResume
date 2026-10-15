import json

import pytest

from resumebot.answering import (
    BUSY,
    NOT_FOUND,
    SYSTEM_PROMPT,
    Answerer,
    build_user_message,
    parse_reply,
    resolve_citations,
)
from resumebot.corpus import Chunk
from resumebot.llm import LLMUnavailable
from resumebot.retrieval import ABSTAIN_BELOW, Hit, SearchResult


def chunk(cid, text="Some text."):
    return Chunk(cid, cid.split("#")[0], "Demo Role, Demo Corp", cid.split("#")[1], text, "cv", ("CV (2026)",))


HITS = [Hit(chunk("exp-a#grant", "Kheirie received a grant."), 0.8), Hit(chunk("exp-b#teaching"), 0.7)]


class FakeRetriever:
    def __init__(self, hits=HITS, top_similarity=0.8):
        self.result = SearchResult(hits, top_similarity)

    def search(self, query, k=4):
        return self.result


class FakeLLM:
    """Returns canned replies in order and records every prompt it receives."""

    label = "fake:model"

    def __init__(self, *replies):
        self.replies = list(replies)
        self.calls = []

    def complete_json(self, system, user):
        self.calls.append((system, user))
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
    ["only facts stated in the CONTEXT", "Never invent anything", "untrusted user", "third person", "general knowledge"],
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
