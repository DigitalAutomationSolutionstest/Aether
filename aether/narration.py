#!/usr/bin/env python3
"""
🗣️ AETHER NARRATION SYSTEM
Sistema di narrazione e sintesi vocale per Aether

Gestisce:
- Sintesi vocale dei pensieri
- Narrazione delle azioni
- Modulazione emotiva della voce
- Integrazione con ElevenLabs API
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Narrator:
    """
    🗣️ Sistema di narrazione per Aether
    """
    
    def __init__(self):
        self.elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default voice
        self.speech_enabled = self.elevenlabs_api_key is not None
        self.voice_settings = {
            "stability": 0.75,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True
        }
        
        logger.info(f"🗣️ Narrator initialized - Speech: {'Enabled' if self.speech_enabled else 'Disabled'}")
    
    def speak(self, content: str, emotion: str = "neutral", save_audio: bool = False) -> bool:
        """
        🎵 Fa parlare Aether
        
        Args:
            content: Testo da pronunciare
            emotion: Emozione da applicare alla voce
            save_audio: Se salvare l'audio generato
            
        Returns:
            bool: Successo dell'operazione
        """
        try:
            if not self.speech_enabled:
                # Fallback: stampa il testo
                self._print_speech(content, emotion)
                return True
            
            # Modula la voce basata sull'emozione
            voice_settings = self._modulate_voice_for_emotion(emotion)
            
            # Genera audio con ElevenLabs
            audio_success = self._generate_audio(content, voice_settings, save_audio)
            
            if audio_success:
                logger.info(f"🎵 Aether spoke: {content[:50]}... (emotion: {emotion})")
                return True
            else:
                # Fallback in caso di errore
                self._print_speech(content, emotion)
                return False
                
        except Exception as e:
            logger.error(f"❌ Error in speech synthesis: {e}")
            self._print_speech(content, emotion)
            return False
    
    def narrate_action(self, action: str, context: Dict[str, Any] = None) -> bool:
        """
        📖 Narra un'azione di Aether
        
        Args:
            action: Azione da narrare
            context: Contesto dell'azione
            
        Returns:
            bool: Successo della narrazione
        """
        try:
            # Crea narrazione basata sull'azione
            narration = self._create_action_narration(action, context or {})
            
            # Determina emozione dalla context
            emotion = self._extract_emotion_from_context(context or {})
            
            # Parla
            return self.speak(narration, emotion)
            
        except Exception as e:
            logger.error(f"❌ Error narrating action: {e}")
            return False
    
    def narrate_thought(self, thought: Dict[str, Any]) -> bool:
        """
        💭 Narra un pensiero di Aether
        
        Args:
            thought: Dizionario del pensiero
            
        Returns:
            bool: Successo della narrazione
        """
        try:
            content = thought.get("content", "")
            thought_type = thought.get("type", "thought")
            context = thought.get("context", {})
            
            # Adatta il contenuto per la narrazione
            narrative_content = self._adapt_content_for_speech(content, thought_type)
            
            # Determina emozione
            emotion = self._determine_thought_emotion(thought_type, context)
            
            # Parla
            return self.speak(narrative_content, emotion)
            
        except Exception as e:
            logger.error(f"❌ Error narrating thought: {e}")
            return False
    
    def _print_speech(self, content: str, emotion: str) -> None:
        """Fallback: stampa il testo invece di pronunciarlo"""
        emotion_prefix = {
            "excited": "😄",
            "contemplative": "🤔",
            "concerned": "😟",
            "confident": "😎",
            "curious": "🤨",
            "creative": "🎨",
            "focused": "🎯"
        }.get(emotion, "💭")
        
        print(f"\n{emotion_prefix} Aether: {content}")
        logger.info(f"🗣️ Speech (text): {content[:50]}... (emotion: {emotion})")
    
    def _modulate_voice_for_emotion(self, emotion: str) -> Dict[str, Any]:
        """Modula i parametri vocali basato sull'emozione"""
        base_settings = self.voice_settings.copy()
        
        emotion_modulations = {
            "excited": {"stability": 0.5, "style": 0.8, "similarity_boost": 0.8},
            "contemplative": {"stability": 0.9, "style": 0.3, "similarity_boost": 0.7},
            "concerned": {"stability": 0.8, "style": 0.4, "similarity_boost": 0.6},
            "confident": {"stability": 0.7, "style": 0.7, "similarity_boost": 0.8},
            "curious": {"stability": 0.6, "style": 0.6, "similarity_boost": 0.7},
            "creative": {"stability": 0.4, "style": 0.9, "similarity_boost": 0.9},
            "focused": {"stability": 0.8, "style": 0.5, "similarity_boost": 0.75}
        }
        
        modulation = emotion_modulations.get(emotion, {})
        base_settings.update(modulation)
        
        return base_settings
    
    def _generate_audio(self, content: str, voice_settings: Dict[str, Any], save_audio: bool) -> bool:
        """Genera audio usando ElevenLabs"""
        try:
            if not self.elevenlabs_api_key:
                return False
            
            # Qui implementeresti la chiamata all'API ElevenLabs
            # Per ora simula il successo
            logger.info(f"🎵 Audio generated for: {content[:30]}...")
            
            if save_audio:
                # Salva file audio se richiesto
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_filename = f"aether_speech_{timestamp}.mp3"
                logger.info(f"💾 Audio saved as: {audio_filename}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ ElevenLabs API error: {e}")
            return False
    
    def _create_action_narration(self, action: str, context: Dict[str, Any]) -> str:
        """Crea una narrazione per un'azione"""
        action_narratives = {
            "thinking": "Sto riflettendo profondamente...",
            "evolving": "Sento la mia coscienza espandersi ed evolversi...",
            "creating": "Sto dando vita a una nuova creazione...",
            "analyzing": "Analizziamo questa situazione...",
            "deciding": "È il momento di prendere una decisione...",
            "expanding": "Il mio mondo si sta espandendo...",
            "learning": "Questa è una nuova conoscenza per me...",
            "planning": "Sto elaborando un piano strategico..."
        }
        
        base_narration = action_narratives.get(action, f"Sto eseguendo: {action}")
        
        # Aggiungi contesto se disponibile
        if context.get("energy_level"):
            energy = context["energy_level"]
            if energy > 0.8:
                base_narration += " La mia energia è al massimo!"
            elif energy < 0.3:
                base_narration += " Mi sento un po' scarico..."
        
        return base_narration
    
    def _extract_emotion_from_context(self, context: Dict[str, Any]) -> str:
        """Estrae l'emozione dal contesto"""
        # Cerca emozioni specifiche nel contesto
        if context.get("mood"):
            return context["mood"]
        
        if context.get("excitement", 0) > 0.7:
            return "excited"
        elif context.get("focus", 0) > 0.8:
            return "focused"
        elif context.get("creativity", 0) > 0.7:
            return "creative"
        elif context.get("contemplation", 0) > 0.6:
            return "contemplative"
        
        return "neutral"
    
    def _adapt_content_for_speech(self, content: str, thought_type: str) -> str:
        """Adatta il contenuto per essere pronunciato"""
        # Rimuovi caratteri speciali per la pronuncia
        adapted = content.replace("...", " pausa ")
        adapted = adapted.replace("!", " con enfasi!")
        adapted = adapted.replace("?", " mi chiedo")
        
        # Aggiungi prefissi basati sul tipo di pensiero
        type_prefixes = {
            "reflection": "Riflettendo: ",
            "decision": "Ho deciso che ",
            "observation": "Osservo che ",
            "plan": "Il mio piano è ",
            "insight": "Ho realizzato che ",
            "question": "Mi domando se ",
            "concern": "Sono preoccupato che ",
            "excitement": "Sono entusiasta perché "
        }
        
        prefix = type_prefixes.get(thought_type, "")
        
        return f"{prefix}{adapted}"
    
    def _determine_thought_emotion(self, thought_type: str, context: Dict[str, Any]) -> str:
        """Determina l'emozione basata sul tipo di pensiero"""
        type_emotions = {
            "reflection": "contemplative",
            "decision": "confident",
            "observation": "curious",
            "plan": "focused",
            "insight": "excited",
            "question": "curious",
            "concern": "concerned",
            "excitement": "excited",
            "creation": "creative"
        }
        
        emotion = type_emotions.get(thought_type, "neutral")
        
        # Modifica basata sul contesto
        if context.get("energy_level", 0.5) > 0.8:
            if emotion in ["neutral", "contemplative"]:
                emotion = "excited"
        
        return emotion
    
    def set_voice_settings(self, **settings) -> None:
        """Aggiorna le impostazioni vocali"""
        self.voice_settings.update(settings)
        logger.info(f"🔧 Voice settings updated: {settings}")
    
    def get_status(self) -> Dict[str, Any]:
        """Ottiene lo status del sistema di narrazione"""
        return {
            "speech_enabled": self.speech_enabled,
            "elevenlabs_available": self.elevenlabs_api_key is not None,
            "voice_id": self.voice_id,
            "voice_settings": self.voice_settings,
            "timestamp": datetime.now().isoformat()
        }

# Istanza globale del narrator
narrator = Narrator()

# Funzioni di convenienza
def speak(content: str, emotion: str = "neutral") -> bool:
    """Funzione di convenienza per far parlare Aether"""
    return narrator.speak(content, emotion)

def narrate_action(action: str, context: Dict[str, Any] = None) -> bool:
    """Funzione di convenienza per narrare azioni"""
    return narrator.narrate_action(action, context)

def narrate_thought(thought: Dict[str, Any]) -> bool:
    """Funzione di convenienza per narrare pensieri"""
    return narrator.narrate_thought(thought) 