from src.utils.model_loader import (
    load_system_prompt,
    load_retriever,
    load_llm,
    format_docs,
    build_prompt
)


class InteractiveBot:
    def __init__(self, default_topk: int = 4):
        self.default_topk = default_topk
        self.system_text = load_system_prompt()
        self.retriever = load_retriever(k=default_topk)
        self.llm = load_llm()
        self.topk = default_topk
        self.show_sources = True

    def _do_answer(self, q: str):
        docs = self.retriever.invoke(q)
        context = format_docs(docs)
        prompt = build_prompt(self.system_text)
        messages = prompt.format_messages(question=q, context=context)
        resp = self.llm.invoke(messages)
        print("\n--- Answer ---\n" + resp.content.strip() + "\n")
        if self.show_sources:
            print("--- Sources ---")
            for i, d in enumerate(docs, 1):
                print(f"[{i}] {d.metadata.get('source','unknown')}")
            print()

    def chat(self):
        print("RAG interactive mode. Type /help for commands. Press Ctrl+C or type /exit to quit.")

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
                        f"  /topk N        set number of retrieved chunks. 3-4 -> tighter, more on-topic, but may miss relevant bits. 8-12 -> more coverage, but more noise and longer prompts.\n"
                        "  /sources on|off  toggle printing sources\n"
                        "  /help          show this help\n"
                        "  /exit          quit\n"
                        f"\nCurrent: topk={self.topk}, sources={'on' if self.show_sources else 'off'}\n"
                    )
                elif cmd == "/topk":
                    try:
                        newk = int(arg)
                        if newk <= 0:
                            raise ValueError
                        self.topk = newk
                        self.retriever = load_retriever(k=self.topk)
                        print(f"topk set to {self.topk}")
                    except ValueError:
                        print("Usage: /topk 4")
                elif cmd == "/sources":
                    if arg.lower() in ("on", "off"):
                        self.show_sources = (arg.lower() == "on")
                        print(f"sources {'enabled' if self.show_sources else 'disabled'}.")
                    else:
                        print("Usage: /sources on|off")
                else:
                    print("Unknown command. Try /help")
                continue

            self._do_answer(q)