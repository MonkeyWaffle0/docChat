# RAG-based Chatbot for Straumann Group Documentation

A Retrieval-Augmented Generation (RAG) chatbot powered by Qwen2 models for querying Straumann Group documentation.

## Requirements

### Python Packages

Install the required packages:

```bash
pip install langchain-core langchain-text-splitters langchain-community langchain-ollama faiss-cpu
```

### Ollama

Install [Ollama](https://ollama.ai/) and pull the required models:

```bash
ollama pull nomic-embed-text
ollama pull qwen2:7b-instruct
```

## Setup

1. Place your documentation files in the `data_raw/` folder

2. Run the ingestion script to create the FAISS index:
   ```bash
   python src/ingestion/ingest.py
   ```
   This will process all `.md` files in `data_raw/` and create a searchable vector index in `index/faiss/`

## Usage

Run the chatbot in interactive mode:

```bash
python src/main.py
```

Or ask a single question:

```bash
python src/main.py "What is Straumann's approach to...?"
```

### Interactive Commands

- `/topk N` - Set number of retrieved chunks
- `/reload` - Reload index after re-running ingestion
- `/sources on|off` - Toggle source citations
- `/help` - Show available commands
- `/exit` - Quit

## How It Works

The system uses:
- **nomic-embed-text** for document embeddings
- **qwen2:7b-instruct** as the language model
- **FAISS** for efficient vector similarity search
- **LangChain** for RAG orchestration

## Using by docker

 - Download & Install python (https://www.python.org/downloads/)
 - Download & Install Docker (https://docs.docker.com/desktop/setup/install/windows-install/)
 - Clone de repo https://github.com/MonkeyWaffle0/docChat
 - Add at the folder ../data_raw the documentation you want to use.
 - Run the following command from the project root folder `py -m src.ingestion.ingest` (It will index the given documentation)
 - Create the docker image ```bash docker-compose build``` using the cmd.
 - Run the image just created ```docker-compose run --rm docchat``` using the cmd.
 - Enjoy