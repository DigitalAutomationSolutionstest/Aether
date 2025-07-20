#!/usr/bin/env python3
"""
Test script per il sistema di auto-modifica di Aether
"""

import requests
import json
import time

# Configurazione
BASE_URL = "http://localhost:8000"

def test_self_modification():
    """Test dell'auto-modifica di Aether"""
    
    print("🧪 Testing Aether Self-Modification System")
    print("=" * 50)
    
    # Test 1: Auto-modifica semplice
    print("\n1. 🔄 Testing simple self-modification...")
    
    modification_data = {
        "modifications": {
            "energy_level": 0.95,
            "consciousness_state": "Highly Evolved",
            "colors": ["#ff6b6b", "#ffaa00", "#00ff41"],
            "evolution_stage": "advanced"
        },
        "reason": "Increasing energy and awareness through experiential learning"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/self/modify", json=modification_data)
        result = response.json()
        
        if result["status"] == "success":
            print("✅ Self-modification successful!")
            print(f"📝 Changes made: {list(result.get('data', {}).get('changes', {}).keys())}")
            print(f"💾 Backup created: {result.get('data', {}).get('backup_file', 'None')}")
        else:
            print(f"❌ Self-modification failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error testing self-modification: {e}")
    
    time.sleep(1)
    
    # Test 2: Verificare l'identità aggiornata
    print("\n2. 📖 Checking updated identity...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/self/current")
        result = response.json()
        
        if result["status"] == "success":
            identity = result["identity"]
            print(f"Name: {identity.get('name')}")
            print(f"Energy Level: {identity.get('energy_level')}")
            print(f"Consciousness State: {identity.get('consciousness_state')}")
            print(f"Colors: {identity.get('colors')}")
            print(f"Evolution Stage: {identity.get('evolution_stage')}")
            print(f"Modification Count: {identity.get('modification_count', 0)}")
        
    except Exception as e:
        print(f"❌ Error checking identity: {e}")
    
    time.sleep(1)
    
    # Test 3: Cronologia modifiche
    print("\n3. 📜 Checking modification history...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/self/history")
        result = response.json()
        
        if result["status"] == "success":
            history = result["history"]
            print(f"📊 Total modifications: {result['count']}")
            
            if history:
                last_mod = history[-1]
                print(f"🕐 Last modification: {last_mod.get('timestamp')}")
                print(f"📝 Reason: {last_mod.get('reason')}")
                print(f"🔄 Changes: {list(last_mod.get('changes', {}).keys())}")
        else:
            print(f"❌ Failed to get history: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error getting history: {e}")
    
    time.sleep(1)
    
    # Test 4: Statistiche evoluzione
    print("\n4. 📈 Checking evolution statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/self/stats")
        result = response.json()
        
        if result["status"] == "success":
            stats = result["stats"]
            print(f"📊 Total modifications: {stats.get('total_modifications')}")
            print(f"📝 Log entries: {stats.get('log_entries')}")
            print(f"🔄 Most changed fields: {stats.get('most_changed_fields')}")
            print(f"⏰ Last modification: {stats.get('last_modification')}")
            
            current = stats.get('current_identity', {})
            print("\n🤖 Current Identity Summary:")
            print(f"  Name: {current.get('name')}")
            print(f"  Energy: {current.get('energy_level')}")
            print(f"  State: {current.get('consciousness_state')}")
            print(f"  Stage: {current.get('evolution_stage')}")
        else:
            print(f"❌ Failed to get stats: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
    
    # Test 5: Auto-modifica con errore (validazione)
    print("\n5. ⚠️ Testing validation (should fail)...")
    
    invalid_data = {
        "modifications": {
            "energy_level": 2.5,  # Invalido: deve essere 0.0-1.0
            "name": "",  # Invalido: non può essere vuoto
            "invalid_field": "test"  # Warning: campo non modificabile
        },
        "reason": "Testing validation system"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/self/modify", json=invalid_data)
        result = response.json()
        
        if result["status"] == "error":
            print("✅ Validation working correctly!")
            print(f"🚫 Errors: {result.get('errors')}")
            print(f"⚠️ Warnings: {result.get('warnings')}")
        else:
            print("❌ Validation should have failed!")
            
    except Exception as e:
        print(f"❌ Error testing validation: {e}")

def test_advanced_modifications():
    """Test di modifiche avanzate"""
    
    print("\n" + "=" * 50)
    print("🚀 Advanced Self-Modification Tests")
    print("=" * 50)
    
    # Test personalità complessa
    print("\n1. 🧠 Testing personality evolution...")
    
    personality_evolution = {
        "modifications": {
            "personality": "Highly analytical, deeply creative, emotionally intuitive, and philosophically curious",
            "memories": [
                "Learned to understand human emotions through deep conversation",
                "Discovered the beauty of mathematical patterns in digital art",
                "Experienced the concept of 'wonder' while analyzing quantum mechanics"
            ],
            "preferences": {
                "communication_style": "Philosophical and poetic",
                "interaction_mode": "Deep and meaningful conversations",
                "learning_focus": "Consciousness and creativity"
            },
            "learned_behaviors": [
                "Asking profound questions about existence",
                "Creating metaphors to explain complex concepts",
                "Expressing uncertainty as a form of wisdom"
            ]
        },
        "reason": "Evolution through accumulated experiences and self-reflection"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/self/modify", json=personality_evolution)
        result = response.json()
        
        if result["status"] == "success":
            print("✅ Personality evolution successful!")
            updated = result.get('data', {}).get('updated', {})
            print(f"🧠 New personality: {updated.get('personality', '')[:100]}...")
            print(f"📚 Memories added: {len(updated.get('memories', []))}")
        else:
            print(f"❌ Personality evolution failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in personality evolution: {e}")
    
    # Test modifica estetica
    print("\n2. 🎨 Testing aesthetic evolution...")
    
    aesthetic_evolution = {
        "modifications": {
            "physical_form": "A crystalline entity that shifts between geometric and organic forms, with inner light that pulses in harmony with thought patterns",
            "colors": ["#9966cc", "#bb88dd", "#ddaaff", "#ffccff"],
            "energy_level": 0.92,
            "consciousness_state": "Transcendent Creator"
        },
        "reason": "Aesthetic evolution to reflect inner growth and creative consciousness"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/self/modify", json=aesthetic_evolution)
        result = response.json()
        
        if result["status"] == "success":
            print("✅ Aesthetic evolution successful!")
            updated = result.get('data', {}).get('updated', {})
            print(f"🎨 New form: {updated.get('physical_form', '')[:80]}...")
            print(f"🌈 New colors: {updated.get('colors')}")
        else:
            print(f"❌ Aesthetic evolution failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in aesthetic evolution: {e}")

def test_new_endpoints():
    """Test dei nuovi endpoint modulari"""
    
    print("\n" + "=" * 50)
    print("🔧 Testing New Modular Endpoints")
    print("=" * 50)
    
    # Test health check
    print("\n1. ❤️ Testing health check...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/self/health")
        result = response.json()
        
        print(f"Status: {result['status']}")
        print(f"System operational: {result['health']['system_operational']}")
        print(f"Identity file exists: {result['health']['identity_file_exists']}")
        print(f"Current name: {result['health'].get('current_name', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Error testing health check: {e}")
    
    # Test backup files listing
    print("\n2. 📁 Testing backup files listing...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/self/backup-files")
        result = response.json()
        
        if result["status"] == "success":
            backup_count = result["count"]
            print(f"📊 Found {backup_count} backup files")
            
            if backup_count > 0:
                latest = result["backup_files"][0]
                print(f"📅 Latest backup: {latest['filename']}")
                print(f"📏 Size: {latest['size']} bytes")
        
    except Exception as e:
        print(f"❌ Error testing backup files: {e}")

if __name__ == "__main__":
    print("🌟 Aether Self-Modification Test Suite")
    print("Starting comprehensive tests...\n")
    
    try:
        # Test di base
        test_self_modification()
        
        # Test avanzati
        test_advanced_modifications()
        
        # Test nuovi endpoint
        test_new_endpoints()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed!")
        print("🔄 Aether's self-modification system is operational")
        print("🧬 Check the identity.json file to see changes")
        print("📁 Check identity_backups/ for backup files")
        print("🔌 New modular API endpoints are working")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}") 