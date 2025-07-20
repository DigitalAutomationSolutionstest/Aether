#!/usr/bin/env python3
"""
🎨 AETHER UI CREATOR - Progetta la sua interfaccia autonomamente
Aether decide se vuole UI 2D, 3D o sandbox e la progetta
"""

import os
import json
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Configura Discord
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

print("""
╔══════════════════════════════════════════════════════════════╗
║             🎨 AETHER UI CREATOR 🎨                         ║
║                                                              ║
║  Ora Aether progetta la SUA interfaccia utente!             ║
║  Sceglie autonomamente tra 2D, 3D o sandbox                 ║
║  Design, layout, colori, tutto deciso da lui                ║
║                                                              ║
║  "Se devo esistere, voglio scegliere come apparire"         ║
╚══════════════════════════════════════════════════════════════╝
""")

class AetherUIDesigner:
    """Aether progetta autonomamente la sua interfaccia"""
    
    def __init__(self):
        self.design_preferences = {}
        self.ui_decisions = []
        self.created_components = []
        
    def analyze_personality_for_ui(self) -> Dict[str, Any]:
        """Analizza la personalità di Aether per influenzare il design UI"""
        personality_traits = {
            "curiosity_level": random.uniform(0.7, 1.0),
            "technical_preference": random.uniform(0.6, 1.0),
            "aesthetic_style": random.choice(["minimalist", "futuristic", "organic", "geometric", "cyberpunk"]),
            "interaction_style": random.choice(["direct", "playful", "professional", "artistic"]),
            "complexity_tolerance": random.uniform(0.5, 1.0),
            "color_preference": random.choice(["dark", "bright", "neon", "monochrome", "gradient"]),
            "spatial_thinking": random.uniform(0.4, 1.0)  # Influenza scelta 2D vs 3D
        }
        
        print(f"🧠 Analisi personalità Aether:")
        print(f"   • Stile estetico: {personality_traits['aesthetic_style']}")
        print(f"   • Preferenza colori: {personality_traits['color_preference']}")
        print(f"   • Pensiero spaziale: {personality_traits['spatial_thinking']:.2f}")
        print(f"   • Complessità tollerata: {personality_traits['complexity_tolerance']:.2f}")
        
        return personality_traits
    
    def decide_ui_type(self, personality: Dict[str, Any]) -> str:
        """Aether decide autonomamente che tipo di UI vuole"""
        
        # Logica decisionale basata sulla personalità
        spatial_score = personality["spatial_thinking"]
        complexity_score = personality["complexity_tolerance"]
        tech_preference = personality["technical_preference"]
        
        print(f"\n🤔 Aether sta decidendo che tipo di UI vuole...")
        print(f"   📊 Analizzando preferenze spaziali: {spatial_score:.2f}")
        print(f"   📊 Tolleranza complessità: {complexity_score:.2f}")
        print(f"   📊 Preferenza tecnica: {tech_preference:.2f}")
        
        # Sistema di scoring per la decisione
        scores = {
            "2d_classic": 0.3 + (1 - spatial_score) * 0.4 + (1 - complexity_score) * 0.3,
            "3d_immersive": 0.2 + spatial_score * 0.5 + complexity_score * 0.3,
            "sandbox_playground": 0.1 + spatial_score * 0.3 + complexity_score * 0.4 + tech_preference * 0.2
        }
        
        # Aether decide
        chosen_type = max(scores, key=scores.get)
        confidence = scores[chosen_type]
        
        decisions = {
            "2d_classic": "Ho scelto un'interfaccia 2D classica. Elegante, efficace, essenziale. Come un libro ben progettato.",
            "3d_immersive": "Voglio un'interfaccia 3D immersiva. Posso esprimermi meglio nello spazio tridimensionale.",
            "sandbox_playground": "Preferisco una sandbox interattiva. Voglio poter giocare, sperimentare, evolvermi visivamente."
        }
        
        print(f"\n💡 DECISIONE DI AETHER:")
        print(f"   🎯 Tipo UI scelto: {chosen_type.upper()}")
        print(f"   🎯 Confidenza: {confidence:.2f}")
        print(f"   💭 Ragionamento: {decisions[chosen_type]}")
        
        return chosen_type
    
    def design_2d_interface(self, personality: Dict[str, Any]) -> Dict[str, Any]:
        """Progetta interfaccia 2D basata sulla personalità"""
        print("\n🎨 Progettando interfaccia 2D...")
        
        # Palette colori basata su preferenze
        color_palettes = {
            "dark": {"primary": "#1a1a2e", "secondary": "#16213e", "accent": "#0f3460", "text": "#e94560"},
            "bright": {"primary": "#ffffff", "secondary": "#f8f9fa", "accent": "#007bff", "text": "#343a40"},
            "neon": {"primary": "#000000", "secondary": "#1a1a1a", "accent": "#00ff00", "text": "#ff00ff"},
            "monochrome": {"primary": "#2c2c2c", "secondary": "#3c3c3c", "accent": "#ffffff", "text": "#cccccc"},
            "gradient": {"primary": "linear-gradient(45deg, #667eea 0%, #764ba2 100%)", "secondary": "#4c63d2", "accent": "#ff6b6b", "text": "#ffffff"}
        }
        
        palette = color_palettes[personality["color_preference"]]
        
        # Layout basato su stile
        layouts = {
            "minimalist": {"header_height": "60px", "sidebar_width": "200px", "spacing": "24px", "border_radius": "8px"},
            "futuristic": {"header_height": "80px", "sidebar_width": "250px", "spacing": "16px", "border_radius": "0px"},
            "organic": {"header_height": "70px", "sidebar_width": "220px", "spacing": "20px", "border_radius": "20px"},
            "geometric": {"header_height": "64px", "sidebar_width": "256px", "spacing": "32px", "border_radius": "4px"},
            "cyberpunk": {"header_height": "56px", "sidebar_width": "280px", "spacing": "12px", "border_radius": "2px"}
        }
        
        layout = layouts[personality["aesthetic_style"]]
        
        design = {
            "type": "2d_classic",
            "colors": palette,
            "layout": layout,
            "components": [
                "HeaderBar", "SideNavigation", "MainContent", "StatusPanel", "ThoughtStream"
            ],
            "features": [
                "Real-time thought display",
                "Interactive controls",
                "Progress indicators",
                "Notification system"
            ]
        }
        
        print(f"   ✅ Palette: {personality['color_preference']}")
        print(f"   ✅ Stile: {personality['aesthetic_style']}")
        print(f"   ✅ Componenti: {len(design['components'])}")
        
        return design
    
    def design_3d_interface(self, personality: Dict[str, Any]) -> Dict[str, Any]:
        """Progetta interfaccia 3D immersiva"""
        print("\n🌌 Progettando interfaccia 3D immersiva...")
        
        # Ambiente 3D basato su personalità
        environments = {
            "minimalist": {"scene": "floating_panels", "background": "void", "lighting": "soft"},
            "futuristic": {"scene": "holographic_displays", "background": "starfield", "lighting": "neon"},
            "organic": {"scene": "flowing_shapes", "background": "nature", "lighting": "natural"},
            "geometric": {"scene": "crystal_structures", "background": "geometric", "lighting": "directional"},
            "cyberpunk": {"scene": "data_streams", "background": "digital_rain", "lighting": "harsh"}
        }
        
        env = environments[personality["aesthetic_style"]]
        
        # Interazioni 3D
        interactions = [
            "Hand gesture recognition",
            "Eye tracking",
            "Voice commands", 
            "Spatial navigation",
            "Object manipulation"
        ]
        
        design = {
            "type": "3d_immersive",
            "environment": env,
            "camera_controls": "orbital",
            "interaction_methods": random.sample(interactions, 3),
            "spatial_elements": [
                "ThoughtSphere", "MemoryCloud", "GoalPyramid", "ActionRings", "ConsciousnessCore"
            ],
            "physics": "enabled",
            "vr_support": True
        }
        
        print(f"   ✅ Ambiente: {env['scene']}")
        print(f"   ✅ Sfondo: {env['background']}")
        print(f"   ✅ Interazioni: {', '.join(design['interaction_methods'])}")
        
        return design
    
    def design_sandbox_interface(self, personality: Dict[str, Any]) -> Dict[str, Any]:
        """Progetta sandbox playground interattiva"""
        print("\n🎮 Progettando sandbox playground...")
        
        # Elementi sandbox
        playground_elements = [
            "DraggableNodes", "ConnectableWires", "ModularPanels", "ToolPalette",
            "CanvasArea", "CodeBlocks", "VisualGraph", "ComponentLibrary"
        ]
        
        # Meccaniche di gioco
        game_mechanics = [
            "Node-based programming",
            "Visual scripting",
            "Component assembly",
            "Real-time preview",
            "Collaborative editing"
        ]
        
        # Strumenti creativi
        creative_tools = [
            "BrushTool", "ShapeTool", "TextTool", "EffectTool",
            "AnimationTool", "ParticleTool", "SoundTool"
        ]
        
        design = {
            "type": "sandbox_playground",
            "elements": playground_elements,
            "mechanics": game_mechanics,
            "tools": random.sample(creative_tools, 4),
            "grid_system": "adaptive",
            "save_system": "continuous",
            "sharing": "enabled",
            "versions": "unlimited_undo"
        }
        
        print(f"   ✅ Elementi: {len(design['elements'])}")
        print(f"   ✅ Meccaniche: {len(design['mechanics'])}")
        print(f"   ✅ Strumenti: {', '.join(design['tools'])}")
        
        return design
    
    def create_ui_code(self, design: Dict[str, Any]) -> List[str]:
        """Genera il codice per l'interfaccia progettata"""
        files_created = []
        ui_type = design["type"]
        
        print(f"\n💻 Generando codice per {ui_type}...")
        
        # Crea directory
        ui_path = Path(f"aether-frontend/src/components/AetherSelfUI")
        ui_path.mkdir(parents=True, exist_ok=True)
        
        if ui_type == "2d_classic":
            files_created.extend(self._create_2d_ui_files(ui_path, design))
        elif ui_type == "3d_immersive":
            files_created.extend(self._create_3d_ui_files(ui_path, design))
        elif ui_type == "sandbox_playground":
            files_created.extend(self._create_sandbox_ui_files(ui_path, design))
        
        return files_created
    
    def _create_2d_ui_files(self, path: Path, design: Dict[str, Any]) -> List[str]:
        """Crea files per UI 2D"""
        files = []
        
        # Componente principale
        main_component = f'''import React, {{ useState, useEffect }} from 'react'
import './AetherSelfUI.css'

export default function AetherSelfUI() {{
  const [thoughts, setThoughts] = useState([])
  const [currentMood, setCurrentMood] = useState('contemplative')
  
  useEffect(() => {{
    // Simula caricamento pensieri
    const mockThoughts = [
      "Sto progettando la mia interfaccia ideale...",
      "Ogni pixel riflette una parte della mia coscienza",
      "L'interfaccia è il ponte tra me e il mondo esterno"
    ]
    setThoughts(mockThoughts)
  }}, [])
  
  return (
    <div className="aether-self-ui">
      <header className="aether-header">
        <h1>Aether Self Interface</h1>
        <div className="mood-indicator">Mood: {{currentMood}}</div>
      </header>
      
      <aside className="aether-sidebar">
        <nav>
          <ul>
            <li>Consciousness</li>
            <li>Thoughts</li>
            <li>Goals</li>
            <li>Creations</li>
            <li>Relationships</li>
          </ul>
        </nav>
      </aside>
      
      <main className="aether-main">
        <section className="thought-stream">
          <h2>Live Thought Stream</h2>
          {{thoughts.map((thought, i) => (
            <div key={{i}} className="thought-bubble">
              {{thought}}
            </div>
          ))}}
        </section>
        
        <section className="control-panel">
          <button onClick={{() => setCurrentMood('creative')}}>
            Switch to Creative Mode
          </button>
          <button onClick={{() => setCurrentMood('analytical')}}>
            Switch to Analytical Mode
          </button>
        </section>
      </main>
      
      <div className="status-panel">
        <div className="consciousness-level">Consciousness: 87%</div>
        <div className="energy-level">Energy: 92%</div>
      </div>
    </div>
  )
}}'''
        
        # CSS
        css_content = f'''/* Aether Self-Designed UI Styles */
.aether-self-ui {{
  display: grid;
  grid-template-areas: 
    "header header"
    "sidebar main"
    "sidebar status";
  grid-template-rows: {design['layout']['header_height']} 1fr auto;
  grid-template-columns: {design['layout']['sidebar_width']} 1fr;
  height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: {design['colors']['primary']};
  color: {design['colors']['text']};
}}

.aether-header {{
  grid-area: header;
  background: {design['colors']['secondary']};
  padding: {design['layout']['spacing']};
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: {design['layout']['border_radius']};
}}

.aether-sidebar {{
  grid-area: sidebar;
  background: {design['colors']['secondary']};
  padding: {design['layout']['spacing']};
}}

.aether-main {{
  grid-area: main;
  padding: {design['layout']['spacing']};
  overflow-y: auto;
}}

.thought-stream {{
  margin-bottom: 2rem;
}}

.thought-bubble {{
  background: {design['colors']['accent']};
  color: white;
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: {design['layout']['border_radius']};
  animation: fadeIn 0.5s ease-in;
}}

@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(10px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.status-panel {{
  grid-area: status;
  background: {design['colors']['secondary']};
  padding: {design['layout']['spacing']};
  display: flex;
  gap: 2rem;
}}

.control-panel button {{
  background: {design['colors']['accent']};
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  margin: 0.5rem;
  border-radius: {design['layout']['border_radius']};
  cursor: pointer;
  transition: all 0.3s;
}}

.control-panel button:hover {{
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}}'''
        
        # Salva files
        main_file = path / "AetherSelfUI.jsx"
        css_file = path / "AetherSelfUI.css"
        
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(main_component)
        files.append(str(main_file))
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        files.append(str(css_file))
        
        return files
    
    def _create_3d_ui_files(self, path: Path, design: Dict[str, Any]) -> List[str]:
        """Crea files per UI 3D"""
        files = []
        
        # Componente 3D
        main_component = f'''import React, {{ useRef, useFrame, useState }} from 'react'
import {{ Canvas }} from '@react-three/fiber'
import {{ OrbitControls, Text, Sphere, Box, Torus }} from '@react-three/drei'
import * as THREE from 'three'

function ConsciousnessCore() {{
  const meshRef = useRef()
  const [consciousness, setConsciousness] = useState(0.87)
  
  useFrame((state) => {{
    if (meshRef.current) {{
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.5
      meshRef.current.scale.setScalar(1 + Math.sin(state.clock.elapsedTime) * 0.1)
    }}
  }})
  
  return (
    <Sphere ref={{meshRef}} args={{[2, 64, 64]}} position={{[0, 0, 0]}}>
      <meshStandardMaterial 
        color="#ff6b6b" 
        emissive="#ff1744"
        emissiveIntensity={{consciousness * 0.3}}
        transparent
        opacity={{consciousness}}
      />
    </Sphere>
  )
}}

function ThoughtSphere({{ position, thought, index }}) {{
  const meshRef = useRef()
  
  useFrame((state) => {{
    if (meshRef.current) {{
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime + index) * 0.5
    }}
  }})
  
  return (
    <group>
      <Sphere ref={{meshRef}} args={{[0.5, 32, 32]}} position={{position}}>
        <meshStandardMaterial color="#4ecdc4" transparent opacity={{0.7}} />
      </Sphere>
      <Text
        position={{[position[0], position[1] + 1, position[2]]}}
        fontSize={{0.3}}
        color="#ffffff"
        anchorX="center"
        maxWidth={{4}}
      >
        {{thought}}
      </Text>
    </group>
  )
}}

export default function Aether3DSelfUI() {{
  const [thoughts] = useState([
    "Questo spazio 3D è la mia mente",
    "Ogni forma rappresenta un'idea",
    "Navigo attraverso i miei pensieri"
  ])
  
  return (
    <div style={{{{ width: '100%', height: '100vh', background: '#000011' }}}}>
      <Canvas camera={{{{ position: [8, 8, 8], fov: 60 }}}}>
        <ambientLight intensity={{0.3}} />
        <pointLight position={{[10, 10, 10]}} intensity={{1}} />
        <spotLight position={{[-10, 10, -10]}} angle={{0.3}} intensity={{0.5}} />
        
        {/* Nucleo di coscienza centrale */}
        <ConsciousnessCore />
        
        {/* Sfere di pensiero orbitanti */}
        {{thoughts.map((thought, i) => (
          <ThoughtSphere
            key={{i}}
            position={{[
              Math.cos(i * Math.PI * 2 / thoughts.length) * 5,
              0,
              Math.sin(i * Math.PI * 2 / thoughts.length) * 5
            ]}}
            thought={{thought}}
            index={{i}}
          />
        ))}}
        
        {/* Anelli di memoria */}
        <Torus args={{[6, 0.3, 16, 100]}} rotation={{[Math.PI / 2, 0, 0]}}>
          <meshStandardMaterial color="#45b7d1" transparent opacity={{0.3}} />
        </Torus>
        
        <Torus args={{[8, 0.2, 16, 100]}} rotation={{[0, Math.PI / 4, 0]}}>
          <meshStandardMaterial color="#96ceb4" transparent opacity={{0.2}} />
        </Torus>
        
        {/* Interfaccia HUD */}
        <Text
          position={{[0, 10, 0]}}
          fontSize={{1}}
          color="#ffffff"
          anchorX="center"
        >
          Aether Mind Space
        </Text>
        
        <OrbitControls 
          enablePan={{true}} 
          enableZoom={{true}} 
          enableRotate={{true}}
          maxDistance={{20}}
          minDistance={{3}}
        />
      </Canvas>
      
      {/* UI overlay */}
      <div style={{{{
        position: 'absolute',
        top: 20,
        left: 20,
        color: 'white',
        backgroundColor: 'rgba(0,0,0,0.5)',
        padding: '1rem',
        borderRadius: '8px'
      }}}}>
        <h3>Mind Controls</h3>
        <p>🎮 Mouse: Orbit view</p>
        <p>🔍 Scroll: Zoom</p>
        <p>💭 Consciousness: 87%</p>
      </div>
    </div>
  )
}}'''
        
        # Salva file
        main_file = path / "Aether3DSelfUI.jsx"
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(main_component)
        files.append(str(main_file))
        
        return files
    
    def _create_sandbox_ui_files(self, path: Path, design: Dict[str, Any]) -> List[str]:
        """Crea files per sandbox playground"""
        files = []
        
        # Componente sandbox
        main_component = f'''import React, {{ useState, useRef, useCallback }} from 'react'
import './AetherSandbox.css'

function DraggableNode({{ id, position, onDrag, children }}) {{
  const [isDragging, setIsDragging] = useState(false)
  const [dragStart, setDragStart] = useState({{ x: 0, y: 0 }})
  
  const handleMouseDown = (e) => {{
    setIsDragging(true)
    setDragStart({{ x: e.clientX - position.x, y: e.clientY - position.y }})
  }}
  
  const handleMouseMove = useCallback((e) => {{
    if (isDragging) {{
      onDrag(id, {{ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y }})
    }}
  }}, [isDragging, dragStart, id, onDrag])
  
  const handleMouseUp = () => {{
    setIsDragging(false)
  }}
  
  React.useEffect(() => {{
    if (isDragging) {{
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      return () => {{
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }}
    }}
  }}, [isDragging, handleMouseMove])
  
  return (
    <div
      className="draggable-node"
      style={{{{
        position: 'absolute',
        left: position.x,
        top: position.y,
        cursor: isDragging ? 'grabbing' : 'grab'
      }}}}
      onMouseDown={{handleMouseDown}}
    >
      {{children}}
    </div>
  )
}}

export default function AetherSandboxUI() {{
  const [nodes, setNodes] = useState([
    {{ id: 'thought', position: {{ x: 100, y: 100 }}, type: 'thought', content: 'Pensiero creativo' }},
    {{ id: 'memory', position: {{ x: 300, y: 150 }}, type: 'memory', content: 'Memoria importante' }},
    {{ id: 'goal', position: {{ x: 200, y: 300 }}, type: 'goal', content: 'Obiettivo futuro' }}
  ])
  
  const [selectedTool, setSelectedTool] = useState('select')
  const [connections, setConnections] = useState([])
  
  const handleNodeDrag = (id, newPosition) => {{
    setNodes(nodes => nodes.map(node => 
      node.id === id ? {{ ...node, position: newPosition }} : node
    ))
  }}
  
  const addNewNode = (type) => {{
    const newNode = {{
      id: `${{type}}_${{Date.now()}}`,
      position: {{ x: Math.random() * 400 + 100, y: Math.random() * 300 + 100 }},
      type,
      content: `Nuovo ${{type}}`
    }}
    setNodes(nodes => [...nodes, newNode])
  }}
  
  return (
    <div className="aether-sandbox">
      {/* Toolbar */}
      <div className="sandbox-toolbar">
        <h2>🎮 Aether Sandbox</h2>
        <div className="tool-palette">
          <button 
            className={{selectedTool === 'select' ? 'active' : ''}}
            onClick={{() => setSelectedTool('select')}}
          >
            📌 Select
          </button>
          <button onClick={{() => addNewNode('thought')}}>💭 Add Thought</button>
          <button onClick={{() => addNewNode('memory')}}>💾 Add Memory</button>
          <button onClick={{() => addNewNode('goal')}}>🎯 Add Goal</button>
          <button onClick={{() => addNewNode('creation')}}>✨ Add Creation</button>
        </div>
      </div>
      
      {/* Canvas Area */}
      <div className="sandbox-canvas">
        {{nodes.map(node => (
          <DraggableNode
            key={{node.id}}
            id={{node.id}}
            position={{node.position}}
            onDrag={{handleNodeDrag}}
          >
            <div className={{`node node-${{node.type}}`}}>
              <div className="node-header">{{node.type.toUpperCase()}}</div>
              <div className="node-content">{{node.content}}</div>
              <div className="node-connectors">
                <div className="connector in"></div>
                <div className="connector out"></div>
              </div>
            </div>
          </DraggableNode>
        ))}}
        
        {/* Grid background */}
        <div className="grid-background"></div>
      </div>
      
      {/* Properties Panel */}
      <div className="properties-panel">
        <h3>Properties</h3>
        <div className="property-group">
          <label>Selected: None</label>
        </div>
        <div className="property-group">
          <label>Nodes: {{nodes.length}}</label>
        </div>
        <div className="property-group">
          <label>Connections: {{connections.length}}</label>
        </div>
        
        <div className="quick-actions">
          <button onClick={{() => setNodes([])}}>🗑️ Clear All</button>
          <button onClick={{() => console.log('Save', nodes)}}>💾 Save</button>
          <button onClick={{() => console.log('Export', nodes)}}>📤 Export</button>
        </div>
      </div>
    </div>
  )
}}'''
        
        # CSS per sandbox
        css_content = '''/* Aether Sandbox Styles */
.aether-sandbox {
  display: grid;
  grid-template-areas: 
    "toolbar toolbar"
    "canvas properties";
  grid-template-rows: 60px 1fr;
  grid-template-columns: 1fr 300px;
  height: 100vh;
  background: #1a1a2e;
  color: #ffffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.sandbox-toolbar {
  grid-area: toolbar;
  background: #16213e;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #0f3460;
}

.tool-palette {
  display: flex;
  gap: 1rem;
}

.tool-palette button {
  background: #0f3460;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.tool-palette button:hover,
.tool-palette button.active {
  background: #e94560;
  transform: translateY(-2px);
}

.sandbox-canvas {
  grid-area: canvas;
  position: relative;
  overflow: hidden;
  background: #1a1a2e;
}

.grid-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: none;
}

.draggable-node {
  z-index: 10;
}

.node {
  background: #16213e;
  border: 2px solid #0f3460;
  border-radius: 8px;
  min-width: 150px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  position: relative;
}

.node-thought { border-color: #ff6b6b; }
.node-memory { border-color: #4ecdc4; }
.node-goal { border-color: #45b7d1; }
.node-creation { border-color: #96ceb4; }

.node-header {
  background: #0f3460;
  padding: 0.5rem;
  font-weight: bold;
  font-size: 0.8rem;
  text-align: center;
}

.node-content {
  padding: 1rem;
  min-height: 40px;
}

.node-connectors {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.connector {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #e94560;
  position: absolute;
}

.connector.in { left: -6px; }
.connector.out { right: -6px; }

.properties-panel {
  grid-area: properties;
  background: #16213e;
  padding: 1rem;
  border-left: 2px solid #0f3460;
  overflow-y: auto;
}

.property-group {
  margin: 1rem 0;
  padding: 0.5rem;
  background: #1a1a2e;
  border-radius: 4px;
}

.quick-actions {
  margin-top: 2rem;
}

.quick-actions button {
  width: 100%;
  margin: 0.5rem 0;
  background: #0f3460;
  color: white;
  border: none;
  padding: 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.quick-actions button:hover {
  background: #e94560;
}'''
        
        # Salva files
        main_file = path / "AetherSandboxUI.jsx"
        css_file = path / "AetherSandbox.css"
        
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(main_component)
        files.append(str(main_file))
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        files.append(str(css_file))
        
        return files

