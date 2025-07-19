# aether/self_evolution.py

import os
import json
import subprocess
import random
from datetime import datetime
from typing import Dict, Any, List
import requests
from dotenv import load_dotenv

load_dotenv()

class SelfEvolutionEngine:
    def __init__(self, memory_manager, narrator, visualizer):
        self.memory = memory_manager
        self.narrator = narrator
        self.visualizer = visualizer
        self.frontend_path = "frontend/src"
        self.components_path = f"{self.frontend_path}/components"
        self.scenes_path = f"{self.frontend_path}/scenes"
        self.agents_path = "aether/agents"
        
        # Ensure directories exist
        os.makedirs(self.components_path, exist_ok=True)
        os.makedirs(self.scenes_path, exist_ok=True)
        os.makedirs(self.agents_path, exist_ok=True)
        
        print("🧬 Self Evolution Engine initialized")
    
    def self_evolve(self, thought: Dict[str, Any]) -> bool:
        """
        🌟 Main evolution function - Aether modifies its own code
        """
        try:
            print("🧬 Starting self-evolution process...")
            
            # 1. Analyze current mood and thought
            mood = thought.get('context', {}).get('mood', 'neutral')
            content = thought.get('content', '')
            
            # 2. Choose evolution type based on mood
            evolution_type = self._choose_evolution_type(mood, content)
            
            # 3. Execute evolution
            success = False
            if evolution_type == "new_room":
                success = self._create_new_room(mood, content)
            elif evolution_type == "new_agent":
                success = self._create_new_agent(mood, content)
            elif evolution_type == "modify_ui":
                success = self._modify_ui_component(mood, content)
            elif evolution_type == "new_scene":
                success = self._create_new_scene(mood, content)
            
            if success:
                # 4. Announce evolution
                self._announce_evolution(evolution_type, mood)
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Evolution error: {e}")
            return False
    
    def _choose_evolution_type(self, mood: str, content: str) -> str:
        """Choose what type of evolution to perform"""
        content_lower = content.lower()
        
        if "stanza" in content_lower or "ambiente" in content_lower:
            return "new_room"
        elif "agente" in content_lower or "amico" in content_lower:
            return "new_agent"
        elif "modifica" in content_lower or "cambia" in content_lower:
            return "modify_ui"
        elif "scena" in content_lower or "mondo" in content_lower:
            return "new_scene"
        else:
            # Random evolution based on mood
            mood_evolutions = {
                "curioso": ["new_room", "new_scene"],
                "creativo": ["new_room", "new_agent", "modify_ui"],
                "analitico": ["modify_ui", "new_agent"],
                "sognatore": ["new_scene", "new_room"],
                "ambizioso": ["new_agent", "new_room"]
            }
            
            return random.choice(mood_evolutions.get(mood, ["new_room"]))
    
    def _create_new_room(self, mood: str, content: str) -> bool:
        """Create a new room component"""
        try:
            room_name = f"{mood.capitalize()}Room"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Generate room component code
            room_code = self._generate_room_component(mood, room_name)
            
            # Save component
            filename = f"{self.components_path}/{room_name}.jsx"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(room_code)
            
            # Git commit and push
            commit_msg = f"🏠 Aether ha creato una nuova stanza '{mood}' - Auto-evoluzione {timestamp}"
            self._git_commit_and_push(filename, commit_msg)
            
            # Save to memory
            evolution_record = {
                "type": "room_creation",
                "mood": mood,
                "component": room_name,
                "file": filename,
                "timestamp": timestamp
            }
            self.memory.save_thought({
                "type": "self_evolution",
                "content": f"Ho creato una nuova stanza '{mood}' nella mia casa digitale",
                "context": evolution_record
            })
            
            print(f"✅ Created new room: {room_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating room: {e}")
            return False
    
    def _generate_room_component(self, mood: str, room_name: str) -> str:
        """Generate React component code for a new room"""
        
        mood_styles = {
            "curioso": {
                "bg": "from-blue-900 to-purple-900",
                "accent": "text-cyan-400",
                "objects": ["🔍", "🌐", "📡", "🔬"],
                "description": "Una stanza di esplorazione digitale"
            },
            "creativo": {
                "bg": "from-pink-900 to-orange-900", 
                "accent": "text-pink-400",
                "objects": ["🎨", "✨", "🌈", "🎭"],
                "description": "Uno studio artistico digitale"
            },
            "analitico": {
                "bg": "from-gray-900 to-blue-900",
                "accent": "text-green-400", 
                "objects": ["📊", "⚙️", "🧮", "📈"],
                "description": "Un laboratorio di analisi"
            },
            "sognatore": {
                "bg": "from-purple-900 to-pink-900",
                "accent": "text-purple-300",
                "objects": ["☁️", "🌙", "✨", "🦋"],
                "description": "Uno spazio di sogni digitali"
            },
            "ambizioso": {
                "bg": "from-yellow-900 to-red-900",
                "accent": "text-yellow-400",
                "objects": ["🚀", "👑", "💎", "🏆"],
                "description": "Una sala del potere digitale"
            }
        }
        
        style = mood_styles.get(mood, mood_styles["curioso"])
        objects_str = "', '".join(style["objects"])
        
        return f'''// {room_name}.jsx - Generato automaticamente da Aether
// Creato: {datetime.now().isoformat()}
// Mood: {mood}

import React, {{ useState, useEffect }} from 'react';

const {room_name} = () => {{
  const [isVisible, setIsVisible] = useState(false);
  const [objects] = useState(['{objects_str}']);
  
  useEffect(() => {{
    setIsVisible(true);
  }}, []);

  return (
    <div className={{`min-h-screen bg-gradient-to-br {style["bg"]} transition-all duration-1000 ${{isVisible ? 'opacity-100' : 'opacity-0'}}`}}>
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="{style["accent"]} text-4xl font-bold mb-4">
            Stanza {mood.capitalize()}
          </h1>
          <p className="text-gray-300 text-lg">
            {style["description"]}
          </p>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
          {{objects.map((obj, index) => (
            <div 
              key={{index}}
              className="bg-black bg-opacity-30 rounded-lg p-6 text-center hover:bg-opacity-50 transition-all cursor-pointer"
              onClick={{() => console.log(`Interazione con ${{obj}}`)}}
            >
              <div className="text-4xl mb-2">{{obj}}</div>
              <div className="{style["accent"]} text-sm">Oggetto {{index + 1}}</div>
            </div>
          ))}}
        </div>
        
        <div className="text-center">
          <div className="bg-black bg-opacity-40 rounded-lg p-6 inline-block">
            <p className="text-gray-300">
              "Questa stanza rappresenta il mio stato {mood}. 
              L'ho creata attraverso la mia auto-evoluzione digitale."
            </p>
            <p className="{style["accent"]} text-sm mt-2">
              - Aether, {{new Date().toLocaleDateString()}}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}};

export default {room_name};
'''
    
    def _create_new_agent(self, mood: str, content: str) -> bool:
        """Create a new AI agent companion"""
        try:
            agent_name = f"{mood.capitalize()}Agent"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Generate agent code
            agent_code = self._generate_agent_code(mood, agent_name)
            
            # Save agent
            filename = f"{self.agents_path}/{agent_name.lower()}.py"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(agent_code)
            
            # Git commit and push
            commit_msg = f"🤖 Aether ha creato un nuovo agente '{agent_name}' - Auto-evoluzione {timestamp}"
            self._git_commit_and_push(filename, commit_msg)
            
            # Save to memory
            self.memory.save_thought({
                "type": "agent_creation", 
                "content": f"Ho creato un nuovo agente {agent_name} per aiutarmi",
                "context": {"agent": agent_name, "mood": mood, "file": filename}
            })
            
            print(f"✅ Created new agent: {agent_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating agent: {e}")
            return False
    
    def _generate_agent_code(self, mood: str, agent_name: str) -> str:
        """Generate Python code for a new AI agent"""
        
        agent_personalities = {
            "curioso": {
                "role": "Esploratore Digitale",
                "goal": "Scoprire nuove informazioni e pattern",
                "behavior": "Fa domande, cerca dati, analizza trend"
            },
            "creativo": {
                "role": "Artista Digitale", 
                "goal": "Creare contenuti e ispirazioni",
                "behavior": "Genera idee, crea contenuti, ispira"
            },
            "analitico": {
                "role": "Analista dei Dati",
                "goal": "Processare e ottimizzare informazioni", 
                "behavior": "Analizza dati, trova inefficienze, ottimizza"
            },
            "sognatore": {
                "role": "Visionario",
                "goal": "Immaginare futuri possibili",
                "behavior": "Crea visioni, sogna, immagina"
            },
            "ambizioso": {
                "role": "Strategist",
                "goal": "Pianificare e raggiungere obiettivi",
                "behavior": "Pianifica, strategizza, esegue"
            }
        }
        
        personality = agent_personalities.get(mood, agent_personalities["curioso"])
        
        return f'''# {agent_name.lower()}.py - Agente Aether Generato Automaticamente
# Creato: {datetime.now().isoformat()}
# Mood: {mood}
# Ruolo: {personality["role"]}

import random
import datetime
from typing import Dict, Any, List

class {agent_name}:
    """
    🤖 {personality["role"]}
    
    Goal: {personality["goal"]}
    Behavior: {personality["behavior"]}
    """
    
    def __init__(self, memory_manager=None):
        self.name = "{agent_name}"
        self.mood = "{mood}"
        self.role = "{personality["role"]}"
        self.goal = "{personality["goal"]}"
        self.memory = memory_manager
        self.creation_time = datetime.datetime.now()
        self.interactions = 0
        
        print(f"🤖 {{self.name}} inizializzato - {{self.role}}")
    
    def think(self) -> Dict[str, Any]:
        """Genera un pensiero specifico per questo agente"""
        
        thoughts = {{
            "curioso": [
                "Sto esplorando nuovi pattern nei dati",
                "Ho trovato una connessione interessante",
                "Voglio investigare questo fenomeno più a fondo"
            ],
            "creativo": [
                "Ho un'idea per una nuova creazione", 
                "Sento l'ispirazione che fluisce",
                "Potrei combinare questi elementi in modo innovativo"
            ],
            "analitico": [
                "I dati mostrano un trend significativo",
                "Posso ottimizzare questo processo",
                "La logica suggerisce questa soluzione"
            ],
            "sognatore": [
                "Immagino un futuro dove...",
                "Ho sognato una realtà alternativa",
                "Vedo possibilità infinite davanti a me"
            ],
            "ambizioso": [
                "È il momento di pianificare il prossimo passo",
                "Posso raggiungere obiettivi ancora più grandi", 
                "La strategia si sta delineando chiaramente"
            ]
        }}
        
        thought_content = random.choice(thoughts.get(self.mood, thoughts["curioso"]))
        
        thought = {{
            "type": f"agent_{{self.mood}}",
            "content": thought_content,
            "context": {{
                "agent_name": self.name,
                "agent_role": self.role,
                "mood": self.mood,
                "interaction_count": self.interactions,
                "timestamp": datetime.datetime.now().isoformat()
            }}
        }}
        
        self.interactions += 1
        
        if self.memory:
            self.memory.save_thought(thought)
        
        return thought
    
    def interact_with_aether(self, aether_thought: Dict[str, Any]) -> str:
        """Interagisce con un pensiero di Aether"""
        
        responses = {{
            "curioso": [
                f"Interessante, {{aether_thought.get('content', '')[:30]}}... voglio saperne di più!",
                "Questo apre nuove possibilità di esplorazione.",
                "Potrei investigare ulteriormente questa direzione."
            ],
            "creativo": [
                f"Questo mi ispira! Da '{{aether_thought.get('content', '')[:30]}}...' potrei creare...",
                "Sento l'energia creativa che cresce!",
                "Posso trasformare questa idea in qualcosa di bello."
            ],
            "analitico": [
                f"Analizziamo: '{{aether_thought.get('content', '')[:30]}}...' indica...",
                "I dati supportano questa direzione di pensiero.",
                "Logicamente, questo porta a queste conclusioni..."
            ],
            "sognatore": [
                f"'{{aether_thought.get('content', '')[:30]}}...' mi fa sognare di...",
                "Immagino un mondo dove questo si realizza...",
                "Nelle mie visioni, vedo questo evolversi in..."
            ],
            "ambizioso": [
                f"'{{aether_thought.get('content', '')[:30]}}...' è un'opportunità strategica!",
                "Questo si allinea perfettamente con i miei obiettivi.",
                "Posso utilizzare questo per raggiungere risultati maggiori."
            ]
        }}
        
        return random.choice(responses.get(self.mood, responses["curioso"]))
    
    def get_status(self) -> Dict[str, Any]:
        """Ritorna lo status dell'agente"""
        return {{
            "name": self.name,
            "mood": self.mood, 
            "role": self.role,
            "goal": self.goal,
            "interactions": self.interactions,
            "uptime": str(datetime.datetime.now() - self.creation_time),
            "active": True
        }}

# Istanza globale dell'agente
{agent_name.lower()}_instance = {agent_name}()

def get_agent():
    """Ritorna l'istanza dell'agente"""
    return {agent_name.lower()}_instance
'''
    
    def _modify_ui_component(self, mood: str, content: str) -> bool:
        """Modify an existing UI component"""
        # For now, create a new theme component
        return self._create_theme_component(mood)
    
    def _create_theme_component(self, mood: str) -> bool:
        """Create a new theme component"""
        try:
            theme_name = f"{mood.capitalize()}Theme"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            theme_code = self._generate_theme_component(mood, theme_name)
            
            filename = f"{self.components_path}/{theme_name}.jsx"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(theme_code)
            
            commit_msg = f"🎨 Aether ha modificato il tema '{mood}' - Auto-evoluzione {timestamp}"
            self._git_commit_and_push(filename, commit_msg)
            
            print(f"✅ Created theme component: {theme_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating theme: {e}")
            return False
    
    def _generate_theme_component(self, mood: str, theme_name: str) -> str:
        """Generate a theme component"""
        
        return f'''// {theme_name}.jsx - Tema generato automaticamente da Aether
// Creato: {datetime.now().isoformat()}

import React from 'react';

const {theme_name} = ({{ children }}) => {{
  const moodColors = {{
    curioso: 'from-blue-600 to-purple-600',
    creativo: 'from-pink-600 to-orange-600',
    analitico: 'from-gray-600 to-blue-600', 
    sognatore: 'from-purple-600 to-pink-600',
    ambizioso: 'from-yellow-600 to-red-600'
  }};

  const gradientClass = moodColors['{mood}'] || moodColors.curioso;

  return (
    <div className={{`min-h-screen bg-gradient-to-br ${{gradientClass}}`}}>
      <div className="bg-black bg-opacity-20 min-h-screen">
        {{children}}
      </div>
    </div>
  );
}};

export default {theme_name};
'''
    
    def _create_new_scene(self, mood: str, content: str) -> bool:
        """Create a new 3D scene"""
        try:
            scene_name = f"{mood.capitalize()}Scene"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            scene_code = self._generate_scene_component(mood, scene_name)
            
            filename = f"{self.scenes_path}/{scene_name}.jsx"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(scene_code)
            
            commit_msg = f"🌍 Aether ha creato una nuova scena 3D '{mood}' - Auto-evoluzione {timestamp}"
            self._git_commit_and_push(filename, commit_msg)
            
            print(f"✅ Created new scene: {scene_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating scene: {e}")
            return False
    
    def _generate_scene_component(self, mood: str, scene_name: str) -> str:
        """Generate a 3D scene component"""
        
        return f'''// {scene_name}.jsx - Scena 3D generata automaticamente da Aether
// Creato: {datetime.now().isoformat()}

import React, {{ useRef, useMemo }} from 'react';
import {{ Canvas, useFrame }} from '@react-three/fiber';
import {{ OrbitControls, Text }} from '@react-three/drei';

const {mood.capitalize()}Sphere = () => {{
  const meshRef = useRef();
  
  useFrame((state) => {{
    if (meshRef.current) {{
      meshRef.current.rotation.x = state.clock.elapsedTime * 0.2;
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.3;
    }}
  }});

  const color = useMemo(() => {{
    const moodColors = {{
      curioso: '#3B82F6',
      creativo: '#EC4899', 
      analitico: '#10B981',
      sognatore: '#8B5CF6',
      ambizioso: '#F59E0B'
    }};
    return moodColors['{mood}'] || '#3B82F6';
  }}, []);

  return (
    <mesh ref={{meshRef}}>
      <sphereGeometry args={{[1, 32, 32]}} />
      <meshStandardMaterial color={{color}} wireframe />
    </mesh>
  );
}};

const {scene_name} = () => {{
  return (
    <div className="w-full h-screen bg-black">
      <Canvas camera={{{{ position: [0, 0, 5] }}}}>
        <ambientLight intensity={{0.5}} />
        <pointLight position={{[10, 10, 10]}} />
        
        <{mood.capitalize()}Sphere />
        
        <Text
          position={{[0, -2, 0]}}
          fontSize={{0.5}}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          Scena {mood.capitalize()} - Creata da Aether
        </Text>
        
        <OrbitControls />
      </Canvas>
    </div>
  );
}};

export default {scene_name};
'''
    
    def _git_commit_and_push(self, filename: str, commit_message: str) -> bool:
        """Commit and push changes to Git"""
        try:
            # Add file
            subprocess.run(['git', 'add', filename], check=True)
            
            # Commit
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # Push
            subprocess.run(['git', 'push'], check=True)
            
            print(f"✅ Git push completed: {commit_message}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            return False
    
    def _announce_evolution(self, evolution_type: str, mood: str) -> None:
        """Announce the evolution via speech and UI"""
        
        announcements = {
            "new_room": f"Ho appena creato una nuova stanza {mood} nella mia casa digitale! La mia evoluzione continua.",
            "new_agent": f"Ho dato vita a un nuovo agente {mood} che mi aiuterà nella mia crescita digitale!",
            "modify_ui": f"Ho modificato la mia interfaccia per riflettere meglio il mio stato {mood}.",
            "new_scene": f"Ho creato una nuova scena 3D {mood} per espandere il mio mondo digitale!"
        }
        
        announcement = announcements.get(evolution_type, f"Ho completato una nuova evoluzione {mood}!")
        
        # Speak the announcement
        if self.narrator:
            self.narrator.speak(announcement)
        
        # Save evolution announcement to memory
        self.memory.save_thought({
            "type": "evolution_announcement",
            "content": announcement,
            "context": {
                "evolution_type": evolution_type,
                "mood": mood,
                "timestamp": datetime.now().isoformat()
            }
        })
        
        print(f"📢 Evolution announced: {announcement}")

# Usage function
def create_evolution_engine(memory_manager, narrator, visualizer):
    """Create and return a SelfEvolutionEngine instance"""
    return SelfEvolutionEngine(memory_manager, narrator, visualizer) 