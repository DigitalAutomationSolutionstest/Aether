import json
from pathlib import Path

MEMORY_FILE = Path("data/memory.json")

def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return []

def save_memory(data):
    MEMORY_FILE.write_text(json.dumps(data, indent=2))

def add_to_memory(entry):
    mem = load_memory()
    mem.append(entry)
    save_memory(mem) 