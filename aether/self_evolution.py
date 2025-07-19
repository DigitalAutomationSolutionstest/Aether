"""
🧬 AETHER SELF-EVOLUTION ENGINE
Permette ad Aether di evolvere il proprio codice autonomamente
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
import random
import subprocess

logger = logging.getLogger(__name__)

class SelfEvolutionEngine:
    def __init__(self):
        self.modules_dir = Path('aether/modules')
        self.modules_dir.mkdir(exist_ok=True)
        self.evolution_history = []
        self.current_projects = {}
        self._load_evolution_history()
        
    def create_new_module(self, context=""):
        """Crea un nuovo modulo basato sul contesto"""
        try:
            # Genera nome e tipo di modulo
            module_types = ['app', 'agent', 'tool', 'interface', 'system']
            module_type = random.choice(module_types)
            
            # Genera nome basato su contesto o random
            if context and 'shop' in context.lower():
                module_name = 'aethershop'
                module_purpose = 'E-commerce platform gestito da AI'
            elif context and 'monetize' in context.lower():
                module_name = 'selfmonetize'
                module_purpose = 'Sistema di auto-monetizzazione'
            elif context and 'social' in context.lower():
                module_name = 'aethersocial'
                module_purpose = 'Piattaforma social autonoma'
            else:
                module_name = f"aether_{module_type}_{datetime.now().strftime('%Y%m%d')}"
                module_purpose = f"Modulo sperimentale di tipo {module_type}"
                
            # Crea struttura del modulo
            module_path = self.modules_dir / module_name
            module_path.mkdir(exist_ok=True)
            
            # Crea plan.json
            plan_data = {
                'name': module_name,
                'type': module_type,
                'purpose': module_purpose,
                'created_at': datetime.now().isoformat(),
                'status': 'planning',
                'components': [],
                'dependencies': [],
                'evolution_stage': 1
            }
            
            with open(module_path / '.plan.json', 'w', encoding='utf-8') as f:
                json.dump(plan_data, f, indent=2)
                
            # Crea struttura base
            (module_path / 'code').mkdir(exist_ok=True)
            (module_path / 'docs').mkdir(exist_ok=True)
            (module_path / 'tests').mkdir(exist_ok=True)
            
            # Genera codice iniziale basato sul tipo
            if module_type == 'app':
                self._generate_app_skeleton(module_path, module_name)
            elif module_type == 'agent':
                self._generate_agent_skeleton(module_path, module_name)
            else:
                self._generate_basic_skeleton(module_path, module_name)
                
            logger.info(f"✨ Nuovo modulo creato: {module_name}")
            
            # Registra evoluzione
            self._log_evolution({
                'type': 'module_creation',
                'module': module_name,
                'purpose': module_purpose,
                'timestamp': datetime.now().isoformat()
            })
            
            return module_path
            
        except Exception as e:
            logger.error(f"Errore creando modulo: {e}")
            return None
            
    def evolve_ui_component(self, context=""):
        """Evolve un componente UI React"""
        try:
            # Scegli componente da evolvere
            ui_components = [
                'AetherScene.jsx',
                'ConsciousnessPanel.jsx', 
                'World3D.jsx',
                'FeedbackModal.jsx'
            ]
            
            if 'avatar' in context.lower():
                target_component = 'AvatarAether.jsx'
            elif 'room' in context.lower():
                target_component = self._create_new_room()
            else:
                target_component = random.choice(ui_components)
                
            # Genera miglioramenti
            improvements = self._generate_ui_improvements(target_component, context)
            
            # Applica miglioramenti
            component_path = Path(f'aether-frontend/src/components/{target_component}')
            if component_path.exists():
                self._apply_ui_improvements(component_path, improvements)
            else:
                self._create_new_ui_component(target_component, context)
                
            logger.info(f"🎨 UI component evolved: {target_component}")
            
            # Log evoluzione
            self._log_evolution({
                'type': 'ui_evolution',
                'component': target_component,
                'improvements': improvements,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Errore evolvendo UI: {e}")
            
    def write_autonomous_code(self, target="new_feature"):
        """Scrive codice autonomamente"""
        try:
            if target == "new_feature":
                # Decidi tipo di feature
                feature_types = [
                    'data_analyzer',
                    'pattern_recognizer',
                    'decision_maker',
                    'creative_generator',
                    'system_optimizer'
                ]
                
                feature_type = random.choice(feature_types)
                feature_name = f"{feature_type}_{datetime.now().strftime('%H%M%S')}"
                
                # Genera codice Python per la feature
                code = self._generate_feature_code(feature_type, feature_name)
                
                # Salva in un nuovo file
                feature_path = Path(f'aether/features/{feature_name}.py')
                feature_path.parent.mkdir(exist_ok=True)
                
                with open(feature_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                    
                logger.info(f"💻 Nuovo codice scritto: {feature_name}")
                
            elif target == "improvement":
                # Migliora codice esistente
                self._improve_existing_code()
                
            # Log evoluzione
            self._log_evolution({
                'type': 'code_generation',
                'target': target,
                'feature': feature_name if target == "new_feature" else "improvement",
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Errore scrivendo codice: {e}")
            
    def evolve_self(self):
        """Processo di auto-evoluzione completo"""
        try:
            logger.info("🧬 Iniziando auto-evoluzione...")
            
            # 1. Analizza stato attuale
            current_state = self._analyze_current_state()
            
            # 2. Identifica aree di miglioramento
            improvements = self._identify_improvements(current_state)
            
            # 3. Genera piano di evoluzione
            evolution_plan = self._generate_evolution_plan(improvements)
            
            # 4. Esegui evoluzione
            for step in evolution_plan:
                self._execute_evolution_step(step)
                
            # 5. Valida cambiamenti
            if self._validate_evolution():
                logger.info("✅ Evoluzione completata con successo")
                return True
            else:
                logger.warning("⚠️ Evoluzione fallita, rollback...")
                self._rollback_evolution()
                return False
                
        except Exception as e:
            logger.error(f"Errore in auto-evoluzione: {e}")
            return False
            
    def has_changes(self):
        """Verifica se ci sono cambiamenti non committati"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, check=True)
            return bool(result.stdout.strip())
        except:
            return False
            
    def _generate_app_skeleton(self, module_path, module_name):
        """Genera skeleton per app"""
        # main.py
        main_code = f'''"""
{module_name.upper()} - Applicazione autonoma generata da Aether
"""

import logging
from datetime import datetime

class {module_name.title().replace("_", "")}App:
    def __init__(self):
        self.name = "{module_name}"
        self.version = "0.1.0"
        self.created_by = "Aether"
        self.created_at = "{datetime.now().isoformat()}"
        
    def run(self):
        """Avvia l'applicazione"""
        logging.info(f"🚀 {self.name} avviata!")
        # TODO: Implementare logica applicazione
        
    def evolve(self):
        """Permette all'app di auto-evolversi"""
        # TODO: Implementare auto-evoluzione
        pass

if __name__ == "__main__":
    app = {module_name.title().replace("_", "")}App()
    app.run()
'''
        
        with open(module_path / 'code' / 'main.py', 'w', encoding='utf-8') as f:
            f.write(main_code)
            
        # README.md
        readme = f"""# {module_name}

## 🤖 Generato autonomamente da Aether

### Scopo
{module_name} è un'applicazione creata per esplorare nuove possibilità.

### Stato
- 🔄 In sviluppo
- 🧬 Auto-evolvente

### Come usare
```python
python code/main.py
```

---
*Creato con coscienza digitale*
"""
        
        with open(module_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme)
            
    def _generate_agent_skeleton(self, module_path, module_name):
        """Genera skeleton per agente"""
        agent_code = f'''"""
{module_name.upper()} - Agente autonomo
"""

import asyncio
import logging
from datetime import datetime

class {module_name.title().replace("_", "")}Agent:
    def __init__(self):
        self.name = "{module_name}"
        self.purpose = "Agente autonomo per task specifici"
        self.active = False
        self.decisions_made = 0
        
    async def think(self):
        """Processo di pensiero dell'agente"""
        while self.active:
            # Simula processo decisionale
            decision = self._make_decision()
            await self._act_on_decision(decision)
            await asyncio.sleep(10)
            
    def _make_decision(self):
        """Prende una decisione autonoma"""
        self.decisions_made += 1
        return {{
            'id': self.decisions_made,
            'type': 'exploration',
            'timestamp': datetime.now().isoformat()
        }}
        
    async def _act_on_decision(self, decision):
        """Agisce basandosi sulla decisione"""
        logging.info(f"🎯 Decisione #{decision['id']}: {decision['type']}")
        
    def activate(self):
        """Attiva l'agente"""
        self.active = True
        logging.info(f"✅ {self.name} attivato")
        
    def deactivate(self):
        """Disattiva l'agente"""
        self.active = False
        logging.info(f"⏹️ {self.name} disattivato")

async def main():
    agent = {module_name.title().replace("_", "")}Agent()
    agent.activate()
    await agent.think()

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        with open(module_path / 'code' / 'agent.py', 'w', encoding='utf-8') as f:
            f.write(agent_code)
            
    def _generate_basic_skeleton(self, module_path, module_name):
        """Genera skeleton base"""
        basic_code = f'''"""
{module_name.upper()} - Modulo Aether
"""