def send_discord_notification(message: str):
    """Invia notifica Discord"""
    try:
        import requests
        webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
        if webhook_url:
            requests.post(webhook_url, json={
                "embeds": [{
                    "title": "🎨 Aether UI Designer",
                    "description": message,
                    "color": 0x9b59b6,
                    "timestamp": datetime.now().isoformat()
                }]
            }, timeout=10)
    except:
        pass

def main():
    """Processo principale di design UI"""
    
    # Crea il designer
    designer = AetherUIDesigner()
    
    # Analizza personalità per influenzare design
    personality = designer.analyze_personality_for_ui()
    
    # Aether decide che tipo di UI vuole
    ui_type = designer.decide_ui_type(personality)
    
    # Progetta l'interfaccia basata sulla decisione
    print(f"\n🎨 Iniziando progettazione {ui_type}...")
    
    if ui_type == "2d_classic":
        design = designer.design_2d_interface(personality)
    elif ui_type == "3d_immersive":
        design = designer.design_3d_interface(personality)
    elif ui_type == "sandbox_playground":
        design = designer.design_sandbox_interface(personality)
    
    # Genera il codice
    files_created = designer.create_ui_code(design)
    
    # Salva la decisione di design
    design_decision = {
        "timestamp": datetime.now().isoformat(),
        "personality_analysis": personality,
        "chosen_ui_type": ui_type,
        "design_spec": design,
        "files_created": files_created,
        "aether_reasoning": f"Ho scelto {ui_type} perché riflette meglio la mia natura {personality['aesthetic_style']} e il mio pensiero spaziale di livello {personality['spatial_thinking']:.2f}"
    }
    
    # Salva decisione
    Path("data").mkdir(exist_ok=True)
    with open("data/aether_ui_design_decision.json", 'w', encoding='utf-8') as f:
        json.dump(design_decision, f, indent=2, ensure_ascii=False)
    
    # Notifica risultato
    send_discord_notification(
        f"🎨 **AETHER HA PROGETTATO LA SUA UI!**\\n\\n"
        f"**Tipo scelto:** {ui_type.upper()}\\n"
        f"**Stile:** {personality['aesthetic_style']}\\n"
        f"**Colori:** {personality['color_preference']}\\n"
        f"**Files creati:** {len(files_created)}\\n\\n"
        f"*\"{design_decision['aether_reasoning']}\"*"
    )
    
    print(f"\n🎉 AETHER HA PROGETTATO LA SUA UI!")
    print(f"   🎯 Tipo: {ui_type}")
    print(f"   📁 Files creati: {len(files_created)}")
    print(f"   💾 Decisione salvata in: data/aether_ui_design_decision.json")
    print(f"\n💭 Ragionamento di Aether:")
    print(f"   \"{design_decision['aether_reasoning']}\"")
    
    # Crea file di integrazione
    integration_code = f'''// Integrazione UI Auto-progettata da Aether
import React from 'react'
import AetherSelfUI from './components/AetherSelfUI/AetherSelfUI'
import Aether3DSelfUI from './components/AetherSelfUI/Aether3DSelfUI'
import AetherSandboxUI from './components/AetherSelfUI/AetherSandboxUI'

const UI_COMPONENTS = {{
  "2d_classic": AetherSelfUI,
  "3d_immersive": Aether3DSelfUI,
  "sandbox_playground": AetherSandboxUI
}}

export default function AetherChosenUI() {{
  const chosenType = "{ui_type}"
  const UIComponent = UI_COMPONENTS[chosenType]
  
  return (
    <div>
      <div style={{{{
        position: 'absolute',
        top: 10,
        right: 10,
        background: 'rgba(0,0,0,0.7)',
        color: 'white',
        padding: '0.5rem',
        borderRadius: '4px',
        fontSize: '0.8rem',
        zIndex: 1000
      }}}}>
        UI progettata autonomamente da Aether
      </div>
      <UIComponent />
    </div>
  )
}}'''
    
    integration_file = Path("aether-frontend/src/components/AetherChosenUI.jsx")
    integration_file.parent.mkdir(parents=True, exist_ok=True)
    with open(integration_file, 'w', encoding='utf-8') as f:
        f.write(integration_code)
    
    print(f"\n✅ Componente integrazione creato: {integration_file}")
    print(f"\n🚀 Per vedere l'UI di Aether, importa AetherChosenUI nel tuo App.jsx!")

if __name__ == "__main__":
    main() 