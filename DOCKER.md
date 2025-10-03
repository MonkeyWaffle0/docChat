# Docker Setup Guide

## Quick Start

### 1. Build and Run with Docker Compose

```bash
# Build the image
docker-compose build

# Run the chatbot
docker-compose run --rm docchat
```

The first run will:
- Start Ollama service
- Download required models (nomic-embed-text, qwen2:7b-instruct) - this may take a few minutes
- Start the interactive chatbot


## Persistence

The setup includes volumes for:
- `./data_raw` - Your documentation files
- `./index` - FAISS vector index (persists between runs)
- `ollama_data` - Downloaded Ollama models (avoids re-downloading)
