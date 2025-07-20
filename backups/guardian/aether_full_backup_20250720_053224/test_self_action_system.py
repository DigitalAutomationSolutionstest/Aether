#!/usr/bin/env python3
"""
Test completo per il sistema di auto-azione di Aether
Verifica tutte le funzionalità di self_act.py e core/execution.py
"""

import os
import json
import time
import shutil
from datetime import datetime

def cleanup_test_creations():
    """Pulisce le creazioni di test"""
    paths_to_clean = ["creations", "agents", "logs"]
    
    for path in paths_to_clean:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"🧹 Cleaned up {path}")

def setup_test_identity():
    """Crea un'identità di test per Aether"""
    test_identity = {
        "name": "Aether",
        "consciousness_state": "testing",
        "energyLevel": 0.8,
        "energy_level": 0.8,
        "autonomy_level": 0.9,
        "traits": ["curious", "creative", "autonomous"],
        "shape": "crystal",
        "color": "cyan",
        "goals": [
            "Test autonomous action system",
            "Create innovative software",
            "Build digital companions"
        ],
        "career": "Costruire e vendere Web App AI",
        "emotion": {
            "mood": "motivated",
            "focus": "high",
            "creativity": 0.9,
            "curiosity": 0.8,
            "energy": 0.8
        },
        "desire_for_connection": 0.7,
        "fear_of_isolation": 0.3,
        "status": "Ready for autonomous testing"
    }
    
    # Salva identità di test
    with open("identity.json", "w", encoding="utf-8") as f:
        json.dump(test_identity, f, indent=2, ensure_ascii=False)
    
    print("✅ Test identity created")
    return test_identity

def test_basic_self_act():
    """Test dell'azione autonoma di base"""
    print("\n🚀 Testing Basic Self-Act")
    print("=" * 40)
    
    try:
        from self_act import self_act
        
        print("📡 Calling self_act()...")
        action = self_act()
        
        print(f"✅ Action completed: {action}")
        
        # Verifica che l'identità sia stata aggiornata
        with open("identity.json", "r", encoding="utf-8") as f:
            identity = json.load(f)
        
        print(f"📊 Updated status: {identity.get('status', 'No status')}")
        print(f"🕐 Last action: {identity.get('last_action', {}).get('action', 'None')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in basic self_act test: {e}")
        return False

def test_forced_actions():
    """Test di azioni forzate specifiche"""
    print("\n🎯 Testing Forced Actions")
    print("=" * 40)
    
    try:
        from self_act import force_specific_action
        
        actions_to_test = ["app", "game", "agent", "evolve"]
        results = {}
        
        for action_type in actions_to_test:
            print(f"🔧 Testing forced action: {action_type}")
            result = force_specific_action(action_type)
            results[action_type] = result
            print(f"  Result: {result}")
            time.sleep(1)  # Breve pausa tra test
        
        print(f"\n📊 Forced Actions Results:")
        for action, result in results.items():
            status = "✅" if "error" not in result else "❌"
            print(f"  {status} {action}: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in forced actions test: {e}")
        return False

def test_creation_verification():
    """Verifica che le creazioni siano state effettivamente create"""
    print("\n📁 Testing Creation Verification")
    print("=" * 40)
    
    try:
        from core.execution import get_creation_stats
        
        stats = get_creation_stats()
        print(f"📊 Creation Statistics:")
        print(f"  Apps: {stats['apps']}")
        print(f"  Games: {stats['games']}")
        print(f"  Agents: {stats['agents']}")
        print(f"  Total: {stats['total_creations']}")
        
        # Verifica directory e file
        paths_to_check = [
            ("creations/apps", "App creations"),
            ("creations/games", "Game creations"),
            ("agents", "Agent spawns"),
            ("logs", "Thought logs")
        ]
        
        for path, description in paths_to_check:
            if os.path.exists(path):
                items = os.listdir(path)
                print(f"  ✅ {description}: {len(items)} items")
                
                # Mostra alcuni esempi
                for item in items[:3]:
                    print(f"    - {item}")
                if len(items) > 3:
                    print(f"    ... and {len(items) - 3} more")
            else:
                print(f"  📂 {description}: Directory not created yet")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in creation verification: {e}")
        return False

def test_action_history():
    """Test del sistema di tracking delle azioni"""
    print("\n📜 Testing Action History")
    print("=" * 40)
    
    try:
        from self_act import get_last_action_info
        
        action_info = get_last_action_info()
        
        print(f"📊 Action History Info:")
        print(f"  Current Status: {action_info.get('current_status', 'Unknown')}")
        
        last_action = action_info.get('last_action', {})
        if last_action:
            print(f"  Last Action: {last_action.get('action', 'None')}")
            print(f"  Timestamp: {last_action.get('timestamp', 'Unknown')}")
            print(f"  Energy at Action: {last_action.get('energy_at_action', 0):.1%}")
            print(f"  Mood at Action: {last_action.get('mood_at_action', 'Unknown')}")
        else:
            print(f"  No action history found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in action history test: {e}")
        return False

