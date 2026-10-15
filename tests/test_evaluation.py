from pathlib import Path

import pytest

from resumebot.corpus import Chunk
from resumebot.answering import Answer
from resumebot.evaluation import (
    AnswerResult,
    GoldenItem,
    Result,
    answer_report,
    answer_summary,
    is_hit,
    load_golden,
    reciprocal_rank,
    threshold_table,
)
from resumebot.retrieval import Hit, SearchResult

ROOT = Path(__file__).resolve().parents[1]


def item(expected, match="all", answerable=True, abstain_type=None):
    return GoldenItem("q?", answerable, tuple(expected), match, abstain_type)


@pytest.mark.parametrize(
    "expected, match, retrieved, hit",
    [
        (["a"], "all", ["x", "a"], True),
        (["a", "b"], "all", ["a", "x"], False),  # "all" needs every expected source
        (["a", "b"], "any", ["a", "x"], True),  # "any" needs just one
        ([], "all", ["a"], False),  # unanswerable items never count as hits
    ],
)
def test_is_hit(expected, match, retrieved, hit):
    assert is_hit(item(expected, match), retrieved) is hit


def test_reciprocal_rank_uses_first_expected_source():
    assert reciprocal_rank(item(["b", "c"]), ["a", "b", "c"]) == 0.5
    assert reciprocal_rank(item(["z"]), ["a", "b"]) == 0.0


def fake_result(score, **kwargs):
    chunk = Chunk("d#s", "d", "T", "S", "text", "cv", ("CV",))
    return Result(item(["d#s"], **kwargs), SearchResult([Hit(chunk, score)], score))


def test_threshold_table_counts_questions_below_each_threshold():
    results = [
        fake_result(0.80),
        fake_result(0.70),
        fake_result(0.65, answerable=False, abstain_type="off_topic"),
        fake_result(0.85, answerable=False, abstain_type="near_miss"),
    ]
    row = threshold_table(results, [0.75])[0]
    assert row["answerable"] == (1, 2)  # the 0.70 answerable would be wrongly rejected
    assert row["off_topic"] == (1, 1)
    assert row["near_miss"] == (0, 1)  # near misses score high: a threshold cannot catch them


def test_real_golden_set_loads_with_valid_fields():
    items = load_golden(ROOT / "evals" / "golden.yaml")
    assert all(i.match in ("all", "any") for i in items)
    assert all(i.abstain_type in ("off_topic", "near_miss") for i in items if not i.answerable)


def answer_result(answerable_q, answered, cited=(), outcome=None, abstain_type=None):
    chunks = [Chunk(c, c.split("#")[0], "T", "S", "text", "cv", ("CV",)) for c in cited]
    golden = GoldenItem("Q?", answerable_q, ("d#s",), "all", abstain_type, "a note")
    outcome = outcome or ("answered" if answered else "abstained_llm")
    return AnswerResult(golden, Answer("text", answered, chunks, outcome), 1.0)


def test_outcome_correct_compares_answering_with_the_golden_label():
    assert answer_result(True, True).outcome_correct
    assert not answer_result(True, False).outcome_correct  # over-abstention
    assert answer_result(False, False, abstain_type="near_miss").outcome_correct
    assert not answer_result(False, True, abstain_type="near_miss").outcome_correct  # made something up


def test_answer_summary_counts_groups_and_lists_wrong_outcomes():
    results = [
        answer_result(True, True, cited=["d#s"]),
        answer_result(True, False),
        answer_result(False, False, abstain_type="off_topic", outcome="abstained_retrieval"),
    ]
    summary = answer_summary(results)
    assert "answerable questions answered:   1/2" in summary
    assert "answered with expected sources:  1/1" in summary
    assert "off-topic questions declined:    1/1" in summary
    assert "[should answer] Q?" in summary


def test_answer_report_shows_each_answer_next_to_its_notes():
    report = answer_report([answer_result(True, True, cited=["d#s"])], "test-model")
    assert "# Answer evaluation: test-model" in report
    assert "- notes: a note" in report


def test_answer_summary_reports_token_totals():
    from resumebot.llm import Usage

    golden = GoldenItem("Q?", True, ("d#s",), "all", None, "")
    results = [
        AnswerResult(golden, Answer("t", True, [], "answered", usage=Usage(1000, 100)), 1.0),
        AnswerResult(golden, Answer("t", True, [], "answered", usage=Usage(1200, 300)), 1.0),
    ]
    summary = answer_summary(results)
    assert "2 LLM answers: 2200 in + 400 out = 2600 total" in summary
    assert "mean per answer: 1100 in + 200 out" in summary
