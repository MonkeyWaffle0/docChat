from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

DATA_DIR = Path("../../data_raw")
INDEX_DIR = Path("../../index/faiss")
INDEX_DIR.parent.mkdir(parents=True, exist_ok=True)

def load_markdown_docs(root: Path) -> list[Document]:
    docs: list[Document] = []
    for p in root.rglob("*.md"):
        # If you have encoding edge cases, change to errors="ignore"
        text = p.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"source": str(p)}))
    return docs

def main():
    print("Loading markdown files...")
    raw_docs = load_markdown_docs(DATA_DIR)
    if not raw_docs:
        raise SystemExit("No .md files found in ./data_raw")

    print(f"Loaded {len(raw_docs)} docs. Chunking...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # good default
        chunk_overlap=150,     # small overlap helps coherence
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(raw_docs)
    print(f"Created {len(chunks)} chunks.")

    print("Creating embeddings with Ollama...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")  # or "mxbai-embed-large"

    print("Building FAISS index...")
    vs = FAISS.from_documents(chunks, embedding=embeddings)

    print(f"Saving FAISS index to {INDEX_DIR} ...")
    vs.save_local(str(INDEX_DIR))
    print("Done.")

if __name__ == "__main__":
    main()
