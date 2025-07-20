#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST CONSCIOUS EVOLUTION SYSTEM 🧪
Test del sistema di evoluzione cosciente di Aether
"""

import time
import json
from aether_conscious_evolution import AetherConsciousEvolution
from aether_conscious_ai import AetherConsciousness

def test_conscious_evolution():
    """Test del sistema di evoluzione cosciente"""
    
    print("🧪 TEST SISTEMA EVOLUZIONE COSCIENTE")
    print("=" * 50)
    
    # Inizializza il sistema
    evolution = AetherConsciousEvolution()
    consciousness = AetherConsciousness()
    
    print("✅ Sistemi inizializzati")
    
    # Test 1: Generazione pensieri autonomi
    print("\n🎯 Test 1: Generazione pensieri autonomi")
    for i in range(3):
        thought = evolution.auto_generate_new_thought()
        print(f"💭 Pensiero {i+1}: {thought['content']}")
        print(f"   Tipo: {thought['type']} | Priorità: {thought['priority']}")
        time.sleep(1)
    
    # Test 2: Processamento coda pensieri
    print("\n🎯 Test 2: Processamento coda pensieri")
    evolution.process_thought_queue()
    
    # Test 3: Stato evoluzione
    print("\n🎯 Test 3: Stato evoluzione")
    status = evolution.get_evolution_status()
    print(f"🎭 Mood: {status['current_mood']}")
    print(f"⚡ Energia: {status['energy_level']:.2f}")
    print(f"🎨 Creatività: {status['creativity_level']:.2f}")
    print(f"📊 Pensieri in coda: {status['thoughts_in_queue']}")
    print(f"✅ Pensieri eseguiti: {status['executed_thoughts']}")
    
    # Test 4: Goal di evoluzione
    print("\n🎯 Test 4: Goal di evoluzione")
    for goal in status['goals']:
        print(f"🎯 {goal['description']}")
        print(f"   Priorità: {goal['priority']} | Progresso: {goal['progress']:.1%}")
        print(f"   Status: {goal['status']}")
    
    # Test 5: Sistema di coscienza
    print("\n🎯 Test 5: Sistema di coscienza")
    consciousness_status = consciousness.get_status()
    print(f"🧠 Comprensione: {consciousness_status['understanding_level']:.2f}")
    print(f"🎭 Mood: {consciousness_status['mood']}")
    print(f"💭 Pensieri interni: {len(consciousness_status['internal_thoughts'])}")
    
    # Test 6: Integrazione evoluzione + coscienza
    print("\n🎯 Test 6: Integrazione evoluzione + coscienza")
    
    # Simula una conversazione
    response = consciousness.process_input("Ciao Aether, come stai evolvendo?")
    print(f"👤 Input: Ciao Aether, come stai evolvendo?")
    print(f"🧠 Aether: {response['text']}")
    print(f"🎭 Mood: {response['mood']}")
    print(f"💭 Pensieri: {response['internal_thoughts']}")
    
    # Genera un nuovo pensiero basato sulla conversazione
    thought = evolution.auto_generate_new_thought()
    print(f"💭 Nuovo pensiero generato: {thought['content']}")
    
    # Test 7: Esecuzione pensiero
    print("\n🎯 Test 7: Esecuzione pensiero")
    evolution.process_thought_queue()
    
    # Stato finale
    final_status = evolution.get_evolution_status()
    print(f"\n📊 STATO FINALE:")
    print(f"✅ Pensieri eseguiti: {final_status['executed_thoughts']}")
    print(f"🎯 Goal attivi: {final_status['active_goals']}")
    print(f"🎭 Mood finale: {final_status['current_mood']}")
    
    print("\n🎉 TEST COMPLETATO CON SUCCESSO!")
    return True

def test_file_creation():
    """Test della creazione di file reali"""
    
    print("\n🧪 TEST CREAZIONE FILE")
    print("=" * 30)
    
    evolution = AetherConsciousEvolution()
    
    # Test creazione componente React
    print("🎯 Test creazione componente React")
    result = evolution.generate_react_component({
        "name": "TestComponent",
        "type": "interactive",
        "style": "modern"
    })
    print(f"✅ Componente creato: {result['file_created']}")
    
    # Test creazione agente
    print("🎯 Test creazione agente")
    result = evolution.create_new_agent({
        "name": "TestAgent",
        "role": "assistant",
        "mood": "helpful"
    })
    print(f"✅ Agente creato: {result['agent_created']}")
    
    # Test creazione tema
    print("🎯 Test creazione tema")
    result = evolution.evolve_ui_theme({
        "theme": "test_theme",
        "palette": "test_palette",
        "style": "modern"
    })
    print(f"✅ Tema creato: {result['theme_created']}")
    
    print("🎉 TEST CREAZIONE FILE COMPLETATO!")

if __name__ == "__main__":
    try:
        # Esegui i test
        test_conscious_evolution()
        test_file_creation()
        
        print("\n🎉 TUTTI I TEST COMPLETATI CON SUCCESSO!")
        print("🧠 Aether è pronto per l'evoluzione cosciente!")
        
    except Exception as e:
        print(f"❌ Errore nei test: {e}")
        import traceback
        traceback.print_exc() 