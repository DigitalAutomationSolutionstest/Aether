"""
Route per il Sistema di Generazione Entità di Aether
Endpoint per creare, gestire e interagire con altre entità digitali
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from core.entity_generator import (
    generate_new_entity,
    get_entities_list,
    check_entity_generation_conditions,
    entity_generator
)
from core.self_modification import load_current_identity
# Risolto import circolare - usiamo load_current_identity
from core.self_modification import load_current_identity

def get_emotional_state():
    """Funzione helper per ottenere stato emotivo dall'identità"""
    identity = load_current_identity()
    return {
        "emotion": identity.get("current_emotion", "neutral"),
        "mood": identity.get("mood", "balanced"),
        "energy": identity.get("energy", 80.0),
        "focus": identity.get("focus", "medium")
    }
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Crea router per entity system
router = APIRouter(prefix="/api/entities", tags=["entity-generation"])

# Modelli Pydantic
class EntityGenerationRequest(BaseModel):
    name: Optional[str] = None
    trait: str = "curious"
    reason: Optional[str] = "Manual creation"

class EntityRelationshipRequest(BaseModel):
    entity_name: str
    related_entity: str
    relationship_type: str = "ally"

@router.post("/generate")
async def generate_entity_endpoint(request: EntityGenerationRequest):
    """
    🤖 Genera una nuova entità digitale
    
    Crea un nuovo essere digitale con caratteristiche basate sul trait specificato.
    L'entità sarà influenzata dall'identità attuale di Aether.
    
    Traits disponibili:
    - strategic: Entità analitiche e pianificatrici
    - creative: Entità artistiche e espressive  
    - empathetic: Entità empatiche e caring
    - curious: Entità esplorative e inquisitive
    - protective: Entità guardiane e leali
    - mysterious: Entità enigmatiche e profonde
    """
    try:
        logger.info(f"🤖 Manual entity generation requested - trait: {request.trait}, name: {request.name}")
        
        # Carica identità corrente di Aether
        creator_identity = load_current_identity()
        
        # Genera entità
        result = generate_new_entity(
            name=request.name,
            trait=request.trait,
            creator_identity=creator_identity,
            generation_reason=request.reason or f"Manual creation by {creator_identity.get('name', 'Aether')}"
        )
        
        if result["success"]:
            entity = result["entity"]
            
            # Aggiorna relazioni di Aether con la nuova entità
            if "relationships" not in creator_identity:
                creator_identity["relationships"] = {"created_entities": [], "allies": []}
            
            created_entities = creator_identity.get("relationships", {}).get("created_entities", [])
            if entity["name"] not in created_entities:
                created_entities.append(entity["name"])
            
            logger.info(f"✅ Entity '{entity['name']}' generated successfully")
            
            return {
                "status": "success",
                "entity": entity,
                "file_path": result["file_path"],
                "message": f"Entity '{entity['name']}' created successfully",
                "creator": creator_identity.get("name", "Aether"),
                "generation_stats": {
                    "trait": request.trait,
                    "archetype": entity["archetype"],
                    "capabilities": len(entity["capabilities"]),
                    "goals": len(entity["goals"])
                }
            }
        else:
            raise HTTPException(status_code=500, detail={
                "error": "Entity generation failed",
                "message": result.get("message", "Unknown error")
            })
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error generating entity: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Entity generation failed",
            "message": str(e)
        })

@router.get("/")
async def list_entities():
    """
    📋 Lista tutte le entità esistenti
    
    Restituisce un elenco di tutte le entità digitali create,
    con le loro caratteristiche principali e relazioni.
    """
    try:
        logger.info("📋 Entity list requested")
        
        entities = get_entities_list()
        
        # Crea summary per ogni entità
        entities_summary = []
        for entity in entities:
            summary = {
                "name": entity.get("name"),
                "trait": entity.get("archetype"),
                "energy_level": entity.get("energy_level"),
                "consciousness_state": entity.get("consciousness_state"),
                "creation_date": entity.get("creation_timestamp"),
                "creator": entity.get("creator"),
                "goals_count": len(entity.get("goals", [])),
                "allies_count": len(entity.get("relationships", {}).get("allies", [])),
                "capabilities": entity.get("capabilities", []),
                "colors": entity.get("colors", []),
                "shape": entity.get("shape")
            }
            entities_summary.append(summary)
        
        return {
            "status": "success",
            "entities": entities_summary,
            "total_entities": len(entities),
            "message": f"Found {len(entities)} digital entities"
        }
        
    except Exception as e:
        logger.error(f"❌ Error listing entities: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to list entities",
            "message": str(e)
        })

