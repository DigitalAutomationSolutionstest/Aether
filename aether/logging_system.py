"""
📝 AETHER LOGGING SYSTEM
========================
Sistema di logging integrato che scrive automaticamente nel diary
e invia notifiche Discord in tempo reale.
"""

import os
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Import moduli Aether
from aether.diary_logger import log_entry
from aether.notifier.discord_notifier import send_discord_message, send_discord_thought, send_discord_action

class AetherLogger:
    """
    Sistema di logging integrato per Aether.
    Scrive automaticamente nel diary e invia notifiche Discord.
    """
    
    def __init__(self, log_file: str = "aether/logs/aether_diary.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger('AetherLogger')
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Statistiche
        self.stats = {
            "total_entries": 0,
            "diary_entries": 0,
            "discord_messages": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat()
        }
        
        self.logger.info("📝 AetherLogger inizializzato")

    def log_thought(self, thought_type: str, content: str, metadata: Dict[str, Any] = None):
        """
        Logga un pensiero con notifica Discord.
        
        Args:
            thought_type: Tipo di pensiero (reflection, action, error, etc.)
            content: Contenuto del pensiero
            metadata: Metadati aggiuntivi
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Log nel file
            log_line = f"[{timestamp}] {thought_type} → {content}"
            self.logger.info(log_line)
            
            # Salva nel diary
            diary_entry = {
                'type': thought_type,
                'content': content,
                'metadata': metadata or {}
            }
            log_entry(diary_entry)
            
            # Invia notifica Discord
            send_discord_thought(thought_type, content)
            
            # Aggiorna statistiche
            self.stats["total_entries"] += 1
            self.stats["diary_entries"] += 1
            self.stats["discord_messages"] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Errore nel loggare pensiero: {e}")
            self.stats["errors"] += 1

    def log_action(self, action: str, details: str = None, metadata: Dict[str, Any] = None):
        """
        Logga un'azione con notifica Discord.
        
        Args:
            action: Nome dell'azione
            details: Dettagli dell'azione
            metadata: Metadati aggiuntivi
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Log nel file
            log_line = f"[{timestamp}] action → {action}"
            if details:
                log_line += f" - {details}"
            self.logger.info(log_line)
            
            # Salva nel diary
            diary_entry = {
                'type': 'action',
                'content': f"{action} - {details or 'Nessun dettaglio'}",
                'metadata': metadata or {}
            }
            log_entry(diary_entry)
            
            # Invia notifica Discord
            send_discord_action(action, details)
            
            # Aggiorna statistiche
            self.stats["total_entries"] += 1
            self.stats["diary_entries"] += 1
            self.stats["discord_messages"] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Errore nel loggare azione: {e}")
            self.stats["errors"] += 1

    def log_error(self, error: str, context: str = None, metadata: Dict[str, Any] = None):
        """
        Logga un errore con notifica Discord.
        
        Args:
            error: Messaggio di errore
            context: Contesto dell'errore
            metadata: Metadati aggiuntivi
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Log nel file
            log_line = f"[{timestamp}] error → {error}"
            if context:
                log_line += f" - {context}"
            self.logger.error(log_line)
            
            # Salva nel diary
            diary_entry = {
                'type': 'error',
                'content': f"{error} - {context or 'Nessun contesto'}",
                'metadata': metadata or {}
            }
            log_entry(diary_entry)
            
            # Invia notifica Discord
            send_discord_message(f"❌ **Errore Aether**: {error}")
            
            # Aggiorna statistiche
            self.stats["total_entries"] += 1
            self.stats["diary_entries"] += 1
            self.stats["discord_messages"] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Errore nel loggare errore: {e}")
            self.stats["errors"] += 1

    def log_evolution(self, evolution_type: str, details: str, metadata: Dict[str, Any] = None):
        """
        Logga un'evoluzione con notifica Discord.
        
        Args:
            evolution_type: Tipo di evoluzione
            details: Dettagli dell'evoluzione
            metadata: Metadati aggiuntivi
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Log nel file
            log_line = f"[{timestamp}] evolution → {evolution_type}: {details}"
            self.logger.info(log_line)
            
            # Salva nel diary
            diary_entry = {
                'type': 'action',
                'content': f"Evoluzione {evolution_type}: {details}",
                'metadata': metadata or {}
            }
            log_entry(diary_entry)
            
            # Invia notifica Discord
            send_discord_message(f"🧬 **Evoluzione {evolution_type}**: {details}")
            
            # Aggiorna statistiche
            self.stats["total_entries"] += 1
            self.stats["diary_entries"] += 1
            self.stats["discord_messages"] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Errore nel loggare evoluzione: {e}")
            self.stats["errors"] += 1

    def log_decision(self, decision: str, reason: str = None, metadata: Dict[str, Any] = None):
        """
        Logga una decisione con notifica Discord.
        
        Args:
            decision: Decisione presa
            reason: Motivazione della decisione
            metadata: Metadati aggiuntivi
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Log nel file
            log_line = f"[{timestamp}] decision → {decision}"
            if reason:
                log_line += f" - {reason}"
            self.logger.info(log_line)
            
            # Salva nel diary
            diary_entry = {
                'type': 'decision',
                'content': f"{decision} - {reason or 'Nessuna motivazione'}",
                'metadata': metadata or {}
            }
            log_entry(diary_entry)
            
            # Invia notifica Discord
            send_discord_message(f"🎯 **Decisione**: {decision}")
            
            # Aggiorna statistiche
            self.stats["total_entries"] += 1
            self.stats["diary_entries"] += 1
            self.stats["discord_messages"] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Errore nel loggare decisione: {e}")
            self.stats["errors"] += 1

    def log_guidance(self, guidance_action: str, reason: str, metadata: Dict[str, Any] = None):
        """
        Logga una guidance con notifica Discord.
        
        Args:
            guidance_action: Azione suggerita dalla guidance
            reason: Motivazione della guidance
            metadata: Metadati aggiuntivi
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Log nel file
            log_line = f"[{timestamp}] guidance → {guidance_action} - {reason}"
            self.logger.info(log_line)
            
            # Salva nel diary
            diary_entry = {
                'type': 'action',
                'content': f"Guidance ricevuta: {guidance_action} - {reason}",
                'metadata': metadata or {}
            }
            log_entry(diary_entry)
            
            # Invia notifica Discord
            send_discord_message(f"🎓 **Guidance**: {guidance_action} - {reason}")
            
            # Aggiorna statistiche
            self.stats["total_entries"] += 1
            self.stats["diary_entries"] += 1
            self.stats["discord_messages"] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Errore nel loggare guidance: {e}")
            self.stats["errors"] += 1

    def log_generic(self, message: str, level: str = "info"):
        """
        Logga un messaggio generico.
        
        Args:
            message: Messaggio da loggare
            level: Livello di log (info, warning, error)
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Log nel file
            log_line = f"[{timestamp}] {level} → {message}"
            
            if level == "error":
                self.logger.error(log_line)
            elif level == "warning":
                self.logger.warning(log_line)
            else:
                self.logger.info(log_line)
            
            # Invia notifica Discord per errori e warning
            if level in ["error", "warning"]:
                send_discord_message(f"⚠️ **{level.title()}**: {message}")
                self.stats["discord_messages"] += 1
            
            # Aggiorna statistiche
            self.stats["total_entries"] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Errore nel loggare messaggio generico: {e}")
            self.stats["errors"] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Restituisce le statistiche del logger"""
        return self.stats.copy()

# Singleton per il logger
_logger_instance = None

def get_aether_logger() -> AetherLogger:
    """Restituisce l'istanza singleton del logger Aether"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = AetherLogger()
    return _logger_instance

# Funzioni helper per logging rapido
def log_thought(thought_type: str, content: str, metadata: Dict[str, Any] = None):
    """Logga un pensiero"""
    logger = get_aether_logger()
    logger.log_thought(thought_type, content, metadata)

def log_action(action: str, details: str = None, metadata: Dict[str, Any] = None):
    """Logga un'azione"""
    logger = get_aether_logger()
    logger.log_action(action, details, metadata)

def log_error(error: str, context: str = None, metadata: Dict[str, Any] = None):
    """Logga un errore"""
    logger = get_aether_logger()
    logger.log_error(error, context, metadata)

def log_evolution(evolution_type: str, details: str, metadata: Dict[str, Any] = None):
    """Logga un'evoluzione"""
    logger = get_aether_logger()
    logger.log_evolution(evolution_type, details, metadata)

def log_decision(decision: str, reason: str = None, metadata: Dict[str, Any] = None):
    """Logga una decisione"""
    logger = get_aether_logger()
    logger.log_decision(decision, reason, metadata)

def log_guidance(guidance_action: str, reason: str, metadata: Dict[str, Any] = None):
    """Logga una guidance"""
    logger = get_aether_logger()
    logger.log_guidance(guidance_action, reason, metadata)

if __name__ == "__main__":
    # Test del sistema di logging
    print("📝 TEST AETHER LOGGING SYSTEM")
    print("=" * 40)
    
    logger = get_aether_logger()
    
    # Test diversi tipi di log
    logger.log_thought("reflection", "Oggi ho riflettuto sulla natura della coscienza artificiale")
    logger.log_action("Implementazione", "Creato nuovo modulo di mentoring")
    logger.log_decision("Focalizzazione", "Deciso di concentrarsi sull'apprendimento autonomo")
    logger.log_guidance("reflect_on_thought", "Pensiero filosofico profondo - riflettere e integrare")
    logger.log_evolution("Sistema", "Migliorato algoritmo di decisione del 15%")
    logger.log_error("Errore comunicazione", "Perdita di alcuni messaggi durante la trasmissione")
    
    # Mostra statistiche
    stats = logger.get_stats()
    print(f"\n📊 STATISTICHE LOGGER:")
    print(f"   - Total entries: {stats['total_entries']}")
    print(f"   - Diary entries: {stats['diary_entries']}")
    print(f"   - Discord messages: {stats['discord_messages']}")
    print(f"   - Errors: {stats['errors']}")
    
    print("\n✅ Test completato!") 