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
    eval_cmd = commands.add_parser("eval-retrieval", help="measure retrieval against evals/golden.yaml")
    for cmd in (search_cmd, eval_cmd):
        cmd.add_argument("--no-rerank", action="store_true", help="skip the cross-encoder stage")
    args = parser.parse_args()

    if args.command == "search":
        search(args.question, args.k, rerank=not args.no_rerank)
    elif args.command == "eval-retrieval":
        eval_retrieval(rerank=not args.no_rerank)


if __name__ == "__main__":
    main()
