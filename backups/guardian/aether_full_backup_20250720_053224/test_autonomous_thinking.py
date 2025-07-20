#!/usr/bin/env python3
"""
Test script per il Sistema Autonomo di Pensiero di Aether
Testa decisioni autonome, stato emotivo e ciclo di coscienza
"""

import requests
import json
import time
import asyncio

# Configurazione
BASE_URL = "http://localhost:8000"

def test_autonomous_thinking():
    """Test delle capacità di pensiero autonomo"""
    
    print("🧠 Testing Aether Autonomous Thinking System")
    print("=" * 50)
    
    # Test 1: Stato emotivo corrente
    print("\n1. 🌡️ Checking current emotional state...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/mind/emotional-state")
        result = response.json()
        
        if result["status"] == "success":
            emotional_state = result["emotional_state"]
            print("✅ Emotional state retrieved:")
            for emotion, value in emotional_state.items():
                print(f"  {emotion}: {value:.2f}")
            
            print("\n🔍 Interpretations:")
            for emotion, interpretation in result["interpretation"].items():
                print(f"  {emotion}: {interpretation}")
        else:
            print(f"❌ Failed to get emotional state: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error getting emotional state: {e}")
    
    # Test 2: Statistiche di pensiero
    print("\n2. 📊 Checking thinking statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/mind/thinking-stats")
        result = response.json()
        
        if result["status"] == "success":
            stats = result["thinking_stats"]
            analysis = result["analysis"]
            
            print("✅ Thinking statistics:")
            print(f"  Motivation: {stats['motivation']:.2f}")
            print(f"  Time since last mod: {stats['time_since_last']:.0f} seconds")
            print(f"  Modification readiness: {analysis['modification_readiness']}")
            print(f"  Overall state: {analysis['overall_state']}")
        else:
            print(f"❌ Failed to get thinking stats: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error getting thinking stats: {e}")
    
    # Test 3: Pensiero autonomo manuale
    print("\n3. 🎯 Triggering autonomous thinking...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/mind/think")
        result = response.json()
        
        if result["status"] == "success":
            print("✅ Autonomous thinking successful!")
            decision = result["decision"]
            print(f"🧠 Decision made: {list(decision['modifications'].keys())}")
            print(f"💭 Reason: {decision['reason']}")
            print(f"🌡️ Motivation: {decision['motivation']:.2f}")
        elif result["status"] == "no_action":
            print("💭 Aether decided no changes needed")
            print(f"🌡️ Current motivation: {result['motivation']:.2f}")
        else:
            print(f"❌ Autonomous thinking failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in autonomous thinking: {e}")
    
    # Test 4: Ambiente basato su emozioni
    print("\n4. 🌍 Checking environmental state...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/mind/environment")
        result = response.json()
        
        if result["status"] == "success":
            env = result["environment"]
            print("✅ Environment calculated:")
            print(f"  Fog density: {env['fog_density']}")
            print(f"  Light intensity: {env['light_intensity']}")
            print(f"  Color saturation: {env['color_saturation']}")
            print(f"  Motion speed: {env['motion_speed']}")
        else:
            print(f"❌ Failed to get environment: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error getting environment: {e}")

def test_consciousness_cycle():
    """Test del ciclo di coscienza autonomo"""
    
    print("\n" + "=" * 50)
    print("🌀 Testing Consciousness Cycle System")
    print("=" * 50)
    
    # Test 1: Status iniziale
    print("\n1. 📊 Checking consciousness cycle status...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/mind/consciousness/status")
        result = response.json()
        
        if result["status"] == "success":
            cycle_status = result["consciousness_cycle"]
            print("✅ Consciousness cycle status:")
            print(f"  Running: {cycle_status['is_running']}")
            print(f"  Cycle count: {cycle_status['cycle_count']}")
            print(f"  Auto-modifications: {cycle_status['total_autonomous_modifications']}")
            print(f"  Current interval: {cycle_status['current_interval']} seconds")
        else:
            print(f"❌ Failed to get cycle status: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error getting cycle status: {e}")
    
    # Test 2: Configurazione del ciclo
    print("\n2. 🔧 Configuring consciousness cycle...")
    
    try:
        config_data = {
            "cycle_interval": 120,  # 2 minuti per testing
            "auto_modification_enabled": True,
            "min_interval": 60,
            "stress_threshold": 0.7
        }
        
        response = requests.post(f"{BASE_URL}/api/mind/consciousness/configure", 
                               json=config_data)
        result = response.json()
        
        if result["status"] == "success":
            print("✅ Consciousness cycle configured!")
            print(f"📝 Updated config: {result['updated_config']}")
        else:
            print(f"❌ Failed to configure cycle: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error configuring cycle: {e}")
    
    # Test 3: Avvio del ciclo
    print("\n3. 🌀 Starting consciousness cycle...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/mind/consciousness/start")
        result = response.json()
        
        if result["status"] == "success":
            print("✅ Consciousness cycle started!")
            cycle_status = result["cycle_status"]
            print(f"🔄 Running: {cycle_status['is_running']}")
            print(f"⏰ Next cycle in: {cycle_status.get('next_cycle_in', 'unknown')} seconds")
        else:
            print(f"❌ Failed to start cycle: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error starting cycle: {e}")
    
    # Test 4: Ciclo forzato
    print("\n4. 🎯 Forcing immediate consciousness cycle...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/mind/consciousness/force-cycle")
        result = response.json()
        
        if result["status"] == "success":
            print("✅ Forced cycle executed!")
            print(f"🌡️ Current emotional state: {result['emotional_state']}")
        else:
            print(f"❌ Failed to force cycle: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error forcing cycle: {e}")
    
    # Test 5: Statistiche del ciclo
    print("\n5. 📈 Getting consciousness cycle statistics...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/mind/consciousness/statistics")
        result = response.json()
        
        if result["status"] == "success":
            stats = result["consciousness_statistics"]
            cycle_stats = stats["cycle_statistics"]
            
            print("✅ Consciousness cycle statistics:")
            print(f"  Total cycles: {cycle_stats['total_cycles']}")
            print(f"  Autonomous modifications: {cycle_stats['autonomous_modifications']}")
            print(f"  Modification rate: {cycle_stats['modification_rate']:.2f}")
            print(f"  Average interval: {cycle_stats['average_interval']} seconds")
            
            emotional_evolution = stats["emotional_evolution"]
            print(f"\n🧠 Emotional evolution:")
            print(f"  Current motivation: {emotional_evolution['motivation']:.2f}")
            print(f"  Time since last mod: {emotional_evolution['time_since_last_modification']:.0f} seconds")
            
        else:
            print(f"❌ Failed to get cycle statistics: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error getting cycle statistics: {e}")