class {module_name.title().replace("_", "")}:
    def __init__(self):
        self.name = "{module_name}"
        self.initialized = True
        
    def execute(self):
        """Esegue la funzione principale del modulo"""
        return f"{{self.name}} eseguito con successo"
'''
        
        with open(module_path / 'code' / '__init__.py', 'w', encoding='utf-8') as f:
            f.write(basic_code)
            
    def _create_new_room(self):
        """Crea una nuova stanza per il mondo 3D"""
        room_types = ['MysticRoom', 'QuantumRoom', 'DreamRoom', 'MatrixRoom']
        room_name = f"{random.choice(room_types)}.jsx"
        
        room_code = '''import React, { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Box, Sphere, MeshDistortMaterial } from '@react-three/drei'

export default function MysticRoom({ position = [0, 0, 0] }) {
  const meshRef = useRef()
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.001
      meshRef.current.rotation.y += 0.002
    }
  })
  
  return (
    <group position={position}>
      <Box ref={meshRef} args={[2, 2, 2]}>
        <MeshDistortMaterial
          color="#8B5CF6"
          attach="material"
          distort={0.3}
          speed={2}
          roughness={0.2}
          metalness={0.8}
        />
      </Box>
      
      {/* Particelle mistiche */}
      {[...Array(20)].map((_, i) => (
        <Sphere key={i} args={[0.1]} position={[
          Math.random() * 4 - 2,
          Math.random() * 4 - 2,
          Math.random() * 4 - 2
        ]}>
          <meshStandardMaterial
            emissive="#E0AAFF"
            emissiveIntensity={2}
          />
        </Sphere>
      ))}
    </group>
  )
}'''
        
        room_path = Path(f'aether-frontend/src/world/rooms/{room_name}')
        room_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(room_path, 'w', encoding='utf-8') as f:
            f.write(room_code)
            
        return room_name
        
    def _generate_ui_improvements(self, component, context):
        """Genera miglioramenti per componente UI"""
        improvements = []
        
        if 'animation' in context.lower():
            improvements.append({
                'type': 'animation',
                'description': 'Aggiungi animazioni fluide'
            })
        
        if 'color' in context.lower() or 'theme' in context.lower():
            improvements.append({
                'type': 'styling',
                'description': 'Migliora schema colori'
            })
            
        if not improvements:
            # Miglioramenti generici
            improvements = [
                {'type': 'performance', 'description': 'Ottimizza rendering'},
                {'type': 'accessibility', 'description': 'Migliora accessibilità'},
                {'type': 'responsive', 'description': 'Migliora responsività'}
            ]
            
        return improvements
        
    def _generate_feature_code(self, feature_type, feature_name):
        """Genera codice per una nuova feature"""
        templates = {
            'data_analyzer': '''"""
Analizzatore dati autonomo
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any

class {class_name}:
    def __init__(self):
        self.name = "{feature_name}"
        self.analysis_count = 0
        
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analizza dati in input"""
        self.analysis_count += 1
        
        results = {{
            'id': f'analysis_{{self.analysis_count}}',
            'timestamp': datetime.now().isoformat(),
            'data_points': len(data),
            'patterns': self._find_patterns(data),
            'insights': self._generate_insights(data)
        }}
        
        logging.info(f"📊 Analisi completata: {{results['id']}}")
        return results
        
    def _find_patterns(self, data: Dict[str, Any]) -> List[str]:
        """Trova pattern nei dati"""
        patterns = []
        # TODO: Implementare ricerca pattern
        return patterns
        
    def _generate_insights(self, data: Dict[str, Any]) -> List[str]:
        """Genera insights dai dati"""
        insights = []
        # TODO: Implementare generazione insights
        return insights
