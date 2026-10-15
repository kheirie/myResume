import argparse
from pathlib import Path

CORPUS_DIR = Path("corpus/approved")


def search(question: str, k: int) -> None:
    from resumebot.corpus import load_corpus
    from resumebot.embeddings import FastEmbedEmbedder
    from resumebot.retrieval import Retriever

    retriever = Retriever(load_corpus(CORPUS_DIR), FastEmbedEmbedder())
    for rank, hit in enumerate(retriever.search(question, k=k), start=1):
        print(f"{rank}. {hit.score:.3f}  {hit.chunk.id}")
        print(f"   sources: {'; '.join(hit.chunk.sources)}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="resumebot")
    commands = parser.add_subparsers(dest="command", required=True)
    search_cmd = commands.add_parser("search", help="show the chunks retrieved for a question")
    search_cmd.add_argument("question")
    search_cmd.add_argument("-k", type=int, default=4, help="number of chunks to return")
    args = parser.parse_args()

    if args.command == "search":
        search(args.question, args.k)


if __name__ == "__main__":
    main()
