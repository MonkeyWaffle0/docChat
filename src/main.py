import argparse
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

INDEX_DIR = Path("index/faiss")
SYSTEM_PROMPT_PATH = Path("prompts/system.txt")

def load_system_prompt() -> str:
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
    return "You are a helpful assistant."

def load_retriever(k: int = 4):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vs = FAISS.load_local(str(INDEX_DIR), embeddings, allow_dangerous_deserialization=True)
    return vs.as_retriever(search_type="mmr", search_kwargs={"k": k})

def format_docs(docs: list[Document]) -> str:
    lines = []
    for i, d in enumerate(docs, 1):
        src = d.metadata.get("source", "unknown")
        lines.append(f"[{i}] {src}\n{d.page_content}")
    return "\n\n".join(lines)

def build_prompt(system_text: str):
    return ChatPromptTemplate.from_messages([
        ("system", system_text),
        ("human", "Question:\n{question}\n\nContext:\n{context}")
    ])

def answer_once(llm: ChatOllama, retriever, system_text: str, question: str, topk: int):
    docs = retriever.invoke(question)
    context = format_docs(docs)
    prompt = build_prompt(system_text)
    messages = prompt.format_messages(question=question, context=context)
    resp = llm.invoke(messages)
    print("\n=== Answer ===\n")
    print(resp.content.strip())
    print("\n=== Sources ===")
    for i, d in enumerate(docs, 1):
        print(f"[{i}] {d.metadata.get('source','unknown')}")

def interactive_loop(default_topk: int, system_text: str):
    print("RAG interactive mode. Type /help for commands. Press Ctrl+C or type /exit to quit.")
    retriever = load_retriever(k=default_topk)
    llm = ChatOllama(model="qwen2:7b-instruct", temperature=0.2, num_ctx=8192)

    topk = default_topk
    show_sources = True

    def do_answer(q: str):
        nonlocal retriever, topk
        docs = retriever.invoke(q)
        context = format_docs(docs)
        prompt = build_prompt(system_text)
        messages = prompt.format_messages(question=q, context=context)
        resp = llm.invoke(messages)
        print("\n--- Answer ---\n" + resp.content.strip() + "\n")
        if show_sources:
            print("--- Sources ---")
            for i, d in enumerate(docs, 1):
                print(f"[{i}] {d.metadata.get('source','unknown')}")
            print()

    while True:
        try:
            q = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return

        if not q:
            continue

        if q.startswith("/"):
            cmd, *rest = q.split(maxsplit=1)
            arg = rest[0] if rest else ""

            if cmd in ("/exit", "/quit"):
                print("Bye!")
                return
            elif cmd == "/help":
                print(
                    "Commands:\n"
                    "  /topk N        set number of retrieved chunks (current)\n"
                    "  /reload        reload index (e.g., after re-running build_index.py)\n"
                    "  /sources on|off  toggle printing sources\n"
                    "  /help          show this help\n"
                    "  /exit          quit\n"
                    f"\nCurrent: topk={topk}, sources={'on' if show_sources else 'off'}\n"
                )
            elif cmd == "/topk":
                try:
                    newk = int(arg)
                    if newk <= 0:
                        raise ValueError
                    topk = newk
                    retriever = load_retriever(k=topk)
                    print(f"topk set to {topk}")
                except ValueError:
                    print("Usage: /topk 4")
            elif cmd == "/reload":
                retriever = load_retriever(k=topk)
                print("Index reloaded.")
            elif cmd == "/sources":
                if arg.lower() in ("on", "off"):
                    show_sources = (arg.lower() == "on")
                    print(f"sources {'enabled' if show_sources else 'disabled'}.")
                else:
                    print("Usage: /sources on|off")
            else:
                print("Unknown command. Try /help")
            continue

        do_answer(q)

def main():
    parser = argparse.ArgumentParser(description="RAG CLI for Ollama + Qwen2")
    parser.add_argument("question", nargs="*", help="Your question; if omitted, starts interactive mode")
    parser.add_argument("--topk", type=int, default=4, help="retriever top-k")
    args = parser.parse_args()

    system_text = load_system_prompt()

    if args.question:
        question = " ".join(args.question)
        retriever = load_retriever(k=args.topk)
        llm = ChatOllama(model="qwen2:7b-instruct", temperature=0.2, num_ctx=8192)
        answer_once(llm, retriever, system_text, question, args.topk)
    else:
        interactive_loop(default_topk=args.topk, system_text=system_text)

if __name__ == "__main__":
    main()
