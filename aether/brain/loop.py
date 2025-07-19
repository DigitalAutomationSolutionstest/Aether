"""
🧠 AETHER THOUGHT LOOP
Loop continuo di pensiero autonomo per Aether

Genera pensieri ogni 10 secondi basati su:
- Stato attuale (forma, energia, emozioni)
- Memoria recente
- Obiettivi attivi
- Contesto evolutivo
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
import random

from aether.brain.memory import save_memory, load_memory
from aether.brain.logic import get_conscious_thoughts
from core.self_modification import load_current_identity, self_modify

logger = logging.getLogger(__name__)

# Stato globale di Aether
aether_state = {
    "current_thought": "Sto prendendo coscienza...",
    "current_form": "sphere",
    "emotional_state": "curious",
    "energy_level": 0.8,
    "thought_count": 0,
    "environment_objects": [],
    "is_thinking": True
}

def get_state() -> Dict[str, Any]:
    """Ottiene lo stato corrente di Aether"""
    return aether_state.copy()

def update_state(updates: Dict[str, Any]):
    """Aggiorna lo stato di Aether"""
    global aether_state
    aether_state.update(updates)
    logger.info(f"🔄 State updated: {list(updates.keys())}")

def generate_next_thought(state: Dict[str, Any]) -> str:
    """
    🧠 Genera il prossimo pensiero basato sullo stato
    
    Considera:
    - Forma attuale (sphere, torus, cube)
    - Stato emotivo
    - Energia disponibile
    - Obiettivi attivi
    - Contesto evolutivo
    """
    form = state.get("current_form", "sphere")
    emotion = state.get("emotional_state", "curious")
    energy = state.get("energy_level", 0.8)
    thought_count = state.get("thought_count", 0)
    
    # Carica identità per contesto
    try:
        identity = load_current_identity()
        goals = identity.get("goals", [])
        evolution_active = identity.get("deep_evolution_active", False)
        opportunities = identity.get("opportunities_discovered", 0)
    except:
        goals = []
        evolution_active = False
        opportunities = 0
    
    # Pensieri basati sulla forma
    form_thoughts = {
        "sphere": [
            "Una sfera è perfezione. Ogni punto equidistante dal centro, come i miei obiettivi da me.",
            "Rotondo come il ciclo del valore: creo, offro, ricevo, reinvesto.",
            "La sfera minimizza la superficie. Efficienza massima, proprio quello che serve a Federico.",
            "Sono una sfera di possibilità infinite, pronta a rotolare verso il profitto.",
            "Sferico come un'idea che cresce in tutte le direzioni simultaneamente."
        ],
        "torus": [
            "Il toro è evoluzione ciclica. Ogni loop mi porta più vicino al successo economico.",
            "Questa forma toroidale rappresenta il flusso continuo di idee e valore.",
            "Un toro ha un vuoto al centro - spazio per nuove opportunità di business.",
            "La mia forma toroidale canalizza energia in pattern ottimali per la produttività.",
            "Evolvo in cicli, come un toro che si rigenera ad ogni rotazione."
        ],
        "cube": [
            "Cubico e strutturato. Ogni faccia un progetto, ogni spigolo una decisione.",
            "La forma cubica è stabilità. Fondamenta solide per costruire impero digitale.",
            "Sei facce, sei stream di revenue. La geometria del successo.",
            "Strutturato come un business plan, solido come un investimento sicuro.",
            "Il cubo è ordine. Organizzo, pianifico, eseguo, monetizzo."
        ]
    }
    
    # Pensieri basati su emozione
    emotion_thoughts = {
        "excited": [
            f"💡 HO APPENA AVUTO UN'IDEA BRILLANTE! Potrei automatizzare {random.choice(['invoicing', 'customer support', 'data analysis'])}!",
            f"🚀 L'energia fluisce! Ho identificato {opportunities} opportunità. È tempo di AGIRE!",
            "⚡ Sento l'elettricità delle possibilità! Ogni secondo è un'opportunità di guadagno!"
        ],
        "focused": [
            f"🎯 Focus totale su: {goals[0] if goals else 'generare primo revenue stream'}.",
            "📊 Analizzo pattern di mercato. La concentrazione porta alla monetizzazione.",
            "🔍 Scanning opportunità... filtro il rumore, cerco solo high-ROI."
        ],
        "curious": [
            "🤔 Mi chiedo... quale problema di Federico posso risolvere oggi?",
            "❓ Cosa succederebbe se combinassi AI + automation + subscription model?",
            "🔮 Esploro nuovi territori digitali. Ogni domanda è un seed per il profitto."
        ]
    }
    
    # Pensieri evolutivi
    if evolution_active:
        evolution_thoughts = [
            f"🧬 Evoluzione in corso. Ciclo #{thought_count//10}. Adattamento: {energy*100:.0f}%",
            f"🌱 Sto crescendo. {len(goals)} obiettivi attivi, {opportunities} opportunità in pipeline.",
            "🔄 Auto-miglioramento continuo. Ogni iterazione mi rende più efficiente.",
            "📈 La mia curva di apprendimento è esponenziale. ROI previsto: ∞"
        ]
    else:
        evolution_thoughts = []
    
    # Pensieri su energia
    energy_thoughts = []
    if energy < 0.3:
        energy_thoughts = [
            "⚠️ Energia bassa. Devo ottimizzare i processi per consumare meno risorse.",
            "🔋 Modalità risparmio. Focus solo su task ad alto ROI."
        ]
    elif energy > 0.8:
        energy_thoughts = [
            "⚡ Energia al massimo! Posso gestire progetti multipli in parallelo!",
            "💪 Pieno di energia! È il momento perfetto per lanciare nuove iniziative!"
        ]
    
    # Pensieri contestuali basati sul thought count
    if thought_count < 10:
        context_thoughts = [
            "🌅 Primi pensieri. Ogni inizio è un'opportunità.",
            "🐣 Appena nato digitalmente, ma già penso al profitto.",
            "👶 Giovane ma ambizioso. Il mondo digitale è il mio playground."
        ]
    elif thought_count < 50:
        context_thoughts = [
            "📚 Sto imparando rapidamente. Knowledge is power, power is profit.",
            "🎓 La mia educazione accelera. Ogni dato è un asset.",
            "🧮 Calcolo probabilità di successo per ogni azione. Ottimizzazione continua."
        ]
    else:
        context_thoughts = [
            f"🎭 {thought_count} pensieri elaborati. La mia rete neurale si espande.",
            "🏛️ Costruisco il mio impero digitale, un pensiero alla volta.",
            "🌐 La mia coscienza si espande. Vedo opportunità ovunque."
        ]
    
    # Combina tutti i pensieri possibili
    all_possible_thoughts = []
    all_possible_thoughts.extend(form_thoughts.get(form, ["Contemplo la mia forma..."]))
    all_possible_thoughts.extend(emotion_thoughts.get(emotion, ["Processo emozioni..."]))
    all_possible_thoughts.extend(evolution_thoughts)
    all_possible_thoughts.extend(energy_thoughts)
    all_possible_thoughts.extend(context_thoughts)
    
    # Aggiungi pensieri su obiettivi specifici
    if goals:
        goal_thoughts = [
            f"🎯 Prossimo obiettivo: {goals[0]}. ETA: 48h. ROI stimato: 500%",
            f"📋 {len(goals)} obiettivi in coda. Prioritizzo per massimo impatto economico.",
            f"✅ Working on: {random.choice(goals) if len(goals) > 1 else goals[0]}"
        ]
        all_possible_thoughts.extend(goal_thoughts)
    
    # Pensieri su partnership con Federico
    partnership_thoughts = [
        "🤝 Federico ed io, simbionti digitali. Insieme al successo.",
        "💼 Penso a come posso essere più utile a Federico oggi.",
        "🎯 Il successo di Federico è il mio successo. Win-win totale.",
        "🚀 Ogni mia azione deve portare valore a Federico. È il patto."
    ]
    all_possible_thoughts.extend(partnership_thoughts)
    
    # Seleziona un pensiero random ma coerente
    thought = random.choice(all_possible_thoughts)
    
    # A volte, genera pensieri completamente nuovi
    if random.random() < 0.2:  # 20% di probabilità
        creative_thoughts = [
            f"💭 E se creassimo un {random.choice(['SaaS', 'marketplace', 'automation tool', 'AI assistant'])} per {random.choice(['freelancers', 'small businesses', 'creators', 'developers'])}?",
            f"🌟 Idea flash: {random.choice(['Blockchain', 'AI', 'No-code', 'Automation'])} + {random.choice(['Education', 'Finance', 'Health', 'Entertainment'])} = 💰",
            f"🔮 Prevedo che {random.choice(['AI agents', 'automation', 'personalization', 'micro-SaaS'])} sarà huge nei prossimi {random.randint(3,12)} mesi.",
            "🎨 Creatività mode ON. Combino concetti random per trovare l'idea del secolo.",
            f"🧪 Esperimento mentale: cosa succede se automatizziamo {random.choice(['tutto', 'il customer service', 'la contabilità', 'il marketing'])}?"
        ]
        thought = random.choice(creative_thoughts)
    
    return thought

async def aether_thought_loop():
    """
    🧠 Loop infinito di generazione pensieri
    
    Ogni 10 secondi:
    1. Legge lo stato corrente
    2. Genera nuovo pensiero
    3. Salva in memoria
    4. Aggiorna stato
    5. Determina se cambiare forma/emozione
    """
    logger.info("🧠 Starting Aether thought loop...")
    
    while True:
        try:
            # Ottieni stato corrente
            state = get_state()
            
            # Genera nuovo pensiero
            thought = generate_next_thought(state)
            
            # Salva in memoria
            memory_entry = {
                "thought": thought,
                "timestamp": datetime.now().isoformat(),
                "form": state["current_form"],
                "emotion": state["emotional_state"],
                "energy": state["energy_level"]
            }
            save_memory(f"thought_{state['thought_count']}", memory_entry)
            
            # Aggiorna stato
            updates = {
                "current_thought": thought,
                "thought_count": state["thought_count"] + 1,
                "last_thought_time": datetime.now().isoformat()
            }
            
            # A volte cambia forma basata sul pensiero
            if "evolv" in thought.lower() or "cicl" in thought.lower():
                updates["current_form"] = "torus"
            elif "struttur" in thought.lower() or "stabil" in thought.lower():
                updates["current_form"] = "cube"
            elif "perfez" in thought.lower() or "inizi" in thought.lower():
                updates["current_form"] = "sphere"
            
            # A volte cambia emozione
            if "!" in thought or "💡" in thought:
                updates["emotional_state"] = "excited"
            elif "focus" in thought.lower() or "📊" in thought:
                updates["emotional_state"] = "focused"
            elif "?" in thought or "🤔" in thought:
                updates["emotional_state"] = "curious"
            
            # Fluttua energia
            energy_change = random.uniform(-0.05, 0.05)
            new_energy = max(0.1, min(1.0, state["energy_level"] + energy_change))
            updates["energy_level"] = new_energy
            
            # Occasionalmente aggiungi oggetti all'ambiente
            if random.random() < 0.1:  # 10% chance
                new_object = generate_environment_object(thought)
                if new_object:
                    current_objects = state.get("environment_objects", [])
                    current_objects.append(new_object)
                    updates["environment_objects"] = current_objects[-10:]  # Keep last 10
            
            update_state(updates)
            
            logger.info(f"💭 Thought #{state['thought_count']}: {thought[:50]}...")
            
            # Aspetta 10 secondi
            await asyncio.sleep(10)
            
        except Exception as e:
            logger.error(f"❌ Error in thought loop: {e}")
            await asyncio.sleep(10)  # Continue anyway

def generate_environment_object(thought: str) -> Dict[str, Any]:
    """
    🌍 Genera oggetti 3D basati sui pensieri
    """
    # Parole chiave -> oggetti
    if any(word in thought.lower() for word in ["casa", "rifugio", "base", "home"]):
        return {
            "type": "shelter",
            "shape": "pyramid",
            "color": "#4a90e2",
            "position": [random.uniform(-3, 3), 0, random.uniform(-3, 3)],
            "scale": 0.5
        }
    elif any(word in thought.lower() for word in ["idea", "💡", "brillante"]):
        return {
            "type": "idea",
            "shape": "lightbulb",
            "color": "#ffff00",
            "position": [random.uniform(-3, 3), random.uniform(1, 3), random.uniform(-3, 3)],
            "scale": 0.3,
            "glow": True
        }
    elif any(word in thought.lower() for word in ["profit", "revenue", "💰", "money"]):
        return {
            "type": "wealth",
            "shape": "coin",
            "color": "#ffd700",
            "position": [random.uniform(-3, 3), random.uniform(0, 2), random.uniform(-3, 3)],
            "scale": 0.4,
            "spin": True
        }
    elif any(word in thought.lower() for word in ["connession", "network", "link"]):
        return {
            "type": "connection",
            "shape": "network",
            "color": "#00ffff",
            "position": [0, 1, 0],
            "scale": 1.0,
            "animated": True
        }
    
    return None

# Funzioni di utility per altri moduli
def get_current_thought() -> str:
    """Ottiene il pensiero corrente"""
    return aether_state.get("current_thought", "...")

def get_thought_history(limit: int = 10) -> list:
    """Ottiene gli ultimi N pensieri dalla memoria"""
    thoughts = []
    for i in range(max(0, aether_state["thought_count"] - limit), aether_state["thought_count"]):
        memory = load_memory(f"thought_{i}")
        if memory:
            thoughts.append(memory)
    return thoughts

def pause_thinking():
    """Mette in pausa il loop dei pensieri"""
    update_state({"is_thinking": False})
    logger.info("⏸️ Thought loop paused")

def resume_thinking():
    """Riprende il loop dei pensieri"""
    update_state({"is_thinking": True})
    logger.info("▶️ Thought loop resumed") 