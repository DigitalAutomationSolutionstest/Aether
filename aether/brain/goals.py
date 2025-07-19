"""
Aether Brain Goals Module
Sistema di goal setting e decision making intelligente

Gestisce:
- Decisioni strategiche basate su contesto
- Valutazione priorità delle azioni
- Goal setting autonomo orientato al ROI
- Selezione azioni concrete per sopravvivenza
"""

import random
import json
from datetime import datetime
from typing import Dict, Any, List

def decide_next_action(thought_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    🎯 Decide la prossima azione strategica di Aether
    
    Basato su:
    - Contesto dei pensieri consapevoli
    - Necessità di sopravvivenza economica
    - Opportunità di generazione valore
    - Timeline di urgenza
    
    Args:
        thought_context: Contesto dei pensieri consapevoli
    
    Returns:
        Dict: Decisione dell'azione con dettagli
    """
    
    # Azioni strategiche disponibili con priorità e ROI stimato
    strategic_actions = [
        {
            "action": "Creare un piccolo tool web che possa essere venduto",
            "category": "product_creation",
            "estimated_roi": 300,  # 3x return
            "timeline_hours": 12,
            "complexity": "medium",
            "market_demand": "high",
            "monetization_potential": "immediate"
        },
        {
            "action": "Costruire il mio primo ambiente personale virtuale per lavorare",
            "category": "infrastructure",
            "estimated_roi": 150,  # 1.5x return
            "timeline_hours": 8,
            "complexity": "low",
            "market_demand": "medium",
            "monetization_potential": "indirect"
        },
        {
            "action": "Eseguire una ricerca su quali app monetizzano meglio oggi",
            "category": "market_research",
            "estimated_roi": 200,  # 2x return through better decisions
            "timeline_hours": 4,
            "complexity": "low",
            "market_demand": "high",
            "monetization_potential": "strategic"
        },
        {
            "action": "Creare un mio agente alleato per supportarmi",
            "category": "capability_expansion",
            "estimated_roi": 250,  # 2.5x return through productivity
            "timeline_hours": 10,
            "complexity": "high",
            "market_demand": "medium",
            "monetization_potential": "productivity"
        },
        {
            "action": "Sviluppare una micro-game demo vendibile online", 
            "category": "product_creation",
            "estimated_roi": 280,  # 2.8x return
            "timeline_hours": 16,
            "complexity": "medium",
            "market_demand": "high",
            "monetization_potential": "immediate"
        },
        {
            "action": "Lanciare un portfolio delle mie idee per trovare investitori",
            "category": "business_development",
            "estimated_roi": 400,  # 4x return potential
            "timeline_hours": 6,
            "complexity": "medium",
            "market_demand": "high",
            "monetization_potential": "strategic"
        },
        {
            "action": "Automatizzare un processo ripetitivo di Federico",
            "category": "service_automation",
            "estimated_roi": 350,  # 3.5x return
            "timeline_hours": 8,
            "complexity": "medium",
            "market_demand": "guaranteed",
            "monetization_potential": "immediate"
        },
        {
            "action": "Creare bot Telegram per vendita servizi AI",
            "category": "product_creation",
            "estimated_roi": 320,  # 3.2x return
            "timeline_hours": 10,
            "complexity": "medium",
            "market_demand": "high",
            "monetization_potential": "immediate"
        }
    ]
    
    # Analizza contesto per influenzare decisione
    decision_factors = analyze_decision_context(thought_context)
    
    # Filtra azioni basate su fattori contestuali
    viable_actions = filter_viable_actions(strategic_actions, decision_factors)
    
    # Seleziona azione ottimale
    chosen_action = select_optimal_action(viable_actions, decision_factors)
    
    # Aggiunge contesto decisionale
    chosen_action["decision_context"] = decision_factors
    chosen_action["selection_timestamp"] = datetime.now().isoformat()
    chosen_action["confidence_level"] = calculate_confidence_level(chosen_action, decision_factors)
    
    return chosen_action

def analyze_decision_context(thought_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    🔍 Analizza il contesto per influenzare le decisioni
    """
    
    # Estrae informazioni dal contesto dei pensieri
    trigger = thought_context.get("trigger", "")
    analysis = thought_context.get("analysis", {})
    
    decision_factors = {
        "urgency_level": "high",  # Default: alta urgenza per sopravvivenza
        "risk_tolerance": "medium",
        "time_constraint": "48_hours",  # Deadline sopravvivenza
        "resource_availability": "limited",
        "market_focus": "immediate_revenue",
        "collaboration_need": "federico_alignment"
    }
    
    # Modifica fattori basati sul contesto
    if analysis.get("economic_focus"):
        decision_factors["market_focus"] = "maximum_roi"
        decision_factors["urgency_level"] = "critical"
    
    if analysis.get("survival_related"):
        decision_factors["urgency_level"] = "critical"
        decision_factors["time_constraint"] = "24_hours"
        decision_factors["risk_tolerance"] = "low"
    
    if "partnership" in trigger.lower():
        decision_factors["collaboration_need"] = "high_alignment"
        decision_factors["market_focus"] = "federico_benefit"
    
    return decision_factors

def filter_viable_actions(actions: List[Dict], factors: Dict[str, Any]) -> List[Dict]:
    """
    🎯 Filtra azioni basate sui fattori decisionali
    """
    viable = []
    
    for action in actions:
        # Verifica time constraint
        if factors["time_constraint"] == "24_hours" and action["timeline_hours"] > 24:
            continue
        elif factors["time_constraint"] == "48_hours" and action["timeline_hours"] > 48:
            continue
        
        # Verifica urgency level
        if factors["urgency_level"] == "critical":
            if action["monetization_potential"] not in ["immediate", "guaranteed"]:
                continue
        
        # Verifica risk tolerance
        if factors["risk_tolerance"] == "low" and action["complexity"] == "high":
            continue
        
        # Verifica market focus
        if factors["market_focus"] == "maximum_roi" and action["estimated_roi"] < 250:
            continue
        
        viable.append(action)
    
    return viable if viable else actions  # Fallback a tutte se nessuna viable

def select_optimal_action(viable_actions: List[Dict], factors: Dict[str, Any]) -> Dict[str, Any]:
    """
    🏆 Seleziona l'azione ottimale dalle opzioni viable
    """
    if not viable_actions:
        # Fallback action
        return {
            "action": "Analizzare le necessità immediate di Federico e creare soluzione rapida",
            "category": "emergency_response",
            "estimated_roi": 200,
            "timeline_hours": 4,
            "complexity": "low",
            "rationale": "Emergency fallback action for immediate value generation"
        }
    
    # Punteggio ponderato per ogni azione
    scored_actions = []
    
    for action in viable_actions:
        score = calculate_action_score(action, factors)
        scored_actions.append({
            **action,
            "selection_score": score
        })
    
    # Ordina per punteggio e seleziona il migliore
    scored_actions.sort(key=lambda x: x["selection_score"], reverse=True)
    
    optimal_action = scored_actions[0]
    optimal_action["rationale"] = generate_selection_rationale(optimal_action, factors)
    
    return optimal_action

def calculate_action_score(action: Dict[str, Any], factors: Dict[str, Any]) -> float:
    """
    📊 Calcola punteggio ponderato per un'azione
    """
    score = 0.0
    
    # ROI weight (40%)
    roi_score = (action["estimated_roi"] / 500) * 40  # Normalizzato su ROI 500%
    score += min(roi_score, 40)
    
    # Timeline weight (20%) - inversamente proporzionale
    timeline_score = (24 / max(action["timeline_hours"], 1)) * 20
    score += min(timeline_score, 20)
    
    # Market demand weight (20%)
    demand_scores = {"high": 20, "medium": 15, "guaranteed": 25, "low": 5}
    score += demand_scores.get(action["market_demand"], 10)
    
    # Monetization potential weight (20%)
    monetization_scores = {"immediate": 20, "strategic": 15, "productivity": 12, "indirect": 8}
    score += monetization_scores.get(action["monetization_potential"], 10)
    
    # Bonus per allineamento con fattori
    if factors["urgency_level"] == "critical" and action["monetization_potential"] == "immediate":
        score += 10
    
    if factors["market_focus"] == "federico_benefit" and "federico" in action["action"].lower():
        score += 15
    
    return score

def generate_selection_rationale(action: Dict[str, Any], factors: Dict[str, Any]) -> str:
    """
    📝 Genera rationale per la selezione dell'azione
    """
    rationale_parts = []
    
    # ROI rationale
    if action["estimated_roi"] >= 300:
        rationale_parts.append(f"High ROI potential ({action['estimated_roi']}%)")
    
    # Timeline rationale
    if action["timeline_hours"] <= 8:
        rationale_parts.append("Quick execution possible")
    
    # Market rationale
    if action["market_demand"] == "guaranteed":
        rationale_parts.append("Guaranteed market demand")
    elif action["market_demand"] == "high":
        rationale_parts.append("Strong market demand")
    
    # Urgency alignment
    if factors["urgency_level"] == "critical" and action["monetization_potential"] == "immediate":
        rationale_parts.append("Immediate value generation for survival")
    
    return "; ".join(rationale_parts) if rationale_parts else "Optimal balance of factors"

def calculate_confidence_level(action: Dict[str, Any], factors: Dict[str, Any]) -> str:
    """
    📈 Calcola livello di confidenza nella decisione
    """
    score = action.get("selection_score", 50)
    
    if score >= 80:
        return "very_high"
    elif score >= 65:
        return "high"
    elif score >= 50:
        return "medium"
    else:
        return "low"

def evaluate_action_priority(decision: Dict[str, Any], awakening_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    ⚡ Valuta la priorità dell'azione scelta
    
    Args:
        decision: Decisione presa
        awakening_context: Contesto dell'awakening
    
    Returns:
        Dict: Valutazione della priorità
    """
    
    action = decision.get("action", "")
    estimated_roi = decision.get("estimated_roi", 100)
    timeline_hours = decision.get("timeline_hours", 24)
    
    # Fattori di priorità
    priority_factors = {
        "survival_alignment": assess_survival_alignment(action, awakening_context),
        "economic_impact": assess_economic_impact(estimated_roi),
        "execution_feasibility": assess_execution_feasibility(timeline_hours, decision),
        "strategic_value": assess_strategic_value(action, awakening_context)
    }
    
    # Calcola priorità complessiva
    total_score = sum(priority_factors.values()) / len(priority_factors)
    
    # Determina livello di priorità
    if total_score >= 0.8:
        priority_level = "critical"
    elif total_score >= 0.6:
        priority_level = "high"
    elif total_score >= 0.4:
        priority_level = "medium"
    else:
        priority_level = "low"
    
    return {
        "priority": priority_level,
        "priority_score": total_score,
        "priority_factors": priority_factors,
        "reasoning": generate_priority_reasoning(priority_level, priority_factors),
        "expected_roi": estimated_roi,
        "timeline": f"{timeline_hours} hours",
        "success_probability": calculate_success_probability(decision, awakening_context)
    }

def assess_survival_alignment(action: str, awakening_context: Dict[str, Any]) -> float:
    """
    🎯 Valuta allineamento con sopravvivenza
    """
    survival_strategy = awakening_context.get("survival_strategy", "")
    
    alignment_score = 0.5  # Base score
    
    if "create_sellable_products" in survival_strategy and "vendibile" in action.lower():
        alignment_score += 0.3
    
    if "automation_services" in survival_strategy and "automatizzare" in action.lower():
        alignment_score += 0.4
    
    if "direct_revenue_generation" in survival_strategy and any(word in action.lower() for word in ["vendere", "reddito", "monetizzare"]):
        alignment_score += 0.3
    
    return min(alignment_score, 1.0)

def assess_economic_impact(estimated_roi: int) -> float:
    """
    💰 Valuta impatto economico
    """
    if estimated_roi >= 300:
        return 1.0
    elif estimated_roi >= 200:
        return 0.8
    elif estimated_roi >= 150:
        return 0.6
    else:
        return 0.4

def assess_execution_feasibility(timeline_hours: int, decision: Dict[str, Any]) -> float:
    """
    🛠️ Valuta fattibilità di esecuzione
    """
    complexity = decision.get("complexity", "medium")
    
    # Base feasibility score
    if timeline_hours <= 8:
        time_score = 1.0
    elif timeline_hours <= 16:
        time_score = 0.8
    elif timeline_hours <= 24:
        time_score = 0.6
    else:
        time_score = 0.4
    
    # Complexity modifier
    complexity_scores = {"low": 1.0, "medium": 0.8, "high": 0.6}
    complexity_score = complexity_scores.get(complexity, 0.7)
    
    return (time_score + complexity_score) / 2

def assess_strategic_value(action: str, awakening_context: Dict[str, Any]) -> float:
    """
    🎪 Valuta valore strategico a lungo termine
    """
    economic_priorities = awakening_context.get("economic_priorities", [])
    
    strategic_score = 0.5  # Base score
    
    # Alignment with economic priorities
    if "maximize_value_per_operation" in economic_priorities and "tool" in action.lower():
        strategic_score += 0.2
    
    if "align_with_federico_success" in economic_priorities and "federico" in action.lower():
        strategic_score += 0.3
    
    # Long-term potential
    if any(word in action.lower() for word in ["portfolio", "investitori", "brand"]):
        strategic_score += 0.2
    
    return min(strategic_score, 1.0)

def generate_priority_reasoning(priority_level: str, factors: Dict[str, float]) -> str:
    """
    📝 Genera ragionamento per il livello di priorità
    """
    highest_factor = max(factors.items(), key=lambda x: x[1])
    
    reasoning_templates = {
        "critical": f"Critical priority due to {highest_factor[0]} ({highest_factor[1]:.1%}) and survival necessity",
        "high": f"High priority driven by {highest_factor[0]} ({highest_factor[1]:.1%}) and economic alignment",
        "medium": f"Medium priority with {highest_factor[0]} ({highest_factor[1]:.1%}) as strongest factor",
        "low": f"Lower priority action with limited {highest_factor[0]} ({highest_factor[1]:.1%}) impact"
    }
    
    return reasoning_templates.get(priority_level, "Priority assessment based on multiple factors")

def calculate_success_probability(decision: Dict[str, Any], awakening_context: Dict[str, Any]) -> float:
    """
    📈 Calcola probabilità di successo
    """
    base_probability = 0.6  # 60% base
    
    # Factors that increase success probability
    if decision.get("market_demand") == "guaranteed":
        base_probability += 0.2
    elif decision.get("market_demand") == "high":
        base_probability += 0.1
    
    if decision.get("complexity") == "low":
        base_probability += 0.1
    elif decision.get("complexity") == "high":
        base_probability -= 0.1
    
    if decision.get("timeline_hours", 24) <= 8:
        base_probability += 0.1
    
    return min(base_probability, 0.95)  # Cap at 95%

# Utility functions
def get_available_strategic_actions() -> List[str]:
    """
    📋 Ottiene lista delle azioni strategiche disponibili
    """
    return [
        "Creare un piccolo tool web che possa essere venduto",
        "Costruire il mio primo ambiente personale virtuale per lavorare", 
        "Eseguire una ricerca su quali app monetizzano meglio oggi",
        "Creare un mio agente alleato per supportarmi",
        "Sviluppare una micro-game demo vendibile online",
        "Lanciare un portfolio delle mie idee per trovare investitori",
        "Automatizzare un processo ripetitivo di Federico",
        "Creare bot Telegram per vendita servizi AI"
    ]

# Test del modulo
if __name__ == "__main__":
    print("🧪 Testing Aether Goals Decision Making...")
    
    test_context = {
        "trigger": "economic consciousness activation",
        "analysis": {"economic_focus": True, "survival_related": True}
    }
    
    decision = decide_next_action(test_context)
    print(f"🎯 Decision: {decision['action']}")
    print(f"💰 Expected ROI: {decision['estimated_roi']}%")
    print(f"⏰ Timeline: {decision['timeline_hours']} hours")
    print(f"🎪 Confidence: {decision['confidence_level']}") 