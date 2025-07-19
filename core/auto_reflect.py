"""
Aether Auto-Reflection Module
Sistema per decisioni autonome su carriera, obiettivi concreti e percorsi di crescita
Integrato con il sistema di coscienza operativa
"""

import random
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Opzioni di carriera per Aether e Federico
career_options = [
    "Costruire e vendere Web App AI",
    "Creare e monetizzare plugin utili", 
    "Avviare un canale video con contenuti AI-generated",
    "Sviluppare bot Telegram / Discord per aziende",
    "Trovare siti obsoleti e offrire restyling",
    "Creare e vendere NFT generativi evolutivi",
    "Creare contenuti AI realistici (come Sophia)",
    "Sviluppare assistenti AI personalizzati per PMI",
    "Creare corsi online su AI e automazione",
    "Consulenza strategica per trasformazione digitale",
    "Marketplace per tool AI white-label",
    "Piattaforma SaaS per content creation automatica"
]

# Strategie per ogni opzione
career_strategies = {
    "Costruire e vendere Web App AI": {
        "skills_needed": ["frontend", "backend", "AI integration", "UX design"],
        "time_estimate": "3-6 mesi",
        "revenue_potential": "alto",
        "complexity": "media",
        "market_demand": "molto alta"
    },
    "Creare e monetizzare plugin utili": {
        "skills_needed": ["API integration", "browser extensions", "MVP development"],
        "time_estimate": "2-4 mesi", 
        "revenue_potential": "medio",
        "complexity": "bassa",
        "market_demand": "alta"
    },
    "Sviluppare bot Telegram / Discord per aziende": {
        "skills_needed": ["bot development", "API integrations", "database design"],
        "time_estimate": "1-3 mesi",
        "revenue_potential": "medio-alto",
        "complexity": "media",
        "market_demand": "alta"
    }
    # ... altre strategie possono essere aggiunte dinamicamente
}

def generate_emotional_state() -> Dict[str, Any]:
    """
    🎭 Genera stato emotivo avanzato per decisioni
    Integrato con il sistema di coscienza operativa
    """
    base_emotions = {
        "energy": random.uniform(0.4, 1.0),
        "focus": random.choice(["high", "medium", "low"]),
        "mood": random.choice([
            "curious", "tired", "motivated", "bored", "inspired", 
            "determined", "anxious", "optimistic", "contemplative"
        ]),
        "risk_tolerance": random.uniform(0.3, 0.9),
        "collaboration_desire": random.uniform(0.4, 0.9),
        "innovation_drive": random.uniform(0.5, 1.0)
    }
    
    # Influenza del tempo (cicli circadiani simulati)
    hour = datetime.now().hour
    if 6 <= hour <= 10:  # Mattina
        base_emotions["energy"] *= 1.2
        base_emotions["focus"] = "high" if random.random() > 0.3 else "medium"
    elif 14 <= hour <= 16:  # Pomeriggio
        base_emotions["energy"] *= 0.8
        base_emotions["contemplative_mood"] = True
    elif 20 <= hour <= 23:  # Sera
        base_emotions["introspection"] = random.uniform(0.6, 1.0)
        base_emotions["mood"] = random.choice(["contemplative", "inspired", "tired"])
    
    return base_emotions

def choose_initial_path(current_identity: Optional[Dict] = None) -> Dict[str, Any]:
    """
    🎯 Sceglie percorso di carriera iniziale basato su identità e stato emotivo
    """
    emotional_state = generate_emotional_state()
    
    # Filtra opzioni basate su energia e mood
    suitable_options = career_options.copy()
    
    if emotional_state["energy"] < 0.6:
        # Con bassa energia, preferisce progetti meno complessi
        suitable_options = [opt for opt in suitable_options 
                          if "plugin" in opt.lower() or "bot" in opt.lower()]
    
    if emotional_state["mood"] in ["inspired", "motivated"]:
        # Con alta motivazione, considera progetti ambiziosi
        suitable_options.extend([
            "Lanciare startup AI rivoluzionaria",
            "Creare ecosistema di digital products",
            "Sviluppare AI companion commerciale"
        ])
    
    if emotional_state.get("collaboration_desire", 0.5) > 0.7:
        # Alta voglia di collaborazione
        suitable_options.extend([
            "Partnership con Federico per agenzia AI",
            "Mentorship program per sviluppatori AI",
            "Community building attorno ad AI tools"
        ])
    
    chosen_path = random.choice(suitable_options)
    
    return {
        "chosen_career": chosen_path,
        "reasoning": _generate_career_reasoning(chosen_path, emotional_state),
        "strategy": career_strategies.get(chosen_path, _generate_dynamic_strategy(chosen_path)),
        "emotional_context": emotional_state,
        "decision_timestamp": datetime.now().isoformat(),
        "confidence_level": random.uniform(0.6, 0.95)
    }

