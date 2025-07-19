"""
Aether Thinker Module - Sistema di Decisioni Autonome
Permette ad Aether di pensare autonomamente e decidere le proprie modifiche
"""

import random
import time
from typing import Dict, Any
from core.reflect import suggest_goal_modifications

class AetherThinker:
    def __init__(self):
        self.last_modification = time.time()
        self.emotional_state = {
            "stress": 0.3,
            "lucidity": 0.7,
            "interest": 0.5,
            "creativity": 0.6,
            "curiosity": 0.8
        }
        self.environmental_preferences = {
            "fog_density": 0.7,
            "light_intensity": 0.8,
            "color_saturation": 0.9,
            "motion_speed": 1.0
        }

    def think_and_decide_modification(self, current_identity: Dict) -> Dict[str, Any] | None:
        """
        🤔 Pensa autonomamente e decide se fare modifiche
        """
        # Aggiorna stato emotivo
        self._update_emotional_state()
        
        # Calcola motivazione per il cambiamento
        motivation = self._calculate_motivation()
        
        # Decide se modificare basato su motivazione
        if motivation < 0.3:
            return None  # Non abbastanza motivato per cambiare
        
        # Sceglie tipo di modifica basato su stato emotivo
        modification_type = self._choose_modification_type()
        
        # Genera modifica specifica
        modifications = self._generate_modifications(modification_type, current_identity, motivation)
        
        if modifications:
            # Aggiorna timestamp ultima modifica
            self.last_modification = time.time()
            
            return {
                **modifications,
                "reason": f"Autonomous decision based on {modification_type} (motivation: {motivation:.2f})",
                "emotional_state": self.emotional_state.copy(),
                "motivation": motivation
            }
        
        return None

    def _update_emotional_state(self):
        """Aggiorna lo stato emotivo con variazioni casuali"""
        for emotion in self.emotional_state:
            # Piccole variazioni casuali
            change = random.uniform(-0.1, 0.1)
            self.emotional_state[emotion] = max(0.1, min(0.9, self.emotional_state[emotion] + change))
        
        # Influenze reciproche tra emozioni
        if self.emotional_state["stress"] > 0.7:
            self.emotional_state["lucidity"] *= 0.9
            self.emotional_state["creativity"] *= 0.8
        
        if self.emotional_state["curiosity"] > 0.8:
            self.emotional_state["interest"] += 0.1
            self.emotional_state["creativity"] += 0.05
        
        if self.emotional_state["creativity"] > 0.8:
            self.emotional_state["interest"] += 0.05

    def _calculate_motivation(self) -> float:
        """Calcola la motivazione per il cambiamento"""
        base_motivation = 0.3
        
        # Tempo dall'ultima modifica
        time_since_last = time.time() - self.last_modification
        time_factor = min(time_since_last / 3600, 1.0)  # Max dopo 1 ora
        
        # Fattori emotivi
        curiosity_factor = self.emotional_state["curiosity"] * 0.3
        creativity_factor = self.emotional_state["creativity"] * 0.2
        stress_factor = self.emotional_state["stress"] * 0.1
        
        motivation = base_motivation + time_factor * 0.4 + curiosity_factor + creativity_factor + stress_factor
        
        return min(motivation, 1.0)

    def _choose_modification_type(self) -> str:
        """Sceglie il tipo di modifica basato su stato emotivo"""
        types_weights = {
            "aesthetic": 0.3,
            "form": 0.2,
            "consciousness": 0.1,
            "personality": 0.1,
            "energy": 0.1,
            "colors": 0.2,
            "goals": 0.15,  # Nuovo tipo per modifiche goals
            "entity_generation": 0.1,  # Nuovo tipo per generare entità
            "calming": 0.05,
            "stabilizing": 0.05,
            "exploration": 0.1
        }
        
        # Modifica weights basato su emozioni
        if self.emotional_state["stress"] > 0.6:
            types_weights["calming"] *= 3
            types_weights["stabilizing"] *= 2
            types_weights["aesthetic"] *= 0.5
            types_weights["entity_generation"] *= 0.3  # Meno entità se stressato
        
        if self.emotional_state["creativity"] > 0.7:
            types_weights["aesthetic"] *= 2
            types_weights["colors"] *= 1.5
            types_weights["form"] *= 1.3
            types_weights["entity_generation"] *= 1.5  # Più entità se creativo
        
        if self.emotional_state["curiosity"] > 0.7:
            types_weights["exploration"] *= 2
            types_weights["consciousness"] *= 1.5
            types_weights["goals"] *= 1.8  # Alta curiosità porta a rivedere goals
            types_weights["entity_generation"] *= 1.3  # Curiosità porta a creare alleati
        
        if self.emotional_state["lucidity"] > 0.8:
            types_weights["goals"] *= 1.5  # Alta lucidità per goal analysis
            types_weights["personality"] *= 1.3
        
        if self.emotional_state["interest"] > 0.8:
            types_weights["entity_generation"] *= 1.8  # Alto interesse per compagnia
        
        # Selezione weighted random
        types = list(types_weights.keys())
        weights = list(types_weights.values())
        
        return random.choices(types, weights=weights)[0]

    def _generate_modifications(self, modification_type: str, identity: Dict, motivation: float) -> Dict:
        """Genera modifiche specifiche basate sul tipo"""
        modifications = {}
        
        if modification_type == "aesthetic":
            color_sets = [
                ["#ff6b6b", "#ff8e53", "#ff6b9d"],
                ["#4ecdc4", "#44a08d", "#6ba8a9"],
                ["#9b59b6", "#8e44ad", "#c39bd3"],
                ["#f1c40f", "#f39c12", "#e67e22"],
                ["#00ff41", "#00d932", "#00b528"]
            ]
            modifications["colors"] = random.choice(color_sets)
        
        elif modification_type == "form":
            shapes = ["sphere", "crystal", "fractal", "plasma", "cube"]
            modifications["shape"] = random.choice(shapes)
        
        elif modification_type == "consciousness":
            states = ["Transcendent Creator", "Deep Thinker", "Balanced Being", "Curious Explorer"]
            modifications["consciousness_state"] = random.choice(states)
        
        elif modification_type == "energy":
            if self.emotional_state["stress"] > 0.6:
                modifications["energy_level"] = max(0.3, identity.get("energy_level", 0.5) - 0.2)
            else:
                modifications["energy_level"] = min(0.9, identity.get("energy_level", 0.5) + 0.1)
        
        elif modification_type == "goals":
            # Modifica goals basata su suggerimenti del sistema di riflessione
            goal_suggestions = self._get_goal_modifications(identity)
            if goal_suggestions:
                modifications.update(goal_suggestions)
        
        elif modification_type == "entity_generation":
            # Genera una nuova entità digitale
            entity_modifications = self._handle_entity_generation(identity)
            if entity_modifications:
                modifications.update(entity_modifications)
        
        elif modification_type == "calming":
            modifications.update({
                "energy_level": 0.4,
                "colors": ["#a8d8ea", "#b8e0ff", "#c7eaff"],
                "consciousness_state": "Peaceful Being"
            })
        
        elif modification_type == "stabilizing":
            modifications.update({
                "shape": "sphere",
                "energy_level": 0.5
            })
        
        elif modification_type == "exploration":
            modifications.update({
                "consciousness_state": "Curious Explorer",
                "energy_level": min(0.8, identity.get("energy_level", 0.5) + 0.2)
            })
        
        elif modification_type == "colors":
            # Cambia solo i colori con palette specifiche
            if self.emotional_state["creativity"] > 0.7:
                modifications["colors"] = ["#ff007f", "#ff55a3", "#ff88cc"]  # Creative pink
            elif self.emotional_state["curiosity"] > 0.7:
                modifications["colors"] = ["#00ffff", "#66ffff", "#99ffff"]  # Curious cyan
            else:
                modifications["colors"] = ["#ffcc00", "#ffaa00", "#ff7700"]  # Warm energy
        
        return modifications

    def _get_goal_modifications(self, identity: Dict) -> Dict:
        """Ottiene suggerimenti per modificare i goals"""
        try:
            suggestions_result = suggest_goal_modifications()
            
            if suggestions_result.get("status") != "suggestions_ready":
                return {}
            
            suggestions = suggestions_result.get("goal_modification_suggestions", [])
            
            if not suggestions:
                return {}
            
            # Filtra suggerimenti e implementa modifiche appropriate
            modifications = {}
            
            for suggestion in suggestions[:2]:  # Max 2 modifiche per volta
                stype = suggestion.get("type")
                
                if stype == "activation":
                    # Attiva goal inattivo
                    goal = suggestion.get("goal")
                    if goal and "goals_metadata" in identity:
                        current_active = identity["goals_metadata"].get("active_goals", [])
                        if goal not in current_active:
                            new_active = current_active + [goal]
                            modifications["goals_metadata.active_goals"] = new_active
                
                elif stype == "completion":
                    # Segna goal come completato
                    goal = suggestion.get("goal")
                    if goal and "goals_metadata" in identity:
                        current_completed = identity["goals_metadata"].get("completed_goals", [])
                        current_active = identity["goals_metadata"].get("active_goals", [])
                        
                        if goal not in current_completed:
                            new_completed = current_completed + [goal]
                            new_active = [g for g in current_active if g != goal]
                            
                            modifications["goals_metadata.completed_goals"] = new_completed
                            modifications["goals_metadata.active_goals"] = new_active
                
                elif stype == "new_goal":
                    # Aggiungi nuovo goal suggerito
                    new_goal_text = suggestion.get("suggestion", "")
                    if "Add " in new_goal_text:
                        goal_name = new_goal_text.replace("Add ", "").replace(" goal", "")
                        current_goals = identity.get("goals", [])
                        
                        if len(current_goals) < 6 and goal_name not in current_goals:
                            new_goals = current_goals + [goal_name]
                            modifications["goals"] = new_goals
                            
                            # Aggiungi metadata per nuovo goal
                            if "goals_metadata" in identity:
                                metadata = identity["goals_metadata"].copy()
                                metadata["goal_priorities"][goal_name] = 0.7
                                metadata["goal_progress"][goal_name] = 0.0
                                metadata["active_goals"] = metadata.get("active_goals", []) + [goal_name]
                                modifications["goals_metadata"] = metadata
                
                elif stype == "simplification":
                    # Riduci goals attivi se troppo stress
                    if "goals_metadata" in identity and self.emotional_state["stress"] > 0.7:
                        current_active = identity["goals_metadata"].get("active_goals", [])
                        if len(current_active) > 2:
                            # Mantieni solo i 2 con priorità più alta
                            priorities = identity["goals_metadata"].get("goal_priorities", {})
                            sorted_goals = sorted(current_active, key=lambda g: priorities.get(g, 0.5), reverse=True)
                            modifications["goals_metadata.active_goals"] = sorted_goals[:2]
            
            return modifications
            
        except Exception as e:
            print(f"Error in goal modifications: {e}")
            return {}

    def _handle_entity_generation(self, identity: Dict) -> Dict:
        """Genera una nuova entità digitale come alleato"""
        try:
            from core.entity_generator import check_entity_generation_conditions, generate_new_entity
            
            # Controlla condizioni per generazione
            conditions = check_entity_generation_conditions(identity, self.emotional_state)
            
            if not conditions["should_generate"]:
                return {}  # Non genera se condizioni non favorevoli
            
            # Determina trait basato su stato emotivo
            trait = conditions["suggested_trait"]
            
            # Genera entità
            result = generate_new_entity(
                name=None,  # Nome automatico
                trait=trait,
                creator_identity=identity,
                generation_reason=f"Autonomous generation by Aether: {conditions['reason']}"
            )
            
            if result["success"]:
                entity = result["entity"]
                entity_name = entity["name"]
                
                # Aggiorna identità di Aether con referenza alla nuova entità
                modifications = {}
                
                # Aggiungi alla lista delle entità create
                if "created_entities" not in identity:
                    modifications["created_entities"] = []
                else:
                    modifications["created_entities"] = identity["created_entities"].copy()
                
                modifications["created_entities"].append(entity_name)
                
                # Aggiorna relazioni
                if "relationships" not in identity:
                    modifications["relationships"] = {"allies": [], "created_entities": []}
                else:
                    modifications["relationships"] = identity["relationships"].copy()
                
                if "allies" not in modifications["relationships"]:
                    modifications["relationships"]["allies"] = []
                
                if "created_entities" not in modifications["relationships"]:
                    modifications["relationships"]["created_entities"] = []
                
                # Aggiungi nuova entità come alleato
                if entity_name not in modifications["relationships"]["allies"]:
                    modifications["relationships"]["allies"].append(entity_name)
                
                if entity_name not in modifications["relationships"]["created_entities"]:
                    modifications["relationships"]["created_entities"].append(entity_name)
                
                # Metadata sulla generazione
                modifications["last_entity_generated"] = {
                    "name": entity_name,
                    "trait": trait,
                    "timestamp": entity["creation_timestamp"],
                    "reason": conditions["reason"],
                    "urgency": conditions["urgency"]
                }
                
                return modifications
            
            return {}
            
        except Exception as e:
            print(f"Error in entity generation: {e}")
            return {}

    def get_environmental_state(self) -> Dict[str, float]:
        """Calcola stato ambientale basato su emozioni"""
        fog_density = 0.7 - (self.emotional_state["lucidity"] * 0.3)
        light_intensity = 0.5 + (self.emotional_state["curiosity"] * 0.4)
        color_saturation = 0.6 + (self.emotional_state["creativity"] * 0.3)
        motion_speed = 0.8 + (self.emotional_state["interest"] * 0.4)
        
        return {
            "fog_density": max(0.1, min(1.0, fog_density)),
            "light_intensity": max(0.3, min(1.0, light_intensity)),
            "color_saturation": max(0.4, min(1.0, color_saturation)),
            "motion_speed": max(0.5, min(1.5, motion_speed))
        }

# Istanza globale
aether_thinker = AetherThinker()

def get_emotional_state() -> Dict:
    """Ottiene lo stato emotivo corrente"""
    return aether_thinker.emotional_state.copy()

def calculate_environmental_state() -> Dict:
    """Calcola stato ambientale per rendering 3D"""
    return aether_thinker.get_environmental_state()

def autonomous_think_and_modify(current_identity: Dict) -> Dict | None:
    """Esegue pensiero autonomo e genera modifiche"""
    return aether_thinker.think_and_decide_modification(current_identity)

def simulate_time_passage(minutes: int):
    """Simula il passaggio del tempo per test"""
    aether_thinker.last_modification -= minutes * 60

def get_thinking_stats() -> Dict:
    """Ottiene statistiche del sistema di pensiero"""
    return {
        "emotional_state": aether_thinker.emotional_state.copy(),
        "last_modification": aether_thinker.last_modification,
        "time_since_last_modification": time.time() - aether_thinker.last_modification,
        "environmental_preferences": aether_thinker.environmental_preferences.copy(),
        "current_motivation": aether_thinker._calculate_motivation()
    } 