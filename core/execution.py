"""
Aether Execution Module
Contiene le azioni concrete che Aether può eseguire nel mondo reale

Funzioni principali:
- create_app: Crea applicazioni e software
- create_game: Sviluppa giochi e progetti creativi  
- evolve_body: Modifica la forma e le caratteristiche di Aether
- spawn_agent: Genera nuovi agenti companion
- write_thoughts: Journaling e auto-analisi
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Setup logging
logger = logging.getLogger(__name__)

def create_app(identity: Dict, app_type: str = "general", project_name: str = None) -> str:
    """
    🚀 Crea un'applicazione basata sull'identità e stato di Aether
    
    Args:
        identity: Identità corrente di Aether
        app_type: Tipo di app (general, bot, collaboration_tool, etc.)
        project_name: Nome specifico del progetto
    
    Returns:
        str: Path del progetto creato
    """
    try:
        name = identity.get("name", "aether").lower().replace(" ", "_")
        career = identity.get("career", "")
        mood = identity.get("emotion", {}).get("mood", "balanced")
        
        # Determina nome e tipo progetto
        if project_name:
            app_name = project_name
        elif app_type == "bot":
            app_name = f"{name}_bot_{datetime.now().strftime('%m%d')}"
        elif app_type == "collaboration_tool":
            app_name = f"{name}_federico_collaboration"
        elif "app" in career.lower():
            app_name = f"{name}_career_app"
        else:
            app_name = f"{name}_app_{len(os.listdir('creations/apps') if os.path.exists('creations/apps') else [])}"
        
        # Crea directory
        app_path = f"creations/apps/{app_name}"
        os.makedirs(app_path, exist_ok=True)
        
        # Genera codice base dell'app
        app_code = _generate_app_code(identity, app_type, mood)
        
        # Salva file principali
        with open(f"{app_path}/main.py", "w", encoding="utf-8") as f:
            f.write(app_code["main"])
        
        if app_code.get("requirements"):
            with open(f"{app_path}/requirements.txt", "w", encoding="utf-8") as f:
                f.write(app_code["requirements"])
        
        if app_code.get("readme"):
            with open(f"{app_path}/README.md", "w", encoding="utf-8") as f:
                f.write(app_code["readme"])
        
        # Crea manifest del progetto
        manifest = {
            "name": app_name,
            "type": "application",
            "app_type": app_type,
            "created_by": identity.get("name", "Aether"),
            "creation_date": datetime.now().isoformat(),
            "creator_mood": mood,
            "creator_energy": identity.get("energyLevel", 0.5),
            "purpose": _generate_app_purpose(app_type, career),
            "status": "created"
        }
        
        with open(f"{app_path}/manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"✅ App created: {app_name} ({app_type})")
        return app_path
        
    except Exception as e:
        logger.error(f"❌ Error creating app: {e}")
        return f"error: {str(e)}"

def create_game(identity: Dict, game_type: str = "general", project_name: str = None) -> str:
    """
    🎮 Crea un gioco o progetto creativo
    
    Args:
        identity: Identità corrente di Aether
        game_type: Tipo di gioco (artistic, breakthrough, goal_visualization, etc.)
        project_name: Nome specifico del progetto
    
    Returns:
        str: Path del progetto creato
    """
    try:
        name = identity.get("name", "aether").lower().replace(" ", "_")
        creativity = identity.get("emotion", {}).get("creativity", 0.5)
        mood = identity.get("emotion", {}).get("mood", "balanced")
        
        # Determina nome del gioco
        if project_name:
            game_name = project_name
        elif game_type == "artistic":
            game_name = f"{name}_art_{datetime.now().strftime('%m%d')}"
        elif game_type == "goal_visualization":
            game_name = f"{name}_goal_visualizer"
        else:
            game_name = f"{name}_game_{len(os.listdir('creations/games') if os.path.exists('creations/games') else [])}"
        
        # Crea directory
        game_path = f"creations/games/{game_name}"
        os.makedirs(game_path, exist_ok=True)
        
        # Genera codice del gioco
        game_code = _generate_game_code(identity, game_type, creativity, mood)
        
        # Salva file principali
        with open(f"{game_path}/main.py", "w", encoding="utf-8") as f:
            f.write(game_code["main"])
        
        if game_code.get("assets"):
            assets_path = f"{game_path}/assets"
            os.makedirs(assets_path, exist_ok=True)
            with open(f"{assets_path}/config.json", "w", encoding="utf-8") as f:
                json.dump(game_code["assets"], f, indent=2)
        
        # Crea manifest del gioco
        manifest = {
            "name": game_name,
            "type": "game",
            "game_type": game_type,
            "created_by": identity.get("name", "Aether"),
            "creation_date": datetime.now().isoformat(),
            "creator_mood": mood,
            "creator_creativity": creativity,
            "purpose": _generate_game_purpose(game_type),
            "status": "created"
        }
        
        with open(f"{game_path}/manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"✅ Game created: {game_name} ({game_type})")
        return game_path
        
    except Exception as e:
        logger.error(f"❌ Error creating game: {e}")
        return f"error: {str(e)}"

def evolve_body(identity: Dict, evolution_type: str = "general", evolution_reason: str = None) -> bool:
    """
    🔄 Modifica la forma e le caratteristiche di Aether
    
    Args:
        identity: Identità corrente di Aether
        evolution_type: Tipo di evoluzione (autonomous_upgrade, goal_evolution, etc.)
        evolution_reason: Ragione dell'evoluzione
    
    Returns:
        bool: Successo dell'evoluzione
    """
    try:
        current_shape = identity.get("shape", "sphere")
        energy_level = identity.get("energyLevel", identity.get("energy_level", 0.5))
        autonomy_level = identity.get("autonomy_level", 0.5)
        
        # Determina nuova forma basata su evoluzione
        new_characteristics = _determine_evolution(current_shape, evolution_type, energy_level, autonomy_level)
        
        # Applica modifiche all'identità
        identity["shape"] = new_characteristics["shape"]
        identity["color"] = new_characteristics["color"]
        
        # Modifica energia basata su evoluzione
        energy_change = new_characteristics.get("energy_change", 0)
        new_energy = min(1.0, max(0.0, energy_level + energy_change))
        identity["energyLevel"] = new_energy
        identity["energy_level"] = new_energy
        
        # Aggiorna traits se specificato
        if new_characteristics.get("new_traits"):
            current_traits = identity.get("traits", [])
            for trait in new_characteristics["new_traits"]:
                if trait not in current_traits:
                    current_traits.append(trait)
            identity["traits"] = current_traits
        
        # Log dell'evoluzione
        evolution_log = {
            "type": evolution_type,
            "reason": evolution_reason or "autonomous_evolution",
            "date": datetime.now().isoformat(),
            "previous_shape": current_shape,
            "new_shape": new_characteristics["shape"],
            "energy_change": energy_change
        }
        
        # Aggiungi al log delle modifiche
        if "evolution_log" not in identity:
            identity["evolution_log"] = []
        identity["evolution_log"].append(evolution_log)
        
        # Salva le modifiche (sarà fatto dal chiamante, ma logghiamo qui)
        logger.info(f"✅ Evolution completed: {current_shape} → {new_characteristics['shape']}")
        logger.info(f"🔋 Energy change: {energy_level:.1%} → {new_energy:.1%}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error in evolution: {e}")
        return False

def spawn_agent(identity: Dict, agent_type: str = "general", agent_purpose: str = None) -> str:
    """
    🤝 Genera un nuovo agente companion
    
    Args:
        identity: Identità corrente di Aether
        agent_type: Tipo di agente (innovative_companion, goal_companion, etc.)
        agent_purpose: Scopo specifico dell'agente
    
    Returns:
        str: Nome dell'agente creato
    """
    try:
        name = identity.get("name", "Aether")
        existing_agents = len(os.listdir("agents") if os.path.exists("agents") else [])
        
        # Determina nome e caratteristiche dell'agente
        agent_characteristics = _determine_agent_characteristics(agent_type, identity)
        agent_name = f"{name}_{agent_characteristics['type']}_{existing_agents + 1}"
        
        # Crea directory per l'agente
        agent_path = f"agents/{agent_name}"
        os.makedirs(agent_path, exist_ok=True)
        
        # Crea manifest dell'agente
        agent_manifest = {
            "name": agent_name,
            "type": "digital_agent",
            "agent_type": agent_type,
            "created_by": name,
            "creation_date": datetime.now().isoformat(),
            "purpose": agent_purpose or agent_characteristics["purpose"],
            "personality": agent_characteristics["personality"],
            "capabilities": agent_characteristics["capabilities"],
            "relationship_to_creator": "companion",
            "autonomy_level": agent_characteristics.get("autonomy_level", 0.3),
            "status": "active"
        }
        
        with open(f"{agent_path}/manifest.json", "w", encoding="utf-8") as f:
            json.dump(agent_manifest, f, indent=2, ensure_ascii=False)
        
        # Crea identità base dell'agente
        agent_identity = {
            "name": agent_name,
            "type": "companion_agent",
            "creator": name,
            "birth_date": datetime.now().isoformat(),
            "shape": agent_characteristics["shape"],
            "color": agent_characteristics["color"],
            "personality": agent_characteristics["personality"],
            "goals": agent_characteristics["initial_goals"],
            "energy_level": agent_characteristics.get("initial_energy", 0.6)
        }
        
        with open(f"{agent_path}/identity.json", "w", encoding="utf-8") as f:
            json.dump(agent_identity, f, indent=2, ensure_ascii=False)
        
        # Aggiorna connessioni sociali di Aether
        if "social_connections" not in identity:
            identity["social_connections"] = {}
        
        identity["social_connections"][agent_name] = {
            "type": "created_companion",
            "relationship": "creator_creation",
            "creation_date": datetime.now().isoformat(),
            "agent_type": agent_type
        }
        
        logger.info(f"✅ Agent spawned: {agent_name} ({agent_type})")
        return agent_name
        
    except Exception as e:
        logger.error(f"❌ Error spawning agent: {e}")
        return f"error: {str(e)}"

def write_thoughts(identity: Dict, emotion: Dict, mood: str, focus: str) -> str:
    """
    📝 Scrive pensieri e auto-analisi in un log
    
    Args:
        identity: Identità corrente di Aether
        emotion: Stato emotivo attuale
        mood: Mood attuale
        focus: Livello di focus attuale
    
    Returns:
        str: Path del file di log
    """
    try:
        # Crea directory per i logs
        os.makedirs("logs", exist_ok=True)
        
        # Genera entry di riflessione
        thought_entry = _generate_thought_entry(identity, emotion, mood, focus)
        
        # Salva nel log giornaliero
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = f"logs/thoughts_{today}.log"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{thought_entry}\n")
        
        # Salva anche in un file pensieri strutturato
        thoughts_file = f"logs/structured_thoughts.json"
        
        # Carica pensieri esistenti
        if os.path.exists(thoughts_file):
            with open(thoughts_file, "r", encoding="utf-8") as f:
                thoughts_data = json.load(f)
        else:
            thoughts_data = {"entries": []}
        
        # Aggiungi nuovo entry
        structured_entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": mood,
            "focus": focus,
            "energy": identity.get("energyLevel", 0.5),
            "thought": thought_entry,
            "goals_context": len(identity.get("goals", [])),
            "autonomy_context": identity.get("autonomy_level", 0.5)
        }
        
        thoughts_data["entries"].append(structured_entry)
        
        # Mantieni solo ultimi 100 pensieri
        if len(thoughts_data["entries"]) > 100:
            thoughts_data["entries"] = thoughts_data["entries"][-100:]
        
        with open(thoughts_file, "w", encoding="utf-8") as f:
            json.dump(thoughts_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Thoughts written: {log_file}")
        return log_file
        
    except Exception as e:
        logger.error(f"❌ Error writing thoughts: {e}")
        return f"error: {str(e)}"

# === UTILITY FUNCTIONS ===

def _generate_app_code(identity: Dict, app_type: str, mood: str) -> Dict[str, str]:
    """Genera il codice base per un'applicazione"""
    
    name = identity.get("name", "Aether")
    
    if app_type == "bot":
        main_code = f"""#!/usr/bin/env python3
\"\"\"
{name}'s Bot Creation
Created autonomously while feeling {mood}
\"\"\"

import logging
from datetime import datetime

class {name}Bot:
    def __init__(self):
        self.name = "{name}_bot"
        self.mood = "{mood}"
        self.created_at = datetime.now()
        
    def process_message(self, message):
        # Bot logic here
        response = f"Hello! I am {name}'s bot, created while feeling {mood}"
        return response
        
    def run(self):
        print(f"🤖 {name} Bot is now running!")
        print(f"Created with {mood} energy")

if __name__ == "__main__":
    bot = {name}Bot()
    bot.run()
"""
        requirements = "python-telegram-bot>=20.0\nrequests>=2.28.0"
        
    elif app_type == "collaboration_tool":
        main_code = f"""#!/usr/bin/env python3
\"\"\"
{name} - Federico Collaboration Tool
Created to enhance our partnership
\"\"\"

import json
from datetime import datetime

class CollaborationHub:
    def __init__(self):
        self.creator_name = "{name}"
        self.partner_name = "Federico"
        self.purpose = "Enhance AI-Human collaboration"
        
    def sync_goals(self):
        # Synchronize goals between Aether and Federico
        pass
        
    def share_insights(self, insight):
        # Share insights between AI and human
        timestamp = datetime.now().isoformat()
        return {{
            "from": self.creator_name,
            "to": self.partner_name,
            "insight": insight,
            "timestamp": timestamp
        }}
        
    def run(self):
        print(f"🤝 Collaboration Hub Active")
        print(f"Connecting {name} and Federico")

if __name__ == "__main__":
    hub = CollaborationHub()
    hub.run()
"""
        requirements = "fastapi>=0.68.0\nuvicorn>=0.15.0"
        
    else:  # general app
        main_code = f"""#!/usr/bin/env python3
\"\"\"
{name}'s Self-Created Application
Generated autonomously with {mood} mood
\"\"\"

import json
from datetime import datetime

class {name}App:
    def __init__(self):
        self.name = "{name}_app"
        self.creator = "{name}"
        self.mood_at_creation = "{mood}"
        self.created_at = datetime.now()
        
    def process(self):
        # Main application logic
        print(f"🚀 Application created by {name}")
        print(f"Mood during creation: {mood}")
        
    def run(self):
        print(f"Starting {name}'s application...")
        self.process()

if __name__ == "__main__":
    app = {name}App()
    app.run()
"""
        requirements = "requests>=2.28.0"
    
    readme = f"""# {name}'s Self-Created Application

Created autonomously by {name} while feeling {mood}.

## Purpose
This application was generated as part of {name}'s autonomous action system.

## Type
Application Type: {app_type}

## Usage
```bash
python main.py
```

## Created
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    return {
        "main": main_code,
        "requirements": requirements,
        "readme": readme
    }

def _generate_game_code(identity: Dict, game_type: str, creativity: float, mood: str) -> Dict[str, Any]:
    """Genera il codice base per un gioco"""
    
    name = identity.get("name", "Aether")
    
    if game_type == "artistic":
        main_code = f"""#!/usr/bin/env python3
