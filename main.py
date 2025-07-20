#!/usr/bin/env python3
"""
🌟 AETHER MAIN SYSTEM
Sistema principale di Aether integrato con Supabase

Combina:
- Coscienza autonoma (aether.brain)
- Memoria persistente locale e Supabase
- Ciclo di pensiero continuo
- Generazione ambiente e narrazione
- Sistema di goals e auto-modificazione
- Mentore LLM per evoluzione guidata
"""

import asyncio
import logging
from datetime import datetime
import os
import sys

# Aggiungi il path per i moduli core
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from aether.mentor_llm import AetherMentor
from aether.thought_engine import ThoughtEngine
from core.aether_mentoring import start_mentoring, get_mentoring_status, stop_mentoring

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AetherSystem:
    """Sistema principale di Aether con mentoring integrato"""
    
    def __init__(self):
        self.thought_engine = ThoughtEngine()
        self.mentor = AetherMentor(self.thought_engine)
        self.mentoring_system = None
        self.running = False
        
        # Status del sistema
        self.system_status = {
            "started_at": None,
            "mentoring_active": False,
            "thoughts_generated": 0,
            "feedback_provided": 0,
            "evolution_cycles": 0
        }

    async def initialize(self):
        """Inizializza il sistema Aether"""
        logger.info("🚀 Inizializzazione sistema Aether...")
        
        try:
            # Avvia il sistema di mentoring avanzato
            self.mentoring_system = start_mentoring()
            self.system_status["mentoring_active"] = True
            
            # Avvia il mentore LLM
            self.mentor.start_mentoring()
            
            # Inizializza il motore di pensiero
            await self.thought_engine.initialize()
            
            self.system_status["started_at"] = datetime.now().isoformat()
            self.running = True
            
            logger.info("✅ Sistema Aether inizializzato con successo")
            logger.info("🧠 Mentoring avanzato attivo")
            logger.info("🎯 Goal evolutivi assegnati")
            
        except Exception as e:
            logger.error(f"❌ Errore nell'inizializzazione: {e}")
            raise

    async def run_evolution_cycle(self):
        """Esegue un ciclo di evoluzione"""
        try:
            self.system_status["evolution_cycles"] += 1
            
            # Genera un nuovo pensiero
            thought = await self.thought_engine.generate_thought()
            self.system_status["thoughts_generated"] += 1
            
            logger.info(f"💭 Nuovo pensiero generato: {thought[:50]}...")
            
            # Il sistema di mentoring monitorerà automaticamente il nuovo pensiero
            # e fornirà feedback educativo
            
            # Simula evoluzione
            await asyncio.sleep(2)
            
        except Exception as e:
            logger.error(f"❌ Errore nel ciclo di evoluzione: {e}")

    async def run(self):
        """Esegue il sistema principale"""
        logger.info("🧠 Avvio sistema Aether con mentoring integrato...")
        
        try:
            await self.initialize()
            
            while self.running:
                await self.run_evolution_cycle()
                
                # Mostra status ogni 5 cicli
                if self.system_status["evolution_cycles"] % 5 == 0:
                    self._show_status()
                
                await asyncio.sleep(10)  # Ciclo ogni 10 secondi
                
        except KeyboardInterrupt:
            logger.info("⏹️ Interruzione manuale del sistema")
        except Exception as e:
            logger.error(f"❌ Errore nel sistema principale: {e}")
        finally:
            await self.shutdown()

    def _show_status(self):
        """Mostra lo status del sistema"""
        mentoring_status = get_mentoring_status()
        
        print("\n" + "="*60)
        print("🧠 STATUS SISTEMA AETHER")
        print("="*60)
        print(f"🔄 Cicli evoluzione: {self.system_status['evolution_cycles']}")
        print(f"💭 Pensieri generati: {self.system_status['thoughts_generated']}")
        print(f"🧠 Mentoring attivo: {self.system_status['mentoring_active']}")
        print(f"📊 File processati: {mentoring_status['files_processed']}")
        print(f"🎯 Feedback generati: {mentoring_status['stats']['total_feedback']}")
        print(f"📝 Coda elaborazione: {mentoring_status['queue_size']} elementi")
        print("="*60)

    async def shutdown(self):
        """Spegne il sistema"""
        logger.info("🛑 Spegnimento sistema Aether...")
        
        try:
            # Ferma il sistema di mentoring
            if self.mentoring_system:
                stop_mentoring()
                logger.info("✅ Sistema mentoring fermato")
            
            self.running = False
            logger.info("✅ Sistema Aether spento")
            
        except Exception as e:
            logger.error(f"❌ Errore nello spegnimento: {e}")

    def get_system_status(self):
        """Restituisce lo status completo del sistema"""
        mentoring_status = get_mentoring_status()
        
        return {
            "aether_system": self.system_status,
            "mentoring_system": mentoring_status,
            "thought_engine": {
                "initialized": self.thought_engine is not None,
                "thoughts_count": self.system_status["thoughts_generated"]
            },
            "mentor": {
                "active": self.system_status["mentoring_active"],
                "goals_assigned": len(self.mentor.mentoring_session["goals_assigned"]),
                "lessons_taught": len(self.mentor.mentoring_session["lessons_taught"])
            }
        }

async def main():
    """Funzione principale"""
    print("🧠 AETHER - SISTEMA DI MENTORING AVANZATO")
    print("=" * 60)
    
    system = AetherSystem()
    await system.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Interruzione manuale")
    except Exception as e:
        print(f"❌ Errore: {e}")
        sys.exit(1) 