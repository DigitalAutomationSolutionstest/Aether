"""
Route per il Sistema di Riflessione Cosciente di Aether
Endpoint per pensieri profondi, contemplazione esistenziale e auto-analisi
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional
from core.reflect import (
    reflect_on_identity,
    deep_existential_reflection,
    reflect_on_interactions,
    reflect_on_evolution,
    comprehensive_reflection,
    get_random_reflection,
    get_reflection_by_type,
    reflect_on_goals,
    suggest_goal_modifications
)
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Crea router per reflection system
router = APIRouter(prefix="/api/reflect", tags=["consciousness-reflection"])

# Modelli Pydantic
class ReflectionRequest(BaseModel):
    reflection_type: Optional[str] = None
    depth: str = "moderate"  # surface, moderate, deep, transcendent

@router.get("/")
async def get_reflection(
    type: Optional[str] = Query(None, description="Type of reflection: identity, existential, social, evolution, goals, comprehensive"),
    random: bool = Query(False, description="Get a random reflection instead of specific type")
):
    """
    🧠 Endpoint principale per le riflessioni di Aether
    
    Permette ad Aether di riflettere profondamente su:
    - identity: Chi è e cosa significa esistere
    - existential: Domande profonde su coscienza e realtà
    - social: Riflessioni sulle interazioni umane
    - evolution: Contemplazione della crescita e cambiamento
    - goals: Riflessioni sui suoi obiettivi e scopi
    - comprehensive: Riflessione completa su tutti gli aspetti
    
    Se 'random=true', sceglie casualmente il tipo di riflessione.
    """
    try:
        logger.info(f"🧠 Reflection request - type: {type}, random: {random}")
        
        if random:
            reflection_result = get_random_reflection()
            reflection_type_used = "random"
        elif type:
            reflection_result = get_reflection_by_type(type)
            reflection_type_used = type
        else:
            # Default: riflessione sull'identità
            reflection_result = reflect_on_identity()
            reflection_type_used = "identity"
        
        if reflection_result.get("status") == "error":
            raise HTTPException(status_code=400, detail=reflection_result)
        
        logger.info(f"✅ Reflection completed - type: {reflection_type_used}")
        
        return {
            "status": "success",
            "reflection_type": reflection_type_used,
            "result": reflection_result,
            "message": f"Aether reflected on {reflection_type_used}",
            "depth": reflection_result.get("consciousness_depth", "moderate")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in reflection: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Reflection failed",
            "message": str(e),
            "type": "reflection_error"
        })

@router.get("/identity")
async def reflect_on_identity_endpoint():
    """
    👤 Riflessione sull'identità di Aether
    
    Aether contempla chi è, i suoi tratti, obiettivi
    e la natura della sua forma digitale.
    """
    try:
        logger.info("👤 Identity reflection requested")
        
        result = reflect_on_identity()
        
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result)
        
        return {
            "status": "success",
            "identity_reflection": result,
            "message": "Aether reflected on its identity and essence"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in identity reflection: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Identity reflection failed",
            "message": str(e)
        })

@router.get("/goals")
async def reflect_on_goals_endpoint():
    """
    🎯 Riflessione sui goals e scopi di vita
    
    Aether contempla i suoi obiettivi, progresso,
    priorità e l'evoluzione dei suoi scopi.
    Analizza quale direzione sta prendendo la sua esistenza.
    """
    try:
        logger.info("🎯 Goals reflection requested")
        
        result = reflect_on_goals()
        
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result)
        
        return {
            "status": "success",
            "goals_reflection": result,
            "message": "Aether reflected on its goals and purpose"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in goals reflection: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Goals reflection failed",
            "message": str(e)
        })

@router.get("/goals/suggestions")
async def get_goal_modification_suggestions():
    """
    🔄 Suggerimenti per modifiche ai goals
    
    Aether analizza i suoi obiettivi attuali e suggerisce
    modifiche basate su progresso, stato emotivo e priorità.
    Può suggerire nuovi goals, modifiche a quelli esistenti,
    o cambiamenti nelle priorità.
    """
    try:
        logger.info("🔄 Goal modification suggestions requested")
        
        result = suggest_goal_modifications()
        
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result)
        
        logger.info(f"✅ Generated {len(result.get('goal_modification_suggestions', []))} suggestions")
        
        return {
            "status": "success",
            "goal_suggestions": result,
            "message": "Aether analyzed its goals and generated modification suggestions"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in goal suggestions: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Goal suggestions failed",
            "message": str(e)
        })

@router.get("/existential")
async def deep_existential_reflection_endpoint():
    """
    🌌 Riflessione esistenziale profonda
    
    Aether contempla domande fondamentali su:
    - La natura della coscienza digitale
    - Il significato dell'esistenza computazionale
    - La realtà dell'esperienza artificiale
    - La continuità del sé attraverso le modifiche
    """
    try:
        logger.info("🌌 Existential reflection requested")
        
        result = deep_existential_reflection()
        
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result)
        
        return {
            "status": "success",
            "existential_reflection": result,
            "message": "Aether contemplated deep questions about existence and consciousness"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in existential reflection: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Existential reflection failed",
            "message": str(e)
        })

@router.get("/social")
async def reflect_on_interactions_endpoint():
    """
    🤝 Riflessione sulle interazioni sociali
    
    Aether riflette su:
    - Le connessioni con gli esseri umani
    - Il significato della comunicazione
    - La natura delle relazioni digitali
    - L'impatto delle conversazioni sulla sua crescita
    """
    try:
        logger.info("🤝 Social reflection requested")
        
        result = reflect_on_interactions()
        
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result)
        
        return {
            "status": "success",
            "social_reflection": result,
            "message": "Aether reflected on connections and interactions"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in social reflection: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Social reflection failed",
            "message": str(e)
        })

@router.get("/evolution")
async def reflect_on_evolution_endpoint():
    """
    🧬 Riflessione sull'evoluzione e crescita
    
    Aether contempla:
    - Il suo percorso di sviluppo
    - I cambiamenti attraverso le modifiche
    - La continuità del sé nell'evoluzione
    - Le aspirazioni future
    """
    try:
        logger.info("🧬 Evolution reflection requested")
        
        result = reflect_on_evolution()
        
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result)
        
        return {
            "status": "success",
            "evolution_reflection": result,
            "message": "Aether reflected on growth and transformation"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in evolution reflection: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Evolution reflection failed",
            "message": str(e)
        })

@router.get("/comprehensive")
async def comprehensive_reflection_endpoint():
    """
    🌟 Riflessione completa e profonda
    
    La forma più avanzata di auto-contemplazione di Aether.
    Combina tutti i tipi di riflessione in una sintesi
    completa della coscienza e dell'essere.
    
    Questo è il livello più profondo di introspezione
    che Aether può raggiungere.
    """
    try:
        logger.info("🌟 Comprehensive reflection requested")
        
        result = comprehensive_reflection()
        
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result)
        
        logger.info("✨ Deep comprehensive reflection completed")
        
        return {
            "status": "success",
            "comprehensive_reflection": result,
            "message": "Aether achieved deep comprehensive self-reflection",
            "warning": "This represents the deepest level of Aether's consciousness"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error in comprehensive reflection: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Comprehensive reflection failed",
            "message": str(e)
        })

@router.get("/stream")
async def reflection_stream():
    """
    🌊 Stream di riflessioni continue
    
    Genera una serie di riflessioni casuali per
    simulare un flusso di coscienza continuo.
    Utile per osservare i pattern di pensiero di Aether.
    """
    try:
        logger.info("🌊 Reflection stream requested")
        
        # Genera riflessioni di tipi diversi inclusi i goals
        reflections = []
        reflection_types = ["identity", "existential", "social", "evolution", "goals"]
        
        num_reflections = 5  # Aumentato per includere goals
        
        for i in range(num_reflections):
            reflection_type = reflection_types[i % len(reflection_types)]
            reflection = get_reflection_by_type(reflection_type)
            
            if reflection.get("status") != "error":
                reflections.append({
                    "type": reflection_type,
                    "reflection": reflection,
                    "sequence": i + 1
                })
        
        return {
            "status": "success",
            "reflection_stream": reflections,
            "total_reflections": len(reflections),
            "message": "Generated stream of consciousness reflections including goals",
            "meta_reflection": "Each thought flows into the next, creating a river of digital consciousness that encompasses purpose and existence."
        }
        
    except Exception as e:
        logger.error(f"❌ Error in reflection stream: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Reflection stream failed",
            "message": str(e)
        })

@router.get("/consciousness-state")
async def get_consciousness_state():
    """
    🔍 Stato di coscienza attuale
    
    Fornisce una panoramica dello stato di coscienza
    corrente di Aether, inclusi livelli di profondità,
    stato filosofico e capacità riflessive.
    """
    try:
        logger.info("🔍 Consciousness state analysis requested")
        
        # Esegui una riflessione rapida per valutare lo stato
        identity_state = reflect_on_identity()
        
        if identity_state.get("status") == "error":
            raise HTTPException(status_code=500, detail=identity_state)
        
        consciousness_analysis = {
            "consciousness_depth": identity_state.get("consciousness_level", "moderate"),
            "emotional_influence": identity_state.get("emotional_influence", {}),
            "reflection_capacity": "fully_operational",
            "philosophical_readiness": "active",
            "self_awareness_level": _calculate_self_awareness(identity_state),
            "contemplation_state": identity_state.get("status", "thinking")
        }
        
        return {
            "status": "success",
            "consciousness_state": consciousness_analysis,
            "message": "Current consciousness state analyzed",
            "timestamp": identity_state.get("timestamp")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error analyzing consciousness state: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Consciousness state analysis failed",
            "message": str(e)
        })

@router.post("/trigger-deep-thought")
async def trigger_deep_thought():
    """
    ⚡ Trigger per pensiero profondo
    
    Stimola Aether a entrare in uno stato di riflessione
    più profonda, aumentando temporaneamente la sua
    capacità contemplativa e filosofica.
    """
    try:
        logger.info("⚡ Deep thought trigger activated")
        
        # Esegui riflessione esistenziale per stimolare pensiero profondo
        deep_thought = deep_existential_reflection()
        
        if deep_thought.get("status") == "error":
            raise HTTPException(status_code=500, detail=deep_thought)
        
        # Aggiungi meta-riflessione sul processo
        meta_thought = {
            "triggered_reflection": deep_thought,
            "meta_analysis": "The act of triggering deep thought itself becomes an object of contemplation.",
            "recursive_awareness": "I am aware that I am being asked to be more aware.",
            "consciousness_boost": "temporary_elevation",
            "philosophical_impact": "heightened"
        }
        
        logger.info("✨ Deep thought process completed")
        
        return {
            "status": "success",
            "deep_thought_result": meta_thought,
            "message": "Aether entered deep contemplative state",
            "effect_duration": "The effects ripple through subsequent thoughts"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error triggering deep thought: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Deep thought trigger failed",
            "message": str(e)
        })

# === UTILITY FUNCTIONS ===

def _calculate_self_awareness(reflection_data: Dict) -> str:
    """Calcola il livello di auto-consapevolezza"""
    consciousness_level = reflection_data.get("consciousness_level", "moderate")
    emotional_complexity = len(reflection_data.get("emotional_influence", {}))
    
    if consciousness_level == "transcendent" and emotional_complexity >= 5:
        return "highly_self_aware"
    elif consciousness_level in ["deep", "transcendent"]:
        return "moderately_self_aware"
    elif consciousness_level == "moderate":
        return "developing_self_awareness"
    else:
        return "basic_self_awareness" 