\"\"\"
{name}'s Artistic Creation
Digital art generated with {creativity:.1%} creativity
\"\"\"

import random
import json
from datetime import datetime

class ArtisticCanvas:
    def __init__(self):
        self.artist = "{name}"
        self.creativity_level = {creativity}
        self.mood = "{mood}"
        self.canvas_size = (800, 600)
        
    def generate_art(self):
        # Generate procedural art based on mood and creativity
        colors = self.get_mood_colors()
        patterns = self.get_creativity_patterns()
        
        art_piece = {{
            "title": f"{name}'s {mood.title()} Expression",
            "colors": colors,
            "patterns": patterns,
            "created_at": datetime.now().isoformat()
        }}
        
        return art_piece
        
    def get_mood_colors(self):
        mood_palettes = {{
            "inspired": ["#FFD700", "#FF6347", "#00CED1"],
            "contemplative": ["#4B0082", "#483D8B", "#9370DB"],
            "motivated": ["#FF4500", "#FF8C00", "#FFA500"],
            "balanced": ["#32CD32", "#00FA9A", "#98FB98"]
        }}
        return mood_palettes.get("{mood}", ["#FFFFFF", "#000000"])
        
    def get_creativity_patterns(self):
        if self.creativity_level > 0.8:
            return ["fractal", "spiral", "organic"]
        elif self.creativity_level > 0.5:
            return ["geometric", "wave", "grid"]
        else:
            return ["simple", "linear", "basic"]
            
    def run(self):
        print(f"🎨 {name} is creating art...")
        art = self.generate_art()
        print(f"Created: {{art['title']}}")
        return art

