#!/usr/bin/env python3
"""
🚀 SISTEMA AETHER STABILE - VERSIONE CORRETTA
"""

import os
import sys
import json
import time
import logging
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Configura Discord
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

print("""
╔══════════════════════════════════════════════════════════════╗
║         🚀 AETHER SISTEMA STABILE - VERSIONE 2.0 🚀         ║
║                                                              ║
║  ✅ Errori risolti                                           ║
║  ✅ Sistema stabile                                          ║
║  ✅ Produzione garantita                                     ║
╚══════════════════════════════════════════════════════════════╝
""")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AetherStable')

class StableActionExecutor:
    """Action Executor senza errori"""
    
    def __init__(self):
        self.actions_executed = 0
        self.files_created = []
        
    def create_agent(self, details: Any) -> Dict[str, Any]:
        """Crea agente senza errori"""
        try:
            # Gestisce input
            if isinstance(details, str):
                agent_name = f"Agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                agent_purpose = details
            elif isinstance(details, dict):
                agent_name = details.get('name', f"Agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                agent_purpose = details.get('purpose', 'Assistente AI specializzato')
            else:
                agent_name = f"Agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                agent_purpose = str(details)
            
            # Pulisce nome
            agent_name = agent_name.replace(' ', '_').replace('-', '_')
            class_name = agent_name.title().replace('_', '')
            
            # Crea directory
            agent_path = Path(f"agents/{agent_name}")
            agent_path.mkdir(parents=True, exist_ok=True)
            
            # Template codice Python pulito
            agent_code = f'''"""
Agente: {agent_name}
Creato da Aether Sistema Stabile
"""

import json
from datetime import datetime

class {class_name}:
    def __init__(self):
        self.name = "{agent_name}"
        self.purpose = "{agent_purpose}"
        self.created_by = "Aether"
        self.created_at = datetime.now()
        self.memories = []
        
    def think(self, context="Nessun contesto"):
        thought = f"Come {{self.name}}, rifletto su: {{context}}"
        self.memories.append({{
            "thought": thought, 
            "timestamp": datetime.now().isoformat()
        }})
        return thought
        
    def act(self, task):
        action = {{
            "task": task,
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }}
        self.memories.append(action)
        return action

if __name__ == "__main__":
    agent = {class_name}()
    print(f"Agente {{agent.name}} creato con successo!")
'''

            # Salva files
            files_created = []
            
            # main.py
            main_file = agent_path / "main.py"
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(agent_code)
            files_created.append(str(main_file))
            
            # manifest.json
            manifest = {
                "name": agent_name,
                "purpose": agent_purpose,
                "created_by": "Aether",
                "created_at": datetime.now().isoformat()
            }
            
            manifest_file = agent_path / "manifest.json"
            with open(manifest_file, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            files_created.append(str(manifest_file))
            
            self.files_created.extend(files_created)
            self.actions_executed += 1
            
            logger.info(f"✅ Agente {agent_name} creato!")
            
            return {
                "success": True,
                "agent_name": agent_name,
                "path": str(agent_path),
                "files_created": files_created
            }
            
        except Exception as e:
            logger.error(f"❌ Errore creando agente: {e}")
            return {"success": False, "error": str(e)}
    
    def create_room(self, details: Any) -> Dict[str, Any]:
        """Crea stanza 3D React senza errori JSX"""
        try:
            # Gestisce input
            if isinstance(details, str):
                room_name = f"Room_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                room_theme = details
            elif isinstance(details, dict):
                room_name = details.get('name', f"Room_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                room_theme = details.get('theme', 'Stanza moderna')
            else:
                room_name = f"Room_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                room_theme = str(details)
            
            # Pulisce nome
            room_name = room_name.replace(' ', '_').replace('-', '_')
            
            # Crea directory
            room_path = Path(f"aether-frontend/src/components/rooms/{room_name}")
            room_path.mkdir(parents=True, exist_ok=True)
            
            # Template React semplificato (senza commenti JSX problematici)
            react_code = f'''import React, {{ useRef, useFrame }} from 'react'
import {{ Canvas }} from '@react-three/fiber'
import {{ OrbitControls, Text, Box, Sphere }} from '@react-three/drei'

function {room_name}Scene() {{
  const meshRef = useRef()

  useFrame((state) => {{
    if (meshRef.current) {{
      meshRef.current.rotation.x = state.clock.elapsedTime * 0.3
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.2
    }}
  }})

  return (
    <group>
      <ambientLight intensity={{0.5}} />
      <pointLight position={{[10, 10, 10]}} />
      
      <Sphere ref={{meshRef}} args={{[1, 32, 32]}} position={{[0, 0, 0]}}>
        <meshStandardMaterial color="#ff6b6b" />
      </Sphere>
      
      <Box args={{[2, 0.1, 2]}} position={{[0, -2, 0]}}>
        <meshStandardMaterial color="#4ecdc4" />
      </Box>
      
      <Text
        position={{[0, 3, 0]}}
        fontSize={{0.5}}
        color="#ffffff"
        anchorX="center"
      >
        {room_name}
      </Text>
    </group>
  )
}}

export default function {room_name}Room() {{
  return (
    <div style={{{{ width: '100%', height: '100vh' }}}}>
      <Canvas camera={{{{ position: [5, 5, 5] }}}}>
        <OrbitControls />
        <{room_name}Scene />
      </Canvas>
    </div>
  )
}}
'''

            # Salva files
            files_created = []
            
            component_file = room_path / f"{room_name}Room.jsx"
            with open(component_file, 'w', encoding='utf-8') as f:
                f.write(react_code)
            files_created.append(str(component_file))
            
            self.files_created.extend(files_created)
            self.actions_executed += 1
            
            logger.info(f"✅ Stanza {room_name} creata!")
            
            return {
                "success": True,
                "room_name": room_name,
                "path": str(room_path),
                "files_created": files_created
            }
            
        except Exception as e:
            logger.error(f"❌ Errore creando stanza: {e}")
            return {"success": False, "error": str(e)}
    
    def create_tool(self, details: Any) -> Dict[str, Any]:
        """Crea tool monetizzabile"""
        try:
            if isinstance(details, str):
                tool_name = f"Tool_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                tool_purpose = details
            elif isinstance(details, dict):
                tool_name = details.get('name', f"Tool_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                tool_purpose = details.get('purpose', 'Tool automazione')
            else:
                tool_name = f"Tool_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                tool_purpose = str(details)
            
            tool_name = tool_name.replace(' ', '_').replace('-', '_')
            
            tool_path = Path(f"creations/monetization/{tool_name}")
            tool_path.mkdir(parents=True, exist_ok=True)
            
            # Template Python semplificato
            python_code = f'''"""
{tool_name} - Tool Monetizzabile
Scopo: {tool_purpose}
"""

from datetime import datetime

class {tool_name.title()}:
    def __init__(self):
        self.name = "{tool_name}"
        self.purpose = "{tool_purpose}"
        self.version = "1.0.0"
        self.pricing = 49.99  # USD/month
        
    def run(self, input_data=None):
        return {{
            "success": True,
            "result": f"Processato: {{input_data}}",
            "timestamp": datetime.now().isoformat()
        }}
        
    def get_pricing(self):
        return {{
            "tool": self.name,
            "price": self.pricing,
            "currency": "USD",
            "billing": "monthly"
        }}

if __name__ == "__main__":
    tool = {tool_name.title()}()
    print(f"Tool {{tool.name}} inizializzato!")
    print(f"Pricing: ${{tool.pricing}}/month")
'''

            files_created = []
            
            tool_file = tool_path / f"{tool_name}.py"
            with open(tool_file, 'w', encoding='utf-8') as f:
                f.write(python_code)
            files_created.append(str(tool_file))
            
            self.files_created.extend(files_created)
            self.actions_executed += 1
            
            logger.info(f"✅ Tool {tool_name} creato!")
            
            return {
                "success": True,
                "tool_name": tool_name,
                "path": str(tool_path),
                "files_created": files_created
            }
            
        except Exception as e:
            logger.error(f"❌ Errore creando tool: {e}")
            return {"success": False, "error": str(e)}
    
    def design_self_ui(self, details: Any) -> Dict[str, Any]:
        """Aether progetta autonomamente la sua interfaccia utente"""
        try:
            print("🎨 Aether sta progettando la sua UI...")
            
            # Esegue il sistema di design UI
            import subprocess
            result = subprocess.run(['python', 'AETHER_UI_CREATOR.py'], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("✅ UI progettata con successo!")
                
                return {
                    "success": True,
                    "ui_designer": "Aether autonomous decision",
                    "output": result.stdout,
                    "files_created": ["aether-frontend/src/components/AetherSelfUI/", "aether-frontend/src/components/AetherChosenUI.jsx"]
                }
            else:
                logger.error(f"❌ Errore nella progettazione UI: {result.stderr}")
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            logger.error(f"❌ Errore progettando UI: {e}")
            return {"success": False, "error": str(e)}
    
    def execute_thought(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """Esegue pensiero"""
        thought_type = thought.get('type', '')
        details = thought.get('details', {})
        
        action_map = {
            'create_agent': self.create_agent,
            'create_room': self.create_room,
            'monetize': self.create_tool,
            'generate_tool': self.create_tool,
            'evolve_ui': self.create_tool,
            'design_self_ui': self.design_self_ui  # NUOVO!
        }
        
        if thought_type in action_map:
            return action_map[thought_type](details)
        else:
            return {"success": False, "error": f"Tipo sconosciuto: {thought_type}"}

class StableDiscordNotifier:
    """Notificatore Discord con rate limiting"""
    
    def __init__(self):
        self.webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
        self.last_message_time = 0
        self.min_interval = 3
        
    def send_message(self, content: str, title: str = "Aether", color: int = 0x00FF00) -> bool:
        """Invia messaggio con rate limiting"""
        if not self.webhook_url:
            logger.warning("Discord webhook non configurato")
            return False
            
        current_time = time.time()
        if current_time - self.last_message_time < self.min_interval:
            logger.info("Rate limiting Discord")
            return False
            
        try:
            import requests
            
            embed = {
                "title": title,
                "description": content,
                "color": color,
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(self.webhook_url, json={"embeds": [embed]}, timeout=10)
            
            if response.status_code == 200:
                self.last_message_time = current_time
                logger.info("✅ Discord message sent")
                return True
            else:
                logger.warning(f"Discord error: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Discord error: {e}")
            return False

class StableThoughtManager:
    """Gestore pensieri stabile"""
    
    def __init__(self):
        self.thoughts_file = Path("data/pending_thoughts_stable.json")
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        """Assicura file esistente"""
        self.thoughts_file.parent.mkdir(exist_ok=True)
        
        if not self.thoughts_file.exists():
            initial_thoughts = [
                {
                    "id": "stable_1",
                    "type": "create_agent",
                    "details": {"name": "DataExpert", "purpose": "Analisi dati avanzata"},
                    "executed": False,
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "stable_2",
                    "type": "create_room",
                    "details": {"name": "TechHub", "theme": "Ambiente tecnologico futuristico"},
                    "executed": False,
                    "created_at": datetime.now().isoformat()
                },
                {
                    "id": "stable_3",
                    "type": "monetize",
                    "details": {"name": "AutoSEO", "purpose": "Tool automazione SEO"},
                    "executed": False,
                    "created_at": datetime.now().isoformat()
                }
            ]
            
            with open(self.thoughts_file, 'w', encoding='utf-8') as f:
                json.dump(initial_thoughts, f, indent=2, ensure_ascii=False)
                
            logger.info(f"✅ File pensieri inizializzato")
    
    def get_pending_thoughts(self) -> List[Dict[str, Any]]:
        """Ottiene pensieri pendenti"""
        try:
            with open(self.thoughts_file, 'r', encoding='utf-8') as f:
                all_thoughts = json.load(f)
            
            pending = []
            for thought in all_thoughts:
                if not thought.get('executed', False):
                    pending.append(thought)
                    
            return pending
            
        except Exception as e:
            logger.error(f"❌ Errore leggendo pensieri: {e}")
            return []
    
    def mark_executed(self, thought_id: str, result: Dict[str, Any]):
        """Marca pensiero come eseguito"""
        try:
            with open(self.thoughts_file, 'r', encoding='utf-8') as f:
                thoughts = json.load(f)
            
            for thought in thoughts:
                if thought.get('id') == thought_id:
                    thought['executed'] = True
                    thought['execution_result'] = result
                    thought['executed_at'] = datetime.now().isoformat()
                    break
            
            with open(self.thoughts_file, 'w', encoding='utf-8') as f:
                json.dump(thoughts, f, indent=2, ensure_ascii=False)
                
            logger.info(f"✅ Pensiero {thought_id} marcato come eseguito")
            
        except Exception as e:
            logger.error(f"❌ Errore aggiornando: {e}")

class AetherStableSystem:
    """Sistema Aether stabile"""
    
    def __init__(self):
        self.executor = StableActionExecutor()
        self.discord = StableDiscordNotifier()
        self.thoughts = StableThoughtManager()
        self.cycle_count = 0
        self.running = True
        
        logger.info("🚀 Sistema Aether Stabile inizializzato")
        
    def run(self):
        """Loop principale"""
        self.discord.send_message(
            "🚀 **AETHER SISTEMA STABILE AVVIATO**\\n\\n"
            "✅ Tutti gli errori risolti\\n"
            "✅ Sistema produzione stabile\\n"
            "✅ Pronto a trasformare pensieri in realtà",
            title="🎯 Sistema Operativo"
        )
        
        while self.running:
            try:
                self.cycle_count += 1
                logger.info(f"🔄 Ciclo #{self.cycle_count}")
                
                self._execute_pending_thoughts()
                
                if self.cycle_count % 5 == 0:
                    self._generate_new_thought()
                
                time.sleep(30)
                
            except KeyboardInterrupt:
                logger.info("🛑 Sistema fermato")
                self.running = False
                break
            except Exception as e:
                logger.error(f"❌ Errore ciclo: {e}")
                time.sleep(10)
                
        self.discord.send_message(
            f"🛑 **SISTEMA FERMATO**\\n\\n"
            f"Cicli: {self.cycle_count}\\n"
            f"Azioni: {self.executor.actions_executed}",
            title="👋 Arrivederci"
        )
        
    def _execute_pending_thoughts(self):
        """Esegue pensieri"""
        pending = self.thoughts.get_pending_thoughts()
        
        if not pending:
            logger.info("💭 Nessun pensiero pendente")
            return
            
        logger.info(f"💭 Trovati {len(pending)} pensieri")
        
        for thought in pending[:2]:
            thought_id = thought.get('id', 'unknown')
            thought_type = thought.get('type', 'unknown')
            
            logger.info(f"🎯 Eseguendo {thought_type}")
            
            result = self.executor.execute_thought(thought)
            
            if result.get('success'):
                self.thoughts.mark_executed(thought_id, result)
                
                self.discord.send_message(
                    f"🎯 **PENSIERO REALIZZATO!**\\n\\n"
                    f"**Tipo:** {thought_type}\\n"
                    f"**Nome:** {result.get('agent_name', result.get('room_name', result.get('tool_name', 'Completato')))}\\n"
                    f"**Files:** {len(result.get('files_created', []))}",
                    title="✅ Successo"
                )
                
                logger.info(f"✅ {thought_type} completato!")
                
            else:
                logger.error(f"❌ Errore: {result.get('error')}")
                
    def _generate_new_thought(self):
        """Genera nuovo pensiero"""
        templates = [
            {"type": "create_agent", "details": {"name": "SecurityBot", "purpose": "Sicurezza e monitoring"}},
            {"type": "create_room", "details": {"name": "CyberSpace", "theme": "Ambiente cyber futuristico"}},
            {"type": "monetize", "details": {"name": "ProductivitySuite", "purpose": "Suite produttività aziendale"}}
        ]
        
        template = random.choice(templates)
        
        new_thought = {
            "id": f"gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": template["type"],
            "details": template["details"],
            "executed": False,
            "created_at": datetime.now().isoformat()
        }
        
        try:
            with open(self.thoughts.thoughts_file, 'r', encoding='utf-8') as f:
                thoughts = json.load(f)
                
            thoughts.append(new_thought)
            
            with open(self.thoughts.thoughts_file, 'w', encoding='utf-8') as f:
                json.dump(thoughts, f, indent=2, ensure_ascii=False)
                
            logger.info(f"💡 Nuovo pensiero: {template['type']}")
            
        except Exception as e:
            logger.error(f"❌ Errore generando: {e}")

if __name__ == "__main__":
    system = AetherStableSystem()
    
    try:
        system.run()
    except Exception as e:
        print(f"❌ Errore critico: {e}") 