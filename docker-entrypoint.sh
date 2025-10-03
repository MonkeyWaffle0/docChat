#!/bin/bash
set -e

echo "Starting Ollama service..."

ollama serve >"$OLLAMA_LOG_FILE" 2>&1 &

echo "Waiting for Ollama to start..."
sleep 5

ollama pull nomic-embed-text  >"$OLLAMA_LOG_FILE" 2>&1
ollama pull qwen2:7b-instruct  >"$OLLAMA_LOG_FILE" 2>&1

echo ""
echo "=========================================="
echo "Chatbot is ready!"
echo "=========================================="
echo ""

exec python src/main.py "$@"
