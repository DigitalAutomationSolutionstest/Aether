# aether/supabase_client.py

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Client per Supabase (simulato)"""
    
    def __init__(self):
        self.events_file = "data/supabase_events.json"
        self.events = []
        
    def store_event(self, event_type: str, data: Dict[str, Any]):
        """Salva un evento su Supabase (simulato)"""
        event = {
            "id": f"event_{len(self.events) + 1}",
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        self.events.append(event)
        self._save_events()
        
        logger.info(f"📝 Evento salvato: {event_type} - {str(data)[:50]}...")
        return event
        
    def _save_events(self):
        """Salva gli eventi su file"""
        try:
            import os
            os.makedirs("data", exist_ok=True)
            
            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Errore nel salvare eventi: {e}")

# Istanza globale
_supabase_client = None

def get_supabase_client():
    """Restituisce l'istanza del client Supabase"""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = SupabaseClient()
    return _supabase_client

def store_event(event_type: str, data: Dict[str, Any]):
    """Funzione helper per salvare eventi"""
    client = get_supabase_client()
    return client.store_event(event_type, data) 