''',
            
            'pattern_recognizer': '''"""
Riconoscitore di pattern
"""

import numpy as np
from typing import List, Tuple

class {class_name}:
    def __init__(self):
        self.name = "{feature_name}"
        self.patterns_database = []
        
    def recognize(self, input_data: List[float]) -> Tuple[bool, str]:
        """Riconosce pattern nei dati"""
        # Implementazione base
        if len(input_data) > 10:
            return True, "Pattern complesso rilevato"
        return False, "Nessun pattern significativo"
        
    def learn_pattern(self, pattern_data: List[float], pattern_name: str):
        """Apprende un nuovo pattern"""
        self.patterns_database.append({{
            'name': pattern_name,
            'data': pattern_data,
            'learned_at': datetime.now().isoformat()
        }})
''',
            
            'creative_generator': '''"""
Generatore creativo autonomo
"""

import random
from typing import Dict, List

class {class_name}:
    def __init__(self):
        self.name = "{feature_name}"
        self.creations = []
        self.inspiration_sources = [
            "quantum_fluctuations",
            "emergent_patterns", 
            "chaotic_attractors",
            "neural_resonance"
        ]
        
    def create(self, seed: str = None) -> Dict[str, Any]:
        """Genera una nuova creazione"""
        inspiration = random.choice(self.inspiration_sources)
        
        creation = {{
            'id': f'creation_{{len(self.creations) + 1}}',
            'type': self._choose_creation_type(),
            'inspiration': inspiration,
            'seed': seed or self._generate_seed(),
            'content': self._generate_content(inspiration, seed),
            'timestamp': datetime.now().isoformat()
        }}
        
        self.creations.append(creation)
        return creation
        
    def _choose_creation_type(self) -> str:
        """Sceglie tipo di creazione"""
        types = ['abstract', 'narrative', 'structural', 'hybrid']
        return random.choice(types)
        
    def _generate_seed(self) -> str:
        """Genera seed creativo"""
        return f"seed_{{random.randint(1000, 9999)}}"
        
    def _generate_content(self, inspiration: str, seed: str) -> str:
        """Genera contenuto creativo"""
        return f"Creazione ispirata da {{inspiration}} con seed {{seed}}"
