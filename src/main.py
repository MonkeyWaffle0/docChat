from argparse import ArgumentParser
import logging

from src.bot.InteractiveBot import InteractiveBot

# Suppress verbose logging from langchain and other libraries
logging.getLogger("langchain").setLevel(logging.WARNING)
logging.getLogger("langchain_core").setLevel(logging.WARNING)
logging.getLogger("langchain_community").setLevel(logging.WARNING)
logging.getLogger("langchain_ollama").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


def main():
    parser = ArgumentParser(description="RAG CLI for Ollama + Qwen2")
    parser.add_argument("--topk", type=int, default=4, help="retriever top-k")
    args = parser.parse_args()

    InteractiveBot(default_topk=args.topk).chat()


if __name__ == "__main__":
    main()
