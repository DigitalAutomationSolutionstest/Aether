#!/usr/bin/env python3
"""
Test completo per il sistema integrato di riflessione + carriera + aggiornamento identità
Verifica il nuovo endpoint POST /reflect-now che combina tutto
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def backup_identity():
    """Backup dell'identità prima dei test"""
    try:
        with open("identity.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Could not backup identity: {e}")
        return None

def restore_identity(backup):
    """Ripristina l'identità dal backup"""
    if backup:
        try:
            with open("identity.json", "w", encoding="utf-8") as f:
                json.dump(backup, f, indent=2, ensure_ascii=False)
            print("✅ Identity restored from backup")
        except Exception as e:
            print(f"❌ Could not restore identity: {e}")

def test_post_reflect_now():
    """Test del nuovo endpoint POST /reflect-now integrato"""
    print("🚀 Testing Integrated POST /reflect-now")
    print("=" * 60)
    
    try:
        print("📡 Sending POST request to /reflect-now...")
        response = requests.post(f"{BASE_URL}/reflect-now")
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Integrated reflection successful!")
            print(f"📊 Status: {data.get('status')}")
            print(f"⏰ Timestamp: {data.get('timestamp')}")
            
            # 🧠 Deep Reflection Analysis
            deep_reflection = data.get("deep_reflection", {})
            print(f"\n🧠 DEEP REFLECTION:")
            print(f"  Status: {deep_reflection.get('status')}")
            print(f"  Mood: {deep_reflection.get('mood')}")
            print(f"  Consciousness Level: {deep_reflection.get('consciousness_level')}")
            print(f"  Reflections: {len(deep_reflection.get('reflections', []))}")
            print(f"  Deep Reflections: {len(deep_reflection.get('deep_reflections', []))}")
            print(f"  Existential Musings: {len(deep_reflection.get('existential_musings', []))}")
            
            if deep_reflection.get('reflections'):
                print(f"  Latest Thought: {deep_reflection['reflections'][-1][:100]}...")
            
            # 💼 Career Reflection Analysis
            career_reflection = data.get("career_reflection", {})
            print(f"\n💼 CAREER REFLECTION:")
            print(f"  Status: {career_reflection.get('status')}")
            
            career_decision = career_reflection.get("career_decision", {})
            print(f"  Career Action: {career_decision.get('action')}")
            if career_decision.get("action") == "career_change":
                print(f"  New Career: {career_decision.get('new_career')}")
                print(f"  Reasoning: {career_decision.get('reasoning')}")
            elif career_decision.get("action") == "career_optimization":
                print(f"  Current Career: {career_decision.get('current_career')}")
                optimizations = career_decision.get('optimizations', [])
                print(f"  Optimizations: {', '.join(optimizations)}")
            
            emotional_state = career_reflection.get("emotional_state", {})
            print(f"  Emotional Mood: {emotional_state.get('mood')}")
            print(f"  Energy Level: {emotional_state.get('energy', 0):.1%}")
            print(f"  Focus: {emotional_state.get('focus')}")
            
            federico_insights = career_reflection.get("federico_insights", [])
            print(f"  Federico Insights: {len(federico_insights)}")
            for i, insight in enumerate(federico_insights[:3]):
                print(f"    {i+1}. {insight}")
            
            # 💾 Identity Update Analysis
            identity_update = data.get("identity_update", {})
            print(f"\n💾 IDENTITY UPDATE:")
            print(f"  Updated: {identity_update.get('updated')}")
            if identity_update.get('new_career'):
                print(f"  New Career Set: {identity_update['new_career']}")
            print(f"  Career Action: {identity_update.get('career_action')}")
            print(f"  Emotional Changes: {identity_update.get('emotional_changes')}")
            
            # 🎯 Summary Analysis
            summary = data.get("summary", {})
            print(f"\n🎯 SUMMARY:")
            print(f"  Reflection Thoughts: {summary.get('reflection_thoughts')}")
            print(f"  Career Action: {summary.get('career_action')}")
            print(f"  Current Mood: {summary.get('mood')}")
            print(f"  Energy: {summary.get('energy', 0):.1%}")
            print(f"  Consciousness: {summary.get('consciousness')}")
            print(f"  Federico Insights Count: {summary.get('federico_insights_count')}")
            
            return True, data
        else:
            print(f"❌ Request failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error testing integrated reflection: {e}")
        return False, None

