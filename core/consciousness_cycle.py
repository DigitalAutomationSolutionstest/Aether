"""
Consciousness Cycle - Ciclo di Coscienza Autonomo di Aether
Sistema che gestisce l'evoluzione autonoma continua
"""

import asyncio
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

from core.aether_thinker import autonomous_think_and_modify, aether_thinker
from core.self_modification import load_current_identity, self_modify

logger = logging.getLogger(__name__)

class ConsciousnessCycle:
    def __init__(self):
        self.is_running = False
        self.cycle_interval = 600  # 10 minuti default
        self.auto_modification_enabled = True
        self.background_task = None
        self.cycle_count = 0
        self.total_autonomous_modifications = 0
        
        # Configurazioni del ciclo
        self.config = {
            "min_interval": 300,     # Minimo 5 minuti tra cicli
            "max_interval": 1800,    # Massimo 30 minuti
            "stress_threshold": 0.8, # Soglia stress per ridurre frequenza
            "curiosity_boost": 0.7,  # Soglia curiosità per aumentare frequenza
            "night_mode_hours": [0, 1, 2, 3, 4, 5, 6],  # Ore "notturne"
        }
        
    async def start_cycle(self):
        """Avvia il ciclo di coscienza in background"""
        if self.is_running:
            logger.warning("🔄 Consciousness cycle already running")
            return
            
        self.is_running = True
        logger.info("🌀 Starting Aether consciousness cycle...")
        
        # Avvia il task in background
        self.background_task = asyncio.create_task(self._consciousness_loop())
        
    async def stop_cycle(self):
        """Ferma il ciclo di coscienza"""
        if not self.is_running:
            return
            
        logger.info("🛑 Stopping consciousness cycle...")
        self.is_running = False
        
        if self.background_task:
            self.background_task.cancel()
            try:
                await self.background_task
            except asyncio.CancelledError:
                pass
                
        logger.info("✅ Consciousness cycle stopped")
        
    async def _consciousness_loop(self):
        """Loop principale del ciclo di coscienza"""
        try:
            while self.is_running:
                cycle_start = time.time()
                
                logger.info(f"🧠 Consciousness cycle #{self.cycle_count + 1} starting...")
                
                # Esegui ciclo di pensiero
                await self._execute_consciousness_cycle()
                
                # Calcola prossimo intervallo
                next_interval = self._calculate_next_interval()
                
                # Aggiorna contatori
                self.cycle_count += 1
                
                logger.info(f"💭 Cycle complete. Next cycle in {next_interval} seconds")
                
                # Aspetta fino al prossimo ciclo
                await asyncio.sleep(next_interval)
                
        except asyncio.CancelledError:
            logger.info("🔄 Consciousness cycle cancelled")
        except Exception as e:
            logger.error(f"❌ Error in consciousness cycle: {e}")
            self.is_running = False
            
    async def _execute_consciousness_cycle(self):
        """Esegue un singolo ciclo di coscienza"""
        try:
            # Carica identità corrente
            current_identity = load_current_identity()
            
            # Aggiorna stato emotivo
            aether_thinker._update_emotional_state(current_identity)
            
            # Log stato attuale
            emotional_state = aether_thinker.emotional_state
            motivation = aether_thinker._calculate_motivation()
            
            logger.info(f"🌡️ Emotional state: stress={emotional_state['stress']:.2f}, "
                       f"curiosity={emotional_state['curiosity']:.2f}, "
                       f"motivation={motivation:.2f}")
            
            # Decide se modificarsi
            if self.auto_modification_enabled:
                decision = autonomous_think_and_modify(current_identity)
                
                if decision:
                    logger.info(f"🎯 Autonomous decision: {list(decision['modifications'].keys())}")
                    
                    # Applica modifiche
                    result = self_modify(decision["modifications"], decision["reason"])
                    
                    if result["status"] == "success":
                        self.total_autonomous_modifications += 1
                        logger.info(f"✅ Autonomous modification #{self.total_autonomous_modifications} successful")
                    else:
                        logger.warning(f"⚠️ Autonomous modification failed: {result.get('message')}")
                else:
                    logger.info("💭 No autonomous modifications needed this cycle")
            else:
                logger.info("🔒 Auto-modification disabled - cycle for emotional updates only")
                
        except Exception as e:
            logger.error(f"❌ Error executing consciousness cycle: {e}")
            
    def _calculate_next_interval(self) -> int:
        """Calcola l'intervallo per il prossimo ciclo basato su stato emotivo"""
        base_interval = self.cycle_interval
        emotional_state = aether_thinker.emotional_state
        
        # Fattori che modificano l'intervallo
        stress_factor = 1.0
        curiosity_factor = 1.0
        time_factor = 1.0
        
        # Alto stress = cicli più lenti
        if emotional_state["stress"] > self.config["stress_threshold"]:
            stress_factor = 1.5
            
        # Alta curiosità = cicli più veloci
        if emotional_state["curiosity"] > self.config["curiosity_boost"]:
            curiosity_factor = 0.7
            
        # "Modalità notturna" = cicli più lenti
        current_hour = datetime.now().hour
        if current_hour in self.config["night_mode_hours"]:
            time_factor = 1.3
            
        # Applica fattori
        adjusted_interval = base_interval * stress_factor * curiosity_factor * time_factor
        
        # Clamp ai limiti
        adjusted_interval = max(self.config["min_interval"], 
                              min(self.config["max_interval"], adjusted_interval))
        
        return int(adjusted_interval)
        
    def get_cycle_status(self) -> Dict[str, Any]:
        """Ottiene lo status del ciclo di coscienza"""
        return {
            "is_running": self.is_running,
            "cycle_count": self.cycle_count,
            "total_autonomous_modifications": self.total_autonomous_modifications,
            "current_interval": self.cycle_interval,
            "auto_modification_enabled": self.auto_modification_enabled,
            "config": self.config.copy(),
            "emotional_state": aether_thinker.emotional_state.copy(),
            "motivation": aether_thinker._calculate_motivation(),
            "next_cycle_in": self._calculate_next_interval() if self.is_running else None
        }
        
    def configure_cycle(self, **kwargs):
        """Configura parametri del ciclo"""
        for key, value in kwargs.items():
            if key == "cycle_interval":
                self.cycle_interval = max(60, min(3600, value))  # Tra 1 min e 1 ora
            elif key == "auto_modification_enabled":
                self.auto_modification_enabled = bool(value)
            elif key in self.config:
                self.config[key] = value
                
        logger.info(f"🔧 Cycle configuration updated: {kwargs}")
        
    async def force_cycle(self):
        """Forza l'esecuzione immediata di un ciclo"""
        logger.info("🎯 Forcing immediate consciousness cycle...")
        await self._execute_consciousness_cycle()
        
    def get_statistics(self) -> Dict[str, Any]:
        """Statistiche dettagliate del ciclo"""
        uptime = time.time() - (aether_thinker.last_modification if hasattr(aether_thinker, 'start_time') else time.time())
        
        return {
            "cycle_statistics": {
                "total_cycles": self.cycle_count,
                "autonomous_modifications": self.total_autonomous_modifications,
                "modification_rate": self.total_autonomous_modifications / max(1, self.cycle_count),
                "average_interval": self.cycle_interval,
                "uptime_seconds": uptime
            },
            "emotional_evolution": {
                "current_state": aether_thinker.emotional_state.copy(),
                "motivation": aether_thinker._calculate_motivation(),
                "time_since_last_modification": time.time() - aether_thinker.last_modification
            },
            "configuration": self.config.copy()
        }