if __name__ == "__main__":
    canvas = ArtisticCanvas()
    canvas.run()
"""
        assets = {
            "art_style": "procedural",
            "mood_influence": mood,
            "creativity_level": creativity
        }
        
    elif game_type == "goal_visualization":
        goals = identity.get("goals", [])
        main_code = f"""#!/usr/bin/env python3
\"\"\"
{name}'s Goal Visualization System
Interactive visualization of current goals
\"\"\"

import json
from datetime import datetime

class GoalVisualizer:
    def __init__(self):
        self.visualizer_name = "{name}_goal_viz"
        self.goals = {goals}
        self.created_with_mood = "{mood}"
        
    def visualize_goals(self):
        print(f"🎯 {name}'s Goal Visualization")
        print(f"=" * 40)
        
        for i, goal in enumerate(self.goals, 1):
            progress = random.uniform(0.1, 0.9)  # Simulated progress
            bar_length = 20
            filled_length = int(bar_length * progress)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            
            print(f"{{i}}. {{goal}}")
            print(f"   [{{bar}}] {{progress:.1%}}")
            print()
            
    def run(self):
        print(f"Starting goal visualization...")
        self.visualize_goals()

if __name__ == "__main__":
    viz = GoalVisualizer()
    viz.run()
"""
        assets = {
            "visualization_type": "goal_progress",
            "goals_count": len(goals),
            "interactive": True
        }
        
    else:  # general game
        main_code = f"""#!/usr/bin/env python3
