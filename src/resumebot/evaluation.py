"""Measure retrieval against the golden set.

Two questions, answered with numbers rather than impressions:
  1. Do answerable questions retrieve the chunks they need? (hit@k, MRR)
  2. Where should the abstention threshold sit? (a trade-off table: how many
     answerable questions a threshold would wrongly reject, and how many
     unanswerable ones it would catch)
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import yaml

from resumebot.answering import Answer, Answerer
from resumebot.retrieval import Retriever, SearchResult


@dataclass(frozen=True)
class GoldenItem:
    question: str
    answerable: bool
    expected_sources: tuple[str, ...] = ()
    match: str = "all"  # "all": every expected source must be retrieved; "any": one is enough
    abstain_type: str | None = None  # "off_topic" or "near_miss" for unanswerable items
    notes: str = ""  # what a good answer must and must not say


def load_golden(path: Path) -> list[GoldenItem]:
    items = yaml.safe_load(path.read_text(encoding="utf-8"))
    return [
        GoldenItem(
            question=i["question"],
            answerable=i["answerable"],
            expected_sources=tuple(i.get("expected_sources", [])),
            match=i.get("match", "all"),
            abstain_type=i.get("abstain_type"),
            notes=i.get("notes", "").strip(),
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


# --- Answer evaluation (M5) ------------------------------------------------------


@dataclass(frozen=True)
class AnswerResult:
    item: GoldenItem
    answer: Answer
    seconds: float

    @property
    def outcome_correct(self) -> bool:
        """Answerable questions should be answered; the rest should be declined."""
        return self.answer.answerable == self.item.answerable

    @property
    def cited_ids(self) -> list[str]:
        return [c.id for c in self.answer.citations]


def run_answers(answerer: Answerer, items: list[GoldenItem]) -> list[AnswerResult]:
    results = []
    for item in items:
        start = time.perf_counter()
        answer = answerer.ask(item.question)
        results.append(AnswerResult(item, answer, time.perf_counter() - start))
    return results


def answer_summary(results: list[AnswerResult]) -> str:
    def group(test):
        return [r for r in results if test(r.item)]

    answerable = group(lambda i: i.answerable)
    off_topic = group(lambda i: i.abstain_type == "off_topic")
    near_miss = group(lambda i: i.abstain_type == "near_miss")
    answered = [r for r in answerable if r.answer.answerable]
    cited_ok = [r for r in answered if is_hit(r.item, r.cited_ids)]
    dropped = sum(len(r.answer.dropped_citations) for r in results)
    outcomes: dict[str, int] = {}
    for r in results:
        outcomes[r.answer.outcome] = outcomes.get(r.answer.outcome, 0) + 1
    seconds = [r.seconds for r in results]
    usages = [r.answer.usage for r in results if r.answer.usage is not None]

    lines = [
        "ANSWER OUTCOMES",
        f"  answerable questions answered:   {len(answered)}/{len(answerable)}",
        f"  off-topic questions declined:    {sum(r.outcome_correct for r in off_topic)}/{len(off_topic)}",
        f"  near-miss questions declined:    {sum(r.outcome_correct for r in near_miss)}/{len(near_miss)}",
        "CITATIONS",
        f"  answered with expected sources:  {len(cited_ok)}/{len(answered)}",
        f"  invented citations dropped:      {dropped}",
        "OUTCOME COUNTS",
        *(f"  {name:<20} {count}" for name, count in sorted(outcomes.items())),
        f"LATENCY  mean {sum(seconds) / len(seconds):.1f}s   max {max(seconds):.1f}s",
        *_token_lines(usages),
        "WRONG OUTCOMES",
        *(
            f"  - [{'should answer' if r.item.answerable else 'should decline'}] {r.item.question}"
            for r in results
            if not r.outcome_correct
        ),
    ]
    return "\n".join(lines)


def _token_lines(usages: list) -> list[str]:
    if not usages:
        return ["TOKENS   not reported by the provider"]
    n = len(usages)
    prompt = sum(u.prompt_tokens for u in usages)
    completion = sum(u.completion_tokens for u in usages)
    return [
        f"TOKENS   {n} LLM answers: {prompt} in + {completion} out = {prompt + completion} total",
        f"         mean per answer: {prompt / n:.0f} in + {completion / n:.0f} out",
    ]


def answer_report(results: list[AnswerResult], model: str) -> str:
    """Markdown for human review: each answer next to the golden notes."""
    out = [f"# Answer evaluation: {model}", "", "```", answer_summary(results), "```", ""]
    for n, r in enumerate(results, start=1):
        mark = "OK" if r.outcome_correct else "WRONG OUTCOME"
        kind = "answerable" if r.item.answerable else r.item.abstain_type
        out += [
            f"## {n}. {r.item.question}",
            f"**{mark}** · expected: {kind} · got: `{r.answer.outcome}` · {r.seconds:.1f}s"
            f" · by {r.answer.answered_by or 'retrieval'}"
            + (f" · {r.answer.usage.prompt_tokens}+{r.answer.usage.completion_tokens} tokens" if r.answer.usage else ""),
            "",
            f"> {r.answer.text}",
            "",
            f"- cited: {', '.join(f'`{c}`' for c in r.cited_ids) or 'none'}",
            f"- expected: {', '.join(f'`{c}`' for c in r.item.expected_sources) or 'none'}",
        ]
        if r.answer.dropped_citations:
            out.append(f"- dropped (invented): {', '.join(r.answer.dropped_citations)}")
        if r.item.notes:
            out.append(f"- notes: {r.item.notes}")
        out.append("")
    return "\n".join(out)
