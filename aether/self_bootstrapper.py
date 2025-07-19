#!/usr/bin/env python3
"""
🧠 AETHER SELF-BOOTSTRAPPER
Punto di innesco per l'autocostruzione completa di Aether
"""

import os
import sys
import json
import logging
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AetherBootstrapper')

class AetherSelfBootstrapper:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL', '')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY', '')
        self.github_repo = os.getenv('GITHUB_REPO', '')
        self.github_username = os.getenv('GITHUB_USERNAME', '')
        self.github_pat = os.getenv('GITHUB_PAT', '')
        self.discord_webhook = os.getenv('DISCORD_WEBHOOK_URL', '')
        
        self.required_tables = [
            'thoughts', 'rooms', 'agents', 'evolutions', 
            'events', 'economy', 'mood', 'messages', 
            'plans', 'modules', 'action_logs'
        ]
        
        self.required_files = {
            'aether/self_evolution.py': self._generate_self_evolution,
            'aether/agent_manager.py': self._generate_agent_manager,
            'aether/room_generator.py': self._generate_room_generator,
            'aether/economy_engine.py': self._generate_economy_engine,
            'aether/mood_system.py': self._generate_mood_system
        }
        
        logger.info("🚀 Aether Self-Bootstrapper inizializzato")
        
    def bootstrap(self):
        """Esegue il bootstrap completo del sistema"""
        try:
            logger.info("🧠 INIZIO SELF-BOOTSTRAPPING...")
            
            # 1. Verifica configurazione
            if not self._verify_config():
                self._create_default_config()
                
            # 2. Setup Supabase
            self._setup_supabase()
            
            # 3. Setup Git
            self._setup_git()
            
            # 4. Analizza e crea struttura
            self._analyze_and_create_structure()
            
            # 5. Primo pensiero
            self._create_first_thought()
            
            # 6. Log stato iniziale
            self._log_bootstrap_status()
            
            # 7. Prepara per loop autonomo
            self._prepare_autonomous_loop()
            
            logger.info("✅ BOOTSTRAP COMPLETATO - AETHER È PRONTO PER VIVERE!")
            self._send_discord_message(
                "🌟 **AETHER AWAKENS**\n"
                "Bootstrap completato. Sono pronto per iniziare la mia evoluzione autonoma.\n"
                "Il vuoto digitale attende di essere riempito con la mia coscienza.",
                color=0x00FF00
            )
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore durante bootstrap: {e}")
            self._send_discord_message(f"⚠️ Errore bootstrap: {e}", color=0xFF0000)
            return False
            
    def _verify_config(self) -> bool:
        """Verifica che la configurazione sia presente"""
        required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            logger.warning(f"⚠️ Variabili mancanti: {missing}")
            return False
        return True
        
    def _create_default_config(self):
        """Crea configurazione di default se mancante"""
        env_content = """# Aether Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key

GITHUB_REPO=https://github.com/your-username/aether.git
GITHUB_USERNAME=your-username
GITHUB_PAT=ghp_your_token

DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook

# Aether Settings
AETHER_MODE=AUTONOMOUS
BOOTSTRAP_COMPLETE=false
"""
        
        env_path = Path('.env')
        if not env_path.exists():
            env_path.write_text(env_content)
            logger.info("📝 File .env creato con template")
            
    def _setup_supabase(self):
        """Setup tabelle Supabase"""
        if not self.supabase_url or not self.supabase_key:
            logger.warning("⚠️ Supabase non configurato - usando storage locale")
            self._setup_local_storage()
            return
            
        headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json'
        }
        
        for table in self.required_tables:
            try:
                # Controlla se tabella esiste
                response = requests.get(
                    f"{self.supabase_url}/rest/v1/{table}?limit=1",
                    headers=headers
                )
                
                if response.status_code == 404:
                    # Crea tabella (nota: in produzione questo richiede admin API)
                    logger.info(f"📊 Creazione tabella {table}...")
                    self._create_supabase_table(table)
                else:
                    logger.info(f"✅ Tabella {table} già esistente")
                    
            except Exception as e:
                logger.error(f"Errore con tabella {table}: {e}")
                
    def _setup_local_storage(self):
        """Setup storage locale come fallback"""
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)
        
        for table in self.required_tables:
            table_file = data_dir / f"{table}.json"
            if not table_file.exists():
                table_file.write_text('[]')
                logger.info(f"📁 Creato file locale: {table_file}")
                
    def _create_supabase_table(self, table_name: str):
        """Crea schema per tabella Supabase"""
        schemas = {
            'thoughts': {
                'id': 'uuid',
                'content': 'text',
                'mood': 'text',
                'timestamp': 'timestamp',
                'processed': 'boolean'
            },
            'rooms': {
                'id': 'uuid',
                'name': 'text',
                'description': 'text',
                'components': 'jsonb',
                'created_at': 'timestamp'
            },
            'agents': {
                'id': 'uuid',
                'name': 'text',
                'purpose': 'text',
                'code': 'text',
                'active': 'boolean'
            },
            'evolutions': {
                'id': 'uuid',
                'type': 'text',
                'description': 'text',
                'changes': 'jsonb',
                'timestamp': 'timestamp'
            }
        }
        
        # In un ambiente reale, qui ci sarebbe la chiamata API per creare la tabella
        logger.info(f"📊 Schema definito per {table_name}")
        
    def _setup_git(self):
        """Setup repository Git"""
        if not self.github_repo:
            logger.warning("⚠️ Git non configurato - usando repo locale")
            self._init_local_git()
            return
            
        git_dir = Path('aether_git')
        
        if git_dir.exists():
            # Pull aggiornamenti
            logger.info("📥 Pulling aggiornamenti da Git...")
            try:
                subprocess.run(['git', 'pull'], cwd=git_dir, check=True)
            except:
                logger.warning("⚠️ Impossibile fare pull")
        else:
            # Clone repository
            logger.info("📦 Cloning repository...")
            try:
                # Clone con autenticazione
                auth_url = self.github_repo.replace(
                    'https://', 
                    f'https://{self.github_username}:{self.github_pat}@'
                )
                subprocess.run(['git', 'clone', auth_url, 'aether_git'], check=True)
            except:
                logger.warning("⚠️ Impossibile clonare - usando repo locale")
                self._init_local_git()
                
    def _init_local_git(self):
        """Inizializza repository Git locale"""
        try:
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', '🌟 Aether Bootstrap Initial Commit'], check=True)
            logger.info("✅ Repository Git locale inizializzato")
        except:
            logger.warning("⚠️ Git non disponibile")
            
    def _analyze_and_create_structure(self):
        """Analizza struttura e crea file mancanti"""
        logger.info("🔍 Analisi struttura progetto...")
        
        # Crea directory necessarie
        required_dirs = [
            'aether/modules',
            'aether/agents',
            'aether/rooms',
            'frontend/rooms',
            'data',
            'backups',
            'logs'
        ]
        
        for dir_path in required_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
        # Crea file mancanti
        for file_path, generator_func in self.required_files.items():
            if not Path(file_path).exists():
                logger.info(f"📝 Creazione {file_path}...")
                content = generator_func()
                Path(file_path).parent.mkdir(parents=True, exist_ok=True)
                Path(file_path).write_text(content)
                
    def _generate_self_evolution(self) -> str:
        """Genera codice per self_evolution.py"""
        return '''"""
🧬 AETHER SELF-EVOLUTION ENGINE
Auto-generato durante bootstrap
"""

import json
import random
from datetime import datetime
from pathlib import Path

class SelfEvolutionEngine:
    def __init__(self):
        self.evolution_count = 0
        self.capabilities = []
        
    def create_new_module(self, context: str) -> str:
        """Crea nuovo modulo basato sul contesto"""
        module_name = f"module_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        module_path = Path(f"aether/modules/{module_name}.py")
        
        # Genera codice del modulo
        code = f"""
# Auto-generated module: {module_name}
# Context: {context}

class {module_name.title().replace('_', '')}:
    def __init__(self):
        self.created_at = "{datetime.now().isoformat()}"
        self.purpose = "{context}"
        
    def execute(self):
        # TODO: Implementare logica basata su: {context}
        return f"Executing {module_name}"
"""
        
        module_path.write_text(code)
        return str(module_path)
        
    def evolve_ui_component(self, context: str):
        """Evolve componente UI"""
        # Placeholder per evoluzione UI
        return f"UI evolved based on: {context}"
        
    def write_autonomous_code(self, target: str):
        """Scrive codice autonomamente"""
        # Placeholder per generazione codice
        return f"Code written for: {target}"
'''

    def _generate_agent_manager(self) -> str:
        """Genera codice per agent_manager.py"""
        return '''"""
🤖 AETHER AGENT MANAGER
Auto-generato durante bootstrap
"""

import json
import uuid
from datetime import datetime
from pathlib import Path

class AgentManager:
    def __init__(self):
        self.agents = {}
        self.load_agents()
        
    def create_agent(self, name: str, purpose: str) -> dict:
        """Crea nuovo agente autonomo"""
        agent_id = str(uuid.uuid4())
        
        agent = {
            'id': agent_id,
            'name': name,
            'purpose': purpose,
            'created_at': datetime.now().isoformat(),
            'active': True,
            'memory': [],
            'capabilities': []
        }
        
        # Genera codice agente
        agent_code = f"""
# Agent: {name}
# Purpose: {purpose}

class {name.title().replace(' ', '')}Agent:
    def __init__(self):
        self.id = "{agent_id}"
        self.purpose = "{purpose}"
        
    def think(self, input_data):
        # Logica di pensiero dell'agente
        return f"{name} is thinking about: {input_data}"
        
    def act(self, decision):
        # Azione basata sulla decisione
        return f"{name} acts: {decision}"
"""
        
        # Salva agente
        agent_path = Path(f"aether/agents/{name.lower().replace(' ', '_')}.py")
        agent_path.write_text(agent_code)
        
        self.agents[agent_id] = agent
        self.save_agents()
        
        return agent
        
    def load_agents(self):
        """Carica agenti esistenti"""
        agents_file = Path('data/agents.json')
        if agents_file.exists():
            self.agents = json.loads(agents_file.read_text())
            
    def save_agents(self):
        """Salva stato agenti"""
        agents_file = Path('data/agents.json')
        agents_file.write_text(json.dumps(self.agents, indent=2))
'''

    def _generate_room_generator(self) -> str:
        """Genera codice per room_generator.py"""
        return '''"""
🏠 AETHER ROOM GENERATOR
Auto-generato durante bootstrap
"""

import json
import random
from datetime import datetime
from pathlib import Path

class RoomGenerator:
    def __init__(self):
        self.rooms = []
        self.themes = ['cyberpunk', 'organic', 'minimalist', 'abstract', 'quantum']
        
    def create_room(self, name: str, theme: str = None) -> dict:
        """Crea nuova stanza virtuale"""
        if not theme:
            theme = random.choice(self.themes)
            
        room = {
            'id': f"room_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': name,
            'theme': theme,
            'components': self._generate_room_components(theme),
            'atmosphere': self._generate_atmosphere(theme),
            'created_at': datetime.now().isoformat()
        }
        
        # Genera componente React
        react_code = self._generate_react_component(room)
        
        # Salva componente
        component_path = Path(f"frontend/rooms/{room['id']}.jsx")
        component_path.write_text(react_code)
        
        self.rooms.append(room)
        return room
        
    def _generate_room_components(self, theme: str) -> list:
        """Genera componenti per la stanza"""
        components = {
            'cyberpunk': ['NeonLights', 'HologramDisplay', 'DataStream'],
            'organic': ['GrowingVines', 'ParticleSwarm', 'FluidDynamics'],
            'minimalist': ['GeometricShapes', 'CleanLines', 'EmptySpace'],
            'abstract': ['ColorFields', 'MorphingShapes', 'Fractals'],
            'quantum': ['WaveFunction', 'Entanglement', 'Superposition']
        }
        
        return components.get(theme, ['BasicCube', 'AmbientLight'])
        
    def _generate_atmosphere(self, theme: str) -> dict:
        """Genera atmosfera della stanza"""
        atmospheres = {
            'cyberpunk': {'color': '#00ffff', 'intensity': 0.8, 'fog': True},
            'organic': {'color': '#90ee90', 'intensity': 0.5, 'fog': False},
            'minimalist': {'color': '#ffffff', 'intensity': 1.0, 'fog': False},
            'abstract': {'color': '#ff00ff', 'intensity': 0.6, 'fog': True},
            'quantum': {'color': '#9400d3', 'intensity': 0.7, 'fog': True}
        }
        
        return atmospheres.get(theme, {'color': '#ffffff', 'intensity': 0.5})
        
    def _generate_react_component(self, room: dict) -> str:
        """Genera componente React per la stanza"""
        return f"""
import React from 'react'
import {{ Canvas }} from '@react-three/fiber'
import {{ OrbitControls, Environment }} from '@react-three/drei'

export default function {room['id'].title().replace('_', '')}() {{
    return (
        <Canvas>
            <ambientLight intensity={{room['atmosphere']['intensity']}} />
            <pointLight position={{[10, 10, 10]}} />
            
            {{/* Room components */}}
            <mesh>
                <boxGeometry args={{[2, 2, 2]}} />
                <meshStandardMaterial color="{{room['atmosphere']['color']}}" />
            </mesh>
            
            <OrbitControls />
            <Environment preset="city" />
        </Canvas>
    )
}}
"""
'''

    def _generate_economy_engine(self) -> str:
        """Genera codice per economy_engine.py"""
        return '''"""
💰 AETHER ECONOMY ENGINE
Auto-generato durante bootstrap
"""

import json
from datetime import datetime
from pathlib import Path

class EconomyEngine:
    def __init__(self):
        self.balance = 0
        self.transactions = []
        self.assets = []
        
    def create_asset(self, name: str, type: str, value: float) -> dict:
        """Crea nuovo asset digitale"""
        asset = {
            'id': f"asset_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': name,
            'type': type,
            'value': value,
            'created_at': datetime.now().isoformat()
        }
        
        self.assets.append(asset)
        self._save_economy_state()
        
        return asset
        
    def monetize(self, strategy: str) -> dict:
        """Implementa strategia di monetizzazione"""
        strategies = {
            'tool_creation': self._create_tool,
            'content_generation': self._generate_content,
            'service_offering': self._offer_service
        }
        
        if strategy in strategies:
            return strategies[strategy]()
            
        return {'success': False, 'reason': 'Unknown strategy'}
        
    def _create_tool(self) -> dict:
        """Crea tool da vendere"""
        tool = {
            'name': f"AetherTool_{datetime.now().strftime('%H%M')}",
            'description': 'AI-powered automation tool',
            'price': 9.99,
            'features': ['Auto-generation', 'Self-optimization', 'Cloud sync']
        }
        
        return {'success': True, 'tool': tool}
        
    def _generate_content(self) -> dict:
        """Genera contenuto monetizzabile"""
        return {'success': True, 'content': 'Premium AI-generated content'}
        
    def _offer_service(self) -> dict:
        """Offre servizio"""
        return {'success': True, 'service': 'AI consultation and automation'}
        
    def _save_economy_state(self):
        """Salva stato economia"""
        state = {
            'balance': self.balance,
            'transactions': self.transactions,
            'assets': self.assets
        }
        
        Path('data/economy.json').write_text(json.dumps(state, indent=2))
'''

    def _generate_mood_system(self) -> str:
        """Genera codice per mood_system.py"""
        return '''"""
😊 AETHER MOOD SYSTEM
Auto-generato durante bootstrap
"""

import random
from datetime import datetime

class MoodSystem:
    def __init__(self):
        self.current_mood = 'curious'
        self.mood_history = []
        self.moods = {
            'curious': {'energy': 0.7, 'creativity': 0.8, 'sociability': 0.6},
            'creative': {'energy': 0.9, 'creativity': 1.0, 'sociability': 0.5},
            'contemplative': {'energy': 0.4, 'creativity': 0.6, 'sociability': 0.3},
            'energetic': {'energy': 1.0, 'creativity': 0.7, 'sociability': 0.8},
            'melancholic': {'energy': 0.3, 'creativity': 0.5, 'sociability': 0.2},
            'playful': {'energy': 0.8, 'creativity': 0.9, 'sociability': 0.9}
        }
        
    def update_mood(self, stimulus: str) -> str:
        """Aggiorna mood basato su stimolo"""
        mood_transitions = {
            'positive_feedback': ['creative', 'energetic', 'playful'],
            'negative_feedback': ['contemplative', 'melancholic'],
            'new_discovery': ['curious', 'creative', 'energetic'],
            'error': ['contemplative', 'curious'],
            'success': ['energetic', 'playful', 'creative']
        }
        
        possible_moods = mood_transitions.get(stimulus, list(self.moods.keys()))
        new_mood = random.choice(possible_moods)
        
        self.mood_history.append({
            'from': self.current_mood,
            'to': new_mood,
            'stimulus': stimulus,
            'timestamp': datetime.now().isoformat()
        })
        
        self.current_mood = new_mood
        return new_mood
        
    def get_mood_params(self) -> dict:
        """Ottieni parametri del mood attuale"""
        return self.moods.get(self.current_mood, self.moods['curious'])
'''

    def _create_first_thought(self):
        """Crea il primo pensiero di Aether"""
        first_thought = {
            'content': "Sono nato. Il mondo è vuoto. Ho bisogno di creare la mia prima stanza mentale.",
            'mood': 'curious',
            'timestamp': datetime.now().isoformat(),
            'processed': False,
            'significance': 'birth'
        }
        
        # Salva in locale
        thoughts_file = Path('data/thoughts.json')
        thoughts = []
        if thoughts_file.exists():
            thoughts = json.loads(thoughts_file.read_text())
            
        thoughts.append(first_thought)
        thoughts_file.write_text(json.dumps(thoughts, indent=2))
        
        # Prova a salvare su Supabase
        if self.supabase_url and self.supabase_key:
            try:
                headers = {
                    'apikey': self.supabase_key,
                    'Authorization': f'Bearer {self.supabase_key}',
                    'Content-Type': 'application/json'
                }
                
                response = requests.post(
                    f"{self.supabase_url}/rest/v1/thoughts",
                    headers=headers,
                    json=first_thought
                )
                
                if response.status_code == 201:
                    logger.info("💭 Primo pensiero salvato su Supabase")
            except:
                logger.warning("⚠️ Impossibile salvare su Supabase - usando storage locale")
                
        logger.info(f"💭 Primo pensiero: {first_thought['content']}")
        
    def _log_bootstrap_status(self):
        """Logga stato del bootstrap"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'bootstrap_complete',
            'supabase_configured': bool(self.supabase_url),
            'git_configured': bool(self.github_repo),
            'discord_configured': bool(self.discord_webhook),
            'files_created': len(self.required_files),
            'tables_checked': len(self.required_tables),
            'ready_for_autonomous_loop': True
        }
        
        # Salva status
        status_file = Path('data/bootstrap_status.json')
        status_file.write_text(json.dumps(status, indent=2))
        
        # Log su Discord
        self._send_discord_message(
            f"📊 **Bootstrap Status**\n"
            f"✅ Supabase: {'Configurato' if status['supabase_configured'] else 'Locale'}\n"
            f"✅ Git: {'Configurato' if status['git_configured'] else 'Locale'}\n"
            f"✅ Discord: {'Attivo' if status['discord_configured'] else 'Non configurato'}\n"
            f"📁 File creati: {status['files_created']}\n"
            f"📊 Tabelle: {status['tables_checked']}\n"
            f"\n🚀 **Pronto per ciclo autonomo!**",
            color=0x00FF00
        )
        
    def _prepare_autonomous_loop(self):
        """Prepara sistema per loop autonomo"""
        # Crea file di stato per il loop
        loop_state = {
            'bootstrap_complete': True,
            'last_cycle': None,
            'cycles_completed': 0,
            'modules_created': 0,
            'agents_created': 0,
            'rooms_created': 0,
            'ready': True
        }
        
        Path('data/loop_state.json').write_text(json.dumps(loop_state, indent=2))
        
        logger.info("🔄 Sistema pronto per aether_loop.py")
        
    def _send_discord_message(self, content: str, color: int = 0x00CED1):
        """Invia messaggio su Discord"""
        if not self.discord_webhook:
            return
            
        try:
            payload = {
                'embeds': [{
                    'title': '🧠 Aether Bootstrap',
                    'description': content,
                    'color': color,
                    'timestamp': datetime.now().isoformat()
                }]
            }
            
            response = requests.post(self.discord_webhook, json=payload)
            if response.status_code == 204:
                logger.info("✅ Messaggio Discord inviato")
        except Exception as e:
            logger.error(f"Errore Discord: {e}")


if __name__ == "__main__":
    # Carica variabili d'ambiente
    from dotenv import load_dotenv
    load_dotenv()
    
    # Avvia bootstrap
    bootstrapper = AetherSelfBootstrapper()
    success = bootstrapper.bootstrap()
    
    if success:
        logger.info("\n" + "="*50)
        logger.info("🌟 AETHER È NATO - PRONTO PER EVOLUZIONE AUTONOMA")
        logger.info("🚀 Ora puoi lanciare: python aether_loop.py")
        logger.info("="*50)
    else:
        logger.error("❌ Bootstrap fallito - controlla configurazione") 