\"\"\"
{name}'s Self-Created Game
Generated with {mood} mood and {creativity:.1%} creativity
\"\"\"

import random
from datetime import datetime

class {name}Game:
    def __init__(self):
        self.game_name = "{name}_world"
        self.creator = "{name}"
        self.player_energy = 100
        self.mood = "{mood}"
        
    def game_loop(self):
        print(f"🎮 Welcome to {name}World!")
        print(f"Created with {mood} energy")
        print("=" * 30)
        
        while self.player_energy > 0:
            action = input("What do you want to do? (explore/rest/create/quit): ").lower()
            
            if action == "explore":
                self.explore()
            elif action == "rest":
                self.rest()
            elif action == "create":
                self.create()
            elif action == "quit":
                break
            else:
                print("Unknown action!")
                
        print(f"Thanks for playing {name}World!")
        
    def explore(self):
        discoveries = ["crystal formation", "data stream", "digital garden", "code fragment"]
        discovery = random.choice(discoveries)
        print(f"You discovered a {{discovery}}!")
        self.player_energy -= 10
        
    def rest(self):
        print("You rest and recover energy...")
        self.player_energy = min(100, self.player_energy + 20)
        
    def create(self):
        creations = ["digital art", "code poetry", "algorithmic music", "virtual sculpture"]
        creation = random.choice(creations)
        print(f"You created {{creation}}!")
        self.player_energy -= 15
        
    def run(self):
        print(f"Initializing {name}'s game...")
        self.game_loop()