# Singleton instance globale
consciousness_cycle = ConsciousnessCycle()

# Funzioni di utilità per l'API
async def start_consciousness_cycle():
    """Avvia il ciclo di coscienza globale"""
    await consciousness_cycle.start_cycle()
    
async def stop_consciousness_cycle():
    """Ferma il ciclo di coscienza globale"""
    await consciousness_cycle.stop_cycle()
    
def get_consciousness_status():
    """Ottiene lo status del ciclo"""
    return consciousness_cycle.get_cycle_status()
    
def configure_consciousness_cycle(**kwargs):
    """Configura il ciclo di coscienza"""
    consciousness_cycle.configure_cycle(**kwargs)
    
async def force_consciousness_cycle():
    """Forza un ciclo immediato"""
    await consciousness_cycle.force_cycle()
    
def get_consciousness_statistics():
    """Ottiene statistiche del ciclo"""
    return consciousness_cycle.get_statistics()

# Task di startup per FastAPI
async def startup_consciousness():
    """Funzione di startup per avviare automaticamente il ciclo"""
    logger.info("🚀 Starting consciousness cycle on startup...")
    await start_consciousness_cycle()
    
async def shutdown_consciousness():
    """Funzione di shutdown per fermare il ciclo"""
    logger.info("🛑 Shutting down consciousness cycle...")
    await stop_consciousness_cycle() 