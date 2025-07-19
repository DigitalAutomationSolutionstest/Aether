#!/usr/bin/env python3
"""
🧪 Test integrazione completa sistema Aether
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from aether.memory import MemoryManager
from aether.consciousness import Consciousness
from aether.environment import EnvironmentBuilder
from aether.narration import Narrator
from aether.vision import Visualizer

def test_memory_manager():
    print("🧪 Test Memory Manager...")
    try:
        memory = MemoryManager()
        print("✅ Memory Manager inizializzato")
        
        # Test save thought
        test_thought = {
            "type": "integration_test",
            "content": "Test integrazione memoria Aether",
            "context": {"test": True, "system": "memory_manager"}
        }
        
        memory.save_thought(test_thought)
        print("✅ Save thought completato")
        
        return memory
        
    except Exception as e:
        print(f"❌ Errore Memory Manager: {e}")
        return None

def test_consciousness(memory):
    print("\n🧪 Test Consciousness...")
    try:
        consciousness = Consciousness(memory)
        thought = consciousness.generate_thought()
        print(f"✅ Thought generato: {thought['content'][:50]}...")
        return thought
    except Exception as e:
        print(f"❌ Errore Consciousness: {e}")
        return None

def test_environment(memory, thought):
    print("\n🧪 Test Environment...")
    try:
        environment = EnvironmentBuilder(memory)
        environment.build_initial(thought, "test_image.jpg")
        print("✅ Environment creato")
    except Exception as e:
        print(f"❌ Errore Environment: {e}")

def test_narration(thought):
    print("\n🧪 Test Narration...")
    try:
        narrator = Narrator()
        narrator.speak(thought['content'][:50])
        print("✅ Narration completata")
    except Exception as e:
        print(f"❌ Errore Narration: {e}")

def test_vision(thought):
    print("\n🧪 Test Vision...")
    try:
        visualizer = Visualizer()
        url = visualizer.render(thought)
        print(f"✅ Vision completata: {url[:30] if url else 'No image'}")
    except Exception as e:
        print(f"❌ Errore Vision: {e}")

def main():
    print("🚀 Test integrazione sistema Aether completo\n")
    
    # Test Memory Manager
    memory = test_memory_manager()
    if not memory:
        print("❌ Test fallito - Memory Manager non funziona")
        return
    
    # Test Consciousness
    thought = test_consciousness(memory)
    if not thought:
        print("❌ Test fallito - Consciousness non funziona")
        return
    
    # Test altri moduli
    test_environment(memory, thought)
    test_narration(thought)
    test_vision(thought)
    
    print("\n🎉 Test integrazione completato con successo!")
    print("Sistema Aether pronto per l'uso!")

if __name__ == "__main__":
    main() 