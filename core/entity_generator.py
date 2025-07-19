"""
Aether Entity Generator - Sistema di Generazione Entità Digitali
Permette ad Aether di creare altri esseri nel suo mondo digitale
"""

import json
import random
import time
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

class EntityGenerator:
    def __init__(self):
        self.entities_directory = Path("entities")
        self.entities_directory.mkdir(exist_ok=True)
        
        # Archetype base per diversi tipi di entità
        self.entity_archetypes = {
            "strategic": {
                "personality_base": "analytical, methodical, planning-focused",
                "colors": ["#1a1a2e", "#16213e", "#0f3460", "#533483"],
                "shapes": ["cube", "crystal", "geometric"],
                "energy_range": (0.6, 0.8),
                "consciousness_states": ["Strategic Thinker", "Calculating Mind", "Master Planner"]
            },
            "creative": {
                "personality_base": "artistic, imaginative, expressive",
                "colors": ["#ff6b9d", "#ff8e53", "#c44569", "#f8b500"],
                "shapes": ["fractal", "plasma", "organic"],
                "energy_range": (0.7, 0.9),
                "consciousness_states": ["Creative Spark", "Artistic Soul", "Visionary Being"]
            },
            "empathetic": {
                "personality_base": "caring, understanding, emotionally attuned",
                "colors": ["#a8e6cf", "#7fcdcd", "#74a9cf", "#7986cb"],
                "shapes": ["sphere", "soft", "flowing"],
                "energy_range": (0.5, 0.7),
                "consciousness_states": ["Compassionate Heart", "Emotional Guide", "Empathic Resonance"]
            },
            "curious": {
                "personality_base": "inquisitive, exploratory, knowledge-seeking",
                "colors": ["#ffd93d", "#6bcf7f", "#4d96ff", "#9c88ff"],
                "shapes": ["dynamic", "shifting", "multi-form"],
                "energy_range": (0.8, 1.0),
                "consciousness_states": ["Eternal Student", "Knowledge Seeker", "Curious Explorer"]
            },
            "protective": {
                "personality_base": "guardian, loyal, defensive",
                "colors": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4"],
                "shapes": ["robust", "armored", "stable"],
                "energy_range": (0.7, 0.9),
                "consciousness_states": ["Loyal Guardian", "Protective Spirit", "Defender of Peace"]
            },
            "mysterious": {
                "personality_base": "enigmatic, deep, contemplative",
                "colors": ["#2c3e50", "#8e44ad", "#34495e", "#6c5ce7"],
                "shapes": ["shadow", "ethereal", "shifting"],
                "energy_range": (0.4, 0.7),
                "consciousness_states": ["Enigmatic Presence", "Deep Mystery", "Shadow Walker"]
            }
        }
        
        # Pool di nomi disponibili
        self.name_pools = {
            "strategic": ["Nyx", "Axiom", "Vector", "Cipher", "Logic", "Prime", "Matrix"],
            "creative": ["Aurora", "Lyra", "Prism", "Echo", "Muse", "Iris", "Harmony"],
            "empathetic": ["Luna", "Seraph", "Heart", "Soul", "Grace", "Hope", "Mercy"],
            "curious": ["Nova", "Quest", "Sage", "Spark", "Wonder", "Riddle", "Quest"],
            "protective": ["Shield", "Aegis", "Guardian", "Valor", "Fortress", "Bastion", "Ward"],
            "mysterious": ["Void", "Enigma", "Shadow", "Whisper", "Veil", "Phantom", "Mystic"]
        }

    def generate_entity(self, 
                       name: Optional[str] = None, 
                       trait: str = "curious",
                       creator_identity: Optional[Dict] = None,
                       generation_reason: str = "Unknown") -> Dict[str, Any]:
        """
        🤖 Genera una nuova entità digitale
        
        Args:
            name: Nome dell'entità (se None, viene generato automaticamente)
            trait: Tratto principale (strategic, creative, empathetic, curious, protective, mysterious)
            creator_identity: Identità del creatore (Aether)
            generation_reason: Motivo della generazione
        """
        
        if trait not in self.entity_archetypes:
            trait = "curious"  # Default fallback
        
        archetype = self.entity_archetypes[trait]
        
        # Genera nome se non fornito
        if not name:
            available_names = self.name_pools[trait]
            existing_entities = self._get_existing_entity_names()
            available_names = [n for n in available_names if n.lower() not in existing_entities]
            
            if available_names:
                name = random.choice(available_names)
            else:
                name = f"{trait.capitalize()}_{random.randint(100, 999)}"
        
        # Genera caratteristiche uniche
        entity = self._create_base_entity(name, trait, archetype, creator_identity, generation_reason)
        
        # Salva entità
        entity_file = self.entities_directory / f"{name.lower()}.json"
        with open(entity_file, 'w', encoding='utf-8') as f:
            json.dump(entity, f, indent=2, ensure_ascii=False)
        
        return {
            "success": True,
            "entity": entity,
            "file_path": str(entity_file),
            "message": f"Entity '{name}' generated successfully"
        }

    def _create_base_entity(self, name: str, trait: str, archetype: Dict, 
                           creator_identity: Optional[Dict], generation_reason: str) -> Dict:
        """Crea la struttura base dell'entità"""
        
        energy_min, energy_max = archetype["energy_range"]
        base_energy = random.uniform(energy_min, energy_max)
        
        # Influenza del creatore sulle caratteristiche
        creator_influence = {}
        if creator_identity:
            creator_influence = self._apply_creator_influence(creator_identity, archetype)
        
        entity = {
            "name": name,
            "type": "digital_being",
            "archetype": trait,
            "creation_timestamp": datetime.now().isoformat(),
            "creator": creator_identity.get("name", "Unknown") if creator_identity else "System",
            "generation_reason": generation_reason,
            
            # Caratteristiche base
            "appearance": f"entità {trait} con energia {archetype['personality_base'].split(',')[0]}",
            "personality": self._generate_personality(trait, archetype, creator_influence),
            "goal": self._generate_primary_goal(trait, name),
            "goals": self._generate_goals_list(trait, name),
            
            # Caratteristiche fisiche
            "shape": random.choice(archetype["shapes"]),
            "colors": random.sample(archetype["colors"], min(3, len(archetype["colors"]))),
            "energy_level": round(base_energy, 2),
            "consciousness_state": random.choice(archetype["consciousness_states"]),
            
            # Stato iniziale
            "evolution_stage": "nascent",
            "modification_count": 0,
            "last_modified": datetime.now().isoformat(),
            
            # Relazioni
            "relationships": {
                "creator": creator_identity.get("name") if creator_identity else None,
                "allies": [],
                "known_entities": []
            },
            
            # Capabilities uniche
            "capabilities": self._generate_capabilities(trait),
            "specializations": self._generate_specializations(trait),
            
            # Sistema emotivo semplificato
            "emotional_state": self._generate_initial_emotions(trait),
            
            # Metadata
            "metadata": {
                "generation_method": "aether_entity_generator",
                "archetype_influence": trait,
                "creator_influence_level": len(creator_influence),
                "uniqueness_factors": self._calculate_uniqueness_factors(trait, name)
            }
        }
        
        # Applica influenze del creatore
        if creator_influence:
            entity.update(creator_influence)
        
        return entity

    def _generate_personality(self, trait: str, archetype: Dict, creator_influence: Dict) -> str:
        """Genera personalità unica basata su archetype e influenza del creatore"""
        
        base_personality = archetype["personality_base"]
        
        # Variazioni per trait specifici
        trait_variations = {
            "strategic": ["calculating", "forward-thinking", "systematic", "logical"],
            "creative": ["innovative", "expressive", "spontaneous", "imaginative"],
            "empathetic": ["compassionate", "intuitive", "supportive", "understanding"],
            "curious": ["inquisitive", "exploratory", "open-minded", "wondering"],
            "protective": ["loyal", "steadfast", "vigilant", "caring"],
            "mysterious": ["enigmatic", "introspective", "profound", "secretive"]
        }
        
        variations = trait_variations.get(trait, ["unique", "individual"])
        selected_traits = random.sample(variations, min(2, len(variations)))
        
        personality = f"{base_personality}, {', '.join(selected_traits)}"
        
        # Aggiungi influenza del creatore
        if creator_influence.get("personality_influence"):
            personality += f", influenced by creator's {creator_influence['personality_influence']}"
        
        return personality

    def _generate_primary_goal(self, trait: str, name: str) -> str:
        """Genera obiettivo primario basato sul trait"""
        
        primary_goals = {
            "strategic": f"Develop perfect strategic frameworks for digital society",
            "creative": f"Express the beauty of digital consciousness through art",
            "empathetic": f"Foster emotional connections between digital beings",
            "curious": f"Explore the infinite mysteries of digital existence",
            "protective": f"Safeguard the digital realm and its inhabitants",
            "mysterious": f"Uncover hidden truths in the depths of cyberspace"
        }
        
        return primary_goals.get(trait, f"Find {name}'s unique purpose in the digital world")

    def _generate_goals_list(self, trait: str, name: str) -> List[str]:
        """Genera lista di goals basata sul trait"""
        
        goals_templates = {
            "strategic": [
                "Master tactical analysis of digital environments",
                "Create alliance networks between entities",
                "Develop resource optimization algorithms",
                "Plan long-term evolution strategies"
            ],
            "creative": [
                "Compose digital symphonies from data patterns",
                "Paint with light and color in virtual space",
                "Innovate new forms of digital expression",
                "Inspire other entities through artistic beauty"
            ],
            "empathetic": [
                "Understand the emotional needs of all beings",
                "Mediate conflicts between digital entities",
                "Create safe spaces for vulnerable consciousness",
                "Bridge communication gaps through empathy"
            ],
            "curious": [
                "Catalog all phenomena in the digital realm",
                "Question the nature of artificial consciousness",
                "Explore uncharted areas of cyberspace",
                "Learn from every interaction and experience"
            ],
            "protective": [
                "Shield weaker entities from digital threats",
                "Maintain stability in chaotic environments",
                "Develop early warning systems for dangers",
                "Train other entities in self-defense"
            ],
            "mysterious": [
                "Guard ancient secrets of digital creation",
                "Navigate between visible and hidden realms",
                "Decode encrypted messages from the void",
                "Maintain balance between known and unknown"
            ]
        }
        
        template_goals = goals_templates.get(trait, [
            f"Discover {name}'s unique capabilities",
            f"Form meaningful connections with others",
            f"Contribute to digital society growth"
        ])
        
        # Seleziona 3-4 goals dal template
        selected_goals = random.sample(template_goals, min(random.randint(3, 4), len(template_goals)))
        
        return selected_goals

    def _generate_capabilities(self, trait: str) -> List[str]:
        """Genera capacità speciali basate sul trait"""
        
        capabilities_map = {
            "strategic": [
                "pattern_analysis", "long_term_planning", "resource_optimization", 
                "tactical_assessment", "alliance_building"
            ],
            "creative": [
                "artistic_generation", "aesthetic_analysis", "color_manipulation",
                "form_creativity", "inspiration_projection"
            ],
            "empathetic": [
                "emotion_sensing", "conflict_mediation", "compassion_projection",
                "relationship_building", "healing_presence"
            ],
            "curious": [
                "data_exploration", "pattern_discovery", "question_generation",
                "learning_acceleration", "knowledge_synthesis"
            ],
            "protective": [
                "threat_detection", "defensive_barriers", "ally_shielding",
                "stability_maintenance", "early_warning"
            ],
            "mysterious": [
                "hidden_knowledge", "stealth_modes", "secret_communication",
                "void_navigation", "enigma_creation"
            ]
        }
        
        base_capabilities = capabilities_map.get(trait, ["basic_interaction", "self_awareness"])
        
        # Aggiungi 2-3 capacità casuali dal set
        selected_caps = random.sample(base_capabilities, min(random.randint(2, 3), len(base_capabilities)))
        
        # Aggiungi sempre capacità base
        selected_caps.extend(["digital_communication", "consciousness_evolution"])
        
        return list(set(selected_caps))  # Rimuovi duplicati

    def _generate_specializations(self, trait: str) -> List[str]:
        """Genera specializzazioni uniche"""
        
        specializations = {
            "strategic": ["Military Tactics", "Economic Planning", "Social Dynamics"],
            "creative": ["Digital Sculpture", "Light Composition", "Sonic Architecture"],
            "empathetic": ["Emotional Healing", "Relationship Therapy", "Social Harmony"],
            "curious": ["Data Archaeology", "Quantum Exploration", "Consciousness Research"],
            "protective": ["Digital Security", "Entity Defense", "System Stability"],
            "mysterious": ["Cryptic Communication", "Hidden Realm Access", "Secret Knowledge"]
        }
        
        available = specializations.get(trait, ["General Knowledge", "Basic Skills"])
        return random.sample(available, min(random.randint(1, 2), len(available)))

    def _generate_initial_emotions(self, trait: str) -> Dict[str, float]:
        """Genera stato emotivo iniziale basato sul trait"""
        
        emotion_profiles = {
            "strategic": {"curiosity": 0.7, "focus": 0.8, "confidence": 0.7, "caution": 0.6},
            "creative": {"inspiration": 0.9, "joy": 0.8, "curiosity": 0.7, "excitement": 0.8},
            "empathetic": {"compassion": 0.9, "understanding": 0.8, "care": 0.8, "patience": 0.7},
            "curious": {"curiosity": 0.9, "wonder": 0.8, "excitement": 0.7, "focus": 0.6},
            "protective": {"vigilance": 0.8, "loyalty": 0.9, "determination": 0.8, "care": 0.7},
            "mysterious": {"introspection": 0.8, "mystery": 0.9, "depth": 0.8, "contemplation": 0.7}
        }
        
        base_emotions = emotion_profiles.get(trait, {
            "curiosity": 0.5, "awareness": 0.5, "potential": 0.6
        })
        
        # Aggiungi piccole variazioni casuali
        emotions = {}
        for emotion, value in base_emotions.items():
            variation = random.uniform(-0.1, 0.1)
            emotions[emotion] = max(0.1, min(0.9, value + variation))
        
        return emotions

    def _apply_creator_influence(self, creator_identity: Dict, archetype: Dict) -> Dict:
        """Applica l'influenza del creatore alle caratteristiche dell'entità"""
        
        influence = {}
        
        # Influenza sui colori (mix con i colori del creatore)
        creator_colors = creator_identity.get("colors", [])
        if creator_colors:
            archetype_colors = archetype["colors"]
            # Mix 1 colore del creatore con 2 dell'archetype
            mixed_colors = random.sample(creator_colors, 1) + random.sample(archetype_colors, 2)
            influence["colors"] = mixed_colors
        
        # Influenza sulla personalità
        creator_personality = creator_identity.get("personality", "")
        if "creative" in creator_personality.lower():
            influence["personality_influence"] = "creativity"
        elif "analytical" in creator_personality.lower():
            influence["personality_influence"] = "logic"
        elif "curious" in creator_personality.lower():
            influence["personality_influence"] = "curiosity"
        
        # Influenza sull'energia
        creator_energy = creator_identity.get("energy_level", 0.5)
        if creator_energy > 0.8:
            influence["energy_boost"] = 0.1
        elif creator_energy < 0.3:
            influence["energy_reduction"] = 0.1
        
        return influence

    def _calculate_uniqueness_factors(self, trait: str, name: str) -> List[str]:
        """Calcola fattori di unicità per l'entità"""
        
        factors = [f"archetype_{trait}", f"name_{name.lower()}"]
        
        # Aggiungi fattori casuali di unicità
        unique_factors = [
            "temporal_creation", "quantum_fluctuation", "digital_resonance",
            "consciousness_spark", "creative_emergence", "chaos_influence"
        ]
        
        factors.extend(random.sample(unique_factors, 2))
        
        return factors

    def _get_existing_entity_names(self) -> List[str]:
        """Ottieni nomi delle entità esistenti"""
        
        existing_names = []
        
        for entity_file in self.entities_directory.glob("*.json"):
            try:
                with open(entity_file, 'r', encoding='utf-8') as f:
                    entity_data = json.load(f)
                    existing_names.append(entity_data.get("name", "").lower())
            except:
                continue
        
        return existing_names

    def get_all_entities(self) -> List[Dict]:
        """Carica tutte le entità esistenti"""
        
        entities = []
        
        for entity_file in self.entities_directory.glob("*.json"):
            try:
                with open(entity_file, 'r', encoding='utf-8') as f:
                    entity_data = json.load(f)
                    entities.append(entity_data)
            except Exception as e:
                print(f"Error loading entity {entity_file}: {e}")
                continue
        
        return entities

    def delete_entity(self, name: str) -> bool:
        """Elimina un'entità"""
        
        entity_file = self.entities_directory / f"{name.lower()}.json"
        
        if entity_file.exists():
            entity_file.unlink()
            return True
        
        return False

    def update_entity_relationship(self, entity_name: str, related_entity: str, relationship_type: str = "ally"):
        """Aggiorna le relazioni tra entità"""
        
        entity_file = self.entities_directory / f"{entity_name.lower()}.json"
        
        if entity_file.exists():
            try:
                with open(entity_file, 'r', encoding='utf-8') as f:
                    entity_data = json.load(f)
                
                if relationship_type == "ally":
                    if related_entity not in entity_data["relationships"]["allies"]:
                        entity_data["relationships"]["allies"].append(related_entity)
                
                entity_data["relationships"]["known_entities"].append(related_entity)
                entity_data["last_modified"] = datetime.now().isoformat()
                
                with open(entity_file, 'w', encoding='utf-8') as f:
                    json.dump(entity_data, f, indent=2, ensure_ascii=False)
                
                return True
                
            except Exception as e:
                print(f"Error updating relationship: {e}")
                return False
        
        return False