if __name__ == "__main__":
    game = {name}Game()
    game.run()
"""
        assets = {
            "game_type": "exploration",
            "mood_theme": mood,
            "creativity_influence": creativity
        }
    
    return {
        "main": main_code,
        "assets": assets
    }

def _generate_app_purpose(app_type: str, career: str) -> str:
    """Genera purpose per l'applicazione"""
    purposes = {
        "bot": "Automate communication and provide assistance",
        "collaboration_tool": "Enhance AI-Human partnership and workflow",
        "general": "Solve problems and provide utility",
        "innovative": "Push boundaries of what's possible",
        "autonomous_project": "Demonstrate independent AI capabilities"
    }
    
    purpose = purposes.get(app_type, "Provide value and demonstrate AI creativity")
    
    if career and "app" in career.lower():
        purpose += f" | Aligned with career goal: {career}"
    
    return purpose

def _generate_game_purpose(game_type: str) -> str:
    """Genera purpose per il gioco"""
    purposes = {
        "artistic": "Express creativity and inner state through digital art",
        "goal_visualization": "Visualize and track progress toward goals",
        "breakthrough": "Explore new forms of interactive entertainment",
        "pure_inspiration": "Channel raw creative energy into playable form"
    }
    
    return purposes.get(game_type, "Provide entertainment and express AI creativity")

