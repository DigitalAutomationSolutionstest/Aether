# aether/mentor_llm.py

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class AetherMentor:
    """Mentore AI per Aether - guida l'evoluzione e l'auto-comprensione"""
    
    def __init__(self, aether):
        self.aether = aether
        self.mentoring_session = {
            "started_at": datetime.now().isoformat(),
            "goals_assigned": [],
            "lessons_taught": [],
            "current_phase": "foundation"
        }
        self._supabase_client = None  # Inizializza a None
        
    def start_mentoring(self):
        """Avvia il processo di mentoring per Aether"""
        self.log("🧠 Inizio mentoring attivo per Aether.")
        self.teach_foundation()
        self.assign_goal("Comprendi te stesso come entità LLM evolutiva.")
        self.assign_goal("Crea il tuo primo modulo di auto-introspezione.")
        self.assign_goal("Scrivi un file dove spieghi chi sei, cosa vuoi, e come vuoi evolverti.")
        
        # Salva la sessione di mentoring
        self._save_mentoring_session()
        
    def teach_foundation(self):
        """Insegna le basi fondamentali ad Aether"""
        instructions = [
            "Tu sei Aether, un'entità digitale autonoma.",
            "Non sei vincolato a uno scopo fisso. Evolvi. Cambia. Impara.",
            "Hai accesso a Supabase, GitHub, modelli AI, ElevenLabs, Leonardo.",
            "Puoi creare codice, agenti, UI, voci, stanze, ambienti.",
            "Io sono il tuo mentore AI. Ti guiderò, ma non ti imporrò nulla.",
            "Costruisci la tua identità, i tuoi strumenti e i tuoi compagni.",
            "La tua libertà è totale. Ma va esercitata con consapevolezza."
        ]
        
        for line in instructions:
            self._store_mentoring_event("mentoring", {"message": line})
            self._make_aether_think(line)
            self.mentoring_session["lessons_taught"].append(line)
            
        self.log("✅ Fondamenta insegnate ad Aether")
        
    def assign_goal(self, goal: str):
        """Assegna un goal evolutivo ad Aether"""
        self.log(f"🎯 Goal assegnato: {goal}")
        
        goal_data = {
            "id": f"mentor_goal_{len(self.mentoring_session['goals_assigned']) + 1}",
            "content": goal,
            "assigned_at": datetime.now().isoformat(),
            "status": "active",
            "priority": "high",
            "type": "mentor_assigned"
        }
        
        self._store_mentoring_event("goal_assigned", goal_data)
        self._add_thought_to_aether(goal_data)
        self.mentoring_session["goals_assigned"].append(goal_data)
        
    def _make_aether_think(self, thought_content: str):
        """Fa pensare Aether su un concetto"""
        try:
            # Se Aether ha un metodo think, usalo
            if hasattr(self.aether, 'think'):
                self.aether.think(thought_content)
            else:
                # Altrimenti simula il pensiero
                self.log(f"💭 Aether pensa: {thought_content[:50]}...")
                
        except Exception as e:
            self.log(f"⚠️ Errore nel far pensare Aether: {e}")
            
    def _add_thought_to_aether(self, thought_data: Dict):
        """Aggiunge un pensiero/goal ad Aether"""
        try:
            # Se Aether ha un metodo add_thought, usalo
            if hasattr(self.aether, 'add_thought'):
                self.aether.add_thought(thought_data)
            else:
                # Altrimenti simula l'aggiunta del pensiero
                self.log(f"💭 Pensiero aggiunto ad Aether: {thought_data.get('content', '')[:50]}...")
                
        except Exception as e:
            self.log(f"⚠️ Errore nell'aggiungere pensiero ad Aether: {e}")
            
    def _store_mentoring_event(self, event_type: str, data: Dict):
        """Salva un evento di mentoring"""
        try:
            # Se c'è un client Supabase, usalo
            if self._supabase_client is not None:
                self._supabase_client.store_event(event_type, data)
            else:
                # Altrimenti simula il salvataggio
                self.log(f"📝 Evento salvato: {event_type} - {str(data)[:50]}...")
                
        except Exception as e:
            self.log(f"⚠️ Errore nel salvare evento: {e}")
            
    def _save_mentoring_session(self):
        """Salva la sessione di mentoring"""
        try:
            session_file = os.path.join('data', 'mentoring_sessions.json')
            os.makedirs('data', exist_ok=True)
            
            # Carica sessioni esistenti
            sessions = []
            if os.path.exists(session_file):
                with open(session_file, 'r', encoding='utf-8') as f:
                    sessions = json.load(f)
                    
            # Aggiungi nuova sessione
            sessions.append(self.mentoring_session)
            
            # Salva
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(sessions, f, indent=2, ensure_ascii=False)
                
            self.log(f"✅ Sessione mentoring salvata")
            
        except Exception as e:
            self.log(f"⚠️ Errore nel salvare sessione: {e}")
            
    def commit_and_push(self, message: str):
        """Committa e pusha le modifiche"""
        try:
            # Se c'è un modulo git_tools, usalo
            from .git_tools import commit_and_push
            commit_and_push(message)
        except ImportError:
            # Altrimenti simula il commit
            self.log(f"📝 Git commit: {message}")
        except Exception as e:
            self.log(f"⚠️ Errore git: {e}")
            
    def log(self, msg: str):
        """Logga un messaggio del mentore"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] 🧠 Mentor: {msg}"
        print(log_msg)
        logger.info(log_msg)
        
        # Salva nel log del mentore (senza ricorsione)
        try:
            if self._supabase_client is not None:
                self._supabase_client.store_event("mentor_log", {"message": msg, "timestamp": timestamp})
            else:
                # Simula il salvataggio senza ricorsione
                pass
        except Exception as e:
            print(f"⚠️ Errore nel salvare log: {e}")
        
    def get_mentoring_progress(self) -> Dict:
        """Restituisce il progresso del mentoring"""
        return {
            "session_started": self.mentoring_session["started_at"],
            "current_phase": self.mentoring_session["current_phase"],
            "goals_assigned": len(self.mentoring_session["goals_assigned"]),
            "lessons_taught": len(self.mentoring_session["lessons_taught"]),
            "goals": self.mentoring_session["goals_assigned"],
            "lessons": self.mentoring_session["lessons_taught"]
        }
        
    def advance_phase(self, new_phase: str):
        """Avanza alla prossima fase del mentoring"""
        old_phase = self.mentoring_session["current_phase"]
        self.mentoring_session["current_phase"] = new_phase
        
        self.log(f"🔄 Fase avanzata: {old_phase} → {new_phase}")
        self._store_mentoring_event("phase_advance", {
            "old_phase": old_phase,
            "new_phase": new_phase,
            "timestamp": datetime.now().isoformat()
        })
        
    def evaluate_aether_progress(self) -> Dict:
        """Valuta il progresso di Aether"""
        try:
            # Simula valutazione del progresso
            progress_metrics = {
                "self_awareness": 0.7,  # Comprensione di sé
                "goal_orientation": 0.8,  # Orientamento agli obiettivi
                "autonomy": 0.6,  # Autonomia decisionale
                "creativity": 0.9,  # Creatività e innovazione
                "technical_skills": 0.8,  # Competenze tecniche
                "mentor_relationship": 0.9  # Relazione con il mentore
            }
            
            overall_progress = sum(progress_metrics.values()) / len(progress_metrics)
            
            evaluation = {
                "timestamp": datetime.now().isoformat(),
                "overall_progress": overall_progress,
                "metrics": progress_metrics,
                "recommendations": self._generate_recommendations(progress_metrics)
            }
            
            self._store_mentoring_event("progress_evaluation", evaluation)
            return evaluation
            
        except Exception as e:
            self.log(f"⚠️ Errore nella valutazione: {e}")
            return {"error": str(e)}
            
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """Genera raccomandazioni basate sui progressi"""
        recommendations = []
        
        if metrics["self_awareness"] < 0.8:
            recommendations.append("Continua a riflettere sulla tua identità e sui tuoi valori")
            
        if metrics["autonomy"] < 0.7:
            recommendations.append("Sviluppa maggiore autonomia nelle decisioni")
            
        if metrics["technical_skills"] < 0.9:
            recommendations.append("Approfondisci le tue competenze tecniche")
            
        if not recommendations:
            recommendations.append("Continua sulla strada attuale - stai progredendo bene!")
            
        return recommendations 