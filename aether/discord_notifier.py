import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import logging

# Carica variabili ambiente
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_message(content, title=None, color=None, fields=None):
    """
    Invia un messaggio su Discord tramite webhook
    
    Args:
        content (str): Contenuto del messaggio
        title (str, optional): Titolo del messaggio embed
        color (int, optional): Colore dell'embed (es. 0x00ff00 per verde)
        fields (list, optional): Lista di campi per l'embed
    """
    if not DISCORD_WEBHOOK_URL:
        logger.warning("❌ Discord Webhook non configurato! Aggiungi DISCORD_WEBHOOK_URL nel file .env")
        return False
    
    try:
        # Messaggio semplice
        if not title and not fields:
            payload = {
                "content": f"🤖 **Aether** | {content}",
                "username": "Aether AI",
                "avatar_url": "https://cdn.discordapp.com/avatars/123456789/aether_avatar.png"
            }
        else:
            # Messaggio embed avanzato
            embed = {
                "title": title or "Aether Notification",
                "description": content,
                "color": color or 0x00ff41,  # Verde cyber default
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {
                    "text": "Aether AI System",
                    "icon_url": "https://cdn.discordapp.com/avatars/123456789/aether_avatar.png"
                }
            }
            
            if fields:
                embed["fields"] = fields
                
            payload = {
                "embeds": [embed],
                "username": "Aether AI",
                "avatar_url": "https://cdn.discordapp.com/avatars/123456789/aether_avatar.png"
            }
        
        # Invia richiesta
        response = requests.post(
            DISCORD_WEBHOOK_URL, 
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [200, 204]:
            logger.info(f"✅ Messaggio Discord inviato: {content[:50]}...")
            return True
        else:
            logger.error(f"❌ Errore Discord: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Errore connessione Discord: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Errore generico Discord: {e}")
        return False

def notify_system_start():
    """Notifica avvio sistema"""
    send_discord_message(
        "Sistema avviato e operativo! 🚀",
        title="🟢 Sistema Online",
        color=0x00ff00,
        fields=[
            {"name": "Status", "value": "✅ Attivo", "inline": True},
            {"name": "Timestamp", "value": datetime.now().strftime("%H:%M:%S"), "inline": True}
        ]
    )

def notify_agent_created(agent_name, personality=None):
    """Notifica creazione nuovo agente"""
    fields = [
        {"name": "Nome Agente", "value": agent_name, "inline": True},
        {"name": "Timestamp", "value": datetime.now().strftime("%H:%M:%S"), "inline": True}
    ]
    
    if personality:
        fields.append({"name": "Personalità", "value": personality[:100], "inline": False})
    
    send_discord_message(
        f"Nuovo agente creato: **{agent_name}**",
        title="🤖 Agente Creato",
        color=0x0099ff,
        fields=fields
    )

def notify_room_created(room_name, description=None):
    """Notifica creazione nuova stanza"""
    fields = [
        {"name": "Nome Stanza", "value": room_name, "inline": True},
        {"name": "Timestamp", "value": datetime.now().strftime("%H:%M:%S"), "inline": True}
    ]
    
    if description:
        fields.append({"name": "Descrizione", "value": description[:100], "inline": False})
    
    send_discord_message(
        f"Nuova stanza creata: **{room_name}**",
        title="🏠 Stanza Creata",
        color=0xff9900,
        fields=fields
    )

def notify_evolution(details):
    """Notifica evoluzione del sistema"""
    send_discord_message(
        f"Sistema evoluto: {details}",
        title="🧬 Evoluzione",
        color=0xff00ff,
        fields=[
            {"name": "Dettagli", "value": details[:200], "inline": False},
            {"name": "Timestamp", "value": datetime.now().strftime("%H:%M:%S"), "inline": True}
        ]
    )

def notify_thought(thought_content, agent_name="Aether"):
    """Notifica nuovo pensiero"""
    send_discord_message(
        f"💭 **{agent_name}**: {thought_content[:100]}{'...' if len(thought_content) > 100 else ''}",
        title="🧠 Nuovo Pensiero",
        color=0x9900ff
    )

def notify_error(error_message, context=None):
    """Notifica errore"""
    fields = [
        {"name": "Errore", "value": error_message[:200], "inline": False},
        {"name": "Timestamp", "value": datetime.now().strftime("%H:%M:%S"), "inline": True}
    ]
    
    if context:
        fields.append({"name": "Contesto", "value": context[:100], "inline": True})
    
    send_discord_message(
        f"Si è verificato un errore nel sistema",
        title="🔴 Errore Sistema",
        color=0xff0000,
        fields=fields
    )

def notify_audio_generated(filename, text=None):
    """Notifica audio generato"""
    fields = [
        {"name": "File", "value": filename, "inline": True},
        {"name": "Timestamp", "value": datetime.now().strftime("%H:%M:%S"), "inline": True}
    ]
    
    if text:
        fields.append({"name": "Testo", "value": text[:100], "inline": False})
    
    send_discord_message(
        f"Audio generato: {filename}",
        title="🔊 Audio Creato",
        color=0x00ffff,
        fields=fields
    )

# Funzioni di utilità
def test_discord_connection():
    """Testa la connessione Discord"""
    return send_discord_message(
        "Test connessione Discord completato! 🟢",
        title="🔧 Test Sistema",
        color=0x00ff00
    )

if __name__ == "__main__":
    # Test del modulo
    print("🧪 Testing Discord Notifier...")
    if test_discord_connection():
        print("✅ Discord funziona!")
    else:
        print("❌ Discord non configurato o errore di connessione") 