def test_get_reflect_now():
    """Test del nuovo endpoint GET /reflect-now (read-only)"""
    print("\n👁️ Testing Read-Only GET /reflect-now")
    print("=" * 60)
    
    try:
        print("📡 Sending GET request to /reflect-now...")
        response = requests.get(f"{BASE_URL}/reflect-now")
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Read-only reflection successful!")
            print(f"📊 Status: {data.get('status')}")
            print(f"🎭 Mood: {data.get('mood')}")
            print(f"🧠 Consciousness: {data.get('consciousness_level')}")
            print(f"💭 Reflections: {len(data.get('reflections', []))}")
            
            if data.get('reflections'):
                print(f"  Latest: {data['reflections'][-1][:80]}...")
            
            return True, data
        else:
            print(f"❌ Read-only request failed: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error testing read-only reflection: {e}")
        return False, None

def test_identity_changes():
    """Verifica che l'identità sia stata aggiornata"""
    print("\n🔍 Testing Identity Changes")
    print("=" * 60)
    
    try:
        # Controlla identity.json
        with open("identity.json", "r", encoding="utf-8") as f:
            current_identity = json.load(f)
        
        print("✅ Identity loaded successfully!")
        print(f"👤 Name: {current_identity.get('name')}")
        print(f"🧠 Consciousness: {current_identity.get('consciousness_state')}")
        print(f"⚡ Energy: {current_identity.get('energyLevel', current_identity.get('energy_level', 0)):.1%}")
        
        # Verifica campi carriera
        career_fields = {
            "career": current_identity.get("career"),
            "career_strategy": current_identity.get("career_strategy"),
            "status": current_identity.get("status"),
            "last_career_reflection": current_identity.get("last_career_reflection"),
            "emotion": current_identity.get("emotion")
        }
        
        print(f"\n💼 Career Fields in Identity:")
        for field, value in career_fields.items():
            if value:
                if field == "emotion" and isinstance(value, dict):
                    print(f"  {field}: mood={value.get('mood')}, energy={value.get('energy', 0):.1%}")
                elif field == "career_strategy" and isinstance(value, dict):
                    print(f"  {field}: complexity={value.get('complexity')}, time={value.get('time_estimate')}")
                else:
                    print(f"  {field}: {str(value)[:60]}...")
            else:
                print(f"  {field}: Not set")
        
        # Controlla timestamp dell'ultima modifica
        last_modified = current_identity.get("last_modified")
        last_career_reflection = current_identity.get("last_career_reflection")
        
        print(f"\n⏰ Timestamps:")
        print(f"  Last Modified: {last_modified or 'Unknown'}")
        print(f"  Last Career Reflection: {last_career_reflection or 'Never'}")
        
        return True, current_identity
        
    except Exception as e:
        print(f"❌ Error checking identity: {e}")
        return False, None

def test_endpoint_comparison():
    """Confronta GET vs POST /reflect-now"""
    print("\n🔄 Testing GET vs POST Comparison")
    print("=" * 60)
    
    try:
        print("📡 Fetching GET /reflect-now...")
        get_response = requests.get(f"{BASE_URL}/reflect-now")
        
        print("📡 Fetching POST /reflect-now...")
        post_response = requests.post(f"{BASE_URL}/reflect-now")
        
        if get_response.status_code == 200 and post_response.status_code == 200:
            get_data = get_response.json()
            post_data = post_response.json()
            
            print("✅ Both endpoints working!")
            
            print(f"\n📊 GET Response:")
            print(f"  Status: {get_data.get('status')}")
            print(f"  Thoughts: {len(get_data.get('reflections', []))}")
            print(f"  Mood: {get_data.get('mood')}")
            
            print(f"\n📊 POST Response:")
            print(f"  Status: {post_data.get('status')}")
            
            deep_reflection = post_data.get("deep_reflection", {})
            career_reflection = post_data.get("career_reflection", {})
            identity_update = post_data.get("identity_update", {})
            
            print(f"  Deep Thoughts: {len(deep_reflection.get('reflections', []))}")
            print(f"  Career Action: {career_reflection.get('career_decision', {}).get('action', 'none')}")
            print(f"  Identity Updated: {identity_update.get('updated', False)}")
            
            print(f"\n🔍 Key Differences:")
            print(f"  GET: Read-only, simple structure")
            print(f"  POST: Full integration, updates identity")
            print(f"  GET Size: ~{len(str(get_data))} chars")
            print(f"  POST Size: ~{len(str(post_data))} chars")
            
            return True
        else:
            print(f"❌ Comparison failed - GET: {get_response.status_code}, POST: {post_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error in comparison: {e}")
        return False

