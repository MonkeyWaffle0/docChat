from argparse import ArgumentParser

from src.bot.InteractiveBot import InteractiveBot


def main():
    parser = ArgumentParser(description="RAG CLI for Ollama + Qwen2")
    parser.add_argument("--topk", type=int, default=4, help="retriever top-k")
    args = parser.parse_args()

    InteractiveBot(default_topk=args.topk).chat()


if __name__ == "__main__":
    main()