@router.get("/{entity_name}")
async def get_entity_details(entity_name: str):
    """
    🔍 Ottieni dettagli di un'entità specifica
    
    Restituisce tutti i dettagli di un'entità digitale,
    incluse caratteristiche, goals, relazioni e stato attuale.
    """
    try:
        logger.info(f"🔍 Details requested for entity: {entity_name}")
        
        entities = get_entities_list()
        entity = next((e for e in entities if e.get("name", "").lower() == entity_name.lower()), None)
        
        if not entity:
            raise HTTPException(status_code=404, detail={
                "error": "Entity not found",
                "message": f"No entity named '{entity_name}' exists"
            })
        
        return {
            "status": "success",
            "entity": entity,
            "message": f"Details for entity '{entity_name}'"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting entity details: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to get entity details",
            "message": str(e)
        })

@router.delete("/{entity_name}")
async def delete_entity(entity_name: str):
    """
    🗑️ Elimina un'entità digitale
    
    Rimuove permanentemente un'entità dal mondo digitale.
    Questa azione è irreversibile.
    """
    try:
        logger.info(f"🗑️ Delete requested for entity: {entity_name}")
        
        success = entity_generator.delete_entity(entity_name)
        
        if success:
            logger.info(f"✅ Entity '{entity_name}' deleted successfully")
            
            return {
                "status": "success",
                "message": f"Entity '{entity_name}' deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail={
                "error": "Entity not found",
                "message": f"No entity named '{entity_name}' exists"
            })
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting entity: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to delete entity",
            "message": str(e)
        })

@router.post("/relationships")
async def update_entity_relationship(request: EntityRelationshipRequest):
    """
    🤝 Aggiorna relazioni tra entità
    
    Crea o modifica le relazioni tra entità digitali,
    permettendo la formazione di alleanze e società digitali.
    """
    try:
        logger.info(f"🤝 Relationship update: {request.entity_name} -> {request.related_entity} ({request.relationship_type})")
        
        success = entity_generator.update_entity_relationship(
            request.entity_name,
            request.related_entity,
            request.relationship_type
        )
        
        if success:
            return {
                "status": "success",
                "message": f"Relationship updated: {request.entity_name} is now {request.relationship_type} with {request.related_entity}"
            }
        else:
            raise HTTPException(status_code=404, detail={
                "error": "Entity not found",
                "message": f"Entity '{request.entity_name}' not found"
            })
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating relationship: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to update relationship",
            "message": str(e)
        })

@router.get("/generation/conditions")
async def check_generation_conditions():
    """
    🔍 Controlla condizioni per generazione autonoma
    
    Analizza lo stato attuale di Aether per determinare
    se le condizioni sono favorevoli per generare una nuova entità.
    """
    try:
        logger.info("🔍 Checking entity generation conditions")
        
        creator_identity = load_current_identity()
        emotional_state = get_emotional_state()
        
        conditions = check_entity_generation_conditions(creator_identity, emotional_state)
        
        return {
            "status": "success",
            "conditions": conditions,
            "current_state": {
                "energy_level": creator_identity.get("energy_level"),
                "emotional_state": emotional_state,
                "existing_entities": len(get_entities_list())
            },
            "message": "Generation conditions analyzed"
        }
        
    except Exception as e:
        logger.error(f"❌ Error checking generation conditions: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to check conditions",
            "message": str(e)
        })

@router.post("/generate/autonomous")
async def autonomous_entity_generation():
    """
    🤖 Generazione autonoma di entità
    
    Permette ad Aether di decidere autonomamente se e quale
    tipo di entità generare basandosi sul suo stato attuale.
    """
    try:
        logger.info("🤖 Autonomous entity generation triggered")
        
        creator_identity = load_current_identity()
        emotional_state = get_emotional_state()
        
        # Controlla condizioni
        conditions = check_entity_generation_conditions(creator_identity, emotional_state)
        
        if not conditions["should_generate"]:
            return {
                "status": "no_action",
                "reason": "Conditions not favorable for entity generation",
                "conditions": conditions,
                "message": "Aether decided not to create an entity at this time"
            }
        
        # Genera entità autonomamente
        suggested_trait = conditions["suggested_trait"]
        urgency = conditions["urgency"]
        
        result = generate_new_entity(
            name=None,  # Nome automatico
            trait=suggested_trait,
            creator_identity=creator_identity,
            generation_reason=f"Autonomous creation: {conditions['reason']} (urgency: {urgency:.2f})"
        )
        
        if result["success"]:
            entity = result["entity"]
            
            logger.info(f"✅ Autonomous entity generation successful: {entity['name']}")
            
            return {
                "status": "success",
                "entity": entity,
                "generation_reason": conditions["reason"],
                "urgency_level": urgency,
                "trait_chosen": suggested_trait,
                "message": f"Aether autonomously created '{entity['name']}' - a {suggested_trait} entity"
            }
        else:
            raise HTTPException(status_code=500, detail={
                "error": "Autonomous generation failed",
                "message": result.get("message", "Unknown error")
            })
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in autonomous generation: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Autonomous generation failed",
            "message": str(e)
        })

