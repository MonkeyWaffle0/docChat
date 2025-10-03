#!/bin/bash
set -e

echo "Starting Ollama service..."
ollama serve &

echo "Waiting for Ollama to start..."
sleep 5

ollama pull nomic-embed-text
ollama pull qwen2:7b-instruct

echo ""
echo "=========================================="
echo "Chatbot is ready!"
echo "=========================================="
echo ""

exec python src/main.py "$@"
