FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir \
    langchain-core \
    langchain-text-splitters \
    langchain-community \
    langchain-ollama \
    faiss-cpu

COPY src/ /app/src/
COPY prompts/ /app/prompts/
COPY README.md /app/

RUN mkdir -p /app/data_raw /app/index/faiss

COPY docker-entrypoint.sh /app/
RUN sed -i 's/\r$//' /app/docker-entrypoint.sh && chmod +x /app/docker-entrypoint.sh

EXPOSE 11434

ENTRYPOINT ["/app/docker-entrypoint.sh"]