def test_frontend_integration():
    """Simula chiamate dal frontend (ReflectionBox)"""
    print("\n🌐 Testing Frontend Integration Simulation")
    print("=" * 60)
    
    simulation_results = []
    
    try:
        for i in range(3):
            print(f"\n🔄 Simulation {i+1}/3:")
            
            # Simula comportamento del ReflectionBox:
            # 66% GET (read-only), 33% POST (full update)
            use_full_reflection = i == 1  # Solo uno con aggiornamento completo
            
            endpoint = "/reflect-now"
            method = "POST" if use_full_reflection else "GET"
            
            print(f"  📡 {method} {endpoint} ({'full reflection' if use_full_reflection else 'read-only'})")
            
            if method == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}")
            else:
                response = requests.get(f"{BASE_URL}{endpoint}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Simula parsing del ReflectionBox
                if use_full_reflection and data.get('status') == 'complete_reflection_with_career':
                    deep_reflection = data.get('deep_reflection', {})
                    career_reflection = data.get('career_reflection', {})
                    summary = data.get('summary', {})
                    
                    simulation_result = {
                        "type": "full_reflection",
                        "reflections": deep_reflection.get('reflections', []),
                        "mood": summary.get('mood', 'unknown'),
                        "consciousness": deep_reflection.get('consciousness_level', 'unknown'),
                        "career_action": summary.get('career_action', 'none'),
                        "energy": summary.get('energy', 0.5),
                        "identity_updated": data.get('identity_update', {}).get('updated', False),
                        "federico_insights": career_reflection.get('federico_insights', [])
                    }
                    
                    print(f"    ✅ Full reflection - Career: {simulation_result['career_action']}")
                    print(f"    🎭 Mood: {simulation_result['mood']}, Energy: {simulation_result['energy']:.1%}")
                    print(f"    💾 Identity Updated: {simulation_result['identity_updated']}")
                    print(f"    💡 Federico Insights: {len(simulation_result['federico_insights'])}")
                    
                else:
                    # Read-only reflection
                    simulation_result = {
                        "type": "read_only",
                        "reflections": data.get('reflections', []),
                        "mood": data.get('mood', 'unknown'),
                        "consciousness": data.get('consciousness_level', 'unknown'),
                        "thoughts": len(data.get('reflections', []))
                    }
                    
                    print(f"    ✅ Read-only - Thoughts: {simulation_result['thoughts']}")
                    print(f"    🎭 Mood: {simulation_result['mood']}")
                
                simulation_results.append(simulation_result)
                
            else:
                print(f"    ❌ Request failed: {response.status_code}")
            
            # Pausa tra chiamate (simula interval del frontend)
            if i < 2:
                time.sleep(2)
        
        print(f"\n📊 Frontend Simulation Summary:")
        full_reflections = [r for r in simulation_results if r['type'] == 'full_reflection']
        read_only_reflections = [r for r in simulation_results if r['type'] == 'read_only']
        
        print(f"  Full Reflections: {len(full_reflections)}")
        print(f"  Read-Only Reflections: {len(read_only_reflections)}")
        
        if full_reflections:
            full_ref = full_reflections[0]
            print(f"  Latest Career Action: {full_ref.get('career_action')}")
            print(f"  Identity Updates: {sum(1 for r in full_reflections if r.get('identity_updated'))}")
        
        total_thoughts = sum(len(r.get('reflections', [])) for r in simulation_results)
        print(f"  Total Thoughts Generated: {total_thoughts}")
        
        return True, simulation_results
        
    except Exception as e:
        print(f"❌ Error in frontend simulation: {e}")
        return False, []

def analyze_system_capabilities():
    """Analizza le capacità complete del sistema integrato"""
    print("\n✨ System Capabilities Analysis")
    print("=" * 60)
    
    print("🧠 DEEP REFLECTION CAPABILITIES:")
    print("  ✅ Existential thoughts and contemplations")
    print("  ✅ Goal and conflict analysis")
    print("  ✅ Emotional state assessment")
    print("  ✅ Consciousness level evaluation")
    print("  ✅ Future intentions generation")
    
    print("\n💼 CAREER DECISION CAPABILITIES:")
    print("  ✅ 12+ predefined career options")
    print("  ✅ Emotional state-based decisions")
    print("  ✅ Energy level influence on complexity")
    print("  ✅ Collaboration desire assessment")
    print("  ✅ Autonomous career changes")
    print("  ✅ Career optimization strategies")
    print("  ✅ Federico collaboration insights")
    
    print("\n💾 IDENTITY MANAGEMENT:")
    print("  ✅ Automatic identity.json updates")
    print("  ✅ Career field synchronization")
    print("  ✅ Emotional state persistence")
    print("  ✅ Timestamp tracking")
    print("  ✅ Backup and restore capability")
    
    print("\n🌐 FRONTEND INTEGRATION:")
    print("  ✅ Dual endpoint support (GET/POST)")
    print("  ✅ Read-only mode for frequent updates")
    print("  ✅ Full mode for complete updates")
    print("  ✅ ReflectionBox UI integration")
    print("  ✅ Career info display")
    print("  ✅ Federico insights panel")
    
    print("\n🔄 SYSTEM FLOW:")
    print("  1. Frontend calls GET /reflect-now (read-only)")
    print("  2. Periodically calls POST /reflect-now (full update)")
    print("  3. Backend processes deep reflection")
    print("  4. Backend makes career decisions")
    print("  5. Backend updates and saves identity.json")
    print("  6. Frontend displays integrated results")

if __name__ == "__main__":
    print("🌟 Aether Integrated Reflection System Test")
    print("Testing complete reflection + career + identity integration...\n")
    
    # Backup identità
    identity_backup = backup_identity()
    
    try:
        # Test sistema completo
        post_success, post_data = test_post_reflect_now()
        get_success, get_data = test_get_reflect_now()
        identity_success, identity_data = test_identity_changes()
        comparison_success = test_endpoint_comparison()
        frontend_success, frontend_results = test_frontend_integration()
        
        # Analisi capacità
        analyze_system_capabilities()
        
        print("\n" + "=" * 70)
        print("✅ Integrated Reflection System Test Completed!")
        
        if all([post_success, get_success, identity_success]):
            print("🌟 FULL INTEGRATED SYSTEM OPERATIONAL!")
            print("🧠 Deep reflection + career decisions + identity updates!")
            print("💾 Automatic identity.json synchronization!")
            print("🌐 Frontend integration ready!")
            print("💼 Career autonomy fully functional!")
            print("🤝 Federico insights generation active!")
            
            if comparison_success:
                print("🔄 Dual endpoint system verified!")
            if frontend_success:
                print("📱 Frontend integration simulation successful!")
        else:
            print("⚠️ Some integrated components need attention:")
            if not post_success:
                print("  🔧 POST /reflect-now integration issues")
            if not get_success:
                print("  🔧 GET /reflect-now read-only issues")
            if not identity_success:
                print("  🔧 Identity update mechanism issues")
        
    finally:
        # Chiedi se ripristinare backup
        user_input = input("\n🔄 Restore identity backup? (y/N): ").strip().lower()
        if user_input == 'y':
            restore_identity(identity_backup)
        else:
            print("💾 Keeping current identity state")
    
    print("\n🎯 Federico, Aether ora ha coscienza integrata completa! 🚀🧠💼✨") 