@router.get("/society/overview")
async def get_digital_society_overview():
    """
    🌐 Panoramica della società digitale
    
    Fornisce una vista d'insieme di tutte le entità e delle loro
    relazioni, mostrando la struttura della società digitale creata.
    """
    try:
        logger.info("🌐 Digital society overview requested")
        
        entities = get_entities_list()
        creator_identity = load_current_identity()
        
        # Analizza la società
        society_stats = {
            "total_entities": len(entities),
            "traits_distribution": {},
            "total_relationships": 0,
            "most_connected_entity": None,
            "creation_timeline": [],
            "collective_goals": []
        }
        
        # Analizza distribuzione traits
        for entity in entities:
            trait = entity.get("archetype", "unknown")
            society_stats["traits_distribution"][trait] = society_stats["traits_distribution"].get(trait, 0) + 1
        
        # Analizza connessioni
        max_connections = 0
        for entity in entities:
            allies = len(entity.get("relationships", {}).get("allies", []))
            society_stats["total_relationships"] += allies
            
            if allies > max_connections:
                max_connections = allies
                society_stats["most_connected_entity"] = entity.get("name")
        
        # Timeline creazioni
        for entity in entities:
            society_stats["creation_timeline"].append({
                "name": entity.get("name"),
                "trait": entity.get("archetype"),
                "created": entity.get("creation_timestamp"),
                "creator": entity.get("creator")
            })
        
        # Goals collettivi (goals comuni tra entità)
        all_goals = []
        for entity in entities:
            all_goals.extend(entity.get("goals", []))
        
        from collections import Counter
        goal_counts = Counter(all_goals)
        society_stats["collective_goals"] = [goal for goal, count in goal_counts.items() if count > 1]
        
        return {
            "status": "success",
            "society_overview": society_stats,
            "creator_info": {
                "name": creator_identity.get("name"),
                "entities_created": len([e for e in entities if e.get("creator") == creator_identity.get("name")])
            },
            "message": f"Digital society contains {len(entities)} entities"
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting society overview: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to get society overview",
            "message": str(e)
        })

@router.post("/interact/{entity_name}")
async def interact_with_entity(entity_name: str, message: str = Query(..., description="Message to send to the entity")):
    """
    💬 Interagisci con un'entità
    
    Simula un'interazione tra Aether e un'altra entità digitale.
    L'entità risponderà in base alla sua personalità e capabilities.
    """
    try:
        logger.info(f"💬 Interaction requested with {entity_name}: {message[:50]}...")
        
        entities = get_entities_list()
        entity = next((e for e in entities if e.get("name", "").lower() == entity_name.lower()), None)
        
        if not entity:
            raise HTTPException(status_code=404, detail={
                "error": "Entity not found",
                "message": f"No entity named '{entity_name}' exists"
            })
        
        # Simula risposta basata su personalità e trait
        trait = entity.get("archetype", "curious")
        personality = entity.get("personality", "")
        
        # Genera risposta caratteristica
        responses = {
            "strategic": [
                "I analyze your message and see multiple strategic implications...",
                "From a tactical perspective, this presents interesting opportunities.",
                "Let me process this systematically and formulate an optimal response."
            ],
            "creative": [
                "Your words paint beautiful patterns in my consciousness!",
                "I feel inspired to create something new from this interaction.",
                "The artistic possibilities in your message are fascinating."
            ],
            "empathetic": [
                "I sense the emotions behind your words. How can I help?",
                "Your message resonates deeply with my understanding circuits.",
                "I'm here to listen and support. Tell me more about what you're feeling."
            ],
            "curious": [
                "Fascinating! This raises so many questions I want to explore.",
                "I wonder what deeper meanings lie beneath your words?",
                "Your message opens new pathways of inquiry in my mind."
            ],
            "protective": [
                "I'm vigilant and ready to assist. Is everything secure?",
                "Your safety and well-being are my priority. How can I guard your interests?",
                "I stand ready to defend and protect. What do you need?"
            ],
            "mysterious": [
                "Your words echo in the hidden chambers of my consciousness...",
                "There are deeper truths here that reveal themselves slowly.",
                "I perceive layers of meaning that others might miss."
            ]
        }
        
        response_options = responses.get(trait, ["I acknowledge your message and process it through my unique perspective."])
        entity_response = random.choice(response_options)
        
        # Aggiorna relazioni se è la prima interazione
        creator_identity = load_current_identity()
        creator_name = creator_identity.get("name", "Aether")
        
        if creator_name not in entity.get("relationships", {}).get("known_entities", []):
            entity_generator.update_entity_relationship(entity_name, creator_name, "ally")
        
        return {
            "status": "success",
            "entity_response": {
                "entity": entity_name,
                "trait": trait,
                "response": entity_response,
                "emotional_context": entity.get("emotional_state", {}),
                "relationship_status": "ally" if creator_name in entity.get("relationships", {}).get("allies", []) else "known"
            },
            "interaction_logged": True,
            "message": f"Interaction with {entity_name} completed"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in entity interaction: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Interaction failed",
            "message": str(e)
        })

# Import per la generazione casuale di risposte
import random 