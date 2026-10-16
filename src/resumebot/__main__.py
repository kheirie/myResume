import argparse
from pathlib import Path

CORPUS_DIR = Path("corpus/approved")
GOLDEN_PATH = Path("evals/golden.yaml")


def build_retriever(rerank: bool = True):
    from resumebot.corpus import load_corpus
    from resumebot.embeddings import FastEmbedEmbedder
    from resumebot.reranking import FastEmbedReranker
    from resumebot.retrieval import Retriever

    reranker = FastEmbedReranker() if rerank else None
    return Retriever(load_corpus(CORPUS_DIR), FastEmbedEmbedder(), reranker=reranker)


def search(question: str, k: int, rerank: bool) -> None:
    from resumebot.retrieval import ABSTAIN_BELOW

    result = build_retriever(rerank).search(question, k=k)
    verdict = "ABSTAIN" if result.should_abstain else "answer"
    print(f"top similarity {result.top_similarity:.3f} (threshold {ABSTAIN_BELOW}) -> {verdict}")
    for rank, hit in enumerate(result.hits, start=1):
        rerank_note = f"  rerank {hit.rerank_score:6.2f}" if hit.rerank_score is not None else ""
        print(f"{rank}. similarity {hit.score:.3f}{rerank_note}  {hit.chunk.id}")


def ask(question: str, provider: str | None) -> None:
    import time

    from resumebot.answering import Answerer
    from resumebot.llm import build_llm

    llm = build_llm(provider)
    answerer = Answerer(build_retriever(), llm)
    start = time.perf_counter()
    answer = answerer.ask(question)
    print(answer.text)
    for chunk in answer.citations:
        print(f"  [{chunk.id}] {'; '.join(chunk.sources)}")
    if answer.dropped_citations:
        print(f"  (dropped invented citations: {', '.join(answer.dropped_citations)})")
    print(f"\n{answer.outcome} | {answer.answered_by or 'no LLM call'} | {time.perf_counter() - start:.1f}s")
    if answer.usage:
        u = answer.usage
        print(f"tokens: {u.prompt_tokens} in + {u.completion_tokens} out = {u.total_tokens}")
    remaining = getattr(llm, "rate_limit", {}).get("x-ratelimit-remaining-tokens")
    if remaining:
        print(f"rate limit: {remaining} tokens left this minute")


def eval_answers(provider: str | None) -> None:
    from datetime import datetime

    from resumebot.answering import PROMPT_VERSION, Answerer
    from resumebot.evaluation import answer_report, answer_summary, load_golden, run_answers
    from resumebot.llm import build_llm
    from resumebot.retrieval import ABSTAIN_BELOW

    llm = build_llm(provider)
    results = run_answers(Answerer(build_retriever(), llm), load_golden(GOLDEN_PATH))
    report_dir = Path("evals/reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    label = f"{llm.label}, prompt {PROMPT_VERSION}, threshold {ABSTAIN_BELOW}"
    name = provider or "default"
    stamp = f"{datetime.now():%Y-%m-%d-%H%M}-{name}-prompt-{PROMPT_VERSION}"
    path = report_dir / f"answers-{stamp}.md"
    path.write_text(answer_report(results, label), encoding="utf-8")
    print(answer_summary(results))
    print(f"\nFull report for review: {path}")


def eval_retrieval(rerank: bool) -> None:
    from resumebot.evaluation import load_golden, report, run

    results = run(build_retriever(rerank), load_golden(GOLDEN_PATH), k=6)
    print(report(results, ks=[1, 3, 4, 6], thresholds=[0.50, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62]))


def main() -> None:
    parser = argparse.ArgumentParser(prog="resumebot")
    commands = parser.add_subparsers(dest="command", required=True)
    search_cmd = commands.add_parser("search", help="show the chunks retrieved for a question")
    search_cmd.add_argument("question")
    search_cmd.add_argument("-k", type=int, default=4, help="number of chunks to return")
    ask_cmd = commands.add_parser("ask", help="answer a question with citations")
    ask_cmd.add_argument("question")
    answers_cmd = commands.add_parser("eval-answers", help="run every golden question through the full pipeline")
    for cmd in (ask_cmd, answers_cmd):
        cmd.add_argument(
            "--provider",
            choices=["ollama", "groq", "openrouter", "huggingface", "chain"],
            help="LLM to use; 'chain' tries LLM_FALLBACK_ORDER in turn (default: LLM_PROVIDER or ollama)",
        )
    eval_cmd = commands.add_parser("eval-retrieval", help="measure retrieval against evals/golden.yaml")
    for cmd in (search_cmd, eval_cmd):
        cmd.add_argument("--no-rerank", action="store_true", help="skip the cross-encoder stage")
    args = parser.parse_args()

    if args.command == "search":
        search(args.question, args.k, rerank=not args.no_rerank)
    elif args.command == "ask":
        ask(args.question, args.provider)
    elif args.command == "eval-answers":
        eval_answers(args.provider)
    elif args.command == "eval-retrieval":
        eval_retrieval(rerank=not args.no_rerank)


if __name__ == "__main__":
    main()