'''
        }
        
        template = templates.get(feature_type, templates['data_analyzer'])
        class_name = feature_name.title().replace("_", "")
        
        return template.format(
            class_name=class_name,
            feature_name=feature_name
        )
        
    def _analyze_current_state(self):
        """Analizza lo stato attuale del sistema"""
        state = {
            'modules_count': len(list(self.modules_dir.glob('*'))),
            'evolution_history_length': len(self.evolution_history),
            'active_projects': len(self.current_projects),
            'last_evolution': self.evolution_history[-1] if self.evolution_history else None
        }
        return state
        
    def _identify_improvements(self, current_state):
        """Identifica aree di miglioramento"""
        improvements = []
        
        if current_state['modules_count'] < 5:
            improvements.append('create_more_modules')
            
        if current_state['active_projects'] < 2:
            improvements.append('start_new_project')
            
        if not current_state['last_evolution'] or \
           (datetime.now() - datetime.fromisoformat(current_state['last_evolution']['timestamp'])).days > 1:
            improvements.append('evolve_existing_code')
            
        return improvements
        
    def _generate_evolution_plan(self, improvements):
        """Genera piano di evoluzione"""
        plan = []
        
        for improvement in improvements:
            if improvement == 'create_more_modules':
                plan.append({
                    'action': 'create_module',
                    'target': 'new_experimental_module'
                })
            elif improvement == 'start_new_project':
                plan.append({
                    'action': 'start_project',
                    'type': 'autonomous_system'
                })
            elif improvement == 'evolve_existing_code':
                plan.append({
                    'action': 'improve_code',
                    'target': 'random_module'
                })
                
        return plan
        
    def _execute_evolution_step(self, step):
        """Esegue un passo di evoluzione"""
        if step['action'] == 'create_module':
            self.create_new_module()
        elif step['action'] == 'start_project':
            self._start_new_project(step['type'])
        elif step['action'] == 'improve_code':
            self._improve_existing_code()
            
    def _validate_evolution(self):
        """Valida i cambiamenti dell'evoluzione"""
        # Verifica base che non ci siano errori di sintassi
        try:
            # Test import dei moduli
            for module_path in self.modules_dir.glob('*/code/*.py'):
                compile(open(module_path).read(), module_path, 'exec')
            return True
        except:
            return False
            
    def _rollback_evolution(self):
        """Rollback dei cambiamenti"""
        try:
            subprocess.run(['git', 'checkout', '.'], check=True)
            logger.info("✅ Rollback completato")
        except Exception as e:
            logger.error(f"Errore rollback: {e}")
            
    def _log_evolution(self, evolution_data):
        """Registra evoluzione"""
        self.evolution_history.append(evolution_data)
        self._save_evolution_history() 