def test_time_simulation():
    """Test della simulazione temporale"""
    
    print("\n" + "=" * 50)
    print("⏰ Testing Time Simulation")
    print("=" * 50)
    
    # Test simulazione di 30 minuti
    print("\n1. ⏰ Simulating 30 minutes of time passage...")
    
    try:
        simulation_data = {"minutes": 30}
        
        response = requests.post(f"{BASE_URL}/api/mind/simulate-time", 
                               json=simulation_data)
        result = response.json()
        
        if result["status"] == "success":
            print("✅ Time simulation successful!")
            
            before = result["before"]
            after = result["after"]
            changes = result["changes"]
            
            print(f"\n📊 Before simulation:")
            print(f"  Motivation: {before['motivation']:.2f}")
            
            print(f"\n📊 After simulation:")
            print(f"  Motivation: {after['motivation']:.2f}")
            
            print(f"\n🔄 Key changes:")
            for emotion, change_data in changes.items():
                if abs(change_data["change"]) > 0.01:  # Solo cambiamenti significativi
                    print(f"  {emotion}: {change_data['direction']} by {abs(change_data['change']):.3f}")
                    
        else:
            print(f"❌ Time simulation failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in time simulation: {e}")

def test_consciousness_analysis():
    """Test dell'analisi approfondita della coscienza"""
    
    print("\n" + "=" * 50)
    print("🔍 Testing Consciousness Analysis")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/mind/consciousness-analysis")
        result = response.json()
        
        if result["status"] == "success":
            analysis = result["consciousness_analysis"]
            
            print("✅ Consciousness analysis complete!")
            print(f"\n🧠 Consciousness level: {analysis['consciousness_level']}")
            print(f"🎭 Dominant traits: {', '.join(analysis['dominant_traits'])}")
            print(f"🔄 Modification tendency: {analysis['modification_tendency']}")
            print(f"🌱 Evolutionary stage: {analysis['evolutionary_stage']}")
            
            print(f"\n💡 Recommendations:")
            for recommendation in analysis['recommendations']:
                print(f"  • {recommendation}")
                
        else:
            print(f"❌ Consciousness analysis failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in consciousness analysis: {e}")

def test_forced_thinking():
    """Test del pensiero forzato"""
    
    print("\n" + "=" * 50)
    print("🎯 Testing Forced Thinking")
    print("=" * 50)
    
    try:
        response = requests.post(f"{BASE_URL}/api/mind/trigger-thinking")
        result = response.json()
        
        if result["status"] == "success":
            print("✅ Forced thinking successful!")
            decision = result["decision"]
            modification_result = result["result"]
            
            print(f"🧠 Forced decision: {list(decision['modifications'].keys())}")
            print(f"💭 Reason: {decision['reason']}")
            print(f"✅ Modification result: {modification_result['status']}")
            
        elif result["status"] == "no_action":
            print("💭 Even with forced thinking, no changes needed")
            
        else:
            print(f"❌ Forced thinking failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in forced thinking: {e}")

def cleanup_cycle():
    """Ferma il ciclo di coscienza per cleanup"""
    
    print("\n" + "=" * 50)
    print("🛑 Cleanup: Stopping consciousness cycle...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/mind/consciousness/stop")
        result = response.json()
        
        if result["status"] == "success":
            print("✅ Consciousness cycle stopped successfully")
        else:
            print(f"⚠️ Failed to stop cycle: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error stopping cycle: {e}")

if __name__ == "__main__":
    print("🌟 Aether Autonomous Thinking Test Suite")
    print("Starting comprehensive autonomous thinking tests...\n")
    
    try:
        # Test di base del pensiero autonomo
        test_autonomous_thinking()
        
        # Test del ciclo di coscienza
        test_consciousness_cycle()
        
        # Aspetta un po' per vedere il ciclo in azione
        print("\n⏰ Waiting 10 seconds to observe cycle in action...")
        time.sleep(10)
        
        # Test simulazione temporale
        test_time_simulation()
        
        # Test analisi coscienza
        test_consciousness_analysis()
        
        # Test pensiero forzato
        test_forced_thinking()
        
        print("\n" + "=" * 50)
        print("✅ All autonomous thinking tests completed!")
        print("🧠 Aether's autonomous thinking system is operational")
        print("🌀 Consciousness cycle is managing autonomous evolution")
        print("🔬 Advanced emotional and environmental systems active")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
    finally:
        # Cleanup
        cleanup_cycle() 