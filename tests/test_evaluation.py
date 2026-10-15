from pathlib import Path

import pytest

from resumebot.corpus import Chunk
from resumebot.evaluation import GoldenItem, Result, is_hit, load_golden, reciprocal_rank, threshold_table
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
