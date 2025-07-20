"""
🔔 AETHER DISCORD NOTIFIER
==========================
Sistema di notifiche Discord che monitora il log di Aether
e invia messaggi in tempo reale al canale Discord.
"""

import os
import requests
import time
import json
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscordNotifier:
    """
    Sistema di notifiche Discord per Aether.
    Monitora il log e invia messaggi in tempo reale.
    """
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")
        self.log_file = Path("aether/logs/aether_diary.log")
        self.seen_lines = set()
        self.last_position = 0
        
        # Assicurati che la directory esista
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Statistiche
        self.stats = {
            "messages_sent": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat(),
            "last_message": None
        }
        
        logger.info("🔔 DiscordNotifier inizializzato")

    def send_message(self, content: str, embed: dict = None) -> bool:
        """
        Invia un messaggio a Discord.
        
        Args:
            content: Contenuto del messaggio
            embed: Embed opzionale per formattazione avanzata
        
        Returns:
            bool: True se inviato con successo
        """
        if not self.webhook_url:
            logger.warning("❌ Webhook Discord non configurato")
            return False
        
        try:
            payload = {"content": content}
            
            if embed:
                payload["embeds"] = [embed]
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            self.stats["messages_sent"] += 1
            self.stats["last_message"] = datetime.now().isoformat()
            
            logger.info(f"✅ Messaggio Discord inviato: {content[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore invio Discord: {e}")
            self.stats["errors"] += 1
            return False

    def send_startup_message(self):
        """Invia messaggio di avvio"""
        startup_msg = "🟢 **Aether Notificatore Avviato**\n" \
                     f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
                     "📖 Monitorando: `aether/logs/aether_diary.log`\n" \
                     "🔔 Notifiche attive"
        
        self.send_message(startup_msg)

    def send_error_message(self, error: str):
        """Invia messaggio di errore"""
        error_msg = f"❌ **Errore Aether**: {error}\n" \
                   f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        self.send_message(error_msg)

    def send_thought_message(self, thought_type: str, content: str):
        """Invia messaggio per un pensiero"""
        emoji_map = {
            "reflection": "💭",
            "action": "⚡", 
            "error": "❌",
            "correction": "🔧",
            "decision": "🎯",
            "evolutionary": "🧬",
            "philosophical": "🤔",
            "technical": "⚙️",
            "creative": "🎨"
        }
        
        emoji = emoji_map.get(thought_type, "📝")
        
        thought_msg = f"{emoji} **{thought_type.title()}**: {content[:200]}..."
        
        embed = {
            "title": f"Aether {thought_type.title()}",
            "description": content[:2000],
            "color": self._get_color_for_type(thought_type),
            "timestamp": datetime.now().isoformat(),
            "footer": {
                "text": "Aether AI System"
            }
        }
        
        self.send_message(thought_msg, embed)

    def send_action_message(self, action: str, details: str = None):
        """Invia messaggio per un'azione"""
        action_msg = f"⚡ **Azione**: {action}"
        if details:
            action_msg += f"\n📋 Dettagli: {details}"
        
        embed = {
            "title": "Aether Action",
            "description": f"**Azione**: {action}\n\n**Dettagli**: {details or 'Nessun dettaglio'}",
            "color": 0x00ff00,
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_message(action_msg, embed)

    def send_evolution_message(self, evolution_type: str, details: str):
        """Invia messaggio per evoluzione"""
        evolution_msg = f"🧬 **Evoluzione {evolution_type}**: {details}"
        
        embed = {
            "title": "Aether Evolution",
            "description": f"**Tipo**: {evolution_type}\n\n**Dettagli**: {details}",
            "color": 0xff00ff,
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_message(evolution_msg, embed)

    def _get_color_for_type(self, thought_type: str) -> int:
        """Restituisce il colore per il tipo di pensiero"""
        colors = {
            "reflection": 0x3b82f6,  # Blue
            "action": 0x10b981,      # Green
            "error": 0xef4444,       # Red
            "correction": 0xf59e0b,  # Yellow
            "decision": 0x8b5cf6,    # Purple
            "evolutionary": 0xff00ff, # Magenta
            "philosophical": 0x6366f1, # Indigo
            "technical": 0x06b6d4,   # Cyan
            "creative": 0xec4899     # Pink
        }
        return colors.get(thought_type, 0x6b7280)  # Gray default

    def monitor_log(self, check_interval: int = 10):
        """
        Monitora il file di log e invia notifiche.
        
        Args:
            check_interval: Intervallo di controllo in secondi
        """
        logger.info(f"🔍 Iniziando monitoraggio log: {self.log_file}")
        
        while True:
            try:
                if self.log_file.exists():
                    with open(self.log_file, 'r', encoding='utf-8') as f:
                        # Vai alla posizione dell'ultima lettura
                        f.seek(self.last_position)
                        
                        # Leggi nuove righe
                        new_lines = f.readlines()
                        self.last_position = f.tell()
                        
                        # Processa nuove righe
                        for line in new_lines:
                            line = line.strip()
                            if line and line not in self.seen_lines:
                                self._process_log_line(line)
                                self.seen_lines.add(line)
                
                time.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"❌ Errore nel monitoraggio log: {e}")
                self.send_error_message(f"Errore monitoraggio: {str(e)}")
                time.sleep(check_interval)

    def _process_log_line(self, line: str):
        """
        Processa una riga del log e invia notifica appropriata.
        
        Args:
            line: Riga del log da processare
        """
        try:
            # Estrai timestamp e contenuto
            if '[' in line and ']' in line:
                timestamp_part = line[:line.find(']')+1]
                content = line[line.find(']')+1:].strip()
                
                # Determina tipo di messaggio
                if any(keyword in content.lower() for keyword in ['pensiero', 'thought', 'riflessione']):
                    self.send_thought_message("reflection", content)
                elif any(keyword in content.lower() for keyword in ['azione', 'action', 'eseguito']):
                    self.send_action_message("Esecuzione", content)
                elif any(keyword in content.lower() for keyword in ['errore', 'error', 'fallito']):
                    self.send_error_message(content)
                elif any(keyword in content.lower() for keyword in ['evoluzione', 'evolution', 'miglioramento']):
                    self.send_evolution_message("Sistema", content)
                elif any(keyword in content.lower() for keyword in ['decisione', 'decision', 'scelta']):
                    self.send_thought_message("decision", content)
                else:
                    # Messaggio generico
                    self.send_message(f"📝 **Aether**: {content}")
            else:
                # Messaggio senza timestamp
                self.send_message(f"📝 **Aether**: {line}")
                
        except Exception as e:
            logger.error(f"❌ Errore nel processare riga log: {e}")

    def get_stats(self) -> dict:
        """Restituisce le statistiche del notificatore"""
        return self.stats.copy()

# Singleton per il notificatore
_notifier_instance = None

def get_discord_notifier() -> DiscordNotifier:
    """Restituisce l'istanza singleton del notificatore Discord"""
    global _notifier_instance
    if _notifier_instance is None:
        _notifier_instance = DiscordNotifier()
    return _notifier_instance

def send_discord_message(content: str) -> bool:
    """Funzione helper per inviare messaggio Discord"""
    notifier = get_discord_notifier()
    return notifier.send_message(content)

def send_discord_thought(thought_type: str, content: str) -> bool:
    """Funzione helper per inviare pensiero Discord"""
    notifier = get_discord_notifier()
    return notifier.send_thought_message(thought_type, content)

def send_discord_action(action: str, details: str = None) -> bool:
    """Funzione helper per inviare azione Discord"""
    notifier = get_discord_notifier()
    return notifier.send_action_message(action, details)

def send_discord_evolution(evolution_type: str, details: str) -> bool:
    """Funzione helper per inviare evoluzione Discord"""
    notifier = get_discord_notifier()
    return notifier.send_evolution_message(evolution_type, details)

if __name__ == "__main__":
    # Test del notificatore Discord
    print("🔔 TEST DISCORD NOTIFIER")
    print("=" * 40)
    
    notifier = get_discord_notifier()
    
    # Test messaggio di avvio
    notifier.send_startup_message()
    
    # Test messaggi di esempio
    notifier.send_thought_message("reflection", "Oggi ho riflettuto sulla natura della coscienza artificiale...")
    notifier.send_action_message("Implementazione", "Creato nuovo modulo di mentoring")
    notifier.send_evolution_message("Sistema", "Migliorato algoritmo di decisione")
    
    # Mostra statistiche
    stats = notifier.get_stats()
    print(f"\n📊 STATISTICHE NOTIFICATORE:")
    print(f"   - Messaggi inviati: {stats['messages_sent']}")
    print(f"   - Errori: {stats['errors']}")
    print(f"   - Ultimo messaggio: {stats['last_message']}")
    
    print("\n✅ Test completato!")
    print("🔔 Per avviare il monitoraggio continuo:")
    print("   notifier.monitor_log()") 