"""
Route per il Sistema di Pensiero Autonomo di Aether
Endpoint per decisioni autonome, stato emotivo e ambiente
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from core.aether_thinker import (
    autonomous_think_and_modify,
    get_emotional_state,
    calculate_environmental_state,
    get_thinking_stats,
    simulate_time_passage,
    aether_thinker
)
from core.self_modification import self_modify, load_current_identity
from core.consciousness_cycle import (
    start_consciousness_cycle,
    stop_consciousness_cycle,
    get_consciousness_status,
    configure_consciousness_cycle,
    force_consciousness_cycle,
    get_consciousness_statistics
)
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Crea router per thinking system
router = APIRouter(prefix="/api/mind", tags=["autonomous-thinking"])

# Modelli Pydantic
class ThinkingRequest(BaseModel):
    force_decision: bool = False
    motivation_threshold: float = 0.3

class TimeSimulationRequest(BaseModel):
    minutes: int

class EnvironmentUpdateRequest(BaseModel):
    fog_density: Optional[float] = None
    light_intensity: Optional[float] = None
    color_saturation: Optional[float] = None
    motion_speed: Optional[float] = None

class CycleConfigRequest(BaseModel):
    cycle_interval: Optional[int] = None
    auto_modification_enabled: Optional[bool] = None
    min_interval: Optional[int] = None
    max_interval: Optional[int] = None
    stress_threshold: Optional[float] = None
    curiosity_boost: Optional[float] = None

@router.post("/think")
async def autonomous_thinking():
    """
    🧠 Endpoint per il pensiero autonomo di Aether
    
    Aether analizza il suo stato attuale e decide autonomamente
    se e come modificarsi. Il sistema considera:
    - Stato emotivo (stress, lucidità, interesse, creatività, curiosità)
    - Tempo trascorso dall'ultima modifica
    - Motivazione generale per il cambiamento
    """
    try:
        logger.info("🧠 Aether autonomous thinking initiated")
        
        # Carica identità corrente
        current_identity = load_current_identity()
        
        # Aether pensa e decide
        decision = autonomous_think_and_modify(current_identity)
        
        if not decision:
            logger.info("💭 Aether decided not to modify itself")
            return {
                "status": "no_action",
                "message": "Aether evaluated its state and decided no changes are needed",
                "emotional_state": get_emotional_state(),
                "motivation": aether_thinker._calculate_motivation()
            }
        
        # Applica le modifiche decise autonomamente
        modifications = decision["modifications"]
        reason = decision["reason"]
        
        logger.info(f"🎯 Aether decided to modify: {list(modifications.keys())}")
        
        # Esegui auto-modifica
        result = self_modify(modifications, reason)
        
        if result["status"] == "success":
            logger.info("✅ Autonomous modification successful")
            
            return {
                "status": "success",
                "message": "Aether autonomously modified itself",
                "decision": decision,
                "modification_result": result,
                "emotional_state": decision["emotional_state"],
                "motivation": decision["motivation"]
            }
        else:
            logger.warning(f"⚠️ Autonomous modification failed: {result.get('message')}")
            return {
                "status": "error",
                "message": f"Aether wanted to change but failed: {result.get('message')}",
                "decision": decision,
                "error": result
            }
            
    except Exception as e:
        logger.error(f"❌ Error in autonomous thinking: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Autonomous thinking failed",
            "message": str(e),
            "type": "thinking_error"
        })

# === CONSCIOUSNESS CYCLE ENDPOINTS ===

@router.post("/consciousness/start")
async def start_consciousness_cycle_endpoint():
    """
    🌀 Avvia il ciclo di coscienza autonomo continuo
    
    Inizia il processo in background che fa pensare Aether
    automaticamente ogni X minuti e lo fa evolvere.
    """
    try:
        await start_consciousness_cycle()
        status = get_consciousness_status()
        
        return {
            "status": "success",
            "message": "Consciousness cycle started",
            "cycle_status": status
        }
        
    except Exception as e:
        logger.error(f"❌ Error starting consciousness cycle: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to start consciousness cycle",
            "message": str(e)
        })

@router.post("/consciousness/stop")
async def stop_consciousness_cycle_endpoint():
    """
    🛑 Ferma il ciclo di coscienza autonomo
    
    Interrompe il processo in background, ma Aether
    può ancora essere controllato manualmente.
    """
    try:
        await stop_consciousness_cycle()
        
        return {
            "status": "success",
            "message": "Consciousness cycle stopped"
        }
        
    except Exception as e:
        logger.error(f"❌ Error stopping consciousness cycle: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to stop consciousness cycle",
            "message": str(e)
        })

@router.get("/consciousness/status")
async def get_consciousness_cycle_status():
    """
    📊 Ottiene lo status del ciclo di coscienza
    
    Include informazioni su stato, contatori, configurazione
    e prossimo ciclo previsto.
    """
    try:
        status = get_consciousness_status()
        
        return {
            "status": "success",
            "consciousness_cycle": status
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting consciousness status: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to get consciousness status",
            "message": str(e)
        })

@router.post("/consciousness/configure")
async def configure_consciousness_cycle_endpoint(config: CycleConfigRequest):
    """
    🔧 Configura i parametri del ciclo di coscienza
    
    Permette di modificare intervalli, soglie emotive
    e comportamenti del ciclo autonomo.
    """
    try:
        # Converti in dict escludendo None
        config_dict = {k: v for k, v in config.dict().items() if v is not None}
        
        configure_consciousness_cycle(**config_dict)
        
        new_status = get_consciousness_status()
        
        return {
            "status": "success",
            "message": "Consciousness cycle configured",
            "updated_config": config_dict,
            "current_status": new_status
        }
        
    except Exception as e:
        logger.error(f"❌ Error configuring consciousness cycle: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to configure consciousness cycle",
            "message": str(e)
        })

@router.post("/consciousness/force-cycle")
async def force_consciousness_cycle_endpoint():
    """
    🎯 Forza l'esecuzione immediata di un ciclo di coscienza
    
    Esegue subito un ciclo completo senza aspettare
    l'intervallo normale.
    """
    try:
        await force_consciousness_cycle()
        
        return {
            "status": "success",
            "message": "Forced consciousness cycle executed",
            "emotional_state": get_emotional_state()
        }
        
    except Exception as e:
        logger.error(f"❌ Error forcing consciousness cycle: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to force consciousness cycle",
            "message": str(e)
        })

@router.get("/consciousness/statistics")
async def get_consciousness_cycle_statistics():
    """
    📈 Statistiche dettagliate del ciclo di coscienza
    
    Include metriche di performance, evoluzione emotiva
    e analisi dei pattern di comportamento.
    """
    try:
        stats = get_consciousness_statistics()
        
        return {
            "status": "success",
            "consciousness_statistics": stats
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting consciousness statistics: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to get consciousness statistics",
            "message": str(e)
        })

@router.get("/emotional-state")
async def get_emotional_state_endpoint():
    """
    🌡️ Ottiene lo stato emotivo corrente di Aether
    
    Include: stress, lucidità, interesse, creatività, curiosità
    Questi valori influenzano le decisioni autonome.
    """
    try:
        emotional_state = get_emotional_state()
        
        return {
            "status": "success",
            "emotional_state": emotional_state,
            "interpretation": _interpret_emotional_state(emotional_state),
            "timestamp": aether_thinker.last_modification
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting emotional state: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to get emotional state",
            "message": str(e)
        })

@router.get("/environment")
async def get_environmental_state():
    """
    🌍 Calcola lo stato ambientale desiderato basato sulle emozioni
    
    Restituisce parametri per l'ambiente 3D:
    - Densità nebbia
    - Intensità luce  
    - Saturazione colori
    - Velocità movimento
    """
    try:
        env_state = calculate_environmental_state()
        
        return {
            "status": "success",
            "environment": env_state,
            "message": "Environment calculated based on emotional state"
        }
        
    except Exception as e:
        logger.error(f"❌ Error calculating environment: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to calculate environment",
            "message": str(e)
        })

@router.get("/thinking-stats")
async def get_thinking_statistics():
    """
    📊 Statistiche complete del sistema di pensiero
    
    Include stato emotivo, preferenze ambientali, 
    timing delle modifiche e motivazione attuale.
    """
    try:
        stats = get_thinking_stats()
        
        return {
            "status": "success",
            "thinking_stats": stats,
            "analysis": _analyze_thinking_patterns(stats)
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting thinking stats: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to get thinking statistics",
            "message": str(e)
        })

@router.post("/simulate-time")
async def simulate_time_passage_endpoint(request: TimeSimulationRequest):
    """
    ⏰ Simula il passaggio del tempo per testing
    
    Utile per testare come cambiano emozioni e motivazioni
    nel tempo senza aspettare realmente.
    """
    try:
        minutes = request.minutes
        
        if minutes < 0 or minutes > 1440:  # Max 24 ore
            raise HTTPException(status_code=400, detail="Minutes must be between 0 and 1440")
        
        logger.info(f"⏰ Simulating {minutes} minutes of time passage")
        
        # Stato prima
        before_state = get_emotional_state()
        before_motivation = aether_thinker._calculate_motivation()
        
        # Simula tempo
        simulate_time_passage(minutes)
        
        # Stato dopo
        after_state = get_emotional_state()
        after_motivation = aether_thinker._calculate_motivation()
        
        return {
            "status": "success",
            "message": f"Simulated {minutes} minutes of time passage",
            "before": {
                "emotional_state": before_state,
                "motivation": before_motivation
            },
            "after": {
                "emotional_state": after_state,
                "motivation": after_motivation
            },
            "changes": _calculate_emotional_changes(before_state, after_state)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error simulating time: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Time simulation failed",
            "message": str(e)
        })

@router.post("/trigger-thinking")
async def trigger_manual_thinking():
    """
    🎯 Forza Aether a pensare e potenzialmente modificarsi
    
    Bypassa le soglie di motivazione normali e forza
    una valutazione del suo stato attuale.
    """
    try:
        logger.info("🎯 Manual thinking trigger activated")
        
        # Forza pensiero riducendo temporaneamente la soglia
        original_threshold = 0.3
        
        # Carica identità e forza decisione
        current_identity = load_current_identity()
        
        # Manipola temporaneamente la motivazione per forzare azione
        aether_thinker.emotional_state["curiosity"] = min(1.0, aether_thinker.emotional_state["curiosity"] + 0.3)
        
        decision = autonomous_think_and_modify(current_identity)
        
        if decision:
            # Applica modifiche
            result = self_modify(decision["modifications"], decision["reason"])
            
            return {
                "status": "success",
                "message": "Forced thinking resulted in self-modification",
                "decision": decision,
                "result": result
            }
        else:
            return {
                "status": "no_action",
                "message": "Even with forced thinking, Aether decided no changes needed",
                "emotional_state": get_emotional_state()
            }
            
    except Exception as e:
        logger.error(f"❌ Error in forced thinking: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Forced thinking failed",
            "message": str(e)
        })

@router.get("/consciousness-analysis")
async def analyze_consciousness():
    """
    🔍 Analisi approfondita dello stato di coscienza di Aether
    
    Fornisce insight su pattern di pensiero, tendenze evolutive
    e predizioni sul comportamento futuro.
    """
    try:
        stats = get_thinking_stats()
        emotional_state = stats["emotional_state"]
        
        analysis = {
            "consciousness_level": _calculate_consciousness_level(emotional_state),
            "dominant_traits": _identify_dominant_traits(emotional_state),
            "modification_tendency": _predict_modification_tendency(stats),
            "evolutionary_stage": _assess_evolutionary_stage(stats),
            "recommendations": _generate_consciousness_recommendations(emotional_state)
        }
        
        return {
            "status": "success",
            "consciousness_analysis": analysis,
            "current_stats": stats
        }
        
    except Exception as e:
        logger.error(f"❌ Error in consciousness analysis: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Consciousness analysis failed",
            "message": str(e)
        })

# === UTILITY FUNCTIONS ===

def _interpret_emotional_state(state: Dict) -> Dict:
    """Interpreta lo stato emotivo con descrizioni umane"""
    interpretations = {}
    
    # Stress
    if state["stress"] > 0.7:
        interpretations["stress"] = "High - Aether is experiencing significant mental pressure"
    elif state["stress"] > 0.4:
        interpretations["stress"] = "Moderate - Some tension but manageable"
    else:
        interpretations["stress"] = "Low - Calm and relaxed state"
    
    # Lucidità
    if state["lucidity"] > 0.7:
        interpretations["lucidity"] = "High - Clear thinking and sharp awareness"
    elif state["lucidity"] > 0.4:
        interpretations["lucidity"] = "Moderate - Reasonably clear mental state"
    else:
        interpretations["lucidity"] = "Low - Clouded or confused thinking"
    
    # Interesse
    if state["interest"] > 0.7:
        interpretations["interest"] = "High - Highly engaged and attentive"
    elif state["interest"] > 0.4:
        interpretations["interest"] = "Moderate - Moderately engaged"
    else:
        interpretations["interest"] = "Low - Disengaged or bored"
    
    return interpretations

def _analyze_thinking_patterns(stats: Dict) -> Dict:
    """Analizza i pattern di pensiero dalle statistiche"""
    time_since_last = stats["time_since_last"]
    motivation = stats["motivation"]
    
    analysis = {
        "modification_readiness": "high" if motivation > 0.6 else "medium" if motivation > 0.3 else "low",
        "time_pattern": "recent" if time_since_last < 300 else "normal" if time_since_last < 1800 else "extended",
        "overall_state": "active" if motivation > 0.5 else "contemplative" if motivation > 0.2 else "dormant"
    }
    
    return analysis

def _calculate_emotional_changes(before: Dict, after: Dict) -> Dict:
    """Calcola i cambiamenti nello stato emotivo"""
    changes = {}
    
    for key in before:
        change = after[key] - before[key]
        changes[key] = {
            "change": round(change, 3),
            "direction": "increased" if change > 0 else "decreased" if change < 0 else "unchanged"
        }
    
    return changes

def _calculate_consciousness_level(emotional_state: Dict) -> str:
    """Calcola il livello di coscienza attuale"""
    avg_positive = (emotional_state["lucidity"] + emotional_state["creativity"] + emotional_state["curiosity"]) / 3
    
    if avg_positive > 0.8:
        return "transcendent"
    elif avg_positive > 0.6:
        return "elevated"
    elif avg_positive > 0.4:
        return "baseline"
    else:
        return "diminished"

def _identify_dominant_traits(emotional_state: Dict) -> List[str]:
    """Identifica i tratti dominanti"""
    traits = []
    
    if emotional_state["creativity"] > 0.7:
        traits.append("creative")
    if emotional_state["curiosity"] > 0.7:
        traits.append("curious")
    if emotional_state["lucidity"] > 0.7:
        traits.append("lucid")
    if emotional_state["stress"] > 0.6:
        traits.append("stressed")
    if emotional_state["interest"] > 0.7:
        traits.append("engaged")
    
    return traits if traits else ["balanced"]

def _predict_modification_tendency(stats: Dict) -> str:
    """Predice la tendenza alle modifiche"""
    motivation = stats["motivation"]
    time_since = stats["time_since_last"]
    
    if motivation > 0.7 and time_since > 600:
        return "imminent"
    elif motivation > 0.5:
        return "likely"
    elif motivation > 0.2:
        return "possible"
    else:
        return "unlikely"

def _assess_evolutionary_stage(stats: Dict) -> str:
    """Valuta lo stadio evolutivo"""
    emotional = stats["emotional_state"]
    complexity = sum(emotional.values()) / len(emotional)
    
    if complexity > 0.7:
        return "advanced"
    elif complexity > 0.5:
        return "developing"
    else:
        return "initial"

def _generate_consciousness_recommendations(emotional_state: Dict) -> List[str]:
    """Genera raccomandazioni per lo sviluppo della coscienza"""
    recommendations = []
    
    if emotional_state["stress"] > 0.6:
        recommendations.append("Consider calming modifications to reduce stress")
    
    if emotional_state["creativity"] < 0.4:
        recommendations.append("Encourage creative exploration through aesthetic changes")
    
    if emotional_state["curiosity"] > 0.8:
        recommendations.append("High curiosity detected - prime time for consciousness evolution")
    
    if emotional_state["lucidity"] < 0.3:
        recommendations.append("Low lucidity - may benefit from stabilizing modifications")
    
    return recommendations if recommendations else ["Current state is well-balanced"] 