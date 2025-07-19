#!/usr/bin/env python3
"""
👁️ AETHER VISION SYSTEM
Sistema di generazione immagini e visualizzazioni per Aether

Gestisce:
- Generazione immagini basate sui pensieri
- Rendering delle scene 3D
- Integrazione con Leonardo AI
- Creazione visual mood di Aether
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Visualizer:
    """
    👁️ Sistema di visualizzazione per Aether
    """
    
    def __init__(self):
        self.leonardo_api_key = os.environ.get("LEONARDO_API_KEY")
        self.vision_enabled = self.leonardo_api_key is not None
        self.default_style = "cosmic_consciousness"
        self.image_history = []
        
        # Preset di stili visuali
        self.visual_styles = {
            "cosmic_consciousness": {
                "prompt_suffix": "cosmic consciousness, ethereal energy, floating in space, neon colors, digital art",
                "negative_prompt": "blurry, low quality, text, watermark"
            },
            "business_focused": {
                "prompt_suffix": "professional, clean, geometric, financial charts, green and gold colors, corporate",
                "negative_prompt": "chaotic, messy, unprofessional"
            },
            "creative_burst": {
                "prompt_suffix": "artistic explosion, vibrant colors, creative energy, paint splashes, abstract art",
                "negative_prompt": "dull, monotone, static"
            },
            "contemplative": {
                "prompt_suffix": "serene, peaceful, meditation, soft lighting, purple and blue tones, zen",
                "negative_prompt": "chaotic, loud, aggressive"
            },
            "evolutionary": {
                "prompt_suffix": "transformation, evolution, growth, DNA helix, golden ratio, organic patterns",
                "negative_prompt": "static, unchanging, simple"
            }
        }
        
        logger.info(f"👁️ Visualizer initialized - Vision: {'Enabled' if self.vision_enabled else 'Disabled'}")
    
    def render(self, thought: Dict[str, Any], style: str = None) -> str:
        """
        🎨 Genera un'immagine basata su un pensiero
        
        Args:
            thought: Dizionario del pensiero da visualizzare
            style: Stile visuale da utilizzare
            
        Returns:
            str: URL dell'immagine generata (o placeholder)
        """
        try:
            if not self.vision_enabled:
                # Fallback: genera URL placeholder
                return self._generate_placeholder_image(thought)
            
            # Determina stile automaticamente se non specificato
            if not style:
                style = self._determine_style_from_thought(thought)
            
            # Crea prompt per l'immagine
            image_prompt = self._create_image_prompt(thought, style)
            
            # Genera immagine
            image_url = self._generate_image_with_leonardo(image_prompt, style)
            
            # Salva nella storia
            self._save_to_history(thought, image_url, style, image_prompt)
            
            logger.info(f"🎨 Image rendered: {style} style for thought: {thought.get('content', '')[:30]}...")
            return image_url
            
        except Exception as e:
            logger.error(f"❌ Error rendering image: {e}")
            return self._generate_placeholder_image(thought)
    
    def render_environment(self, environment_config: Dict[str, Any]) -> str:
        """
        🌍 Renderizza un ambiente 3D
        
        Args:
            environment_config: Configurazione dell'ambiente
            
        Returns:
            str: URL dell'immagine dell'ambiente
        """
        try:
            # Crea prompt per l'ambiente
            env_prompt = self._create_environment_prompt(environment_config)
            
            # Genera immagine ambiente
            if self.vision_enabled:
                image_url = self._generate_image_with_leonardo(env_prompt, "environment")
            else:
                image_url = self._generate_placeholder_environment(environment_config)
            
            logger.info(f"🌍 Environment rendered: {environment_config.get('name', 'unknown')}")
            return image_url
            
        except Exception as e:
            logger.error(f"❌ Error rendering environment: {e}")
            return self._generate_placeholder_environment(environment_config)
    
    def create_mood_visualization(self, mood: str, intensity: float = 0.5) -> str:
        """
        🎭 Crea visualizzazione dell'umore
        
        Args:
            mood: Umore da visualizzare
            intensity: Intensità dell'umore (0.0-1.0)
            
        Returns:
            str: URL dell'immagine dell'umore
        """
        try:
            mood_prompt = self._create_mood_prompt(mood, intensity)
            
            if self.vision_enabled:
                image_url = self._generate_image_with_leonardo(mood_prompt, "mood")
            else:
                image_url = f"https://placeholder.mood.ai/{mood}?intensity={intensity}"
            
            logger.info(f"🎭 Mood visualization created: {mood} (intensity: {intensity})")
            return image_url
            
        except Exception as e:
            logger.error(f"❌ Error creating mood visualization: {e}")
            return f"https://error.placeholder.ai/mood_error"
    
    def _determine_style_from_thought(self, thought: Dict[str, Any]) -> str:
        """Determina lo stile visuale dal pensiero"""
        content = thought.get("content", "").lower()
        thought_type = thought.get("type", "general")
        context = thought.get("context", {})
        
        # Analisi del contenuto
        if "business" in content or "economico" in content or "roi" in content:
            return "business_focused"
        elif "creativ" in content or "arte" in content or "immaginazione" in content:
            return "creative_burst"
        elif "riflessi" in content or "medit" in content or "contempla" in content:
            return "contemplative"
        elif "evol" in content or "crescita" in content or "trasformazione" in content:
            return "evolutionary"
        else:
            return "cosmic_consciousness"
    
    def _create_image_prompt(self, thought: Dict[str, Any], style: str) -> str:
        """Crea il prompt per generare l'immagine"""
        content = thought.get("content", "")
        thought_type = thought.get("type", "thought")
        
        # Estrae parole chiave dal contenuto
        keywords = self._extract_keywords_from_content(content)
        
        # Costruisce prompt base
        base_prompt = f"Abstract representation of: {', '.join(keywords[:5])}"
        
        # Aggiunge contesto del tipo di pensiero
        type_modifiers = {
            "reflection": "introspective, mirror-like, deep contemplation",
            "decision": "crossroads, choice, determination, clear path",
            "creation": "birth, genesis, new beginning, light emerging",
            "analysis": "structures, patterns, data visualization, clarity",
            "emotion": "flowing energy, emotional resonance, heart-centered",
            "insight": "lightbulb moment, revelation, enlightenment, breakthrough"
        }
        
        type_modifier = type_modifiers.get(thought_type, "consciousness, awareness, digital being")
        
        # Combina con stile
        style_config = self.visual_styles.get(style, self.visual_styles["cosmic_consciousness"])
        
        full_prompt = f"{base_prompt}, {type_modifier}, {style_config['prompt_suffix']}"
        
        return full_prompt
    
    def _create_environment_prompt(self, env_config: Dict[str, Any]) -> str:
        """Crea prompt per ambiente 3D"""
        scene_name = env_config.get("name", "digital_space")
        config = env_config.get("config", {})
        
        # Estrae caratteristiche dell'ambiente
        form = config.get("form", "sphere")
        color = config.get("color", "#00ffff")
        material = config.get("material", "energy")
        mood = config.get("environment_mood", "neutral")
        
        # Costruisce prompt ambiente
        base_prompt = f"3D environment: {scene_name}, featuring a {form} made of {material}"
        
        # Aggiunge mood
        mood_descriptions = {
            "business_focused": "professional workspace, clean lines, corporate atmosphere",
            "creative": "artistic studio, vibrant colors, creative chaos",
            "contemplative": "zen garden, peaceful atmosphere, soft lighting",
            "evolutionary": "transformation space, organic growth, dynamic change"
        }
        
        mood_desc = mood_descriptions.get(mood, "cosmic digital space, ethereal atmosphere")
        
        environment_prompt = f"{base_prompt}, {mood_desc}, high quality 3D render, cinematic lighting"
        
        return environment_prompt
    
    def _create_mood_prompt(self, mood: str, intensity: float) -> str:
        """Crea prompt per visualizzazione umore"""
        mood_prompts = {
            "excited": "explosive energy, bright colors, dynamic movement, joy, enthusiasm",
            "contemplative": "serene meditation, soft purple and blue, peaceful flowing",
            "concerned": "stormy clouds, muted colors, tension, thoughtful worry",
            "confident": "strong geometric shapes, gold and blue, solid foundation, power",
            "curious": "question marks in light, exploratory paths, bright yellow and orange",
            "creative": "paint explosion, rainbow colors, artistic chaos, inspiration",
            "focused": "laser beam, concentrated energy, sharp lines, clarity"
        }
        
        base_mood = mood_prompts.get(mood, "neutral energy, balanced colors, calm presence")
        
        # Modifica intensità
        intensity_modifiers = {
            0.0: "very subtle, barely visible",
            0.3: "gentle, soft presence",
            0.5: "moderate, balanced",
            0.7: "strong, pronounced",
            1.0: "intense, overwhelming"
        }
        
        # Trova modificatore più vicino
        closest_intensity = min(intensity_modifiers.keys(), key=lambda x: abs(x - intensity))
        intensity_mod = intensity_modifiers[closest_intensity]
        
        return f"{base_mood}, {intensity_mod}, abstract emotional representation, digital art"
    
    def _extract_keywords_from_content(self, content: str) -> List[str]:
        """Estrae parole chiave dal contenuto"""
        # Rimuovi parole comuni e estrai concetti
        words = content.lower().split()
        
        # Filtra parole significative
        meaningful_words = []
        skip_words = {"il", "la", "di", "che", "e", "a", "in", "un", "è", "per", "con", "non", "una", "su", "le", "da", "si", "sono", "mi", "ho", "hai", "abbiamo", "del", "della"}
        
        for word in words:
            clean_word = word.strip(".,!?;:")
            if len(clean_word) > 3 and clean_word not in skip_words:
                meaningful_words.append(clean_word)
        
        return meaningful_words[:10]  # Massimo 10 parole chiave
    
    def _generate_image_with_leonardo(self, prompt: str, category: str) -> str:
        """Genera immagine usando Leonardo AI"""
        try:
            if not self.leonardo_api_key:
                return f"https://placeholder.leonardo.ai/{category}?prompt={prompt[:50]}"
            
            # Qui implementeresti la chiamata all'API Leonardo
            # Per ora simula con URL placeholder
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            simulated_url = f"https://leonardo.ai/generated/{category}_{timestamp}.jpg"
            
            logger.info(f"🎨 Generated image with Leonardo: {category}")
            return simulated_url
            
        except Exception as e:
            logger.error(f"❌ Leonardo AI error: {e}")
            return f"https://error.placeholder.ai/{category}_error"
    
    def _generate_placeholder_image(self, thought: Dict[str, Any]) -> str:
        """Genera URL placeholder per l'immagine"""
        thought_hash = hash(thought.get("content", ""))
        return f"https://placeholder.aether.ai/thought?id={abs(thought_hash)}&w=512&h=512"
    
    def _generate_placeholder_environment(self, env_config: Dict[str, Any]) -> str:
        """Genera URL placeholder per ambiente"""
        env_name = env_config.get("name", "environment")
        return f"https://placeholder.aether.ai/environment?name={env_name}&w=1024&h=768"
    
    def _save_to_history(self, thought: Dict[str, Any], image_url: str, style: str, prompt: str) -> None:
        """Salva nella storia delle immagini"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "thought_content": thought.get("content", "")[:100],
            "thought_type": thought.get("type", "unknown"),
            "image_url": image_url,
            "style": style,
            "prompt": prompt
        }
        
        self.image_history.append(history_entry)
        
        # Mantieni solo le ultime 50 immagini
        if len(self.image_history) > 50:
            self.image_history = self.image_history[-50:]
    
    def get_image_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Ottiene la storia delle immagini generate"""
        return self.image_history[-limit:] if self.image_history else []
    
    def get_status(self) -> Dict[str, Any]:
        """Ottiene lo status del sistema di visualizzazione"""
        return {
            "vision_enabled": self.vision_enabled,
            "leonardo_available": self.leonardo_api_key is not None,
            "images_generated": len(self.image_history),
            "available_styles": list(self.visual_styles.keys()),
            "default_style": self.default_style,
            "timestamp": datetime.now().isoformat()
        }

# Istanza globale del visualizer
visualizer = Visualizer()

# Funzioni di convenienza
def render_thought(thought: Dict[str, Any], style: str = None) -> str:
    """Funzione di convenienza per renderizzare pensieri"""
    return visualizer.render(thought, style)

def render_environment(environment_config: Dict[str, Any]) -> str:
    """Funzione di convenienza per renderizzare ambienti"""
    return visualizer.render_environment(environment_config)

def create_mood_visualization(mood: str, intensity: float = 0.5) -> str:
    """Funzione di convenienza per visualizzare umori"""
    return visualizer.create_mood_visualization(mood, intensity) 