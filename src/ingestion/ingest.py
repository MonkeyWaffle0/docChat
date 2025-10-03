from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader

from src.utils.constants import ensure_dirs, DATA_DIR, INDEX_DIR


def load_documents(root: Path) -> list[Document]:
    docs: list[Document] = []
    extensions = ["*.md", "*.txt", "*.adoc", "*.pdf"]

    for ext in extensions:
        for p in root.rglob(ext):
            if ext == "*.pdf":
                loader = PyPDFLoader(str(p))
                pdf_docs = loader.load()
                for doc in pdf_docs:
                    doc.metadata["source"] = str(p)
                docs.extend(pdf_docs)
            else:
                text = p.read_text(encoding="utf-8")
                docs.append(Document(page_content=text, metadata={"source": str(p)}))

    return docs


def main():
    ensure_dirs()
    print("Loading documents (.md, .pdf, .txt, .adoc)...")
    raw_docs = load_documents(DATA_DIR)
    if not raw_docs:
        raise SystemExit("No supported files found in data directory")

    print(f"Loaded {len(raw_docs)} docs. Chunking...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n---\n", "\n## ", "\n\n", "\n"],
    )
    chunks = splitter.split_documents(raw_docs)
    print(f"Created {len(chunks)} chunks.")

    print("Creating embeddings with Ollama...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    print("Building FAISS index...")
    vs = FAISS.from_documents(chunks, embedding=embeddings)

    print(f"Saving FAISS index to {INDEX_DIR} ...")
    vs.save_local(str(INDEX_DIR))
    print("Done.")


if __name__ == "__main__":
    main()
