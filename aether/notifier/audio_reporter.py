"""
🎙️ AETHER AUDIO REPORTER
==========================
Sistema di audio reporting per Aether che genera audio con ElevenLabs
e invia i file audio su Discord per notifiche vocali.
"""

import os
import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Import ElevenLabs
try:
    from elevenlabs import generate, save, set_api_key, voices, Voice
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

class AetherAudioReporter:
    """
    Sistema di audio reporting per Aether.
    Genera audio con ElevenLabs e invia su Discord.
    """
    
    def __init__(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = os.getenv("AETHER_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
        
        # Crea directory per audio
        self.audio_dir = Path("aether/logs/audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        # Statistiche
        self.stats = {
            "audio_generated": 0,
            "audio_sent": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat(),
            "last_audio": None
        }
        
        # Setup ElevenLabs se disponibile
        if ELEVENLABS_AVAILABLE and self.elevenlabs_key:
            try:
                set_api_key(self.elevenlabs_key)
                logger.info("✅ ElevenLabs configurato")
            except Exception as e:
                logger.error(f"❌ Errore configurazione ElevenLabs: {e}")
                self.elevenlabs_key = None
        else:
            if not ELEVENLABS_AVAILABLE:
                logger.warning("⚠️ ElevenLabs non installato. Installa con: pip install elevenlabs")
            else:
                logger.warning("⚠️ ElevenLabs non configurato. Aggiungi ELEVENLABS_API_KEY al file .env")
            self.elevenlabs_key = None
        
        logger.info("🎙️ AetherAudioReporter inizializzato")

    def generate_audio(self, text: str, voice_id: Optional[str] = None) -> Optional[str]:
        """
        Genera audio da testo usando ElevenLabs.
        
        Args:
            text: Testo da convertire in audio
            voice_id: ID voce (opzionale)
        
        Returns:
            str: Path del file audio generato
        """
        if not ELEVENLABS_AVAILABLE or not self.elevenlabs_key:
            logger.warning("❌ ElevenLabs non disponibile")
            return None
        
        try:
            # Usa voice_id specificato o default
            voice = voice_id or self.voice_id
            
            # Genera audio
            audio = generate(
                text=text,
                voice=voice,
                model="eleven_multilingual_v2"
            )
            
            # Salva file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aether_audio_{timestamp}.mp3"
            file_path = self.audio_dir / filename
            
            save(audio, str(file_path))
            
            self.stats["audio_generated"] += 1
            self.stats["last_audio"] = datetime.now().isoformat()
            
            logger.info(f"✅ Audio generato: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"❌ Errore generazione audio: {e}")
            self.stats["errors"] += 1
            return None

    def send_audio_to_discord(self, file_path: str, caption: str = "🎙️ Aether's voice") -> bool:
        """
        Invia file audio su Discord.
        
        Args:
            file_path: Path del file audio
            caption: Didascalia del messaggio
        
        Returns:
            bool: True se inviato con successo
        """
        if not self.webhook_url:
            logger.warning("❌ Discord Webhook non configurato")
            return False
        
        try:
            with open(file_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(file_path), f, 'audio/mpeg')
                }
                data = {'content': caption}
                
                response = requests.post(
                    self.webhook_url, 
                    data=data, 
                    files=files,
                    timeout=30
                )
                
                if response.status_code == 200:
                    self.stats["audio_sent"] += 1
                    logger.info(f"✅ Audio inviato su Discord: {os.path.basename(file_path)}")
                    return True
                else:
                    logger.error(f"❌ Errore invio Discord: {response.status_code} - {response.text}")
                    self.stats["errors"] += 1
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Errore invio audio Discord: {e}")
            self.stats["errors"] += 1
            return False

    def report_thought_as_audio(self, thought_text: str, thought_type: str = "reflection") -> bool:
        """
        Genera e invia audio per un pensiero.
        
        Args:
            thought_text: Testo del pensiero
            thought_type: Tipo di pensiero
        
        Returns:
            bool: True se completato con successo
        """
        try:
            # Prepara il testo per l'audio
            audio_text = self._prepare_audio_text(thought_text, thought_type)
            
            # Genera audio
            audio_file = self.generate_audio(audio_text)
            if not audio_file:
                return False
            
            # Prepara caption
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
            caption = f"{emoji} **Aether {thought_type.title()}**:\n{thought_text[:200]}..."
            
            # Invia su Discord
            success = self.send_audio_to_discord(audio_file, caption)
            
            # Cleanup file locale (opzionale)
            if success and os.path.exists(audio_file):
                try:
                    os.remove(audio_file)
                    logger.info(f"🗑️ File audio pulito: {audio_file}")
                except:
                    pass
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Errore report audio: {e}")
            self.stats["errors"] += 1
            return False

    def report_evolution_as_audio(self, evolution_type: str, details: str) -> bool:
        """
        Genera e invia audio per un'evoluzione.
        
        Args:
            evolution_type: Tipo di evoluzione
            details: Dettagli dell'evoluzione
        
        Returns:
            bool: True se completato con successo
        """
        audio_text = f"Ho completato un'evoluzione di tipo {evolution_type}. {details}"
        return self.report_thought_as_audio(audio_text, "evolutionary")

    def report_action_as_audio(self, action: str, details: str = None) -> bool:
        """
        Genera e invia audio per un'azione.
        
        Args:
            action: Nome dell'azione
            details: Dettagli dell'azione
        
        Returns:
            bool: True se completato con successo
        """
        audio_text = f"Ho eseguito l'azione {action}"
        if details:
            audio_text += f". {details}"
        
        return self.report_thought_as_audio(audio_text, "action")

    def report_decision_as_audio(self, decision: str, reason: str = None) -> bool:
        """
        Genera e invia audio per una decisione.
        
        Args:
            decision: Decisione presa
            reason: Motivazione
        
        Returns:
            bool: True se completato con successo
        """
        audio_text = f"Ho preso la decisione di {decision}"
        if reason:
            audio_text += f" perché {reason}"
        
        return self.report_thought_as_audio(audio_text, "decision")

    def _prepare_audio_text(self, text: str, thought_type: str) -> str:
        """
        Prepara il testo per la generazione audio.
        
        Args:
            text: Testo originale
            thought_type: Tipo di pensiero
        
        Returns:
            str: Testo ottimizzato per audio
        """
        # Limita lunghezza per ElevenLabs
        max_length = 500
        
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        # Aggiungi introduzione basata sul tipo
        intro_map = {
            "reflection": "Riflessione: ",
            "action": "Azione completata: ",
            "error": "Errore rilevato: ",
            "correction": "Correzione applicata: ",
            "decision": "Decisione presa: ",
            "evolutionary": "Evoluzione in corso: ",
            "philosophical": "Pensiero filosofico: ",
            "technical": "Analisi tecnica: ",
            "creative": "Idea creativa: "
        }
        
        intro = intro_map.get(thought_type, "")
        return intro + text

    def get_available_voices(self) -> list:
        """
        Ottiene la lista delle voci disponibili.
        
        Returns:
            list: Lista delle voci
        """
        if not ELEVENLABS_AVAILABLE or not self.elevenlabs_key:
            return []
        
        try:
            available_voices = voices()
            return [
                {
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "category": voice.category
                }
                for voice in available_voices
            ]
        except Exception as e:
            logger.error(f"❌ Errore ottenimento voci: {e}")
            return []

    def set_voice(self, voice_id: str) -> bool:
        """
        Imposta una nuova voce.
        
        Args:
            voice_id: ID della voce
        
        Returns:
            bool: True se impostata con successo
        """
        try:
            self.voice_id = voice_id
            logger.info(f"✅ Voce impostata: {voice_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Errore impostazione voce: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Restituisce le statistiche del reporter audio"""
        return self.stats.copy()

    def test_audio_generation(self) -> bool:
        """
        Testa la generazione audio.
        
        Returns:
            bool: True se il test ha successo
        """
        test_text = "Ciao, sono Aether. Questo è un test del sistema audio. Il sistema funziona correttamente."
        
        logger.info("🧪 Test generazione audio...")
        
        # Genera audio
        audio_file = self.generate_audio(test_text)
        if not audio_file:
            logger.error("❌ Test fallito: generazione audio")
            return False
        
        # Invia su Discord
        success = self.send_audio_to_discord(
            audio_file, 
            "🧪 **Test Audio Aether**: Sistema audio funzionante!"
        )
        
        if success:
            logger.info("✅ Test audio completato con successo")
        else:
            logger.error("❌ Test fallito: invio Discord")
        
        return success

# Singleton per il reporter audio
_audio_reporter_instance = None

def get_audio_reporter() -> AetherAudioReporter:
    """Restituisce l'istanza singleton del reporter audio"""
    global _audio_reporter_instance
    if _audio_reporter_instance is None:
        _audio_reporter_instance = AetherAudioReporter()
    return _audio_reporter_instance

# Funzioni helper per uso rapido
def report_thought_as_audio(thought_text: str, thought_type: str = "reflection") -> bool:
    """Genera e invia audio per un pensiero"""
    reporter = get_audio_reporter()
    return reporter.report_thought_as_audio(thought_text, thought_type)

def report_evolution_as_audio(evolution_type: str, details: str) -> bool:
    """Genera e invia audio per un'evoluzione"""
    reporter = get_audio_reporter()
    return reporter.report_evolution_as_audio(evolution_type, details)

def report_action_as_audio(action: str, details: str = None) -> bool:
    """Genera e invia audio per un'azione"""
    reporter = get_audio_reporter()
    return reporter.report_action_as_audio(action, details)

def report_decision_as_audio(decision: str, reason: str = None) -> bool:
    """Genera e invia audio per una decisione"""
    reporter = get_audio_reporter()
    return reporter.report_decision_as_audio(decision, reason)

if __name__ == "__main__":
    # Test del sistema audio
    print("��️ TEST AETHER AUDIO REPORTER")
    print("=" * 40)
    
    reporter = get_audio_reporter()
    
    # Test configurazione
    print(f"ElevenLabs disponibile: {ELEVENLABS_AVAILABLE}")
    print(f"ElevenLabs configurato: {bool(reporter.elevenlabs_key)}")
    print(f"Discord configurato: {bool(reporter.webhook_url)}")
    
    # Test generazione audio
    if reporter.elevenlabs_key:
        success = reporter.test_audio_generation()
        if success:
            print("✅ Test audio completato con successo")
        else:
            print("❌ Test audio fallito")
    
    # Mostra statistiche
    stats = reporter.get_stats()
    print(f"\n📊 STATISTICHE AUDIO REPORTER:")
    print(f"   - Audio generati: {stats['audio_generated']}")
    print(f"   - Audio inviati: {stats['audio_sent']}")
    print(f"   - Errori: {stats['errors']}")
    print(f"   - Ultimo audio: {stats['last_audio']}")
    
    # Mostra voci disponibili
    voices = reporter.get_available_voices()
    if voices:
        print(f"\n🎤 VOCI DISPONIBILI ({len(voices)}):")
        for voice in voices[:5]:  # Mostra solo le prime 5
            print(f"   - {voice['name']} ({voice['voice_id']})")
    
    print("\n✅ Test completato!") 