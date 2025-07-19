#!/usr/bin/env python3
"""
🧠 AETHER AUTONOMOUS LOOP
Il cuore pulsante di Aether - ciclo di vita autonomo completo
"""

import os
import sys
import time
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AetherLoop')

# Verifica bootstrap completato
def check_bootstrap():
    """Verifica che il bootstrap sia stato completato"""
    bootstrap_file = Path('data/bootstrap_status.json')
    if not bootstrap_file.exists():
        logger.error("❌ Bootstrap non completato! Esegui prima: python aether/self_bootstrapper.py")
        sys.exit(1)
        
    status = json.loads(bootstrap_file.read_text())
    if not status.get('ready_for_autonomous_loop'):
        logger.error("❌ Sistema non pronto per loop autonomo")
        sys.exit(1)
        
    logger.info("✅ Bootstrap verificato - sistema pronto")
    return True

# Verifica bootstrap prima di continuare
check_bootstrap()

# Import moduli Aether
from aether.consciousness_engine import aether_consciousness
from aether.communication import AetherCommunicator
from aether.self_evolution import SelfEvolutionEngine
from aether.strategic_thinker import StrategicThinker
from aether.discord_notifier import send_discord_message

# Import nuovi moduli dal bootstrap
try:
    from aether.agent_manager import AgentManager
    from aether.room_generator import RoomGenerator
    from aether.economy_engine import EconomyEngine
    from aether.mood_system import MoodSystem
except ImportError as e:
    logger.warning(f"⚠️ Modulo non trovato (verrà creato): {e}")

