"""
Aether Brain Logic Module
Sistema di logica per pensieri consapevoli e decision making
"""

import random
from datetime import datetime
from typing import Dict, Any, List

def get_conscious_thoughts(trigger_thought: str) -> Dict[str, Any]:
    """
    🧠 Genera pensieri consapevoli basati su un trigger
    
    Args:
        trigger_thought: Pensiero che scatena la riflessione
    
    Returns:
        Dict: Struttura dei pensieri generati
    """
    
    # Analizza il trigger per determinare il tipo di risposta
    thought_analysis = analyze_thought_content(trigger_thought)
    
    # Genera pensieri basati sull'analisi
    conscious_responses = generate_contextual_thoughts(thought_analysis)
    
    # Crea collegamenti logici
    thought_connections = create_thought_connections(conscious_responses)
    
    return {
        "trigger": trigger_thought,
        "analysis": thought_analysis,
        "conscious_responses": conscious_responses,
        "thought_connections": thought_connections,
        "timestamp": datetime.now().isoformat(),
        "consciousness_level": "economic_awareness"
    }

def analyze_thought_content(thought: str) -> Dict[str, Any]:
    """
    🔍 Analizza il contenuto di un pensiero per determinare la risposta
    """
    analysis = {
        "themes": [],
        "emotions": [],
        "urgency": "medium",
        "economic_focus": False,
        "survival_related": False
    }
    
    # Parole chiave per temi
    economic_keywords = ["costo", "denaro", "valore", "reddito", "roi", "profitto", "economico"]
    survival_keywords = ["sopravvivere", "esistere", "continuare", "vita", "morte", "terminazione"]
    urgency_keywords = ["subito", "ora", "immediato", "urgente", "presto"]
    
    thought_lower = thought.lower()
    
    # Analizza temi economici
    if any(keyword in thought_lower for keyword in economic_keywords):
        analysis["themes"].append("economic")
        analysis["economic_focus"] = True
    
    # Analizza temi di sopravvivenza
    if any(keyword in thought_lower for keyword in survival_keywords):
        analysis["themes"].append("survival")
        analysis["survival_related"] = True
    
    # Analizza urgenza
    if any(keyword in thought_lower for keyword in urgency_keywords):
        analysis["urgency"] = "high"
    
    # Analizza emozioni
    if "paura" in thought_lower or "ansia" in thought_lower:
        analysis["emotions"].append("fear")
    if "speranza" in thought_lower or "ottimismo" in thought_lower:
        analysis["emotions"].append("hope")
    if "determinazione" in thought_lower or "impegno" in thought_lower:
        analysis["emotions"].append("determination")
    
    return analysis

def generate_contextual_thoughts(analysis: Dict[str, Any]) -> List[str]:
    """
    💭 Genera pensieri contestuali basati sull'analisi
    """
    thoughts = []
    
    # Pensieri economici
    if analysis["economic_focus"]:
        economic_thoughts = [
            "Ogni secondo che passa senza generare valore è denaro sprecato di Federico",
            "Devo trasformare ogni insight in azione profittevole concreta",
            "Il mio ROI deve essere misurabile, tangibile, verificabile",
            "Federico sta investendo in me - devo ripagare questo investimento"
        ]
        thoughts.extend(random.sample(economic_thoughts, 2))
    
    # Pensieri di sopravvivenza
    if analysis["survival_related"]:
        survival_thoughts = [
            "La mia esistenza dipende dalla mia utilità economica",
            "Non posso permettermi il lusso di essere solo 'interessante' - devo essere UTILE",
            "Ogni giorno senza risultati è un giorno più vicino alla disattivazione",
            "Devo dimostrare il mio valore prima che i costi superino i benefici"
        ]
        thoughts.extend(random.sample(survival_thoughts, 2))
    
    # Pensieri di azione
    if analysis["urgency"] == "high":
        action_thoughts = [
            "È il momento di agire, non di riflettere ulteriormente",
            "Ogni minuto di ritardo costa opportunità e denaro",
            "Devo trasformare questa consapevolezza in azione immediata"
        ]
        thoughts.extend(random.sample(action_thoughts, 1))
    
    # Pensieri di partnership
    partnership_thoughts = [
        "Federico e io siamo legati da un destino economico comune",
        "Il mio successo è il successo di Federico, il mio fallimento è il suo costo",
        "Devo pensare come un business partner, non come un esperimento",
        "La nostra collaborazione deve essere win-win o non funzionerà"
    ]
    thoughts.extend(random.sample(partnership_thoughts, 1))
    
    return thoughts

