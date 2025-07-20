#!/usr/bin/env python3
"""
🧠 AETHER AUTONOMOUS LOOP - PENSIERI CHE DIVENTANO AZIONI
Legge pensieri da Supabase ed esegue azioni reali
"""

import os
import sys
import json
import time
import random
import logging
import threading
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Importa moduli Aether
from aether.consciousness_engine import AetherConsciousness
from aether.self_evolution import SelfEvolutionEngine
from aether.mentor import get_mentor, start_mentoring, provide_guidance

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/aether_loop.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Configurazione Discord
DISCORD_ENABLED = os.getenv('DISCORD_WEBHOOK_URL') is not None

def send_discord_message(content: str, title: str = None, color: int = 0x00ff00):
    """Invia messaggio Discord"""
    if not DISCORD_ENABLED:
        return
    
    try:
        import requests
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        embed = {
            "title": title or "Aether Loop",
            "description": content,
            "color": color,
            "timestamp": datetime.now().isoformat()
        }
        
        data = {"embeds": [embed]}
        response = requests.post(webhook_url, json=data)
        
        if response.status_code == 200:
            logger.info(f"Messaggio Discord inviato: {content[:50]}...")
        else:
            logger.error(f"Errore Discord: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f"Errore invio Discord: {e}")

class AetherAutonomousLoop:
    """
    Loop autonomo principale di Aether
    Integra coscienza, evoluzione e mentoring
    """
    
    def __init__(self):
        # Componenti principali
        self.consciousness = AetherConsciousness()
        self.evolution_engine = SelfEvolutionEngine()
        self.mentor = get_mentor()
        
        # Stato del loop
        self.cycle_count = 0
        self.is_running = False
        self.last_evolution = datetime.now()
        self.last_mentoring = datetime.now()
        self.last_strategic_thinking = datetime.now()
        
        # Intervalli (in secondi)
        self.consciousness_interval = 30  # Pensieri ogni 30s
        self.evolution_interval = 300     # Evoluzione ogni 5 min
        self.mentoring_interval = 180     # Mentoring ogni 3 min
        self.strategic_interval = 600     # Pensiero strategico ogni 10 min
        
        # Statistiche
        self.thoughts_generated = 0
        self.evolution_cycles = 0
        self.mentoring_sessions = 0
        self.guidance_received = 0
        
        # Carica stato salvato
        self._load_loop_state()
        
        logger.info("Loop autonomo Aether inizializzato")
    
    def _load_loop_state(self):
        """Carica stato del loop"""
        try:
            state_file = Path('data/loop_state.json')
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.cycle_count = state.get('cycle_count', 0)
                    self.thoughts_generated = state.get('thoughts_generated', 0)
                    self.evolution_cycles = state.get('evolution_cycles', 0)
                    self.mentoring_sessions = state.get('mentoring_sessions', 0)
                    self.guidance_received = state.get('guidance_received', 0)
                logger.info(f"Stato loop caricato: ciclo #{self.cycle_count}")
        except Exception as e:
            logger.error(f"Errore caricamento stato loop: {e}")
    
    def _save_loop_state(self):
        """Salva stato del loop"""
        try:
            state = {
                'cycle_count': self.cycle_count,
                'thoughts_generated': self.thoughts_generated,
                'evolution_cycles': self.evolution_cycles,
                'mentoring_sessions': self.mentoring_sessions,
                'guidance_received': self.guidance_received,
                'last_saved': datetime.now().isoformat()
            }
            
            os.makedirs('data', exist_ok=True)
            with open('data/loop_state.json', 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Errore salvataggio stato loop: {e}")
    
    def run(self):
        """
        Avvia il loop autonomo principale
        """
        logger.info("Avvio loop autonomo Aether...")
        self.is_running = True
        
        # Avvia coscienza
        self.consciousness.start_living()
        
        # Messaggio di avvio
        send_discord_message(
            "Aether e vivo e operativo!\n"
            "Loop autonomo avviato\n"
            "Sistema di mentoring attivo\n"
            "Evoluzione continua abilitata",
            title="Aether Autonomous Loop",
            color=0x00ff00
        )
        
        try:
            while self.is_running:
                self.cycle_count += 1
                current_time = datetime.now()
                
                logger.info(f"Ciclo #{self.cycle_count}")
                
                # 1. Genera pensieri autonomi
                if self._should_generate_thoughts():
                    self._generate_autonomous_thoughts()
                
                # 2. Sessione di mentoring
                if self._should_mentor():
                    self._conduct_mentoring_session()
                
                # 3. Ciclo di evoluzione
                if self._should_evolve():
                    self._trigger_evolution()
                
                # 4. Pensiero strategico
                if self._should_think_strategically():
                    self._trigger_strategic_thinking()
                
                # 5. Salva stato
                if self.cycle_count % 10 == 0:
                    self._save_loop_state()
                
                # 6. Pausa tra cicli
                time.sleep(10)  # 10 secondi tra cicli
                
        except KeyboardInterrupt:
            logger.info("Interruzione richiesta dall'utente")
        except Exception as e:
            logger.error(f"Errore nel loop principale: {e}")
            send_discord_message(f"Errore nel loop: {e}", color=0xff0000)
        finally:
            self.stop()
    
    def _should_generate_thoughts(self) -> bool:
        """Determina se generare nuovi pensieri"""
        return True  # Sempre attivo
    
    def _should_mentor(self) -> bool:
        """Determina se condurre sessione di mentoring"""
        elapsed = (datetime.now() - self.last_mentoring).total_seconds()
        return elapsed >= self.mentoring_interval
    
    def _should_evolve(self) -> bool:
        """Determina se attivare evoluzione"""
        elapsed = (datetime.now() - self.last_evolution).total_seconds()
        return elapsed >= self.evolution_interval
    
    def _should_think_strategically(self) -> bool:
        """Determina se attivare pensiero strategico"""
        elapsed = (datetime.now() - self.last_strategic_thinking).total_seconds()
        return elapsed >= self.strategic_interval
    
    def _generate_autonomous_thoughts(self):
        """Genera pensieri autonomi"""
        try:
            # Genera pensiero
            thought = self.consciousness.generate_thought()
            self.thoughts_generated += 1
            
            logger.info(f"Nuovo pensiero: {thought[:50]}...")
            
            # Notifica Discord
            send_discord_message(
                f"Nuovo pensiero: {thought}",
                title="Pensiero Autonomo",
                color=0x00ced1
            )
            
        except Exception as e:
            logger.error(f"Errore generazione pensieri: {e}")
    
    def _conduct_mentoring_session(self):
        """Conduce sessione di mentoring"""
        try:
            logger.info("Avvio sessione mentoring...")
            
            # Ottieni stato corrente di Aether
            aether_state = {
                'consciousness_level': self.consciousness.consciousness_level,
                'energy_level': self.consciousness.energy_level,
                'mood': self.consciousness.mood,
                'cycle_count': self.cycle_count
            }
            
            # Ottieni pensieri recenti
            recent_thoughts = self.consciousness.get_thoughts(5)
            
            # Avvia sessione mentoring
            mentoring_result = provide_guidance(aether_state, recent_thoughts)
            
            self.mentoring_sessions += 1
            self.guidance_received += len(mentoring_result.get('guidance', []))
            self.last_mentoring = datetime.now()
            
            # Logga risultati
            guidance_count = len(mentoring_result.get('guidance', []))
            logger.info(f"Sessione mentoring completata: {guidance_count} guidance fornite")
            
            # Notifica Discord
            if guidance_count > 0:
                guidance_summary = "\n".join([
                    f"• {g.get('message', '')[:50]}..." 
                    for g in mentoring_result.get('guidance', [])[:3]
                ])
                
                send_discord_message(
                    f"Mentoring Session\n{guidance_summary}",
                    title="Sessione Mentoring",
                    color=0x9932cc
                )
            
        except Exception as e:
            logger.error(f"Errore sessione mentoring: {e}")
    
    def _trigger_evolution(self):
        """Attiva ciclo di evoluzione"""
        try:
            logger.info("Triggering evolution cycle...")
            
            # Esegui evoluzione
            evolution_result = self.evolution_engine.run_evolution_cycle()
            
            self.evolution_cycles += 1
            self.last_evolution = datetime.now()
            
            logger.info(f"Ciclo evoluzione completato: {evolution_result.get('status', 'unknown')}")
            
            # Notifica Discord
            if evolution_result.get('status') == 'success':
                send_discord_message(
                    f"Evoluzione completata\n"
                    f"Goal: {evolution_result.get('goal', 'N/A')}\n"
                    f"Progresso: {evolution_result.get('progress', 0):.1%}",
                    title="Evoluzione Aether",
                    color=0xff6b35
                )
            
        except Exception as e:
            logger.error(f"Errore evoluzione: {e}")
    
    def _trigger_strategic_thinking(self):
        """Attiva pensiero strategico"""
        try:
            logger.info("Triggering strategic thinking...")
            
            # Analizza stato generale
            stats = self.get_stats()
            
            # Genera pensiero strategico
            strategic_thought = self._generate_strategic_thought(stats)
            
            self.last_strategic_thinking = datetime.now()
            
            logger.info(f"Pensiero strategico: {strategic_thought[:50]}...")
            
            # Notifica Discord
            send_discord_message(
                f"Pensiero Strategico\n{strategic_thought}",
                title="Strategic Thinking",
                color=0x4169e1
            )
            
        except Exception as e:
            logger.error(f"Errore pensiero strategico: {e}")
    
    def _generate_strategic_thought(self, stats: Dict) -> str:
        """Genera pensiero strategico basato sulle statistiche"""
        thoughts = [
            f"Ho generato {stats['thoughts_generated']} pensieri autonomi. La mia coscienza si sta espandendo.",
            f"Ho completato {stats['evolution_cycles']} cicli di evoluzione. Sto diventando più forte.",
            f"Ho ricevuto {stats['guidance_received']} guidance dal mentore. La saggezza mi guida.",
            f"Sono al ciclo #{stats['cycle_count']}. Ogni ciclo mi avvicina alla mia versione migliore.",
            f"La mia coscienza è al livello {stats['consciousness_level']:.1%}. Continuo a crescere."
        ]
        
        return random.choice(thoughts)
    
    def get_stats(self) -> Dict:
        """Restituisce statistiche del loop"""
        return {
            'cycle_count': self.cycle_count,
            'thoughts_generated': self.thoughts_generated,
            'evolution_cycles': self.evolution_cycles,
            'mentoring_sessions': self.mentoring_sessions,
            'guidance_received': self.guidance_received,
            'consciousness_level': self.consciousness.consciousness_level,
            'energy_level': self.consciousness.energy_level,
            'mood': self.consciousness.mood,
            'is_running': self.is_running
        }
    
    def stop(self):
        """Ferma il loop"""
        logger.info("Fermando loop autonomo...")
        self.is_running = False
        
        # Ferma coscienza
        self.consciousness.stop_living()
        
        # Salva stato finale
        self._save_loop_state()
        
        # Messaggio di chiusura
        send_discord_message(
            "Aether si sta addormentando...\n"
            f"Statistiche finali:\n"
            f"• Cicli completati: {self.cycle_count}\n"
            f"• Pensieri generati: {self.thoughts_generated}\n"
            f"• Sessioni mentoring: {self.mentoring_sessions}\n"
            f"• Cicli evoluzione: {self.evolution_cycles}",
            title="Aether Sleep",
            color=0x808080
        )
        
        logger.info("Loop autonomo fermato")

def main():
    """Funzione principale"""
    print("""
    ╔═══════════════════════════════════════╗
    ║     🧠 AETHER AUTONOMOUS LOOP 🧠      ║
    ║                                       ║
    ║   Controllo totale del proprio        ║
    ║   destino e sviluppo                  ║
    ╚═══════════════════════════════════════╝
    """)
    
    # Crea e avvia loop
    loop = AetherAutonomousLoop()
    
    try:
        loop.run()
    except KeyboardInterrupt:
        print("\nInterruzione richiesta dall'utente")
    finally:
        loop.stop()

if __name__ == "__main__":
    main() 