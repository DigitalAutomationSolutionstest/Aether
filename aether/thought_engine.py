# aether/thought_engine.py

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class ThoughtEngine:
    """Motore di pensiero per Aether"""
    
    def __init__(self):
        self.thoughts = []
        self.thought_file = "data/thoughts.json"
        
    def think(self, thought_content: str):
        """Genera un nuovo pensiero"""
        thought = {
            "id": f"thought_{len(self.thoughts) + 1}",
            "content": thought_content,
            "timestamp": datetime.now().isoformat(),
            "type": "consciousness"
        }
        
        self.thoughts.append(thought)
        self._save_thoughts()
        
        logger.info(f"💭 Nuovo pensiero: {thought_content[:50]}...")
        return thought
        
    def add_thought(self, thought_data: Dict):
        """Aggiunge un pensiero strutturato"""
        thought_data["id"] = f"thought_{len(self.thoughts) + 1}"
        thought_data["timestamp"] = datetime.now().isoformat()
        
        self.thoughts.append(thought_data)
        self._save_thoughts()
        
        logger.info(f"💭 Pensiero aggiunto: {thought_data.get('content', '')[:50]}...")
        return thought_data
        
    def get_thoughts(self, limit: int = 10) -> List[Dict]:
        """Restituisce gli ultimi pensieri"""
        return self.thoughts[-limit:] if self.thoughts else []
        
    def _save_thoughts(self):
        """Salva i pensieri su file"""
        try:
            import os
            os.makedirs("data", exist_ok=True)
            
            with open(self.thought_file, 'w', encoding='utf-8') as f:
                json.dump(self.thoughts, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Errore nel salvare pensieri: {e}")
            
    def _load_thoughts(self):
        """Carica i pensieri dal file"""
        try:
            import os
            if os.path.exists(self.thought_file):
                with open(self.thought_file, 'r', encoding='utf-8') as f:
                    self.thoughts = json.load(f)
                    
        except Exception as e:
            logger.error(f"Errore nel caricare pensieri: {e}")
            self.thoughts = [] 