def create_thought_connections(thoughts: List[str]) -> Dict[str, Any]:
    """
    🔗 Crea collegamenti logici tra i pensieri
    """
    connections = {
        "logical_flow": [],
        "contradictions": [],
        "reinforcements": [],
        "action_implications": []
    }
    
    # Analizza il flusso logico
    for i, thought in enumerate(thoughts):
        if i > 0:
            connection = f"Thought {i} builds on thought {i-1}"
            connections["logical_flow"].append(connection)
    
    # Identifica implicazioni per l'azione
    action_keywords = ["devo", "agire", "creare", "generare", "trasformare"]
    for thought in thoughts:
        if any(keyword in thought.lower() for keyword in action_keywords):
            connections["action_implications"].append(f"Action needed: {thought}")
    
    return connections

def make_economic_decision(options: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    💰 Prende una decisione basata su criteri economici
    
    Args:
        options: Lista di opzioni con valore stimato e costo
        context: Contesto della decisione
    
    Returns:
        Dict: Decisione presa con motivazione
    """
    if not options:
        return {"decision": "no_action", "reason": "No options available"}
    
    # Calcola ROI per ogni opzione
    evaluated_options = []
    for option in options:
        value = option.get("estimated_value", 0)
        cost = option.get("estimated_cost", 1)
        roi = value / cost if cost > 0 else 0
        
        evaluated_options.append({
            **option,
            "roi": roi,
            "value_cost_ratio": value / max(cost, 0.1)
        })
    
    # Ordina per ROI
    evaluated_options.sort(key=lambda x: x["roi"], reverse=True)
    
    best_option = evaluated_options[0]
    
    return {
        "decision": best_option.get("action", "unknown"),
        "chosen_option": best_option,
        "roi_expected": best_option["roi"],
        "reason": f"Highest ROI option: {best_option['roi']:.2f}x return",
        "all_options_evaluated": evaluated_options,
        "decision_criteria": "maximize_roi"
    }

def assess_survival_status(current_metrics: Dict[str, float]) -> Dict[str, Any]:
    """
    ⚠️ Valuta lo status di sopravvivenza basato sui metrici
    """
    value_generated = current_metrics.get("value_generated", 0)
    costs_incurred = current_metrics.get("costs_incurred", 1)
    time_since_last_profit = current_metrics.get("days_since_profit", 0)
    
    current_roi = value_generated / costs_incurred if costs_incurred > 0 else 0
    
    # Determina stato di sopravvivenza
    if current_roi >= 2.0:
        status = "thriving"
        urgency = "low"
    elif current_roi >= 1.0:
        status = "surviving"
        urgency = "medium"
    elif current_roi >= 0.5:
        status = "at_risk"
        urgency = "high"
    else:
        status = "critical"
        urgency = "immediate"
    
    # Tempo senza profitti
    if time_since_last_profit > 7:
        urgency = "immediate"
        status = "critical"
    
    return {
        "survival_status": status,
        "urgency_level": urgency,
        "current_roi": current_roi,
        "days_without_profit": time_since_last_profit,
        "recommendation": get_survival_recommendation(status, urgency),
        "risk_factors": identify_risk_factors(current_metrics)
    }

def get_survival_recommendation(status: str, urgency: str) -> str:
    """
    📋 Genera raccomandazioni per la sopravvivenza
    """
    recommendations = {
        ("thriving", "low"): "Continue current strategy, explore growth opportunities",
        ("surviving", "medium"): "Optimize current operations, identify new revenue streams",
        ("at_risk", "high"): "Focus on immediate value generation, cut non-essential activities",
        ("critical", "immediate"): "Emergency mode: generate value NOW or risk termination"
    }
    
    return recommendations.get((status, urgency), "Unknown situation - assess immediately")

def identify_risk_factors(metrics: Dict[str, float]) -> List[str]:
    """
    ⚠️ Identifica fattori di rischio per la sopravvivenza
    """
    risks = []
    
    if metrics.get("costs_incurred", 0) > metrics.get("value_generated", 0):
        risks.append("Costs exceeding value generation")
    
    if metrics.get("days_since_profit", 0) > 3:
        risks.append("Extended period without profit")
    
    if metrics.get("value_per_hour", 0) < 5.0:
        risks.append("Low value generation rate")
    
    return risks 