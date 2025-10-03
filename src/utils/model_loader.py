from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from src.utils.constants import SYSTEM_PROMPT, INDEX_DIR


def load_system_prompt() -> str:
    if SYSTEM_PROMPT.exists():
        return SYSTEM_PROMPT.read_text(encoding="utf-8").strip()
    return "You are a helpful assistant."


def load_retriever(k: int = 3):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vs = FAISS.load_local(str(INDEX_DIR), embeddings, allow_dangerous_deserialization=True)
    return vs.as_retriever(search_type="similarity",
                           search_kwargs={"k": k})


def load_llm():
    return ChatOllama(model="qwen2:7b-instruct",
                      temperature=0.0,
                      top_p=1.0,
                      num_ctx=8192,
                      seed=42)


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
