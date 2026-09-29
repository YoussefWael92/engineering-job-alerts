import json
from pathlib import Path

DATA_FILE = Path("data/jobs.json")


def load_seen():
    if not DATA_FILE.exists():
        return set()
    try:
        data = json.loads(DATA_FILE.read_text())
        return set(data if isinstance(data, list) else [])
    except Exception:
        return set()


def save_seen(seen):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(sorted(seen), indent=2),
        encoding="utf-8",
    )
