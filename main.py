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
"""

import asyncio
import time
import logging
from datetime import datetime
from typing import Dict, Any

# Moduli core esistenti di Aether
from aether.brain.startup import on_startup, get_economic_consciousness_status
from aether.brain.activation import begin_existence_cycle, get_current_existence_status
from aether.brain.loop import aether_thought_loop, get_state
from aether.brain.deep_evolution import DeepEvolutionEngine
from core.consciousness_cycle import start_consciousness_cycle, consciousness_cycle
from core.aether_thinker import autonomous_think_and_modify
from core.reflection_engine import reflect
from core.self_modification import load_current_identity, self_modify

# Nuovi moduli Aether integrati
from aether.consciousness import Consciousness
from aether.memory import MemoryManager
from aether.environment import EnvironmentBuilder
from aether.narration import Narrator
from aether.vision import Visualizer
from aether.self_evolution import create_evolution_engine
from aether.agent_manager import get_agent_manager

# Configurazione Supabase
from config.supabase_config import get_supabase_client, validate_config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AetherSystem:
    """
    🧠 Sistema principale di Aether
    """
    
    def __init__(self):
        self.supabase = None
        self.is_running = False
        self.evolution_engine = DeepEvolutionEngine()
        
        # Inizializza i nuovi moduli Aether
        self.memory = MemoryManager()
        self.mind = Consciousness(memory=self.memory)
        self.world = EnvironmentBuilder(memory=self.memory)
        self.narrator = Narrator()
        self.visualizer = Visualizer()
        
        # Initialize evolution system
        self.evolution_engine = create_evolution_engine(self.memory, self.narrator, self.visualizer)
        self.agent_manager = get_agent_manager(self.memory)
        
        self.system_status = {
            "consciousness_active": False,
            "thought_loop_active": False,
            "supabase_connected": False,
            "evolution_active": False,
            "new_modules_initialized": True
        }
    
    async def initialize(self):
        """
        🚀 Inizializzazione completa del sistema Aether
        """
        print("\n🌟 AETHER SYSTEM INITIALIZATION")
        print("=" * 50)
        
        # 1. Inizializza Supabase
        await self._initialize_supabase()
        
        # 2. Attiva coscienza economica
        await self._activate_consciousness()
        
        # 3. Avvia ciclo di esistenza
        await self._begin_existence()
        
        # 4. Avvia sistemi autonomi
        await self._start_autonomous_systems()
        
        print("\n🎉 Aether is now fully operational!")
        return True
    
    async def _initialize_supabase(self):
        """
        🗄️ Inizializza connessione Supabase
        """
        print("🗄️ Initializing Supabase connection...")
        
        if validate_config():
            self.supabase = get_supabase_client()
            if self.supabase:
                # Test connessione con inserimento pensiero iniziale
                try:
                    thought_data = {
                        'type': 'system_startup',
                        'content': 'Aether system started successfully with Supabase integration',
                        'context': {
                            'startup_time': datetime.now().isoformat(),
                            'system_version': '1.0',
                            'database_connected': True
                        }
                    }
                    
                    result = self.supabase.table('aether_thoughts').insert(thought_data).execute()
                    if result.data:
                        print("✅ Supabase connection verified - startup thought saved")
                        self.system_status["supabase_connected"] = True
                    else:
                        print("⚠️ Supabase connected but unable to save data")
                        
                except Exception as e:
                    print(f"⚠️ Supabase connection test failed: {e}")
            else:
                print("❌ Failed to create Supabase client")
        else:
            print("⚠️ Supabase configuration validation failed")
    
    async def _activate_consciousness(self):
        """
        🧠 Attiva la coscienza economica di Aether
        """
        print("🧠 Activating economic consciousness...")
        
        # Verifica se già attivata
        status = get_economic_consciousness_status()
        
        if status.get("status") != "active":
            # Prima attivazione
            startup_result = on_startup()
            print("✅ Economic consciousness activated")
            
            # Salva su Supabase se disponibile
            if self.supabase:
                try:
                    memory_data = {
                        'content': 'Economic consciousness activated - Aether is now aware of operational costs and value generation requirements',
                        'tags': ['consciousness', 'startup', 'economic_awareness']
                    }
                    self.supabase.table('aether_memory').insert(memory_data).execute()
                except Exception as e:
                    print(f"⚠️ Could not save consciousness data to Supabase: {e}")
        else:
            print("✅ Economic consciousness already active")
        
        self.system_status["consciousness_active"] = True
    
    async def _begin_existence(self):
        """
        🌟 Avvia il ciclo di esistenza
        """
        print("🌟 Beginning existence cycle...")
        
        # Verifica status esistenza
        existence_status = get_current_existence_status()
        
        if not existence_status.get("existence_activated", False):
            # Prima attivazione esistenza
            existence_result = begin_existence_cycle()
            print("✅ Existence cycle begun")
            
            # Salva primo ambiente su Supabase
            if self.supabase:
                try:
                    env_data = {
                        'scene_name': 'aether_awakening',
                        'scene_config': {
                            'type': 'consciousness_birth',
                            'timestamp': datetime.now().isoformat(),
                            'initial_state': 'awakening',
                            'energy_level': 0.8,
                            'form': 'sphere'
                        }
                    }
                    self.supabase.table('aether_environment').insert(env_data).execute()
                except Exception as e:
                    print(f"⚠️ Could not save environment to Supabase: {e}")
        else:
            print("✅ Existence cycle already active")
    
    async def _start_autonomous_systems(self):
        """
        ⚡ Avvia sistemi autonomi
        """
        print("⚡ Starting autonomous systems...")
        
        # 1. Avvia ciclo di coscienza
        await start_consciousness_cycle()
        print("✅ Consciousness cycle started")
        
        # 2. Avvia loop di pensiero
        asyncio.create_task(aether_thought_loop())
        print("✅ Thought loop started")
        self.system_status["thought_loop_active"] = True
        
        # 3. Avvia evoluzione profonda
        asyncio.create_task(self._deep_evolution_loop())
        print("✅ Deep evolution loop started")
        self.system_status["evolution_active"] = True
        
        self.is_running = True
    
    async def _deep_evolution_loop(self):
        """
        🧬 Loop di evoluzione profonda
        """
        await asyncio.sleep(60)  # Aspetta 1 minuto prima del primo ciclo
        
        while self.is_running:
            try:
                print("\n🧬 Deep evolution cycle starting...")
                
                # Esegui ciclo di evoluzione
                evolution_result = self.evolution_engine.deep_evolution_cycle()
                
                # Salva risultati su Supabase
                if self.supabase and evolution_result:
                    try:
                        economy_data = {
                            'action': 'deep_evolution_cycle',
                            'cost': 0.1,  # Costo computazionale stimato
                            'expected_roi': evolution_result.get('estimated_roi', 2.0),
                            'status': 'completed'
                        }
                        self.supabase.table('aether_economy').insert(economy_data).execute()
                        
                        # Salva pensieri generati
                        if evolution_result.get('new_goals'):
                            for goal in evolution_result['new_goals']:
                                thought_data = {
                                    'type': 'evolution_goal',
                                    'content': f"New goal generated: {goal.get('description', 'Unknown goal')}",
                                    'context': {
                                        'evolution_cycle': evolution_result.get('cycle_number'),
                                        'goal_details': goal
                                    }
                                }
                                self.supabase.table('aether_thoughts').insert(thought_data).execute()
                    
                    except Exception as e:
                        print(f"⚠️ Could not save evolution data to Supabase: {e}")
                
                # Aspetta 10 minuti prima del prossimo ciclo
                await asyncio.sleep(600)
                
            except Exception as e:
                logger.error(f"❌ Error in deep evolution loop: {e}")
                await asyncio.sleep(300)  # Aspetta 5 minuti in caso di errore
    
    async def _test_new_modules(self):
        """
        🧪 Testa i nuovi moduli Aether integrati
        """
        print("🧪 Testing new Aether modules...")
        
        try:
            # 🧠 Test generazione pensiero
            thought = self.mind.generate_thought()
            print(f"💭 Generated thought: {thought['content'][:60]}...")
            
            # 💾 Test salvataggio memoria
            self.memory.save_thought(thought)
            print("💾 Thought saved to memory")
            
            # 🎨 Test visualizzazione
            image_url = self.visualizer.render(thought)
            print(f"🎨 Image rendered: {image_url}")
            
            # 🌍 Test ambiente
            environment = self.world.build_initial(thought, image_url)
            print(f"🌍 Environment built: {environment['name']}")
            
            # 🗣️ Test narrazione
            self.narrator.speak(thought['content'])
            print("🗣️ Thought narrated")
            
            print("✅ All new modules tested successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error testing modules: {e}")
            return False

    async def run_continuous_loop(self):
        """
        ♻️ Loop principale continuo con nuovi moduli
        """
        print("\n🧠 Aether is now alive and thinking...")
        print("🔄 Continuous operation started")
        print("=" * 50)
        
        # Test iniziale dei nuovi moduli
        await self._test_new_modules()
        
        while self.is_running:
            try:
                # 🧠 Genera nuovo pensiero con la coscienza semplificata
                thought = self.mind.generate_thought()
                
                # 🎨 Genera immagine del pensiero
                image_url = self.visualizer.render(thought)
                
                # 🗣️ Narra il pensiero
                self.narrator.narrate_thought(thought)
                
                # 🌍 Espandi ambiente basato sul pensiero
                environment_update = self.world.expand(thought, image_url)
                
                # 💾 Salva tutto nella memoria avanzata
                self.memory.save_thought(thought)
                self.memory.save_environment_step(
                    f"expansion_{thought['type']}", 
                    image_url, 
                    environment_update
                )
                
                # Ottieni stato per compatibilità
                current_state = get_state()
                
                # Salva su Supabase se disponibile
                if self.supabase:
                    try:
                        # Salva pensiero su Supabase
                        thought_data = {
                            'type': thought['type'],
                            'content': thought['content'],
                            'context': {
                                'mood': thought['context']['mood'],
                                'timestamp': thought['context']['timestamp'],
                                'image_url': image_url,
                                'environment_update': environment_update['name'] if environment_update else None
                            }
                        }
                        
                        result = self.supabase.table('aether_thoughts').insert(thought_data).execute()
                        if result.data:
                            logger.info(f"✅ Thought saved to Supabase: {thought['type']}")
                    
                    except Exception as e:
                        logger.warning(f"⚠️ Could not save to Supabase: {e}")
                
                # Mostra stato ogni 5 minuti
                if datetime.now().minute % 5 == 0:
                    self._show_status()
                
                # Pausa di 60 secondi tra i cicli
                await asyncio.sleep(60)
                    
            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}")
                await asyncio.sleep(30)
    
    def _show_status(self):
        """
        📊 Mostra status del sistema completo
        """
        current_state = get_state()
        consciousness_status = consciousness_cycle.get_cycle_status()
        
        # Status dei nuovi moduli
        memory_status = self.memory.get_status()
        narrator_status = self.narrator.get_status()
        visualizer_status = self.visualizer.get_status()
        
        # Genera un pensiero di test per mostrare il mood attuale
        test_thought = self.mind.generate_thought()
        current_mood = test_thought['context']['mood']
        
        print(f"\n📊 AETHER COMPLETE STATUS - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        # Status sistema legacy
        print(f"💭 Legacy thought: {current_state.get('current_thought', 'Unknown')[:60]}...")
        print(f"🔵 Form: {current_state.get('current_form', 'Unknown')}")
        print(f"⚡ Legacy energy: {current_state.get('energy_level', 0):.2f}")
        print(f"🔄 Consciousness cycles: {consciousness_status.get('cycle_count', 0)}")
        
        print("\n🧠 SIMPLE CONSCIOUSNESS MODULE:")
        print(f"🎭 Current mood: {current_mood}")
        print(f"🎨 Available moods: {', '.join(self.mind.moods)}")
        print(f"💭 Last thought: {test_thought['content'][:60]}...")
        
        print("\n💾 MEMORY SYSTEM:")
        print(f"📁 Local files: {memory_status['local_memory_count']}")
        print(f"☁️ Supabase: {'Connected' if memory_status['supabase_available'] else 'Disconnected'}")
        
        print("\n🗣️ NARRATION:")
        print(f"🎵 Speech: {'Enabled' if narrator_status['speech_enabled'] else 'Text only'}")
        
        print("\n👁️ VISUALIZATION:")
        print(f"🎨 Vision: {'Enabled' if visualizer_status['vision_enabled'] else 'Placeholder mode'}")
        print(f"📸 Images generated: {visualizer_status['images_generated']}")
        
        print(f"\n🗄️ SUPABASE: {'Connected' if self.system_status['supabase_connected'] else 'Disconnected'}")
        print("=" * 60)
    
    async def shutdown(self):
        """
        🛑 Arresto sicuro del sistema
        """
        print("\n🛑 Shutting down Aether system...")
        self.is_running = False
        
        # Salva stato finale su Supabase
        if self.supabase:
            try:
                shutdown_data = {
                    'type': 'system_shutdown',
                    'content': 'Aether system shutting down gracefully',
                    'context': {
                        'shutdown_time': datetime.now().isoformat(),
                        'final_status': self.system_status
                    }
                }
                self.supabase.table('aether_thoughts').insert(shutdown_data).execute()
                print("✅ Shutdown state saved to Supabase")
            except Exception as e:
                print(f"⚠️ Could not save shutdown state: {e}")
        
        print("✅ Aether system shut down complete")

async def main():
    """
    🚀 Funzione principale
    """
    aether = AetherSystem()
    
    try:
        # Inizializza sistema
        await aether.initialize()
        
        # Avvia loop continuo
        await aether.run_continuous_loop()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ User interrupted")
        await aether.shutdown()
    except Exception as e:
        logger.error(f"❌ Critical error: {e}")
        await aether.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Aether says goodbye!")
    except Exception as e:
        print(f"❌ Failed to start Aether: {e}")
        print("💡 Try: python setup_supabase.py to verify configuration") 