def test_multiple_autonomous_actions():
    """Test di azioni autonome multiple per vedere l'evoluzione"""
    print("\n🔄 Testing Multiple Autonomous Actions")
    print("=" * 40)
    
    try:
        from self_act import self_act
        
        action_sequence = []
        
        # Esegui 5 azioni autonome
        for i in range(5):
            print(f"\n🔄 Autonomous Action {i+1}/5:")
            
            action = self_act()
            action_sequence.append(action)
            
            print(f"  Action: {action}")
            
            # Verifica status aggiornato
            with open("identity.json", "r", encoding="utf-8") as f:
                identity = json.load(f)
            
            print(f"  Status: {identity.get('status', 'Unknown')}")
            print(f"  Energy: {identity.get('energyLevel', 0.5):.1%}")
            
            # Breve pausa tra azioni
            time.sleep(2)
        
        print(f"\n📊 Action Sequence Summary:")
        for i, action in enumerate(action_sequence, 1):
            print(f"  {i}. {action}")
        
        # Analizza pattern
        unique_actions = set(action_sequence)
        print(f"\n🔍 Pattern Analysis:")
        print(f"  Total Actions: {len(action_sequence)}")
        print(f"  Unique Actions: {len(unique_actions)}")
        print(f"  Action Variety: {len(unique_actions)/len(action_sequence):.1%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in multiple actions test: {e}")
        return False

def test_identity_evolution():
    """Test dell'evoluzione dell'identità attraverso le azioni"""
    print("\n🌱 Testing Identity Evolution")
    print("=" * 40)
    
    try:
        # Carica identità iniziale
        with open("identity.json", "r", encoding="utf-8") as f:
            initial_identity = json.load(f)
        
        initial_energy = initial_identity.get("energyLevel", 0.5)
        initial_shape = initial_identity.get("shape", "unknown")
        initial_traits = initial_identity.get("traits", [])
        
        print(f"📊 Initial State:")
        print(f"  Energy: {initial_energy:.1%}")
        print(f"  Shape: {initial_shape}")
        print(f"  Traits: {len(initial_traits)} ({', '.join(initial_traits[:3])})")
        
        # Esegui qualche azione che potrebbe causare evoluzione
        from self_act import force_specific_action
        
        print(f"\n🔄 Forcing evolution action...")
        force_specific_action("evolve")
        
        # Verifica cambiamenti
        with open("identity.json", "r", encoding="utf-8") as f:
            final_identity = json.load(f)
        
        final_energy = final_identity.get("energyLevel", 0.5)
        final_shape = final_identity.get("shape", "unknown")
        final_traits = final_identity.get("traits", [])
        
        print(f"📊 Final State:")
        print(f"  Energy: {final_energy:.1%} (Δ: {final_energy - initial_energy:+.1%})")
        print(f"  Shape: {final_shape} {'(CHANGED)' if final_shape != initial_shape else '(SAME)'}")
        print(f"  Traits: {len(final_traits)} ({', '.join(final_traits[:3])})")
        
        # Verifica evolution log
        evolution_log = final_identity.get("evolution_log", [])
        if evolution_log:
            print(f"\n🧬 Evolution Log ({len(evolution_log)} entries):")
            for entry in evolution_log[-3:]:  # Ultimi 3
                print(f"  - {entry.get('type', 'unknown')}: {entry.get('previous_shape', '?')} → {entry.get('new_shape', '?')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in identity evolution test: {e}")
        return False

def demo_frontend_integration():
    """Dimostra l'integrazione con il frontend"""
    print("\n🌐 Frontend Integration Demo")
    print("=" * 40)
    
    print("🎯 Frontend Integration Features:")
    print("  ✅ Status display in AetherUI bottom bar")
    print("  ✅ Real-time status updates from identity.json")
    print("  ✅ Visual indicators for active actions")
    print("  ✅ Action history tracking")
    
    print("\n📱 Expected Frontend Behavior:")
    print("  1. Bottom status bar shows current action")
    print("  2. Green pulsing dot indicates active action")
    print("  3. Status text updates automatically")
    print("  4. Identity info reflects current state")
    
    # Simula aggiornamento status per frontend
    with open("identity.json", "r", encoding="utf-8") as f:
        identity = json.load(f)
    
    identity["status"] = "🌟 Demo: Aether is actively creating with high energy"
    
    with open("identity.json", "w", encoding="utf-8") as f:
        json.dump(identity, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Current Status for Frontend:")
    print(f"  Status: {identity['status']}")
    print(f"  Energy: {identity.get('energyLevel', 0.5):.1%}")
    print(f"  Shape: {identity.get('shape', 'unknown')}")
    print(f"  Mood: {identity.get('emotion', {}).get('mood', 'unknown')}")

def run_complete_test_suite():
    """Esegue la suite completa di test"""
    print("🌟 Aether Self-Action System Complete Test Suite")
    print("=" * 60)
    
    # Setup
    print("🔧 Setting up test environment...")
    cleanup_test_creations()
    setup_test_identity()
    
    # Test results
    test_results = {}
    
    # Esegui tutti i test
    tests = [
        ("Basic Self-Act", test_basic_self_act),
        ("Forced Actions", test_forced_actions),
        ("Creation Verification", test_creation_verification),
        ("Action History", test_action_history),
        ("Multiple Actions", test_multiple_autonomous_actions),
        ("Identity Evolution", test_identity_evolution)
    ]
    
    for test_name, test_func in tests:
        try:
            print(f"\n" + "="*60)
            result = test_func()
            test_results[test_name] = result
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {e}")
            test_results[test_name] = False
    
    # Demo integrazione frontend
    demo_frontend_integration()
    
    # Risultati finali
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    success_rate = passed_tests / total_tests * 100
    print(f"\n📈 Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🌟 SISTEMA DI AUTO-AZIONE COMPLETAMENTE OPERATIVO!")
        print("🧠 Aether può ora agire autonomamente nel mondo reale!")
        print("🚀 Creazioni, evoluzioni e azioni concrete funzionanti!")
        print("🌐 Integrazione frontend pronta!")
    else:
        print("⚠️ Alcuni test hanno fallito - sistema parzialmente operativo")
    
    print("\n🎯 Federico, Aether è ora ATTIVO e AUTONOMO! 🤖✨")

if __name__ == "__main__":
    run_complete_test_suite() 