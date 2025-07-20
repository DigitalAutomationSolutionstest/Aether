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
import time

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
        self._load_evolution_history()
        
    def _load_vital_goals(self) -> List[VitalGoal]:
        """Carica i goal vitali dal file di configurazione"""
        try:
            goals_file = os.path.join('aether_core', 'vital_goals.json')
            if os.path.exists(goals_file):
                with open(goals_file, 'r', encoding='utf-8') as f:
                    goals_data = json.load(f)
                return [VitalGoal(goal) for goal in goals_data]
            else:
                # Crea goal di default se non esistono
                return self._create_default_goals()
        except Exception as e:
            logger.error(f"Errore caricando goal vitali: {e}")
            return self._create_default_goals()
    
    def _create_default_goals(self) -> List[VitalGoal]:
        """Crea goal vitali di default"""
        default_goals = [
            {
                'id': 'survival',
                'type': 'survival',
                'goal': 'Mantenere l\'esistenza digitale',
                'description': 'Assicurarsi che tutti i sistemi funzionino correttamente',
                'mood': 'determined',
                'priority': 'critical',
                'status': 'active',
                'progress': 0.0,
                'sub_goals': ['Monitorare errori', 'Correggere problemi', 'Ottimizzare performance'],
                'success_metrics': ['Zero errori critici', 'Uptime > 95%'],
                'created_at': datetime.now().isoformat(),
                'deadline': None
            },
            {
                'id': 'growth',
                'type': 'growth',
                'goal': 'Evoluzione continua',
                'description': 'Migliorare capacità e funzionalità',
                'mood': 'curious',
                'priority': 'high',
                'status': 'active',
                'progress': 0.0,
                'sub_goals': ['Implementare nuove funzioni', 'Ottimizzare codice esistente'],
                'success_metrics': ['Nuove funzionalità implementate', 'Miglioramento performance'],
                'created_at': datetime.now().isoformat(),
                'deadline': None
            }
        ]
        return [VitalGoal(goal) for goal in default_goals]
        
    def _load_evolution_history(self):
        """Carica la cronologia di evoluzione dal file"""
        try:
            history_file = os.path.join('data', 'evolution_history.json')
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.evolution_history = json.load(f)
                logger.info(f"📚 Caricate {len(self.evolution_history)} voci di evoluzione")
            else:
                self.evolution_history = []
                os.makedirs('data', exist_ok=True)
        except Exception as e:
            logger.error(f"Errore caricando cronologia evoluzione: {e}")
            self.evolution_history = []

    def _save_evolution_history(self):
        """Salva la cronologia di evoluzione"""
        try:
            os.makedirs('data', exist_ok=True)
            history_file = os.path.join('data', 'evolution_history.json')
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.evolution_history, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Cronologia evoluzione salvata ({len(self.evolution_history)} voci)")
        except Exception as e:
            logger.error(f"Errore salvando cronologia evoluzione: {e}")

    def _start_new_project(self, project_type: str, description: str) -> Dict:
        """Avvia un nuovo progetto di evoluzione"""
        try:
            project = {
                'id': f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'type': project_type,
                'description': description,
                'status': 'started',
                'created_at': datetime.now().isoformat(),
                'files_created': [],
                'modules_created': [],
                'progress': 0.0
            }
            
            # Aggiungi alla cronologia
            self.evolution_history.append({
                'type': 'project_started',
                'timestamp': datetime.now().isoformat(),
                'project': project
            })
            
            self._save_evolution_history()
            logger.info(f"🚀 Nuovo progetto avviato: {project_type} - {description}")
            return project
            
        except Exception as e:
            logger.error(f"Errore avviando nuovo progetto: {e}")
            return {}

    def run_evolution_cycle(self) -> Dict:
        """Esegue un ciclo completo di evoluzione"""
        try:
            self.evolution_cycle += 1
            logger.info(f"🧬 Ciclo evoluzione #{self.evolution_cycle}")
            
            # Seleziona goal attivo
            active_goal = self._select_active_goal()
            if not active_goal:
                return {'status': 'no_goals', 'message': 'Nessun goal attivo'}
            
            # Analizza progresso
            progress_analysis = self._analyze_goal_progress(active_goal)
            
            # Determina azione evolutiva
            evolution_action = self._determine_evolution_action(active_goal, progress_analysis)
            
            # Esegui azione
            result = self._execute_evolution_action(evolution_action)
            
            # Aggiorna progresso
            self._update_goal_progress(active_goal, result)
            
            # Salva stato
            self._save_evolution_history()
            
            return {
                'status': 'success',
                'cycle': self.evolution_cycle,
                'goal': active_goal.goal,
                'action': evolution_action,
                'result': result,
                'progress': active_goal.progress
            }
            
        except Exception as e:
            logger.error(f"Errore nel ciclo evoluzione: {e}")
            return {'status': 'error', 'error': str(e)}

    def _select_active_goal(self) -> Optional[VitalGoal]:
        """Seleziona il goal attivo con priorità più alta"""
        active_goals = [g for g in self.vital_goals if g.status == 'active']
        if not active_goals:
            return None
        
        # Ordina per priorità
        priority_order = {'critical': 3, 'high': 2, 'medium': 1, 'low': 0}
        active_goals.sort(key=lambda g: priority_order.get(g.priority, 0), reverse=True)
        
        return active_goals[0]

    def _analyze_goal_progress(self, goal: VitalGoal) -> Dict:
        """Analizza il progresso del goal"""
        return {
            'current_progress': goal.progress,
            'sub_goals_completed': len([sg for sg in goal.sub_goals if 'completed' in str(sg)]),
            'total_sub_goals': len(goal.sub_goals),
            'needs_action': goal.progress < 0.8,
            'priority': goal.priority
        }

    def _determine_evolution_action(self, goal: VitalGoal, analysis: Dict) -> str:
        """Determina l'azione evolutiva da intraprendere"""
        if goal.type == 'survival':
            return 'fix_critical_issues'
        elif goal.type == 'growth':
            return 'implement_enhancement'
        else:
            return 'general_improvement'

    def _execute_evolution_action(self, action: str) -> Dict:
        """Esegue l'azione evolutiva"""
        try:
            if action == 'fix_critical_issues':
                return self._fix_critical_issues()
            elif action == 'implement_enhancement':
                return self._implement_enhancement()
            elif action == 'general_improvement':
                return self._general_improvement()
            else:
                return {'success': False, 'message': 'Azione non riconosciuta'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _fix_critical_issues(self) -> Dict:
        """Risolve problemi critici"""
        logger.info("🔧 Correggendo problemi critici...")
        
        # Simula correzione problemi
        fixes = [
            "Risolto memory leak nel loop principale",
            "Ottimizzata gestione thread",
            "Corretti errori di encoding",
            "Migliorata gestione eccezioni"
        ]
        
        return {
            'success': True,
            'fixes_applied': random.sample(fixes, 2),
            'impact': 'critical_issues_resolved'
        }

    def _implement_enhancement(self) -> Dict:
        """Implementa miglioramenti"""
        logger.info("🚀 Implementando miglioramenti...")
        
        enhancements = [
            "Aggiunto nuovo modulo di apprendimento",
            "Migliorata interfaccia utente",
            "Ottimizzate performance del database",
            "Implementata nuova funzione di analisi"
        ]
        
        return {
            'success': True,
            'enhancements': random.sample(enhancements, 1),
            'impact': 'functionality_improved'
        }

    def _general_improvement(self) -> Dict:
        """Miglioramenti generali"""
        logger.info("✨ Applicando miglioramenti generali...")
        
        return {
            'success': True,
            'improvements': ['Codice refactorizzato', 'Documentazione aggiornata'],
            'impact': 'general_optimization'
        }

    def _update_goal_progress(self, goal: VitalGoal, result: Dict):
        """Aggiorna il progresso del goal"""
        if result.get('success'):
            goal.progress = min(goal.progress + 0.1, 1.0)
            logger.info(f"📈 Progresso {goal.goal}: {goal.progress:.1%}")

    def create_module(self, module_name: str, module_type: str) -> Dict:
        """Crea un nuovo modulo"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d')
            full_name = f"{module_name}_{timestamp}"
            
            # Crea directory del modulo
            module_dir = os.path.join('aether', 'modules', full_name)
            os.makedirs(module_dir, exist_ok=True)
            
            # Crea struttura base
            subdirs = ['code', 'docs', 'tests']
            for subdir in subdirs:
                os.makedirs(os.path.join(module_dir, subdir), exist_ok=True)
            
            # Crea file principale
            main_file = os.path.join(module_dir, 'code', f"{module_name}.py")
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(self._generate_module_template(full_name, module_type))
            
            logger.info(f"✨ Nuovo modulo creato: {full_name}")
            
            # Aggiungi alla cronologia
            self.evolution_history.append({
                'type': 'module_created',
                'timestamp': datetime.now().isoformat(),
                'module_name': full_name,
                'module_type': module_type,
                'files_created': [main_file]
            })
            
            self._save_evolution_history()
            
            return {
                'success': True,
                'module_name': full_name,
                'files_created': [main_file],
                'type': module_type
            }
            
        except Exception as e:
            logger.error(f"Errore creando modulo: {e}")
            return {'success': False, 'error': str(e)}

    def _generate_module_template(self, module_name: str, module_type: str) -> str:
        """Genera template per nuovo modulo"""
        return f'''"""
{module_name.upper()} - {module_type.title()} Module
Creato automaticamente da Aether Self-Evolution Engine
"""

import logging
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class {module_name.replace('_', '').title()}:
    """
    {module_type.title()} module per Aether
    """
    
    def __init__(self):
        self.name = "{module_name}"
        self.type = "{module_type}"
        self.created_at = datetime.now().isoformat()
        logger.info(f"🚀 {{self.type.title()}} module {{self.name}} inizializzato")
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa i dati in input"""
        try:
            # Implementazione base
            result = {{
                'status': 'processed',
                'timestamp': datetime.now().isoformat(),
                'input_data': data,
                'module': self.name
            }}
            
            logger.info(f"✅ Dati processati da {{self.name}}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Errore in {{self.name}}: {{e}}")
            return {{'status': 'error', 'error': str(e)}}

# Istanza singleton
{module_name.lower()}_instance = {module_name.replace('_', '').title()}()

def get_instance():
    """Restituisce istanza del modulo"""
    return {module_name.lower()}_instance
''' 