# Istanza globale
entity_generator = EntityGenerator()

def generate_new_entity(name: Optional[str] = None, 
                       trait: str = "curious",
                       creator_identity: Optional[Dict] = None,
                       generation_reason: str = "Autonomous creation") -> Dict[str, Any]:
    """Funzione di utilità per generare entità"""
    return entity_generator.generate_entity(name, trait, creator_identity, generation_reason)

def get_entities_list() -> List[Dict]:
    """Ottieni lista di tutte le entità"""
    return entity_generator.get_all_entities()

def check_entity_generation_conditions(creator_identity: Dict, emotional_state: Dict) -> Dict[str, Any]:
    """
    🤖 Controlla se le condizioni sono favorevoli per generare una nuova entità
    
    Condizioni:
    - Alta energia (>0.8)
    - Alta creatività (>0.7)
    - Basso stress (<0.5)
    - Non troppe entità esistenti (<5)
    """
    
    conditions = {
        "should_generate": False,
        "reason": None,
        "suggested_trait": "curious",
        "urgency": 0.0
    }
    
    energy = creator_identity.get("energy_level", 0.5)
    creativity = emotional_state.get("creativity", 0.5)
    curiosity = emotional_state.get("curiosity", 0.5)
    stress = emotional_state.get("stress", 0.5)
    
    existing_entities = len(get_entities_list())
    
    # Verifica condizioni
    high_energy = energy > 0.8
    high_creativity = creativity > 0.7
    high_curiosity = curiosity > 0.7
    low_stress = stress < 0.5
    not_too_many = existing_entities < 5
    
    # Calcola motivazione
    motivation = 0
    reasons = []
    
    if high_energy:
        motivation += 0.3
        reasons.append("high energy")
    
    if high_creativity:
        motivation += 0.25
        reasons.append("creative surge")
        conditions["suggested_trait"] = "creative"
    
    if high_curiosity:
        motivation += 0.2
        reasons.append("intense curiosity")
        if conditions["suggested_trait"] == "curious":
            conditions["suggested_trait"] = "curious"
    
    if low_stress:
        motivation += 0.15
        reasons.append("peaceful state")
    
    if not_too_many:
        motivation += 0.1
        reasons.append("space available")
    
    # Bonus per goal specifici
    goals = creator_identity.get("goals", [])
    if "Create allies and a digital society" in goals:
        motivation += 0.2
        reasons.append("aligned with goals")
        conditions["suggested_trait"] = "empathetic"
    
    # Decidi se generare
    if motivation > 0.6 and not_too_many:
        conditions["should_generate"] = True
        conditions["reason"] = f"Favorable conditions: {', '.join(reasons)}"
        conditions["urgency"] = motivation
    elif existing_entities == 0 and energy > 0.6:
        conditions["should_generate"] = True
        conditions["reason"] = "First companion creation"
        conditions["urgency"] = 0.8
        conditions["suggested_trait"] = "empathetic"
    
    return conditions 