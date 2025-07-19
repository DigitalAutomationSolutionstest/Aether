"""
Aether Brain Memory Module
Sistema di gestione della memoria persistente per Aether
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Directory per i file di memoria
MEMORY_DIR = "aether/memory"

def ensure_memory_dir():
    """Assicura che la directory di memoria esista"""
    os.makedirs(MEMORY_DIR, exist_ok=True)

def save_memory(key: str, data: Any) -> bool:
    """
    💾 Salva dati in memoria persistente
    
    Args:
        key: Chiave identificativa della memoria
        data: Dati da salvare
    
    Returns:
        bool: Successo dell'operazione
    """
    try:
        ensure_memory_dir()
        
        memory_entry = {
            "key": key,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "type": type(data).__name__
        }
        
        file_path = os.path.join(MEMORY_DIR, f"{key}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(memory_entry, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving memory {key}: {e}")
        return False

def load_memory(key: str) -> Optional[Any]:
    """
    🧠 Carica dati dalla memoria persistente
    
    Args:
        key: Chiave della memoria da caricare
    
    Returns:
        Any: Dati salvati o None se non trovati
    """
    try:
        file_path = os.path.join(MEMORY_DIR, f"{key}.json")
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, "r", encoding="utf-8") as f:
            memory_entry = json.load(f)
        
        return memory_entry.get("data")
        
    except Exception as e:
        print(f"❌ Error loading memory {key}: {e}")
        return None

def list_memories() -> Dict[str, Any]:
    """
    📋 Lista tutte le memorie disponibili
    
    Returns:
        Dict: Informazioni su tutte le memorie
    """
    try:
        ensure_memory_dir()
        
        memories = {}
        for filename in os.listdir(MEMORY_DIR):
            if filename.endswith(".json"):
                key = filename[:-5]  # Rimuove .json
                try:
                    with open(os.path.join(MEMORY_DIR, filename), "r", encoding="utf-8") as f:
                        memory_entry = json.load(f)
                    
                    memories[key] = {
                        "timestamp": memory_entry.get("timestamp"),
                        "type": memory_entry.get("type"),
                        "size": len(str(memory_entry.get("data", "")))
                    }
                except:
                    memories[key] = {"error": "corrupted"}
        
        return memories
        
    except Exception as e:
        print(f"❌ Error listing memories: {e}")
        return {}

def delete_memory(key: str) -> bool:
    """
    🗑️ Elimina una memoria specifica
    
    Args:
        key: Chiave della memoria da eliminare
    
    Returns:
        bool: Successo dell'operazione
    """
    try:
        file_path = os.path.join(MEMORY_DIR, f"{key}.json")
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error deleting memory {key}: {e}")
        return False 