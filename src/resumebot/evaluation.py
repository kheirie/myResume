"""Measure retrieval against the golden set.

Two questions, answered with numbers rather than impressions:
  1. Do answerable questions retrieve the chunks they need? (hit@k, MRR)
  2. Where should the abstention threshold sit? (a trade-off table: how many
     answerable questions a threshold would wrongly reject, and how many
     unanswerable ones it would catch)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from resumebot.retrieval import Retriever, SearchResult


@dataclass(frozen=True)
class GoldenItem:
    question: str
    answerable: bool
    expected_sources: tuple[str, ...] = ()
    match: str = "all"  # "all": every expected source must be retrieved; "any": one is enough
    abstain_type: str | None = None  # "off_topic" or "near_miss" for unanswerable items


def load_golden(path: Path) -> list[GoldenItem]:
    items = yaml.safe_load(path.read_text(encoding="utf-8"))
    return [
        GoldenItem(
            question=i["question"],
            answerable=i["answerable"],
            expected_sources=tuple(i.get("expected_sources", [])),
            match=i.get("match", "all"),
            abstain_type=i.get("abstain_type"),
        )
        for i in items
    ]


def is_hit(item: GoldenItem, retrieved_ids: list[str]) -> bool:
    if not item.expected_sources:
        return False
    found = [s in retrieved_ids for s in item.expected_sources]
    return any(found) if item.match == "any" else all(found)


def reciprocal_rank(item: GoldenItem, retrieved_ids: list[str]) -> float:
    """1/rank of the first expected source retrieved, or 0 if none was."""
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in item.expected_sources:
            return 1 / rank
    return 0.0


@dataclass(frozen=True)
class Result:
    item: GoldenItem
    search: SearchResult

    @property
    def ids(self) -> list[str]:
        return [h.chunk.id for h in self.search.hits]

    @property
    def top_score(self) -> float:
        """The stage-1 similarity that the abstention threshold uses."""
        return self.search.top_similarity


def run(retriever: Retriever, items: list[GoldenItem], k: int) -> list[Result]:
    return [Result(item, retriever.search(item.question, k=k)) for item in items]


def hit_rate(results: list[Result], k: int) -> float:
    answerable = [r for r in results if r.item.answerable]
    return sum(is_hit(r.item, r.ids[:k]) for r in answerable) / len(answerable)


def mrr(results: list[Result], k: int) -> float:
    answerable = [r for r in results if r.item.answerable]
    return sum(reciprocal_rank(r.item, r.ids[:k]) for r in answerable) / len(answerable)


def threshold_table(results: list[Result], thresholds: list[float]) -> list[dict]:
    """For each threshold: what abstaining below it would do to each group of questions."""
    groups = {
        "answerable": [r for r in results if r.item.answerable],
        "off_topic": [r for r in results if r.item.abstain_type == "off_topic"],
        "near_miss": [r for r in results if r.item.abstain_type == "near_miss"],
    }
    rows = []
    for t in thresholds:
        row = {"threshold": t}
        for name, group in groups.items():
            row[name] = (sum(r.top_score < t for r in group), len(group))
        rows.append(row)
    return rows


def report(results: list[Result], ks: list[int], thresholds: list[float]) -> str:
    lines = ["RETRIEVAL QUALITY (answerable questions)"]
    for k in ks:
        lines.append(f"  hit@{k}: {hit_rate(results, k):.0%}   MRR@{k}: {mrr(results, k):.2f}")

    k_main = 4
    misses = [r for r in results if r.item.answerable and not is_hit(r.item, r.ids[:k_main])]
    lines.append(f"\nMISSES at k={k_main} ({len(misses)})")
    for r in misses:
        lines.append(f"  - {r.item.question}")
        lines.append(f"      expected: {', '.join(r.item.expected_sources)}")
        lines.append(f"      got:      {', '.join(r.ids[:k_main])}")

    lines.append("\nTOP-1 SCORE BY GROUP (min / max)")
    for name, test in [
        ("answerable", lambda r: r.item.answerable),
        ("off_topic", lambda r: r.item.abstain_type == "off_topic"),
        ("near_miss", lambda r: r.item.abstain_type == "near_miss"),
    ]:
        scores = sorted(r.top_score for r in results if test(r))
        lines.append(f"  {name:<11} n={len(scores):<3} {scores[0]:.3f} / {scores[-1]:.3f}")

    lines.append("\nTHRESHOLD TRADE-OFF (questions whose top score falls below the threshold)")
    lines.append("  threshold   answerable wrongly rejected   off_topic caught   near_miss caught")
    for row in threshold_table(results, thresholds):
        a, o, n = row["answerable"], row["off_topic"], row["near_miss"]
        lines.append(
            f"  {row['threshold']:.2f}        {a[0]:>2}/{a[1]:<2}"
            f"                         {o[0]:>2}/{o[1]:<2}              {n[0]:>2}/{n[1]}"
        )
    return "\n".join(lines)
