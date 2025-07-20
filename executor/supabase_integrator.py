#!/usr/bin/env python3
"""
📡 SUPABASE CODE MANAGER - Integrazione Database per Aether

Gestisce automaticamente:
- Salvataggio codice generato
- Risultati esecuzioni
- Pensieri e decisioni
- Statistiche performance
- Backup incrementali
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import configurazione Supabase esistente
try:
    from config.supabase_config import get_supabase_client, validate_config
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

logger = logging.getLogger(__name__)

class SupabaseCodeManager:
    """
    📊 Gestore integrazione Supabase per codice e esecuzioni
    
    Tabelle utilizzate:
    - aether_thoughts: Pensieri e intenzioni
    - aether_code_executions: Risultati esecuzioni
    - aether_generated_code: Codice generato
    - aether_performance: Metriche performance
    """
    
    def __init__(self):
        self.client = None
        self.backup_dir = Path("executor/outputs/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        if SUPABASE_AVAILABLE:
            try:
                self.client = get_supabase_client()
                if self.client and validate_config():
                    logger.info("✅ Supabase integrazione attivata")
                    self._ensure_executor_tables()
                else:
                    logger.warning("⚠️ Configurazione Supabase non valida")
            except Exception as e:
                logger.error(f"❌ Errore inizializzazione Supabase: {e}")
        else:
            logger.warning("⚠️ Supabase non disponibile - backup locale attivato")
    
    def _ensure_executor_tables(self):
        """Assicura che le tabelle per l'executor esistano"""
        if not self.client:
            return
        
        # Verifica tabelle esistenti (le tabelle principali sono già create)
        # Qui possiamo aggiungere tabelle specifiche per l'executor se necessario
        try:
            # Test connessione con tabella esistente
            test_query = self.client.table("aether_thoughts").select("id").limit(1).execute()
            logger.debug("✅ Tabelle Supabase verificate")
        except Exception as e:
            logger.warning(f"⚠️ Verifica tabelle fallita: {e}")
    
    def save_thought(self, thought: Dict[str, Any]) -> bool:
        """
        💭 Salva un pensiero nella tabella aether_thoughts
        
        Args:
            thought: Dizionario con il pensiero
            
        Returns:
            bool: Successo operazione
        """
        try:
            # Prepara dati per Supabase
            thought_data = {
                "type": thought.get("type", "code_generation"),
                "content": json.dumps(thought, ensure_ascii=False),
                "context": {
                    "executor": True,
                    "priority": thought.get("priority", "medium"),
                    "source": "code_executor"
                }
            }
            
            # Salva su Supabase
            if self.client:
                result = self.client.table("aether_thoughts").insert(thought_data).execute()
                if result.data:
                    logger.debug(f"💭 Pensiero salvato: {thought.get('type')}")
                    return True
            
            # Fallback locale
            self._save_local_backup("thoughts", thought_data)
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore salvataggio pensiero: {e}")
            self._save_local_backup("thoughts", thought)
            return False
    
    def save_execution_result(self, result: Dict[str, Any]) -> bool:
        """
        ⚡ Salva risultato di esecuzione
        
        Args:
            result: Risultato dell'esecuzione
            
        Returns:
            bool: Successo operazione
        """
        try:
            # Usa tabella aether_memory per i risultati (o aether_thoughts)
            execution_data = {
                "content": f"Execution {result['execution_id']}: {result.get('thought', {}).get('type', 'unknown')}",
                "tags": [
                    "execution",
                    "code_generation", 
                    result.get("thought", {}).get("type", "unknown"),
                    "success" if result.get("success") else "error"
                ]
            }
            
            # Salva su Supabase
            if self.client:
                supabase_result = self.client.table("aether_memory").insert(execution_data).execute()
                if supabase_result.data:
                    logger.debug(f"⚡ Esecuzione salvata: {result['execution_id']}")
                    
                    # Salva anche dettagli come pensiero
                    thought_data = {
                        "type": "execution_result",
                        "content": json.dumps(result, ensure_ascii=False, default=str),
                        "context": {
                            "execution_id": result['execution_id'],
                            "success": result.get("success", False),
                            "executor": True
                        }
                    }
                    
                    self.client.table("aether_thoughts").insert(thought_data).execute()
                    return True
            
            # Fallback locale
            self._save_local_backup("executions", result)
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore salvataggio esecuzione: {e}")
            self._save_local_backup("executions", result)
            return False
    
    def save_generated_code(self, code: str, metadata: Dict[str, Any]) -> bool:
        """
        📝 Salva codice generato
        
        Args:
            code: Codice sorgente
            metadata: Metadati del codice
            
        Returns:
            bool: Successo operazione
        """
        try:
            # Prepara entry per aether_memory
            code_data = {
                "content": f"Generated code: {metadata.get('filename', 'unknown')}",
                "tags": [
                    "generated_code",
                    metadata.get("type", "script"),
                    "python",
                    "aether_executor"
                ]
            }
            
            # Salva su Supabase
            if self.client:
                result = self.client.table("aether_memory").insert(code_data).execute()
                if result.data:
                    logger.debug(f"📝 Codice salvato: {metadata.get('filename')}")
                    return True
            
            # Fallback locale
            code_backup = {
                "code": code,
                "metadata": metadata,
                "timestamp": datetime.now().isoformat()
            }
            self._save_local_backup("generated_code", code_backup)
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore salvataggio codice: {e}")
            return False
    
    def save_performance_metrics(self, metrics: Dict[str, Any]) -> bool:
        """
        📊 Salva metriche di performance
        
        Args:
            metrics: Dizionario con le metriche
            
        Returns:
            bool: Successo operazione
        """
        try:
            # Usa aether_economy per tracking performance
            metrics_data = {
                "action": "code_execution_metrics",
                "cost": metrics.get("execution_time", 0),
                "expected_roi": metrics.get("success_rate", 0) * 100,
                "status": "completed"
            }
            
            if self.client:
                result = self.client.table("aether_economy").insert(metrics_data).execute()
                if result.data:
                    logger.debug("📊 Metriche salvate")
                    return True
            
            # Fallback locale
            self._save_local_backup("metrics", metrics)
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore salvataggio metriche: {e}")
            return False
    
    def get_recent_thoughts(self, limit: int = 10) -> List[Dict]:
        """
        📖 Recupera pensieri recenti
        
        Args:
            limit: Numero massimo di risultati
            
        Returns:
            Lista dei pensieri
        """
        try:
            if self.client:
                result = self.client.table("aether_thoughts").select("*").order("timestamp", desc=True).limit(limit).execute()
                if result.data:
                    return result.data
            
            # Fallback locale
            return self._load_local_backup("thoughts", limit)
            
        except Exception as e:
            logger.error(f"❌ Errore recupero pensieri: {e}")
            return []
    
    def get_execution_history(self, limit: int = 20) -> List[Dict]:
        """
        📜 Recupera storico esecuzioni
        
        Args:
            limit: Numero massimo di risultati
            
        Returns:
            Lista delle esecuzioni
        """
        try:
            if self.client:
                result = self.client.table("aether_memory").select("*").contains("tags", ["execution"]).order("created_at", desc=True).limit(limit).execute()
                if result.data:
                    return result.data
            
            # Fallback locale
            return self._load_local_backup("executions", limit)
            
        except Exception as e:
            logger.error(f"❌ Errore recupero esecuzioni: {e}")
            return []
    
    def _save_local_backup(self, data_type: str, data: Dict[str, Any]):
        """Salva backup locale"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{data_type}_{timestamp}.json"
        filepath = self.backup_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            logger.debug(f"💾 Backup locale salvato: {filename}")
        except Exception as e:
            logger.error(f"❌ Errore backup locale: {e}")
    
    def _load_local_backup(self, data_type: str, limit: int = 10) -> List[Dict]:
        """Carica backup locali"""
        try:
            backup_files = list(self.backup_dir.glob(f"{data_type}_*.json"))
            backup_files.sort(reverse=True)  # Più recenti prima
            
            results = []
            for backup_file in backup_files[:limit]:
                try:
                    with open(backup_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        results.append(data)
                except:
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Errore caricamento backup: {e}")
            return []
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Verifica stato connessione"""
        return {
            "supabase_available": SUPABASE_AVAILABLE,
            "client_connected": self.client is not None,
            "backup_enabled": True,
            "backup_directory": str(self.backup_dir)
        } 