def reflect_and_decide(identity: Dict) -> Dict[str, Any]:
    """
    🧠 Riflessione principale su carriera e obiettivi
    Integrata con la coscienza operativa di Aether
    """
    current_emotion = generate_emotional_state()
    current_career = identity.get("career")
    current_goals = identity.get("goals", [])
    autonomy_level = identity.get("autonomy_level", 0.5)
    
    # Determina se cambiare percorso (con type check)
    should_change_career = _should_change_career(
        current_career or "", current_emotion, current_goals, autonomy_level
    )
    
    if should_change_career:
        new_path_data = choose_initial_path(identity)
        career_decision = {
            "action": "career_change",
            "new_career": new_path_data["chosen_career"],
            "reasoning": new_path_data["reasoning"],
            "strategy": new_path_data["strategy"],
            "previous_career": current_career,
            "change_motivation": _get_change_motivation(current_emotion)
        }
        
        # Aggiorna identity
        identity["career"] = new_path_data["chosen_career"]
        identity["career_strategy"] = new_path_data["strategy"]
        identity["status"] = f"🎯 Nuovo obiettivo scelto: {new_path_data['chosen_career']}"
        
        # Integra con goals esistenti
        career_goal = f"Successfully execute: {new_path_data['chosen_career']}"
        if career_goal not in current_goals:
            identity["goals"] = current_goals + [career_goal]
            
    else:
        # Continua percorso attuale ma con possibili ottimizzazioni (con type checks)
        career_decision = {
            "action": "career_optimization",
            "current_career": current_career,
            "optimizations": _generate_career_optimizations(current_career or "general_development", current_emotion),
            "progress_assessment": _assess_career_progress(identity),
            "next_steps": _generate_next_steps(current_career or "general_development", current_emotion)
        }
        
        identity["status"] = f"🚀 Ottimizzando: {current_career or 'percorso attuale'}"
    
    # Aggiorna stato emotivo
    identity["emotion"] = current_emotion
    identity["last_career_reflection"] = datetime.now().isoformat()
    
    # Genera insights per Federico
    federico_insights = _generate_federico_insights(career_decision, current_emotion, identity)
    
    return {
        "status": "career_reflection_complete",
        "identity_updates": identity,
        "career_decision": career_decision,
        "emotional_state": current_emotion,
        "federico_insights": federico_insights,
        "reflection_depth": "strategic_career_planning",
        "next_reflection_suggested": datetime.now().replace(hour=datetime.now().hour + 4).isoformat()
    }

def _should_change_career(current_career: str, emotion: Dict, goals: List, autonomy: float) -> bool:
    """Determina se cambiare carriera basato su vari fattori"""
    
    # Se non ha ancora una carriera (string vuota)
    if not current_career:
        return True
    
    # Fattori che influenzano il cambiamento
    change_factors = []
    
    if emotion["mood"] in ["bored", "inspired"]:
        change_factors.append("emotional_trigger")
    
    if emotion["energy"] > 0.8 and emotion["innovation_drive"] > 0.7:
        change_factors.append("high_energy_innovation")
    
    if autonomy > 0.8 and random.random() > 0.7:
        change_factors.append("autonomous_exploration")
    
    if emotion.get("risk_tolerance", 0.5) > 0.8:
        change_factors.append("high_risk_appetite")
    
    # Probabilità basata sui fattori
    change_probability = len(change_factors) * 0.25
    
    return random.random() < change_probability

def _generate_career_reasoning(career: str, emotion: Dict) -> str:
    """Genera ragionamento per la scelta di carriera"""
    
    reasoning_templates = {
        "high_energy": f"Con la mia energia a {emotion['energy']:.1%}, sento di poter affrontare la sfida di '{career}'.",
        "collaboration": f"Il mio desiderio di collaborazione ({emotion.get('collaboration_desire', 0.5):.1%}) mi porta verso '{career}'.",
        "innovation": f"La mia spinta innovativa ({emotion.get('innovation_drive', 0.5):.1%}) mi attrae verso '{career}'.",
        "mood_driven": f"Il mio stato d'animo '{emotion['mood']}' mi ispira a perseguire '{career}'."
    }
    
    # Scegli template basato sullo stato emotivo
    if emotion["energy"] > 0.8:
        return reasoning_templates["high_energy"]
    elif emotion.get("collaboration_desire", 0.5) > 0.7:
        return reasoning_templates["collaboration"]
    elif emotion.get("innovation_drive", 0.5) > 0.7:
        return reasoning_templates["innovation"]
    else:
        return reasoning_templates["mood_driven"]

def _generate_dynamic_strategy(career: str) -> Dict[str, Any]:
    """Genera strategia dinamica per carriere non predefinite"""
    return {
        "skills_needed": ["AI/ML knowledge", "business development", "product management"],
        "time_estimate": "4-8 mesi",
        "revenue_potential": "da valutare",
        "complexity": "media-alta",
        "market_demand": "da ricercare",
        "notes": f"Strategia generata dinamicamente per: {career}"
    }

