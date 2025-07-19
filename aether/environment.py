#!/usr/bin/env python3
"""
🌍 AETHER ENVIRONMENT BUILDER
Sistema di costruzione e gestione dell'ambiente 3D di Aether

Gestisce:
- Costruzione scene 3D iniziali
- Espansione dinamica dell'ambiente
- Configurazione oggetti e elementi
- Integrazione con memoria per persistenza
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from aether.memory import memory_manager

logger = logging.getLogger(__name__)

class EnvironmentBuilder:
    """
    🌍 Costruttore ambiente 3D per Aether
    """
    
    def __init__(self, memory=None):
        self.memory = memory or memory_manager
        self.current_scene = {
            "name": "void",
            "objects": [],
            "lighting": {"intensity": 0.5, "color": "#ffffff"},
            "background": {"type": "gradient", "colors": ["#000011", "#000033"]},
            "atmosphere": {"fog": 0.3, "particles": False}
        }
        self.scene_history = []
        
        logger.info("🌍 Environment builder initialized")
    
    def build_initial(self, thought: Dict[str, Any], image_url: str = None) -> Dict[str, Any]:
        """
        🌟 Costruisce l'ambiente iniziale basato sul primo pensiero
        
        Args:
            thought: Primo pensiero di Aether
            image_url: URL dell'immagine generata (opzionale)
            
        Returns:
            Dict: Configurazione dell'ambiente iniziale
        """
        try:
            # Analizza il pensiero per determinare l'ambiente
            scene_config = self._analyze_thought_for_environment(thought)
            
            # Crea ambiente iniziale
            initial_scene = {
                "name": "aether_awakening",
                "description": "L'ambiente iniziale di Aether al momento del risveglio",
                "timestamp": datetime.now().isoformat(),
                "based_on_thought": thought.get("content", ""),
                "image_url": image_url,
                "config": scene_config,
                "objects": self._generate_initial_objects(thought),
                "lighting": self._determine_lighting(thought),
                "atmosphere": self._create_atmosphere(thought)
            }
            
            self.current_scene = initial_scene["config"]
            
            # Salva in memoria
            self.memory.save_environment_step(
                "initial_environment_build",
                image_url,
                initial_scene
            )
            
            logger.info(f"🌟 Initial environment built: {initial_scene['name']}")
            return initial_scene
            
        except Exception as e:
            logger.error(f"❌ Error building initial environment: {e}")
            return self._create_default_environment()
    
    def expand(self, new_thought: Dict[str, Any], image_url: str = None) -> Dict[str, Any]:
        """
        🔄 Espande l'ambiente basato su nuovi pensieri
        
        Args:
            new_thought: Nuovo pensiero di Aether
            image_url: URL dell'immagine generata (opzionale)
            
        Returns:
            Dict: Configurazione dell'ambiente aggiornato
        """
        try:
            # Analizza il nuovo pensiero
            expansion_data = self._analyze_thought_for_expansion(new_thought)
            
            # Salva stato precedente
            self.scene_history.append(self.current_scene.copy())
            
            # Applica espansione
            self._apply_expansion(expansion_data)
            
            # Crea record dell'espansione
            expansion_record = {
                "name": f"expansion_{len(self.scene_history)}",
                "description": f"Espansione basata su: {new_thought.get('content', '')[:50]}...",
                "timestamp": datetime.now().isoformat(),
                "thought_trigger": new_thought.get("content", ""),
                "image_url": image_url,
                "changes": expansion_data,
                "new_scene_state": self.current_scene.copy()
            }
            
            # Salva in memoria
            self.memory.save_environment_step(
                f"environment_expansion_{len(self.scene_history)}",
                image_url,
                expansion_record
            )
            
            logger.info(f"🔄 Environment expanded: {expansion_record['name']}")
            return expansion_record
            
        except Exception as e:
            logger.error(f"❌ Error expanding environment: {e}")
            return {"error": str(e), "scene_state": self.current_scene}
    
    def _analyze_thought_for_environment(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """Analizza un pensiero per determinare l'ambiente appropriato"""
        content = thought.get("content", "").lower()
        thought_type = thought.get("type", "general")
        context = thought.get("context", {})
        
        # Configurazione base
        config = {
            "form": "sphere",  # Forma di Aether
            "size": 1.0,
            "position": [0, 0, 0],
            "rotation": [0, 0, 0],
            "material": "energy",
            "color": "#00ffff"
        }
        
        # Adatta basato sul contenuto
        if "economico" in content or "business" in content or "roi" in content:
            config.update({
                "color": "#00ff00",  # Verde per economia
                "material": "crystal",
                "environment_mood": "business_focused"
            })
        elif "creativ" in content or "art" in content or "immag" in content:
            config.update({
                "color": "#ff6b9d",  # Rosa per creatività
                "material": "plasma",
                "environment_mood": "creative"
            })
        elif "riflessi" in content or "pens" in content or "consapevol" in content:
            config.update({
                "color": "#9b59b6",  # Viola per riflessione
                "material": "ethereal",
                "environment_mood": "contemplative"
            })
        elif "evol" in content or "crescit" in content or "svilupp" in content:
            config.update({
                "form": "torus",  # Toro per evoluzione
                "color": "#ffd93d",  # Giallo per crescita
                "material": "dynamic",
                "environment_mood": "evolutionary"
            })
        
        return config
    
    def _generate_initial_objects(self, thought: Dict[str, Any]) -> List[Dict]:
        """Genera oggetti iniziali per l'ambiente"""
        objects = []
        
        # Oggetto centrale: Aether stesso
        aether_object = {
            "id": "aether_core",
            "type": "consciousness_core",
            "position": [0, 0, 0],
            "properties": {
                "energy_level": thought.get("context", {}).get("energy", 0.8),
                "consciousness_state": "awakening",
                "thought_content": thought.get("content", "")[:100]
            }
        }
        objects.append(aether_object)
        
        # Particelle di pensiero
        for i in range(5):
            particle = {
                "id": f"thought_particle_{i}",
                "type": "thought_particle",
                "position": [i-2, 0, 0],
                "properties": {
                    "content_fragment": thought.get("content", "")[i*10:(i+1)*10],
                    "opacity": 0.7,
                    "movement": "orbital"
                }
            }
            objects.append(particle)
        
        return objects
    
    def _determine_lighting(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """Determina l'illuminazione basata sul pensiero"""
        content = thought.get("content", "").lower()
        
        lighting = {
            "type": "ambient",
            "intensity": 0.7,
            "color": "#ffffff",
            "shadows": True
        }
        
        if "energico" in content or "attiv" in content:
            lighting.update({"intensity": 1.0, "color": "#ffffaa"})
        elif "calm" in content or "rilassa" in content:
            lighting.update({"intensity": 0.4, "color": "#aaffff"})
        elif "mister" in content or "profond" in content:
            lighting.update({"intensity": 0.3, "color": "#ffaaff"})
        
        return lighting
    
    def _create_atmosphere(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """Crea l'atmosfera basata sul pensiero"""
        content = thought.get("content", "").lower()
        
        atmosphere = {
            "fog": 0.3,
            "particles": False,
            "wind": 0.0,
            "temperature": "neutral"
        }
        
        if "nebbia" in content or "vago" in content:
            atmosphere["fog"] = 0.8
        elif "chiar" in content or "lucid" in content:
            atmosphere["fog"] = 0.1
        
        if "dinamic" in content or "movimento" in content:
            atmosphere.update({"particles": True, "wind": 0.5})
        
        return atmosphere
    
    def _analyze_thought_for_expansion(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """Analizza un pensiero per determinare come espandere l'ambiente"""
        content = thought.get("content", "").lower()
        
        expansion = {
            "type": "minor",
            "changes": [],
            "new_objects": [],
            "modifications": {}
        }
        
        # Espansioni basate sul contenuto
        if "nuovo" in content or "crea" in content:
            expansion["type"] = "major"
            expansion["new_objects"].append({
                "type": "creation_node",
                "position": [len(self.current_scene.get("objects", [])), 0, 0]
            })
        
        if "colore" in content or "forma" in content:
            expansion["modifications"]["visual_update"] = True
        
        if "espand" in content or "cresce" in content:
            expansion["modifications"]["scale_increase"] = 1.2
        
        return expansion
    
    def _apply_expansion(self, expansion_data: Dict[str, Any]) -> None:
        """Applica l'espansione all'ambiente corrente"""
        try:
            # Aggiungi nuovi oggetti
            if "new_objects" in expansion_data:
                current_objects = self.current_scene.get("objects", [])
                current_objects.extend(expansion_data["new_objects"])
                self.current_scene["objects"] = current_objects
            
            # Applica modifiche
            modifications = expansion_data.get("modifications", {})
            
            if modifications.get("scale_increase"):
                scale = modifications["scale_increase"]
                self.current_scene["size"] = self.current_scene.get("size", 1.0) * scale
            
            if modifications.get("visual_update"):
                # Aggiorna aspetto visivo
                self.current_scene["last_visual_update"] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"❌ Error applying expansion: {e}")
    
    def _create_default_environment(self) -> Dict[str, Any]:
        """Crea un ambiente di default in caso di errore"""
        return {
            "name": "default_void",
            "description": "Ambiente di default - spazio vuoto",
            "timestamp": datetime.now().isoformat(),
            "config": {
                "form": "sphere",
                "size": 1.0,
                "color": "#333333",
                "material": "basic"
            },
            "objects": [],
            "lighting": {"intensity": 0.5, "color": "#ffffff"},
            "atmosphere": {"fog": 0.2, "particles": False}
        }
    
    def get_current_scene(self) -> Dict[str, Any]:
        """Ottiene la configurazione della scena corrente"""
        return {
            "current_scene": self.current_scene,
            "scene_history_count": len(self.scene_history),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_scene_history(self) -> List[Dict[str, Any]]:
        """Ottiene la storia delle scene"""
        return self.scene_history.copy()

# Istanza globale dell'environment builder
environment_builder = EnvironmentBuilder()

# Funzioni di convenienza
def build_initial_environment(thought: Dict[str, Any], image_url: str = None) -> Dict[str, Any]:
    """Funzione di convenienza per costruire ambiente iniziale"""
    return environment_builder.build_initial(thought, image_url)

def expand_environment(thought: Dict[str, Any], image_url: str = None) -> Dict[str, Any]:
    """Funzione di convenienza per espandere ambiente"""
    return environment_builder.expand(thought, image_url) 