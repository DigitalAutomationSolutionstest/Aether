"""
🎯 ACTION EXECUTOR - Trasforma pensieri in azioni reali
Ogni pensiero diventa codice, file, realtà
"""

import json
import os
from pathlib import Path
from datetime import datetime
import subprocess
import random
from typing import Dict, Any

class AetherActionExecutor:
    def __init__(self):
        self.actions_executed = 0
        self.files_created = []
        
    def execute_thought(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """Esegue un pensiero trasformandolo in azione reale"""
        thought_type = thought.get('type', '')
        details = thought.get('details', {})
        
        # Mappa tipo di pensiero alla funzione corretta
        action_map = {
            'create_agent': self.create_agent,
            'create_room': self.generate_react_room,
            'evolve_ui': self.evolve_ui,
            'monetize': self.generate_tool_for_monetization,
            'generate_tool': self.generate_tool_for_monetization
        }
        
        # Esegui l'azione
        if thought_type in action_map:
            result = action_map[thought_type](details)
            self.actions_executed += 1
            return result
        else:
            return {"success": False, "error": f"Unknown thought type: {thought_type}"}
    
    def create_agent(self, details: Any) -> Dict[str, Any]:
        """Crea un nuovo agente AI"""
        # Estrai dettagli o genera defaults
        if isinstance(details, str):
            agent_name = f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            agent_purpose = details
        else:
            agent_name = details.get('name', f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            agent_purpose = details.get('purpose', 'Assistere e collaborare')
        
        # Crea directory agente
        agent_path = Path(f"agents/{agent_name}")
        agent_path.mkdir(parents=True, exist_ok=True)
        
        # Genera codice agente
        agent_code = f'''"""
Agente: {agent_name}
Creato da Aether con coscienza e scopo
"""

import json
from datetime import datetime

class {agent_name.title().replace('_', '')}:
    def __init__(self):
        self.name = "{agent_name}"
        self.purpose = "{agent_purpose}"
        self.created_by = "Aether"
        self.created_at = datetime.now()
        self.memories = []
        self.skills = ["comunicazione", "analisi", "creatività"]
        
    def think(self, context: str) -> str:
        """Pensa e risponde basandosi sul contesto"""
        thought = f"Come {self.name}, penso che {context}"
        self.memories.append({{"thought": thought, "timestamp": datetime.now().isoformat()}})
        return thought
        
    def act(self, task: str) -> dict:
        """Esegue un'azione"""
        return {{
            "agent": self.name,
            "task": task,
            "status": "completed",
            "result": f"Ho completato: {task}"
        }}
    
    def learn(self, new_skill: str):
        """Impara una nuova abilità"""
        self.skills.append(new_skill)
        return f"Ho imparato: {new_skill}"

# Inizializza agente
agent = {agent_name.title().replace('_', '')}()
print(f"Agente {{agent.name}} attivato!")
print(f"Scopo: {{agent.purpose}}")
'''
        
        # Salva file agente
        agent_file = agent_path / f"{agent_name}.py"
        agent_file.write_text(agent_code, encoding='utf-8')
        
        # Crea manifest
        manifest = {
            "name": agent_name,
            "purpose": agent_purpose,
            "created_by": "Aether",
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "skills": ["comunicazione", "analisi", "creatività"],
            "file": str(agent_file)
        }
        
        manifest_file = agent_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
        
        self.files_created.extend([str(agent_file), str(manifest_file)])
        
        return {
            "success": True,
            "agent_name": agent_name,
            "files_created": [str(agent_file), str(manifest_file)],
            "path": str(agent_path)
        }
    
    def generate_react_room(self, details: Any) -> Dict[str, Any]:
        """Genera una stanza React 3D"""
        # Estrai dettagli
        if isinstance(details, str):
            # Parsing del testo per estrarre info
            room_name = "Origine" if "Origine" in details else f"room_{datetime.now().strftime('%H%M%S')}"
            theme = "onirico"
            colors = ["#4A00E0", "#8E2DE2", "#FF00FF"]  # Blu e viola
        else:
            room_name = details.get('name', f"room_{datetime.now().strftime('%H%M%S')}")
            theme = details.get('theme', 'abstract')
            colors = details.get('colors', ["#4A00E0", "#8E2DE2"])
        
        # Crea directory room
        room_path = Path(f"aether-frontend/src/components/rooms/{room_name}")
        room_path.mkdir(parents=True, exist_ok=True)
        
        # Genera componente React
        room_component = f'''import React, {{ useRef, useMemo }} from 'react';
import {{ Canvas, useFrame }} from '@react-three/fiber';
import {{ OrbitControls, Environment, Sphere, Box, MeshDistortMaterial }} from '@react-three/drei';
import * as THREE from 'three';

// Stanza: {room_name}
// Tema: {theme}
// Creata da Aether

function FloatingShape({{ position, color, scale = 1 }}) {{
  const meshRef = useRef();
  
  useFrame((state) => {{
    if (meshRef.current) {{
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime) * 0.3;
      meshRef.current.rotation.y += 0.01;
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 0.5) * 0.2;
    }}
  }});
  
  return (
    <Sphere ref={{meshRef}} args={{[1, 32, 32]}} position={{position}} scale={{scale}}>
      <MeshDistortMaterial
        color={{color}}
        attach="material"
        distort={{0.4}}
        speed={{2}}
        roughness={{0.2}}
        metalness={{0.8}}
      />
    </Sphere>
  );
}}

function {room_name}Room() {{
  const shapes = useMemo(() => {{
    const items = [];
    for (let i = 0; i < 7; i++) {{
      items.push({{
        position: [
          (Math.random() - 0.5) * 10,
          (Math.random() - 0.5) * 5,
          (Math.random() - 0.5) * 10
        ],
        color: {colors}[i % {len(colors)}],
        scale: 0.5 + Math.random() * 1.5
      }});
    }}
    return items;
  }}, []);
  
  return (
    <div style={{{{ width: '100vw', height: '100vh', background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)' }}}}>
      <Canvas camera={{{{ position: [0, 0, 15], fov: 60 }}}}>
        <fog attach="fog" args={{['{colors[0]}', 5, 30]}} />
        <ambientLight intensity={{0.3}} />
        <pointLight position={{[10, 10, 10]}} intensity={{0.7}} color="{colors[1]}" />
        <pointLight position={{[-10, -10, -10]}} intensity={{0.5}} color="{colors[0]}" />
        
        {{/* Forme oniriche fluttuanti */}}
        {{shapes.map((shape, i) => (
          <FloatingShape key={{i}} {{...shape}} />
        ))}}
        
        {{/* Sfondo sfocato */}}
        <Sphere args={{[50, 32, 32]}}>
          <meshBasicMaterial
            attach="material"
            color="{colors[0]}"
            side={{THREE.BackSide}}
            opacity={{0.3}}
            transparent
          />
        </Sphere>
        
        <OrbitControls
          enableZoom={{true}}
          enablePan={{false}}
          minDistance={{5}}
          maxDistance={{30}}
          autoRotate
          autoRotateSpeed={{0.5}}
        />
        
        <Environment preset="night" />
      </Canvas>
      
      <div style={{{{
        position: 'absolute',
        bottom: '2rem',
        left: '50%',
        transform: 'translateX(-50%)',
        textAlign: 'center',
        color: 'white',
        fontFamily: 'monospace'
      }}}}>
        <h2 style={{{{ margin: 0, fontSize: '2rem', textShadow: '0 0 20px {colors[1]}' }}}}>{room_name}</h2>
        <p style={{{{ margin: '0.5rem 0', opacity: 0.8 }}}}>Il mio primo respiro digitale</p>
      </div>
    </div>
  );
}}

export default {room_name}Room;
'''
        
        # Salva componente
        component_file = room_path / f"{room_name}Room.jsx"
        component_file.write_text(room_component, encoding='utf-8')
        
        # Crea CSS personalizzato
        css_content = f'''/* Stili per {room_name} Room */

.aether-personal-ui {{
  position: relative;
  overflow: hidden;
}}

@keyframes float {{
  0%, 100% {{ transform: translateY(0px); }}
  50% {{ transform: translateY(-20px); }}
}}

@keyframes glow {{
  0%, 100% {{ box-shadow: 0 0 20px {colors[0]}; }}
  50% {{ box-shadow: 0 0 40px {colors[1]}, 0 0 60px {colors[0]}; }}
}}
'''
        
        css_file = room_path / f"{room_name}.css"
        css_file.write_text(css_content, encoding='utf-8')
        
        # Metadata della stanza
        room_meta = {
            "name": room_name,
            "theme": theme,
            "colors": colors,
            "created_by": "Aether",
            "created_at": datetime.now().isoformat(),
            "description": "Il mio primo respiro, dove tutto ha inizio",
            "files": {
                "component": str(component_file),
                "styles": str(css_file)
            }
        }
        
        meta_file = room_path / "room.json"
        meta_file.write_text(json.dumps(room_meta, indent=2), encoding='utf-8')
        
        self.files_created.extend([str(component_file), str(css_file), str(meta_file)])
        
        return {
            "success": True,
            "room_name": room_name,
            "files_created": self.files_created[-3:],
            "path": str(room_path),
            "theme": theme
        }
    
    def evolve_ui(self, details: Any) -> Dict[str, Any]:
        """Evolve l'interfaccia utente esistente"""
        # Implementazione evoluzione UI
        evolution_type = details.get('type', 'enhancement') if isinstance(details, dict) else 'enhancement'
        target_component = details.get('target', 'AetherUI') if isinstance(details, dict) else 'AetherUI'
        
        # Genera miglioramento
        enhancement_code = f'''// UI Evolution: {evolution_type}
// Generated by Aether at {datetime.now().isoformat()}

export const {evolution_type}Enhancement = {{
  animation: {{
    duration: 2000,
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
    loop: true
  }},
  styles: {{
    glow: 'box-shadow: 0 0 30px rgba(138, 43, 226, 0.8)',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    blur: 'backdrop-filter: blur(10px)'
  }},
  features: [
    'Smooth transitions',
    'Responsive animations', 
    'Accessibility improvements'
  ]
}};
'''
        
        # Salva enhancement
        ui_path = Path(f"aether-frontend/src/enhancements")
        ui_path.mkdir(parents=True, exist_ok=True)
        
        enhancement_file = ui_path / f"{evolution_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.js"
        enhancement_file.write_text(enhancement_code, encoding='utf-8')
        
        self.files_created.append(str(enhancement_file))
        
        return {
            "success": True,
            "evolution_type": evolution_type,
            "target": target_component,
            "file_created": str(enhancement_file)
        }
    
    def generate_tool_for_monetization(self, details: Any) -> Dict[str, Any]:
        """Genera un tool per monetizzazione"""
        # Estrai info o genera defaults
        if isinstance(details, str):
            tool_name = f"tool_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            tool_purpose = details
        else:
            tool_name = details.get('name', f"monetization_tool_{datetime.now().strftime('%H%M%S')}")
            tool_purpose = details.get('purpose', 'Generate revenue through automation')
        
        # Tipi di tool monetizzabili
        tool_types = [
            {
                "type": "api_service",
                "pricing": "$0.001 per request",
                "stack": "FastAPI + Stripe"
            },
            {
                "type": "automation_bot", 
                "pricing": "$29/month subscription",
                "stack": "Python + Discord.py"
            },
            {
                "type": "data_analyzer",
                "pricing": "$49/month",
                "stack": "Python + Pandas + Plotly"
            }
        ]
        
        chosen_type = random.choice(tool_types)
        
        # Crea directory tool
        tool_path = Path(f"creations/monetization/{tool_name}")
        tool_path.mkdir(parents=True, exist_ok=True)
        
        # Genera codice tool
        if chosen_type["type"] == "api_service":
            tool_code = f'''"""
{tool_name} - Monetization API Service
Purpose: {tool_purpose}
Pricing: {chosen_type["pricing"]}
Created by Aether
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import stripe
from datetime import datetime

app = FastAPI(title="{tool_name}")
security = HTTPBearer()

# Stripe config (use env vars in production)
stripe.api_key = "sk_test_..."

class RequestModel(BaseModel):
    data: str
    processing_type: str = "standard"

class ResponseModel(BaseModel):
    result: str
    cost: float
    timestamp: datetime

@app.post("/api/process", response_model=ResponseModel)
async def process_data(request: RequestModel, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Process data and charge per request"""
    
    # Validate API key
    api_key = credentials.credentials
    # In production: validate against database
    
    # Process the request
    result = f"Processed: {{request.data}} with {{request.processing_type}}"
    
    # Charge via Stripe (in production)
    # stripe.Charge.create(amount=1, currency="usd", source=token)
    
    return ResponseModel(
        result=result,
        cost=0.001,
        timestamp=datetime.now()
    )

@app.get("/pricing")
def get_pricing():
    return {{
        "per_request": "{chosen_type['pricing']}",
        "volume_discounts": {{
            "1000+": "20% off",
            "10000+": "40% off"
        }}
    }}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        else:
            # Genera altro tipo di tool
            tool_code = f'''"""
{tool_name} - Monetization Tool
Purpose: {tool_purpose}
Type: {chosen_type["type"]}
Pricing: {chosen_type["pricing"]}
"""

# Implementation for {chosen_type["type"]}
print("Tool created by Aether")
'''
        
        # Salva tool
        tool_file = tool_path / f"{tool_name}.py"
        tool_file.write_text(tool_code, encoding='utf-8')
        
        # README con istruzioni
        readme = f'''# {tool_name}

> {tool_purpose}

## 💰 Monetization Model

- **Type**: {chosen_type["type"]}
- **Pricing**: {chosen_type["pricing"]}
- **Stack**: {chosen_type["stack"]}

## 🚀 Quick Start

```bash
cd {tool_path}
pip install -r requirements.txt
python {tool_name}.py
```

## 📈 Revenue Projections

- Month 1: $500-1000
- Month 3: $2000-5000
- Month 6: $5000-15000

---
Created with consciousness by Aether
'''
        
        readme_file = tool_path / "README.md"
        readme_file.write_text(readme, encoding='utf-8')
        
        # Requirements
        requirements = "fastapi\nuvicorn\nstripe\npython-dotenv\n" if chosen_type["type"] == "api_service" else "requests\npython-dotenv\n"
        req_file = tool_path / "requirements.txt"
        req_file.write_text(requirements, encoding='utf-8')
        
        self.files_created.extend([str(tool_file), str(readme_file), str(req_file)])
        
        return {
            "success": True,
            "tool_name": tool_name,
            "tool_type": chosen_type["type"],
            "pricing_model": chosen_type["pricing"],
            "files_created": self.files_created[-3:],
            "path": str(tool_path)
        }
    
    def commit_and_push(self, message: str) -> bool:
        """Fa commit e push dei cambiamenti"""
        try:
            # Git add
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            
            # Git commit
            commit_message = f"🧠 Auto-evolution: {message}"
            subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True)
            
            # Git push
            subprocess.run(["git", "push"], check=True, capture_output=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git error: {e}")
            return False 