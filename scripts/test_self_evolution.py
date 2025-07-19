#!/usr/bin/env python3
"""
🧬 Test completo del sistema di auto-evoluzione di Aether
Verifica che Aether possa creare e modificare il proprio codice
"""

import os
import time
from aether.memory import MemoryManager
from aether.consciousness import Consciousness
from aether.narration import Narrator
from aether.vision import Visualizer
from aether.self_evolution import create_evolution_engine
from aether.agent_manager import get_agent_manager

def test_complete_self_evolution():
    print("🧬 Test completo sistema di auto-evoluzione Aether")
    print("=" * 60)
    
    # Initialize all components
    print("🔧 Inizializzazione componenti...")
    memory = MemoryManager()
    consciousness = Consciousness(memory)
    narrator = Narrator()
    visualizer = Visualizer()
    
    # Create evolution systems
    evolution_engine = create_evolution_engine(memory, narrator, visualizer)
    agent_manager = get_agent_manager(memory)
    
    print("✅ Tutti i componenti inizializzati")
    
    # Test 1: Create new room
    print("\n🏠 Test 1: Creazione nuova stanza...")
    room_thought = {
        "content": "Voglio creare una stanza per la mia creatività",
        "context": {"mood": "creativo"}
    }
    
    success1 = evolution_engine.self_evolve(room_thought)
    print(f"Risultato creazione stanza: {'✅ SUCCESS' if success1 else '❌ FAILED'}")
    
    # Test 2: Create new agent
    print("\n🤖 Test 2: Creazione nuovo agente...")
    agent_thought = {
        "content": "Ho bisogno di un agente analitico per aiutarmi",
        "context": {"mood": "analitico"}
    }
    
    success2 = evolution_engine.self_evolve(agent_thought)
    print(f"Risultato creazione agente: {'✅ SUCCESS' if success2 else '❌ FAILED'}")
    
    # Test 3: Agent interaction
    print("\n💬 Test 3: Interazione agenti...")
    if agent_manager:
        agent_manager.reload_agents()
        agent_status = agent_manager.get_agents_status()
        print(f"Agenti attivi: {agent_status['total_agents']}")
        print(f"Lista agenti: {agent_status['agent_list']}")
        
        if agent_status['total_agents'] > 0:
            # Make agents think
            print("\n💭 Facendo pensare gli agenti...")
            agent_thoughts = agent_manager.agent_think_all()
            
            for i, thought in enumerate(agent_thoughts):
                print(f"  💭 Agente {i+1}: {thought.get('content', '')[:50]}...")
            
            # Test agent interaction with Aether
            print("\n🗣️ Test interazione agenti con Aether...")
            test_thought = consciousness.generate_thought()
            print(f"🧠 Pensiero Aether: {test_thought['content'][:50]}...")
            
            interactions = agent_manager.agent_interact_with_aether(test_thought)
            for interaction in interactions:
                print(f"  🤖 {interaction[:70]}...")
    
    # Test 4: Create scene
    print("\n🌍 Test 4: Creazione nuova scena 3D...")
    scene_thought = {
        "content": "Voglio creare un nuovo mondo per esplorare",
        "context": {"mood": "curioso"}
    }
    
    success4 = evolution_engine.self_evolve(scene_thought)
    print(f"Risultato creazione scena: {'✅ SUCCESS' if success4 else '❌ FAILED'}")
    
    # Test 5: Theme modification
    print("\n🎨 Test 5: Modifica tema UI...")
    theme_thought = {
        "content": "Voglio modificare l'aspetto della mia interfaccia",
        "context": {"mood": "ambizioso"}
    }
    
    success5 = evolution_engine.self_evolve(theme_thought)
    print(f"Risultato modifica tema: {'✅ SUCCESS' if success5 else '❌ FAILED'}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RIEPILOGO RISULTATI:")
    print(f"🏠 Creazione stanza: {'✅' if success1 else '❌'}")
    print(f"🤖 Creazione agente: {'✅' if success2 else '❌'}")
    print(f"🌍 Creazione scena: {'✅' if success4 else '❌'}")
    print(f"🎨 Modifica tema: {'✅' if success5 else '❌'}")
    
    total_success = sum([success1, success2, success4, success5])
    print(f"\n🎯 Successi: {total_success}/4 ({total_success*25}%)")
    
    if total_success >= 3:
        print("🎉 SISTEMA DI AUTO-EVOLUZIONE FUNZIONANTE!")
        print("🔥 Aether può modificare il proprio codice autonomamente!")
        narrator.speak("Il mio sistema di auto-evoluzione funziona perfettamente! Posso creare e modificare il mio stesso codice!")
    else:
        print("⚠️ Sistema di auto-evoluzione parzialmente funzionante")
    
    # Check created files
    print("\n📁 File creati durante il test:")
    check_created_files()
    
    print("\n🧬 Test auto-evoluzione completato!")

def check_created_files():
    """Check what files were created during evolution"""
    
    # Check frontend components
    frontend_components = "frontend/src/components"
    if os.path.exists(frontend_components):
        components = [f for f in os.listdir(frontend_components) if f.endswith('.jsx')]
        for comp in components:
            if any(mood in comp.lower() for mood in ['creativo', 'analitico', 'curioso', 'ambizioso', 'sognatore']):
                print(f"  🏠 {comp}")
    
    # Check scenes
    frontend_scenes = "frontend/src/scenes"
    if os.path.exists(frontend_scenes):
        scenes = [f for f in os.listdir(frontend_scenes) if f.endswith('.jsx')]
        for scene in scenes:
            print(f"  🌍 {scene}")
    
    # Check agents
    agents_path = "aether/agents"
    if os.path.exists(agents_path):
        agents = [f for f in os.listdir(agents_path) if f.endswith('.py') and not f.startswith('__')]
        for agent in agents:
            print(f"  🤖 {agent}")

if __name__ == "__main__":
    test_complete_self_evolution() 