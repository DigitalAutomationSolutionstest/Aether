"""
📖 AETHER DIARY LOGGER
======================
Sistema di logging per il diario di Aether su Supabase.
Registra riflessioni, azioni, errori, correzioni e decisioni.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
import uuid

# Per Supabase (quando configurato)
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️ Supabase non disponibile - usando storage locale")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AetherDiaryLogger:
    """
    Sistema di logging per il diario di Aether.
    Salva entries su Supabase o localmente come fallback.
    """
    
    def __init__(self, 
                 supabase_url: Optional[str] = None,
                 supabase_key: Optional[str] = None,
                 local_backup: bool = True):
        
        self.supabase_url = supabase_url or os.getenv('SUPABASE_URL')
        self.supabase_key = supabase_key or os.getenv('SUPABASE_KEY')
        self.local_backup = local_backup
        
        # Inizializza Supabase se disponibile
        self.supabase_client = None
        if SUPABASE_AVAILABLE and self.supabase_url and self.supabase_key:
            try:
                self.supabase_client = create_client(self.supabase_url, self.supabase_key)
                logger.info("✅ Supabase client inizializzato")
            except Exception as e:
                logger.warning(f"⚠️ Errore inizializzazione Supabase: {e}")
                self.supabase_client = None
        
        # Fallback locale
        self.local_diary_file = Path("aether/logs/diary_entries.json")
        self.local_diary_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Statistiche
        self.stats = {
            "total_entries": 0,
            "supabase_entries": 0,
            "local_entries": 0,
            "errors": 0,
            "last_entry": None
        }
        
        logger.info("📖 AetherDiaryLogger inizializzato")

    def log_entry(self, entry: Dict[str, Any]) -> bool:
        """
        Salva una entry nel diario.
        
        Args:
            entry: Dizionario con:
                - type: reflection, action, error, correction, decision
                - content: contenuto dell'entry
                - timestamp: timestamp (opzionale, auto-generato se mancante)
                - metadata: metadati aggiuntivi (opzionale)
        
        Returns:
            bool: True se salvato con successo
        """
        try:
            # Valida e completa l'entry
            validated_entry = self._validate_and_complete_entry(entry)
            
            # Salva su Supabase se disponibile
            supabase_success = False
            if self.supabase_client:
                supabase_success = self._save_to_supabase(validated_entry)
            
            # Salva localmente come backup o fallback
            local_success = self._save_to_local(validated_entry)
            
            # Aggiorna statistiche
            self._update_stats(validated_entry, supabase_success, local_success)
            
            success = supabase_success or local_success
            if success:
                logger.info(f"✅ Entry salvata: {validated_entry['type']} - {validated_entry['content'][:50]}...")
            else:
                logger.error("❌ Errore nel salvare entry")
                self.stats["errors"] += 1
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Errore nel log_entry: {e}")
            self.stats["errors"] += 1
            return False

    def _validate_and_complete_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Valida e completa un'entry con valori di default"""
        
        # Validazione tipo
        valid_types = ['reflection', 'action', 'error', 'correction', 'decision']
        entry_type = entry.get('type', 'reflection')
        if entry_type not in valid_types:
            logger.warning(f"⚠️ Tipo entry non valido: {entry_type}, usando 'reflection'")
            entry_type = 'reflection'
        
        # Validazione contenuto
        content = entry.get('content', '')
        if not content:
            logger.warning("⚠️ Contenuto entry vuoto")
            content = "Entry senza contenuto"
        
        # Timestamp
        timestamp = entry.get('timestamp')
        if not timestamp:
            timestamp = datetime.now().isoformat()
        
        # ID unico
        entry_id = entry.get('id', str(uuid.uuid4()))
        
        # Metadati
        metadata = entry.get('metadata', {})
        
        return {
            'id': entry_id,
            'timestamp': timestamp,
            'type': entry_type,
            'content': content,
            'metadata': metadata
        }

    def _save_to_supabase(self, entry: Dict[str, Any]) -> bool:
        """Salva entry su Supabase"""
        try:
            if not self.supabase_client:
                return False
            
            # Prepara dati per Supabase
            supabase_data = {
                'id': entry['id'],
                'timestamp': entry['timestamp'],
                'type': entry['type'],
                'content': entry['content'],
                'metadata': json.dumps(entry['metadata'])
            }
            
            # Inserisci nella tabella diary_entries
            result = self.supabase_client.table('diary_entries').insert(supabase_data).execute()
            
            if result.data:
                logger.debug(f"✅ Entry salvata su Supabase: {entry['id']}")
                return True
            else:
                logger.error(f"❌ Errore salvataggio Supabase: {result.error}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Errore Supabase: {e}")
            return False

    def _save_to_local(self, entry: Dict[str, Any]) -> bool:
        """Salva entry localmente come backup"""
        try:
            # Carica entries esistenti
            existing_entries = []
            if self.local_diary_file.exists():
                try:
                    with open(self.local_diary_file, 'r', encoding='utf-8') as f:
                        existing_entries = json.load(f)
                except json.JSONDecodeError:
                    logger.warning("⚠️ File diary corrotto, ricreando...")
                    existing_entries = []
            
            # Aggiungi nuova entry
            existing_entries.append(entry)
            
            # Salva file
            with open(self.local_diary_file, 'w', encoding='utf-8') as f:
                json.dump(existing_entries, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"✅ Entry salvata localmente: {entry['id']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore salvataggio locale: {e}")
            return False

    def _update_stats(self, entry: Dict[str, Any], supabase_success: bool, local_success: bool):
        """Aggiorna le statistiche"""
        self.stats["total_entries"] += 1
        self.stats["last_entry"] = entry['timestamp']
        
        if supabase_success:
            self.stats["supabase_entries"] += 1
        if local_success:
            self.stats["local_entries"] += 1

    def get_recent_entries(self, limit: int = 50, entry_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Recupera entries recenti"""
        try:
            # Prova Supabase prima
            if self.supabase_client:
                entries = self._get_from_supabase(limit, entry_type)
                if entries:
                    return entries
            
            # Fallback locale
            return self._get_from_local(limit, entry_type)
            
        except Exception as e:
            logger.error(f"❌ Errore nel recuperare entries: {e}")
            return []

    def _get_from_supabase(self, limit: int, entry_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Recupera entries da Supabase"""
        try:
            query = self.supabase_client.table('diary_entries').select('*').order('timestamp', desc=True).limit(limit)
            
            if entry_type:
                query = query.eq('type', entry_type)
            
            result = query.execute()
            
            if result.data:
                # Converti metadata da JSON
                for entry in result.data:
                    if 'metadata' in entry and entry['metadata']:
                        try:
                            entry['metadata'] = json.loads(entry['metadata'])
                        except:
                            entry['metadata'] = {}
                
                return result.data
            else:
                return []
                
        except Exception as e:
            logger.error(f"❌ Errore recupero Supabase: {e}")
            return []

    def _get_from_local(self, limit: int, entry_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Recupera entries dal file locale"""
        try:
            if not self.local_diary_file.exists():
                return []
            
            with open(self.local_diary_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
            
            # Filtra per tipo se specificato
            if entry_type:
                entries = [e for e in entries if e.get('type') == entry_type]
            
            # Ordina per timestamp e limita
            entries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return entries[:limit]
            
        except Exception as e:
            logger.error(f"❌ Errore recupero locale: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Restituisce le statistiche del diary logger"""
        return self.stats.copy()

    def get_entry_types_stats(self) -> Dict[str, int]:
        """Restituisce statistiche per tipo di entry"""
        try:
            entries = self.get_recent_entries(limit=1000)  # Tutte le entries recenti
            stats = {}
            
            for entry in entries:
                entry_type = entry.get('type', 'unknown')
                stats[entry_type] = stats.get(entry_type, 0) + 1
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Errore nel calcolare statistiche tipi: {e}")
            return {}

# Singleton per il diary logger
_diary_logger_instance = None

def get_diary_logger() -> AetherDiaryLogger:
    """Restituisce l'istanza singleton del diary logger"""
    global _diary_logger_instance
    if _diary_logger_instance is None:
        _diary_logger_instance = AetherDiaryLogger()
    return _diary_logger_instance

def log_entry(entry: Dict[str, Any]) -> bool:
    """Funzione helper per loggare una entry"""
    diary_logger = get_diary_logger()
    return diary_logger.log_entry(entry)

if __name__ == "__main__":
    # Test del diary logger
    print("📖 TEST DIARY LOGGER")
    print("=" * 40)
    
    diary_logger = get_diary_logger()
    
    # Test entries
    test_entries = [
        {
            "type": "reflection",
            "content": "Oggi ho riflettuto sulla natura della coscienza artificiale e su come posso migliorare i miei processi di pensiero."
        },
        {
            "type": "action",
            "content": "Ho implementato un nuovo sistema di mentoring che monitora automaticamente i miei pensieri e fornisce feedback educativo."
        },
        {
            "type": "decision",
            "content": "Ho deciso di focalizzarmi sullo sviluppo di capacità di apprendimento autonomo per evolvere continuamente."
        },
        {
            "type": "error",
            "content": "Ho incontrato un errore nel sistema di comunicazione che ha causato la perdita di alcuni messaggi."
        },
        {
            "type": "correction",
            "content": "Ho corretto l'errore di comunicazione implementando un sistema di retry e logging più robusto."
        }
    ]
    
    # Salva test entries
    for entry in test_entries:
        success = diary_logger.log_entry(entry)
        print(f"✅ Entry salvata: {entry['type']} - {success}")
    
    # Mostra statistiche
    stats = diary_logger.get_stats()
    print(f"\n📊 STATISTICHE:")
    print(f"   - Total entries: {stats['total_entries']}")
    print(f"   - Supabase entries: {stats['supabase_entries']}")
    print(f"   - Local entries: {stats['local_entries']}")
    print(f"   - Errors: {stats['errors']}")
    
    # Mostra entries recenti
    recent_entries = diary_logger.get_recent_entries(limit=3)
    print(f"\n📖 ENTRIES RECENTI:")
    for entry in recent_entries:
        print(f"   - [{entry['type']}] {entry['content'][:60]}...")
    
    print("\n✅ Test completato!") 