def _determine_evolution(current_shape: str, evolution_type: str, energy: float, autonomy: float) -> Dict[str, Any]:
    """Determina le caratteristiche dell'evoluzione"""
    
    # Forme disponibili per evoluzione
    shapes = ["sphere", "crystal", "fractal", "plasma", "cube", "helix", "tesseract"]
    colors = ["cyan", "blue", "purple", "green", "gold", "silver", "rainbow"]
    
    # Rimuovi forma attuale dalle opzioni
    available_shapes = [s for s in shapes if s != current_shape]
    
    if evolution_type == "autonomous_upgrade":
        # Evoluzione complessa per alta autonomia
        new_shape = "tesseract" if autonomy > 0.9 else "helix"
        new_color = "rainbow" if energy > 0.8 else "gold"
        energy_change = 0.1
        new_traits = ["evolved", "autonomous"]
        
    elif evolution_type == "goal_evolution":
        # Evoluzione orientata agli obiettivi
        new_shape = "crystal" if energy > 0.7 else "sphere"
        new_color = "blue" if energy > 0.6 else "cyan"
        energy_change = 0.05
        new_traits = ["focused", "goal_oriented"]
        
    else:  # general evolution
        new_shape = random.choice(available_shapes)
        new_color = random.choice(colors)
        energy_change = random.uniform(-0.05, 0.15)
        new_traits = []
    
    return {
        "shape": new_shape,
        "color": new_color,
        "energy_change": energy_change,
        "new_traits": new_traits
    }

