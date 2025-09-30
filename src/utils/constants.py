from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
INDEX_DIR    = PROJECT_ROOT / "index" / "faiss"
DATA_DIR     = PROJECT_ROOT / "data_raw"
PROMPTS_DIR  = PROJECT_ROOT / "prompts"
SYSTEM_PROMPT = PROMPTS_DIR / "system.txt"

def ensure_dirs() -> None:
    (PROJECT_ROOT / "index").mkdir(parents=True, exist_ok=True)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
