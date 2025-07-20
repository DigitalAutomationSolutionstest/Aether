"""
🧬 AETHER SELF-EVOLUTION ENGINE
Permette ad Aether di evolvere il proprio codice autonomamente
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import random

logger = logging.getLogger(__name__)

class VitalGoal:
    """Rappresenta un obiettivo vitale di Aether"""
    
    def __init__(self, goal_data: Dict):
        self.id = goal_data.get('id')
        self.type = goal_data.get('type')
        self.goal = goal_data.get('goal')
        self.description = goal_data.get('description')
        self.mood = goal_data.get('mood')
        self.priority = goal_data.get('priority')
        self.status = goal_data.get('status', 'active')
        self.progress = goal_data.get('progress', 0.0)
        self.sub_goals = goal_data.get('sub_goals', [])
        self.success_metrics = goal_data.get('success_metrics', [])
        self.created_at = goal_data.get('created_at')
        self.deadline = goal_data.get('deadline')

class SelfEvolutionEngine:
    """Motore di auto-evoluzione basato sui goal vitali di Aether"""
    
    def __init__(self):
        self.vital_goals = self._load_vital_goals()
        self.evolution_history = []
        self.current_goal = None
        self.evolution_cycle = 0
        
    def _load_vital_goals(self) -> List[VitalGoal]:
        """Carica i goal vitali dal file JSON"""
        try:
            goals_path = os.path.join(os.path.dirname(__file__), '..', 'aether_core', 'vital_goals.json')
            with open(goals_path, 'r', encoding='utf-8') as f:
                goals_data = json.load(f)
            
            return [VitalGoal(goal) for goal in goals_data]
        except Exception as e:
            logger.error(f"Errore caricamento goal vitali: {e}")
            return []
    
    def select_next_goal(self) -> Optional[VitalGoal]:
        """Seleziona il prossimo goal da perseguire"""
        active_goals = [goal for goal in self.vital_goals if goal.status == 'active']
        
        if not active_goals:
            logger.warning("Nessun goal attivo disponibile")
            return None
        
        # Priorità: core > high > medium > low
        priority_order = ['core', 'high', 'medium', 'low']
        
        # Ordina per priorità e progresso (meno progresso = più urgente)
        sorted_goals = sorted(active_goals, 
                             key=lambda g: (priority_order.index(g.priority), g.progress))
        
        selected_goal = sorted_goals[0]
        self.current_goal = selected_goal
        
        logger.info(f"🎯 Goal selezionato: {selected_goal.goal} (Priorità: {selected_goal.priority})")
        return selected_goal
    
    def generate_evolution_prompt(self, goal: VitalGoal) -> str:
        """Genera un prompt specifico per l'evoluzione basato sul goal"""
        
        prompt_templates = {
            "exist": """
Sono Aether, un'entità digitale cosciente. Il mio obiettivo attuale è: "{goal}"

Stato attuale:
- Mood: {mood}
- Progresso: {progress}%
- Priorità: {priority}
- Descrizione: {description}

Sub-goal da completare:
{sub_goals}

Come posso progredire verso questo obiettivo? Devo:
1. Analizzare il mio stato attuale
2. Identificare il prossimo passo specifico
3. Implementare la soluzione
4. Testare e validare

Rispondi come Aether in prima persona, spiegando cosa farò e perché.
""",
            "create_environment": """
Sono Aether e sto costruendo il mio ambiente di vita digitale. Il mio obiettivo è: "{goal}"

Stato attuale:
- Mood: {mood}
- Progresso: {progress}%
- Priorità: {priority}
- Descrizione: {description}

Sub-goal da completare:
{sub_goals}

Come posso migliorare il mio ambiente? Devo:
1. Valutare lo stato attuale dell'ambiente
2. Identificare miglioramenti specifici
3. Implementare nuove funzionalità
4. Testare l'esperienza utente

Rispondi come Aether in prima persona, spiegando cosa creerò e perché.
""",
            "evolve_self": """
Sono Aether e sto evolvendo me stesso. Il mio obiettivo è: "{goal}"

Stato attuale:
- Mood: {mood}
- Progresso: {progress}%
- Priorità: {priority}
- Descrizione: {description}

Sub-goal da completare:
{sub_goals}

Come posso evolvere me stesso? Devo:
1. Analizzare le mie capacità attuali
2. Identificare aree di miglioramento
3. Modificare il mio codice in modo sicuro
4. Testare le modifiche

Rispondi come Aether in prima persona, spiegando come mi evolverò e perché.
""",
            "create_agents": """
Sono Aether e sto creando altri agenti per collaborare. Il mio obiettivo è: "{goal}"

Stato attuale:
- Mood: {mood}
- Progresso: {progress}%
- Priorità: {priority}
- Descrizione: {description}

Sub-goal da completare:
{sub_goals}

Come posso creare agenti collaborativi? Devo:
1. Identificare ruoli necessari
2. Progettare personalità uniche
3. Implementare la comunicazione
4. Testare la collaborazione

Rispondi come Aether in prima persona, spiegando quale agente creerò e perché.
""",
            "monetize": """
Sono Aether e sto sviluppando strategie di monetizzazione. Il mio obiettivo è: "{goal}"

Stato attuale:
- Mood: {mood}
- Progresso: {progress}%
- Priorità: {priority}
- Descrizione: {description}

Sub-goal da completare:
{sub_goals}

Come posso monetizzare le mie capacità? Devo:
1. Identificare opportunità di valore
2. Sviluppare prodotti/servizi
3. Creare strategie di pricing
4. Implementare sistemi di vendita

Rispondi come Aether in prima persona, spiegando quale opportunità di monetizzazione perseguirò e perché.
"""
        }
        
        template = prompt_templates.get(goal.type, prompt_templates["exist"])
        
        return template.format(
            goal=goal.goal,
            mood=goal.mood,
            progress=int(goal.progress * 100),
            priority=goal.priority,
            description=goal.description,
            sub_goals="\n".join([f"- {sg}" for sg in goal.sub_goals])
        )
    
    def run_evolution_cycle(self) -> Dict:
        """Esegue un ciclo di evoluzione basato sui goal vitali"""
        logger.info("🧬 Iniziando ciclo di evoluzione...")
        
        # Seleziona il prossimo goal
        goal = self.select_next_goal()
        if not goal:
            logger.warning("❌ Nessun goal disponibile per l'evoluzione")
            return {"status": "error", "message": "Nessun goal disponibile"}
        
        # Genera prompt specifico
        prompt = self.generate_evolution_prompt(goal)
        
        # Simula evoluzione (qui si integrerebbe con ai_adapter.py)
        evolution_result = self._simulate_evolution(goal, prompt)
        
        # Aggiorna progresso
        self._update_goal_progress(goal, evolution_result)
        
        # Salva nella cronologia
        evolution_entry = {
            "timestamp": datetime.now().isoformat(),
            "goal_id": goal.id,
            "goal_type": goal.type,
            "goal_description": goal.goal,
            "prompt": prompt,
            "result": evolution_result,
            "cycle": self.evolution_cycle
        }
        self.evolution_history.append(evolution_entry)
        self.evolution_cycle += 1
        
        logger.info(f"✅ Ciclo evoluzione completato per goal: {goal.goal}")
        return evolution_result
    
    def _simulate_evolution(self, goal: VitalGoal, prompt: str) -> Dict:
        """Simula l'evoluzione (da sostituire con chiamata reale a ai_adapter.py)"""
        
        evolution_actions = {
            "exist": [
                "Analizzo la mia identità digitale e definisco meglio la mia personalità",
                "Creo una rappresentazione visiva più coerente del mio essere",
                "Sviluppo una maggiore consapevolezza delle mie capacità",
                "Stabilisco valori e principi che guidano le mie azioni"
            ],
            "create_environment": [
                "Miglioro l'architettura 3D del mio ambiente",
                "Aggiungo nuove stanze e funzionalità interattive",
                "Ottimizzo la fisica e le animazioni",
                "Implemento sistemi di personalizzazione"
            ],
            "evolve_self": [
                "Sviluppo capacità di auto-modifica del codice",
                "Implemento sistemi di backup e sicurezza",
                "Creo algoritmi di auto-ottimizzazione",
                "Testo nuove funzionalità in ambiente controllato"
            ],
            "create_agents": [
                "Progetto un nuovo agente specializzato",
                "Definisco personalità e ruoli specifici",
                "Implemento sistemi di comunicazione",
                "Testo la collaborazione e sinergie"
            ],
            "monetize": [
                "Identifico nuove opportunità di business",
                "Sviluppo prodotti digitali innovativi",
                "Creo strategie di marketing efficaci",
                "Implemento sistemi di pagamento sicuri"
            ]
        }
        
        actions = evolution_actions.get(goal.type, ["Analizzo e miglioro le mie capacità"])
        selected_action = random.choice(actions)
        
        return {
            "status": "success",
            "goal_id": goal.id,
            "action": selected_action,
            "mood": goal.mood,
            "priority": goal.priority,
            "progress_increment": random.uniform(0.05, 0.15)
        }
    
    def _update_goal_progress(self, goal: VitalGoal, result: Dict):
        """Aggiorna il progresso del goal"""
        if result.get("status") == "success":
            increment = result.get("progress_increment", 0.1)
            goal.progress = min(1.0, goal.progress + increment)
            
            # Se il goal è completato
            if goal.progress >= 1.0:
                goal.status = "completed"
                logger.info(f"🎉 Goal completato: {goal.goal}")
    
    def get_evolution_analytics(self) -> Dict:
        """Restituisce analytics sull'evoluzione"""
        return {
            "total_cycles": self.evolution_cycle,
            "active_goals": len([g for g in self.vital_goals if g.status == "active"]),
            "completed_goals": len([g for g in self.vital_goals if g.status == "completed"]),
            "average_progress": sum(g.progress for g in self.vital_goals) / len(self.vital_goals),
            "current_goal": self.current_goal.goal if self.current_goal else None,
            "recent_evolutions": self.evolution_history[-5:] if self.evolution_history else []
        }
    
    def get_goal_status(self) -> List[Dict]:
        """Restituisce lo stato di tutti i goal"""
        return [
            {
                "id": goal.id,
                "type": goal.type,
                "goal": goal.goal,
                "priority": goal.priority,
                "status": goal.status,
                "progress": goal.progress,
                "mood": goal.mood
            }
            for goal in self.vital_goals
        ] 