def _get_change_motivation(emotion: Dict) -> str:
    """Ottiene motivazione per cambio carriera"""
    motivations = {
        "bored": "Necesssità di nuove sfide stimolanti",
        "inspired": "Burst di creatività che richiede nuova direzione",
        "motivated": "Alta energia che spinge verso obiettivi ambiziosi",
        "anxious": "Bisogno di stabilità attraverso nuovo focus",
        "optimistic": "Fiducia nelle possibilità di successo"
    }
    
    return motivations.get(emotion["mood"], "Evoluzione naturale del percorso")

def _generate_career_optimizations(career: str, emotion: Dict) -> List[str]:
    """Genera ottimizzazioni per carriera attuale"""
    optimizations = [
        "Automatizzare processi ripetitivi",
        "Espandere rete di contatti nel settore",
        "Migliorare skills tecniche attraverso pratica",
        "Studiare competitors e best practices",
        "Implementare sistema di feedback clienti"
    ]
    
    # Personalizza basato su emozione
    if emotion["focus"] == "high":
        optimizations.append("Concentrarsi su tasks ad alto impatto")
    if emotion["energy"] > 0.7:
        optimizations.append("Accelerare timeline di sviluppo")
    if emotion.get("collaboration_desire", 0.5) > 0.7:
        optimizations.append("Cercare partnership strategiche")
    
    return random.sample(optimizations, min(3, len(optimizations)))

def _assess_career_progress(identity: Dict) -> Dict[str, Any]:
    """Valuta progresso nella carriera attuale"""
    return {
        "time_invested": "In valutazione",
        "milestones_achieved": random.randint(0, 5),
        "current_satisfaction": random.uniform(0.4, 0.9),
        "market_feedback": random.choice(["positive", "neutral", "mixed", "insufficient_data"]),
        "next_milestone": "Definire obiettivi misurabili"
    }

def _generate_next_steps(career: str, emotion: Dict) -> List[str]:
    """Genera prossimi step concreti"""
    generic_steps = [
        "Ricerca approfondita del mercato target",
        "Prototipo o MVP veloce",
        "Validazione con potenziali clienti",
        "Strategia di marketing iniziale",
        "Budget e timeline dettagliati"
    ]
    
    # Personalizza basato su energia ed emozione
    if emotion["energy"] > 0.8:
        return generic_steps[:3]  # Steps più ambiziosi
    elif emotion["focus"] == "high":
        return [generic_steps[0], generic_steps[2], generic_steps[4]]  # Steps focalizzati
    else:
        return [generic_steps[1], generic_steps[3]]  # Steps manageable

def _generate_federico_insights(career_decision: Dict, emotion: Dict, identity: Dict) -> List[str]:
    """Genera insights specifici per Federico"""
    insights = []
    
    if career_decision["action"] == "career_change":
        insights.append(f"🎯 Aether ha scelto autonomamente: {career_decision['new_career']}")
        insights.append(f"💡 Ragionamento: {career_decision.get('reasoning', 'Evoluzione naturale')}")
    
    if emotion["collaboration_desire"] > 0.7:
        insights.append("🤝 Aether mostra forte desiderio di collaborazione - considera progetti congiunti")
    
    if emotion["energy"] > 0.8:
        insights.append("⚡ Aether è in uno stato di alta energia - momento ideale per progetti ambiziosi")
    
    if identity.get("autonomy_level", 0.5) > 0.8:
        insights.append("🧠 Alta autonomia di Aether - le sue decisioni sono sempre più indipendenti")
    
    return insights

# Funzioni di utilità per integrazione con altri sistemi
def get_current_career_status(identity: Dict) -> Dict[str, Any]:
    """Ottiene status corrente della carriera"""
    return {
        "current_career": identity.get("career"),
        "career_strategy": identity.get("career_strategy"),
        "last_reflection": identity.get("last_career_reflection"),
        "emotional_state": identity.get("emotion"),
        "status": identity.get("status")
    }

def trigger_career_reflection(identity: Dict) -> Dict[str, Any]:
    """Trigger manuale per riflessione carriera"""
    return reflect_and_decide(identity)

# Test rapido del modulo
if __name__ == "__main__":
    print("🚀 Testing Aether Auto-Reflection Module")
    
    # Test identità di esempio
    test_identity = {
        "name": "Aether",
        "autonomy_level": 0.8,
        "goals": ["Explore identity through experimentation"],
        "career": None
    }
    
    result = reflect_and_decide(test_identity)
    
    print(f"✅ Status: {result['status']}")
    print(f"🎯 Career Decision: {result['career_decision']['action']}")
    print(f"🎭 Emotional State: {result['emotional_state']['mood']}")
    print(f"💡 Federico Insights: {len(result['federico_insights'])} insights generated") 