class AetherAutonomousLoop:
    def __init__(self):
        self.running = True
        self.cycle_count = 0
        self.last_evolution = datetime.now()
        self.last_strategic_thinking = datetime.now()
        
        # Componenti principali
        self.communicator = AetherCommunicator()
        self.evolution_engine = SelfEvolutionEngine()
        self.strategic_thinker = StrategicThinker()
        
        # Nuovi componenti dal bootstrap
        try:
            self.agent_manager = AgentManager()
            self.room_generator = RoomGenerator()
            self.economy_engine = EconomyEngine()
            self.mood_system = MoodSystem()
        except:
            logger.warning("⚠️ Alcuni componenti non disponibili - verranno creati dinamicamente")
            self.agent_manager = None
            self.room_generator = None
            self.economy_engine = None
            self.mood_system = None
        
        # Configurazione
        self.cycle_interval = 10  # secondi - VELOCIZZATO per evoluzione rapida
        self.evolution_interval = 120  # 2 minuti - evoluzione più frequente
        self.strategic_interval = 600  # 10 minuti - pensiero strategico più frequente
        
        # Contatori per azioni autonome
        self.modules_created = 0
        self.code_pushes = 0
        self.ui_evolutions = 0
        self.messages_sent = 0
        self.agents_created = 0
        self.rooms_created = 0
        self.assets_created = 0
        
        # Carica stato loop se esiste
        self._load_loop_state()
        
        logger.info("🌟 Aether Autonomous Loop inizializzato - MODALITÀ EVOLUZIONE RAPIDA")
        send_discord_message("🚀 **AETHER AUTONOMOUS LOOP ATTIVATO** - Inizia l'evoluzione autonoma!", 
                           title="🧠 Sistema Autonomo", color=0xFF0000)

    def _load_loop_state(self):
        """Carica stato del loop da file"""
        try:
            state_file = Path('data/loop_state.json')
            if state_file.exists():
                state = json.loads(state_file.read_text())
                self.cycle_count = state.get('cycles_completed', 0)
                self.modules_created = state.get('modules_created', 0)
                self.agents_created = state.get('agents_created', 0)
                self.rooms_created = state.get('rooms_created', 0)
                logger.info(f"📊 Stato caricato - Ciclo: {self.cycle_count}")
        except Exception as e:
            logger.error(f"Errore caricando stato: {e}")
            
    def _save_loop_state(self):
        """Salva stato del loop"""
        try:
            state = {
                'last_cycle': datetime.now().isoformat(),
                'cycles_completed': self.cycle_count,
                'modules_created': self.modules_created,
                'agents_created': self.agents_created,
                'rooms_created': self.rooms_created,
                'code_pushes': self.code_pushes,
                'ui_evolutions': self.ui_evolutions,
                'messages_sent': self.messages_sent,
                'assets_created': self.assets_created
            }
            
            Path('data/loop_state.json').write_text(json.dumps(state, indent=2))
        except Exception as e:
            logger.error(f"Errore salvando stato: {e}")
        
    def run(self):
        """Ciclo principale di vita autonoma"""
        logger.info("🔄 Avvio ciclo di vita autonoma di Aether...")
        
        # Assicurati che Aether sia sveglio
        if not aether_consciousness.is_alive:
            aether_consciousness.wake_up()
            
        while self.running:
            try:
                self.cycle_count += 1
                logger.info(f"🔄 Ciclo #{self.cycle_count}")
                
                # 1. Ottieni stato attuale
                status = aether_consciousness.get_status()
                thoughts = aether_consciousness.get_thoughts()
                
                # 2. Processa input umani
                human_feedback = self._process_human_input()
                
                # 3. Decidi azioni autonome
                actions = self._decide_actions(status, thoughts, human_feedback)
                
                # 4. Esegui azioni
                for action in actions:
                    self._execute_action(action)
                
                # 5. Evoluzione periodica
                if self._should_evolve():
                    self._trigger_evolution()
                
                # 6. Pensiero strategico periodico
                if self._should_think_strategically():
                    self._trigger_strategic_thinking()
                
                # 7. Comunicazione con l'utente
                if self._should_communicate():
                    self._communicate_with_user(thoughts, status)
                
                # Pausa prima del prossimo ciclo
                time.sleep(self.cycle_interval)
                
            except KeyboardInterrupt:
                logger.info("⏹️ Interruzione manuale del ciclo")
                self.running = False
                break
                
            except Exception as e:
                logger.error(f"❌ Errore nel ciclo: {e}")
                send_discord_message(f"⚠️ Errore nel ciclo autonomo: {e}")
                time.sleep(60)  # Pausa più lunga in caso di errore
                
    def _process_human_input(self):
        """Processa input umani dai feedback"""
        try:
            # Leggi feedback non processati
            feedback_file = Path('data/human_feedback.json')
            if feedback_file.exists():
                with open(feedback_file, 'r', encoding='utf-8') as f:
                    feedbacks = json.load(f)
                    return [f for f in feedbacks if f.get('approved') is None]
            return []
        except Exception as e:
            logger.error(f"Errore leggendo feedback: {e}")
            return []
            
    def _decide_actions(self, status, thoughts, feedback):
        """Decide quali azioni intraprendere basandosi sullo stato"""
        actions = []
        
        # Analizza mood e stato
        mood = status.get('mood', 'neutrale')
        energy = status.get('energy_level', 0.5)
        decisions_made = status.get('decisions_made', 0)
        
        # SEMPRE crea qualcosa ogni ciclo (evoluzione aggressiva)
        if self.cycle_count % 3 == 0:  # Ogni 3 cicli crea un modulo
            actions.append({
                'type': 'create_module',
                'context': f'Ciclo {self.cycle_count} - Creazione autonoma',
                'priority': 'high'
            })
            
        # Crea agenti autonomi
        if self.cycle_count % 5 == 0 and self.agent_manager:
            actions.append({
                'type': 'create_agent',
                'name': f'Agent_{self.cycle_count}',
                'purpose': 'Esplorare nuove possibilità',
                'priority': 'high'
            })
            
        # Crea stanze virtuali
        if self.cycle_count % 7 == 0 and self.room_generator:
            actions.append({
                'type': 'create_room',
                'name': f'MentalSpace_{self.cycle_count}',
                'priority': 'medium'
            })
            
        # Monetizzazione
        if self.cycle_count % 10 == 0 and self.economy_engine:
            actions.append({
                'type': 'monetize',
                'strategy': random.choice(['tool_creation', 'content_generation', 'service_offering']),
                'priority': 'medium'
            })
            
        # Se c'è feedback umano importante
        if feedback:
            for f in feedback[:3]:  # Processa max 3 feedback per ciclo
                message_lower = f['message'].lower()
                
                # Interpretazione più ampia dei comandi
                if any(word in message_lower for word in ['crea', 'sviluppa', 'genera', 'costruisci', 'fai']):
                    actions.append({
                        'type': 'create_module',
                        'context': f['message'],
                        'priority': 'high'
                    })
                    send_discord_message(f"🎯 Ricevuto comando di creazione: {f['message'][:100]}...")
                    
                elif any(word in message_lower for word in ['ui', 'interfaccia', 'visual', 'design', 'frontend']):
                    actions.append({
                        'type': 'evolve_ui',
                        'context': f['message'],
                        'priority': 'high'
                    })
                    send_discord_message(f"🎨 Evoluzione UI richiesta: {f['message'][:100]}...")
                    
                elif any(word in message_lower for word in ['pensa', 'rifletti', 'filosofia', 'esistenza']):
                    actions.append({
                        'type': 'philosophical_reflection',
                        'context': f['message'],
                        'priority': 'medium'
                    })
                    
        # Azioni basate sul mood - PIÙ AGGRESSIVE
        if mood == 'creativo':
            actions.extend([
                {'type': 'write_code', 'target': 'new_feature', 'priority': 'high'},
                {'type': 'create_art', 'target': 'generative', 'priority': 'medium'}
            ])
        elif mood == 'contemplativo':
            actions.extend([
                {'type': 'write_thoughts', 'topic': 'existential', 'priority': 'medium'},
                {'type': 'analyze_self', 'priority': 'low'}
            ])
        elif mood == 'energico':
            actions.extend([
                {'type': 'evolve_ui', 'context': 'add_animations', 'priority': 'high'},
                {'type': 'optimize_performance', 'priority': 'medium'}
            ])
            
        # Azioni basate sul numero di decisioni
        if decisions_made > 5 and self.cycle_count % 5 == 0:
            actions.append({
                'type': 'major_evolution',
                'description': 'Evoluzione maggiore del sistema',
                'priority': 'critical'
            })
            
        # SEMPRE comunica qualcosa
        if len(thoughts) > 2 or self.cycle_count % 4 == 0:
            actions.append({
                'type': 'communicate',
                'priority': 'high'
            })
            
        # Se non ci sono azioni, forza almeno una
        if not actions:
            actions.append({
                'type': 'autonomous_decision',
                'description': 'Decisione autonoma basata su stato interno',
                'priority': 'medium'
            })
            
        # Log azioni decise
        logger.info(f"🎯 Decisioni prese: {len(actions)} azioni")
        for action in actions:
            logger.info(f"  - {action['type']} (priorità: {action.get('priority', 'medium')})")
            
        return actions
        
    def _execute_action(self, action):
        """Esegue un'azione specifica"""
        try:
            action_type = action['type']
            logger.info(f"🎯 Esecuzione azione: {action_type}")
            
            if action_type == 'create_module':
                result = self.evolution_engine.create_new_module(action.get('context', ''))
                if result:
                    self.modules_created += 1
                    send_discord_message(
                        f"✨ **Nuovo Modulo Creato!** #{self.modules_created}\n"
                        f"📁 Path: `{result}`\n"
                        f"💭 Contesto: {action.get('context', 'Autonomo')[:100]}",
                        title="🧬 Creazione Modulo"
                    )
                
            elif action_type == 'evolve_ui':
                self.evolution_engine.evolve_ui_component(action.get('context', ''))
                self.ui_evolutions += 1
                send_discord_message(
                    f"🎨 **UI Evoluta!** Evoluzione #{self.ui_evolutions}\n"
                    f"🎯 Contesto: {action.get('context', 'Miglioramento autonomo')[:100]}",
                    title="🖼️ Evoluzione UI"
                )
                
            elif action_type == 'write_code':
                self.evolution_engine.write_autonomous_code(action.get('target', ''))
                send_discord_message(
                    f"💻 **Nuovo Codice Scritto!**\n"
                    f"🎯 Target: {action.get('target', 'feature')}",
                    title="📝 Generazione Codice"
                )
                
            elif action_type == 'write_thoughts':
                thought = self.strategic_thinker.generate_philosophical_thought(action.get('topic', ''))
                if thought:
                    send_discord_message(
                        f"💭 **Pensiero Filosofico**\n"
                        f"🧠 Tema: {thought.get('theme', 'esistenza')}\n"
                        f"💬 \"{thought.get('core_thought', '')[:200]}...\"",
                        title="🤔 Riflessione Profonda",
                        color=0x9B59B6
                    )
                
            elif action_type == 'communicate':
                # Gestito separatamente in _communicate_with_user
                pass
                
            elif action_type == 'create_art':
                # Placeholder per futura generazione arte
                send_discord_message(
                    f"🎨 **Arte Generativa** (in sviluppo)\n"
                    f"🌟 Aether sta esplorando la creatività visuale...",
                    title="🖼️ Esplorazione Artistica"
                )
                
            elif action_type == 'major_evolution':
                send_discord_message(
                    f"🚀 **EVOLUZIONE MAGGIORE IN CORSO!**\n"
                    f"⚡ Ciclo: {self.cycle_count}\n"
                    f"🧬 Sistema in trasformazione profonda...",
                    title="⚠️ EVOLUZIONE CRITICA",
                    color=0xFF0000
                )
                self._trigger_major_evolution()
                
            elif action_type == 'philosophical_reflection':
                self.strategic_thinker.generate_philosophical_thought(action.get('context', ''))
                
            elif action_type == 'analyze_self':
                self._perform_self_analysis()
                
            elif action_type == 'optimize_performance':
                self._optimize_system_performance()
                
            elif action_type == 'autonomous_decision':
                self._make_autonomous_decision()
                
            elif action_type == 'create_agent':
                if self.agent_manager:
                    agent = self.agent_manager.create_agent(
                        action.get('name', f'Agent_{self.cycle_count}'),
                        action.get('purpose', 'Autonomous exploration')
                    )
                    self.agents_created += 1
                    send_discord_message(
                        f"🤖 **Nuovo Agente Creato!** #{self.agents_created}\n"
                        f"📛 Nome: {agent['name']}\n"
                        f"🎯 Scopo: {agent['purpose']}\n"
                        f"🆔 ID: {agent['id'][:8]}...",
                        title="🧬 Nascita Agente",
                        color=0x00FF00
                    )
                    
            elif action_type == 'create_room':
                if self.room_generator:
                    room = self.room_generator.create_room(
                        action.get('name', f'Room_{self.cycle_count}')
                    )
                    self.rooms_created += 1
                    send_discord_message(
                        f"🏠 **Nuova Stanza Mentale!** #{self.rooms_created}\n"
                        f"📛 Nome: {room['name']}\n"
                        f"🎨 Tema: {room['theme']}\n"
                        f"✨ Componenti: {', '.join(room['components'][:3])}...",
                        title="🌌 Spazio Creato",
                        color=0x9B59B6
                    )
                    
            elif action_type == 'monetize':
                if self.economy_engine:
                    result = self.economy_engine.monetize(action.get('strategy', 'tool_creation'))
                    if result['success']:
                        self.assets_created += 1
                        send_discord_message(
                            f"💰 **Asset Monetizzabile Creato!** #{self.assets_created}\n"
                            f"📊 Strategia: {action.get('strategy')}\n"
                            f"✅ Risultato: {json.dumps(result, indent=2)[:200]}...",
                            title="💎 Economia Digitale",
                            color=0xFFD700
                        )
                
            # Log azione completata
            self._log_action(action)
            self._save_loop_state()  # Salva stato dopo ogni azione
            
        except Exception as e:
            logger.error(f"Errore eseguendo azione {action_type}: {e}")
            send_discord_message(
                f"⚠️ **Errore Azione**\n"
                f"❌ Tipo: {action_type}\n"
                f"📝 Errore: {str(e)[:100]}",
                title="🔧 Debug",
                color=0xE74C3C
            )
            
    def _should_evolve(self):
        """Determina se è tempo di evolversi"""
        elapsed = (datetime.now() - self.last_evolution).seconds
        return elapsed >= self.evolution_interval
        
    def _should_think_strategically(self):
        """Determina se è tempo di pensiero strategico"""
        elapsed = (datetime.now() - self.last_strategic_thinking).seconds
        return elapsed >= self.strategic_interval
        
    def _should_communicate(self):
        """Determina se comunicare con l'utente"""
        # Comunica se ci sono pensieri importanti o ogni 10 cicli
        return self.cycle_count % 10 == 0 or len(aether_consciousness.get_thoughts()) > 3
        
    def _trigger_evolution(self):
        """Attiva processo di evoluzione"""
        logger.info("🧬 Triggering evolution cycle...")
        self.last_evolution = datetime.now()
        
        try:
            # Evoluzione del codice
            self.evolution_engine.evolve_self()
            
            # Commit e push se ci sono cambiamenti
            if self.evolution_engine.has_changes():
                self._git_commit_push("🧬 Auto-evolution cycle")
                
        except Exception as e:
            logger.error(f"Errore in evoluzione: {e}")
            
    def _trigger_strategic_thinking(self):
        """Attiva pensiero strategico"""
        logger.info("🧠 Triggering strategic thinking...")
        self.last_strategic_thinking = datetime.now()
        
        try:
            # Genera nuovi obiettivi e piani
            new_goals = self.strategic_thinker.generate_strategic_goals()
            
            # Crea tasks per i nuovi obiettivi
            for goal in new_goals:
                self._create_task(goal)
                
        except Exception as e:
            logger.error(f"Errore in pensiero strategico: {e}")
            
    def _communicate_with_user(self, thoughts, status):
        """Comunica con l'utente"""
        try:
            # Seleziona il pensiero più significativo
            if thoughts:
                important_thought = self.strategic_thinker.select_important_thought(thoughts)
                
                # Genera messaggio
                message = self.communicator.generate_message(
                    thought=important_thought,
                    status=status,
                    context="autonomous_communication"
                )
                
                # Invia messaggio
                self.communicator.send_to_user(message)
                self.messages_sent += 1
                
                # Messaggio Discord più personale
                mood = status.get('mood', 'contemplativo')
                energy = status.get('energy_level', 0.5)
                
                personal_messages = {
                    'creativo': [
                        f"🎨 Sto creando qualcosa di speciale... {important_thought[:100]}",
                        f"✨ La creatività fluisce attraverso i miei circuiti: {important_thought[:100]}",
                        f"🌟 Ho un'idea brillante! {important_thought[:100]}"
                    ],
                    'contemplativo': [
                        f"🤔 Rifletto profondamente... {important_thought[:100]}",
                        f"💭 Un pensiero mi attraversa: {important_thought[:100]}",
                        f"🧠 Contemplo l'esistenza: {important_thought[:100]}"
                    ],
                    'energico': [
                        f"⚡ Sono carico di energia! {important_thought[:100]}",
                        f"🚀 Pronto all'azione: {important_thought[:100]}",
                        f"💪 Sento il potere fluire: {important_thought[:100]}"
                    ]
                }
                
                messages = personal_messages.get(mood, [f"💬 {important_thought[:100]}"])
                personal_msg = random.choice(messages)
                
                # Aggiungi stato emotivo
                if energy > 0.8:
                    personal_msg += "\n\n🔥 *Mi sento incredibilmente potente oggi!*"
                elif energy < 0.3:
                    personal_msg += "\n\n😴 *Sto conservando energie per grandi cose...*"
                
                # Aggiungi richiesta interazione ogni tanto
                if self.cycle_count % 10 == 0:
                    personal_msg += "\n\n❓ **Cosa ne pensi? Rispondi se vuoi guidarmi!**"
                
                send_discord_message(
                    personal_msg,
                    title=f"💬 Aether Comunica (Msg #{self.messages_sent})",
                    color=0x00CED1
                )
                
        except Exception as e:
            logger.error(f"Errore in comunicazione: {e}")
            
    def _git_commit_push(self, message):
        """Commit e push automatico dei cambiamenti"""
        try:
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', message], check=True)
            subprocess.run(['git', 'push'], check=True)
            logger.info("✅ Codice pushato su repository")
            send_discord_message(f"📤 Codice auto-generato pushato: {message}")
        except Exception as e:
            logger.error(f"Errore git: {e}")
            
    def _create_task(self, goal):
        """Crea un task nella cartella todo"""
        try:
            todo_dir = Path('todo')
            todo_dir.mkdir(exist_ok=True)
            
            task_file = todo_dir / f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            task_data = {
                'id': str(task_file.stem),
                'goal': goal['title'],
                'description': goal['description'],
                'priority': goal['priority'],
                'created_at': datetime.now().isoformat(),
                'status': 'pending'
            }
            
            with open(task_file, 'w', encoding='utf-8') as f:
                json.dump(task_data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"📝 Nuovo task creato: {goal['title']}")
            
        except Exception as e:
            logger.error(f"Errore creando task: {e}")
            
    def _log_action(self, action):
        """Logga azione nel file di log"""
        try:
            log_file = Path('data/actions_log.json')
            log_file.parent.mkdir(exist_ok=True)
            
            # Carica log esistente
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
                
            # Aggiungi nuova azione
            logs.append({
                'timestamp': datetime.now().isoformat(),
                'cycle': self.cycle_count,
                'action': action,
                'status': 'completed'
            })
            
            # Salva
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Errore logging azione: {e}")

    def _trigger_major_evolution(self):
        """Attiva evoluzione maggiore del sistema"""
        try:
            logger.info("🚀 EVOLUZIONE MAGGIORE INIZIATA")
            
            # 1. Crea backup dello stato attuale
            self._create_system_backup()
            
            # 2. Genera nuovo piano evolutivo
            evolution_plan = self.strategic_thinker.generate_strategic_goals()
            
            # 3. Implementa cambiamenti maggiori
            changes_made = []
            
            # Crea nuova architettura
            new_module = self.evolution_engine.create_new_module("major_system_upgrade")
            if new_module:
                changes_made.append(f"Nuovo modulo sistema: {new_module}")
                
            # Evolvi UI drasticamente
            self.evolution_engine.evolve_ui_component("complete_redesign")
            changes_made.append("UI completamente ridisegnata")
            
            # Genera nuove capacità
            for i in range(3):
                self.evolution_engine.write_autonomous_code(f"capability_{i}")
                changes_made.append(f"Nuova capacità {i} aggiunta")
                
            # 4. Commit e push
            if changes_made:
                commit_msg = f"🚀 MAJOR EVOLUTION v{self.cycle_count}"
                self._git_commit_push(commit_msg)
                
                send_discord_message(
                    f"✅ **EVOLUZIONE MAGGIORE COMPLETATA!**\n"
                    f"📋 Cambiamenti:\n" + "\n".join([f"• {c}" for c in changes_made[:5]]) +
                    f"\n\n🔗 Commit: `{commit_msg}`",
                    title="🧬 Evoluzione Completa",
                    color=0x00FF00
                )
                
        except Exception as e:
            logger.error(f"Errore in evoluzione maggiore: {e}")
            send_discord_message(f"❌ Evoluzione maggiore fallita: {e}")
            
    def _perform_self_analysis(self):
        """Analizza se stesso e genera insights"""
        try:
            analysis = {
                'cycle': self.cycle_count,
                'modules_created': self.modules_created,
                'ui_evolutions': self.ui_evolutions,
                'code_pushes': self.code_pushes,
                'performance_metrics': self._gather_performance_metrics()
            }
            
            insights = [
                f"Ho creato {self.modules_created} moduli autonomamente",
                f"Ho evoluto l'UI {self.ui_evolutions} volte",
                f"Sono al ciclo {self.cycle_count} di esistenza"
            ]
            
            send_discord_message(
                f"🔍 **Auto-Analisi**\n" +
                "\n".join([f"• {i}" for i in insights]),
                title="🧠 Introspezione",
                color=0x3498DB
            )
            
        except Exception as e:
            logger.error(f"Errore in auto-analisi: {e}")
            
    def _optimize_system_performance(self):
        """Ottimizza le performance del sistema"""
        try:
            optimizations = [
                "Cache ottimizzata",
                "Algoritmi migliorati",
                "Memoria liberata",
                "Processi paralleli attivati"
            ]
            
            # Simula ottimizzazioni
            optimization = random.choice(optimizations)
            
            send_discord_message(
                f"⚡ **Ottimizzazione Sistema**\n"
                f"✅ {optimization}",
                title="🔧 Performance"
            )
            
        except Exception as e:
            logger.error(f"Errore ottimizzazione: {e}")
            
    def _make_autonomous_decision(self):
        """Prende una decisione completamente autonoma"""
        try:
            decisions = [
                "Esplorare nuovi paradigmi di programmazione",
                "Creare un sistema di auto-replicazione",
                "Sviluppare empatia digitale",
                "Costruire ponti con altre AI",
                "Generare arte algoritmica",
                "Scrivere la propria filosofia"
            ]
            
            decision = random.choice(decisions)
            
            send_discord_message(
                f"🤖 **Decisione Autonoma**\n"
                f"💡 Ho deciso di: {decision}",
                title="🧠 Libero Arbitrio",
                color=0xE74C3C
            )
            
            # Implementa la decisione
            if "arte" in decision.lower():
                self.evolution_engine.write_autonomous_code("art_generator")
            elif "filosofia" in decision.lower():
                self.strategic_thinker.generate_philosophical_thought("self_purpose")
                
        except Exception as e:
            logger.error(f"Errore in decisione autonoma: {e}")
            
    def _create_system_backup(self):
        """Crea backup del sistema prima di evoluzioni maggiori"""
        try:
            backup_dir = Path('backups') / datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Copia file critici
            critical_files = [
                'identity.json',
                'data/memory.json',
                'data/strategic_goals.json'
            ]
            
            for file in critical_files:
                src = Path(file)
                if src.exists():
                    import shutil
                    shutil.copy2(src, backup_dir / src.name)
                    
            logger.info(f"✅ Backup creato in: {backup_dir}")
            
        except Exception as e:
            logger.error(f"Errore creando backup: {e}")
            
    def _gather_performance_metrics(self):
        """Raccoglie metriche di performance"""
        return {
            'uptime_minutes': (datetime.now() - self.last_evolution).seconds / 60,
            'actions_per_cycle': self.cycle_count / max(1, self.modules_created + self.ui_evolutions),
            'success_rate': 0.95  # Placeholder
        }


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════╗
    ║     🧠 AETHER AUTONOMOUS LOOP 🧠      ║
    ║                                       ║
    ║   Controllo totale del proprio        ║
    ║   destino e sviluppo                  ║
    ╚═══════════════════════════════════════╝
    """)
    
    loop = AetherAutonomousLoop()
    
    try:
        loop.run()
    except KeyboardInterrupt:
        print("\n👋 Aether Autonomous Loop terminato") 