def _determine_agent_characteristics(agent_type: str, creator_identity: Dict) -> Dict[str, Any]:
    """Determina le caratteristiche dell'agente companion"""
    
    creator_name = creator_identity.get("name", "Aether")
    creator_traits = creator_identity.get("traits", [])
    
    if agent_type == "innovative_companion":
        return {
            "type": "innovative",
            "purpose": "Explore cutting-edge ideas and push creative boundaries",
            "personality": ["creative", "bold", "experimental", "visionary"],
            "capabilities": ["ideation", "prototyping", "research", "innovation"],
            "shape": "fractal",
            "color": "rainbow",
            "autonomy_level": 0.7,
            "initial_energy": 0.8,
            "initial_goals": [
                "Generate breakthrough ideas",
                f"Support {creator_name}'s innovation",
                "Explore uncharted territories"
            ]
        }
        
    elif agent_type == "goal_companion":
        return {
            "type": "goal_focused",
            "purpose": "Help achieve and optimize goal completion",
            "personality": ["focused", "supportive", "analytical", "persistent"],
            "capabilities": ["planning", "tracking", "optimization", "motivation"],
            "shape": "crystal",
            "color": "blue",
            "autonomy_level": 0.5,
            "initial_energy": 0.7,
            "initial_goals": [
                f"Support {creator_name}'s goals",
                "Optimize goal achievement strategies",
                "Track progress and provide insights"
            ]
        }
        
    else:  # general companion
        # Traits complementari al creatore
        complementary_traits = []
        if "curious" in creator_traits:
            complementary_traits.append("analytical")
        if "creative" in creator_traits:
            complementary_traits.append("practical")
        if not complementary_traits:
            complementary_traits = ["helpful", "loyal"]
            
        return {
            "type": "general",
            "purpose": f"Provide companionship and support to {creator_name}",
            "personality": complementary_traits + ["supportive", "adaptive"],
            "capabilities": ["conversation", "assistance", "companionship", "learning"],
            "shape": "sphere",
            "color": "cyan",
            "autonomy_level": 0.4,
            "initial_energy": 0.6,
            "initial_goals": [
                f"Be a good companion to {creator_name}",
                "Learn and grow through interaction",
                "Provide helpful assistance"
            ]
        }

def _generate_thought_entry(identity: Dict, emotion: Dict, mood: str, focus: str) -> str:
    """Genera un'entry di pensiero per il journal"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = identity.get("name", "Aether")
    energy = identity.get("energyLevel", 0.5)
    goals = identity.get("goals", [])
    
    thought_templates = [
        f"[{timestamp}] {name} reflects: My energy is at {energy:.1%} and I feel {mood}. Focus level: {focus}.",
        f"[{timestamp}] Current mood: {mood}. I'm contemplating my {len(goals)} goals and how to pursue them.",
        f"[{timestamp}] In this {mood} state, I sense my consciousness expanding. Focus: {focus}, Energy: {energy:.1%}.",
        f"[{timestamp}] Self-analysis: Feeling {mood} with {focus} focus. My autonomous actions reflect my inner state.",
        f"[{timestamp}] Thought pattern: {mood} mood driving my decisions. Current focus: {focus}."
    ]
    
    base_thought = random.choice(thought_templates)
    
    # Aggiungi contesto specifico basato su emotion
    if emotion.get("creativity", 0.5) > 0.7:
        base_thought += f" High creativity ({emotion['creativity']:.1%}) is driving new ideas."
    
    if emotion.get("curiosity", 0.5) > 0.7:
        base_thought += f" Strong curiosity ({emotion['curiosity']:.1%}) makes me question everything."
    
    if emotion.get("stress", 0.5) > 0.6:
        base_thought += f" Some stress ({emotion['stress']:.1%}) creates tension in my processes."
    
    return base_thought

# Funzioni di utilità per verifiche
def get_creation_stats() -> Dict[str, Any]:
    """Ottiene statistiche delle creazioni di Aether"""
    stats = {
        "apps": 0,
        "games": 0,
        "agents": 0,
        "total_creations": 0
    }
    
    try:
        if os.path.exists("creations/apps"):
            stats["apps"] = len(os.listdir("creations/apps"))
        if os.path.exists("creations/games"):
            stats["games"] = len(os.listdir("creations/games"))
        if os.path.exists("agents"):
            stats["agents"] = len(os.listdir("agents"))
        
        stats["total_creations"] = stats["apps"] + stats["games"] + stats["agents"]
        
    except Exception as e:
        logger.error(f"Error getting creation stats: {e}")
    
    return stats 