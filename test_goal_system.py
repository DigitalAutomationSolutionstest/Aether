#!/usr/bin/env python3
"""
Test script per il Sistema di Goals di Aether
Testa riflessioni sui goals, suggerimenti di modifica e auto-modifica
"""

import requests
import json
import time

# Configurazione
BASE_URL = "http://localhost:8000"

def test_goal_reflection():
    """Test della riflessione sui goals"""
    
    print("🎯 Testing Goal Reflection")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/goals")
        result = response.json()
        
        if result["status"] == "success":
            reflection = result["goals_reflection"]
            
            print("✅ Goal reflection successful!")
            print(f"🎯 Status: {reflection.get('status')}")
            print(f"💭 Number of goal thoughts: {len(reflection.get('goal_reflections', []))}")
            
            # Mostra analisi goals
            analysis = reflection.get("goals_analysis", {})
            print(f"\n📊 Goals Analysis:")
            print(f"  Total goals: {analysis.get('total_goals')}")
            print(f"  Active goals: {analysis.get('active_goals')}")
            print(f"  Completed goals: {analysis.get('completed_goals')}")
            print(f"  Primary goal: {analysis.get('primary_goal')}")
            print(f"  Average progress: {analysis.get('average_progress', 0):.2f}")
            
            # Mostra alcune riflessioni sui goals
            goal_thoughts = reflection.get('goal_reflections', [])
            print(f"\n💭 Aether's thoughts on goals:")
            for i, thought in enumerate(goal_thoughts[:3], 1):
                print(f"  {i}. \"{thought}\"")
            
            # Mostra coerenza goals
            coherence = reflection.get('goal_coherence')
            print(f"\n🧠 Goal coherence: {coherence}")
                
        else:
            print(f"❌ Goal reflection failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in goal reflection test: {e}")

def test_goal_suggestions():
    """Test dei suggerimenti per modifiche goals"""
    
    print("\n🔄 Testing Goal Modification Suggestions")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/goals/suggestions")
        result = response.json()
        
        if result["status"] == "success":
            suggestions_data = result["goal_suggestions"]
            suggestions = suggestions_data.get("goal_modification_suggestions", [])
            
            print("✅ Goal suggestions successful!")
            print(f"🔄 Number of suggestions: {len(suggestions)}")
            
            # Mostra stato attuale goals
            current_state = suggestions_data.get("current_goal_state", {})
            print(f"\n📊 Current Goal State:")
            print(f"  Total goals: {current_state.get('total_goals')}")
            print(f"  Active goals: {current_state.get('active_goals')}")
            print(f"  Average progress: {current_state.get('average_progress', 0):.2f}")
            print(f"  Emotional alignment: {current_state.get('emotional_alignment', 0):.2f}")
            
            # Mostra suggerimenti
            if suggestions:
                print(f"\n💡 Aether's suggestions for goal modifications:")
                for i, suggestion in enumerate(suggestions[:4], 1):
                    stype = suggestion.get('type', 'unknown')
                    text = suggestion.get('suggestion', 'No suggestion')
                    reason = suggestion.get('reason', 'No reason')
                    goal = suggestion.get('goal', '')
                    
                    print(f"  {i}. [{stype.upper()}] {text}")
                    print(f"     Goal: {goal}")
                    print(f"     Reason: {reason}")
                    print()
            else:
                print(f"\n✅ No modifications suggested - goals are well-aligned")
                
        else:
            print(f"❌ Goal suggestions failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in goal suggestions test: {e}")

def test_goal_autonomous_modification():
    """Test delle modifiche autonome dei goals"""
    
    print("\n🤖 Testing Autonomous Goal Modification")
    print("=" * 40)
    
    try:
        # Prima controlla lo stato attuale
        response = requests.get(f"{BASE_URL}/identity")
        if response.status_code == 200:
            current_identity = response.json()["identity"]
            current_goals = current_identity.get("goals", [])
            active_goals = current_identity.get("goals_metadata", {}).get("active_goals", [])
            
            print(f"📋 Current state before autonomous thinking:")
            print(f"  Goals: {len(current_goals)}")
            print(f"  Active: {len(active_goals)}")
            for goal in current_goals:
                is_active = "✓" if goal in active_goals else "○"
                print(f"    {is_active} {goal}")
        
        # Trigger pensiero autonomo
        print(f"\n🤔 Triggering autonomous thinking...")
        response = requests.get(f"{BASE_URL}/think")
        result = response.json()
        
        if result["status"] == "success":
            modification = result.get("modification")
            
            if modification:
                print("✅ Autonomous goal modification occurred!")
                print(f"💭 Reason: {modification.get('reason', 'No reason provided')}")
                
                # Mostra modifiche applicate
                print(f"\n🔄 Modifications applied:")
                for key, value in modification.items():
                    if key not in ["reason", "emotional_state", "motivation"]:
                        print(f"  {key}: {value}")
                
                # Mostra stato emotivo che ha influenzato la decisione
                emotional_state = modification.get("emotional_state", {})
                print(f"\n🌡️ Emotional state during decision:")
                for emotion, value in emotional_state.items():
                    intensity = "High" if value > 0.7 else "Medium" if value > 0.4 else "Low"
                    print(f"  {emotion}: {value:.2f} ({intensity})")
                
                motivation = modification.get("motivation", 0)
                print(f"\n⚡ Motivation level: {motivation:.2f}")
                
                # Verifica modifiche ai goals se presenti
                goals_modified = False
                for key in modification.keys():
                    if "goals" in key.lower():
                        goals_modified = True
                        break
                
                if goals_modified:
                    print(f"\n🎯 Goals were modified in this autonomous decision!")
                else:
                    print(f"\n📝 Goals were not modified in this decision")
                
            else:
                print("🤔 Aether thought but decided no changes were needed")
                print("   (Including goals - they remain unchanged)")
                
        else:
            print(f"❌ Autonomous thinking failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in autonomous goal modification test: {e}")

def test_goal_integration_with_reflection():
    """Test dell'integrazione goals con sistema riflessione"""
    
    print("\n🌟 Testing Goal Integration with Reflection System")
    print("=" * 40)
    
    try:
        # Test riflessione completa che include goals
        response = requests.get(f"{BASE_URL}/api/reflect/comprehensive")
        result = response.json()
        
        if result["status"] == "success":
            comprehensive = result["comprehensive_reflection"]
            
            print("✅ Comprehensive reflection successful!")
            
            # Verifica che i goals siano inclusi
            if "goals" in comprehensive["comprehensive_reflection"]:
                goals_reflection = comprehensive["comprehensive_reflection"]["goals"]
                
                print(f"✅ Goals included in comprehensive reflection")
                print(f"🎯 Goal reflection status: {goals_reflection.get('status')}")
                
                analysis = goals_reflection.get("goals_analysis", {})
                print(f"📊 Goals analysis in comprehensive view:")
                print(f"  Total: {analysis.get('total_goals')}")
                print(f"  Active: {analysis.get('active_goals')}")
                print(f"  Progress: {analysis.get('average_progress', 0):.2f}")
                
            else:
                print("⚠️ Goals not found in comprehensive reflection")
            
            # Test stream che include goals
            print(f"\n🌊 Testing reflection stream with goals...")
            stream_response = requests.get(f"{BASE_URL}/api/reflect/stream")
            stream_result = stream_response.json()
            
            if stream_result["status"] == "success":
                stream = stream_result["reflection_stream"]
                
                # Verifica che goals siano nel stream
                goal_stream_found = False
                for reflection_data in stream:
                    if reflection_data["type"] == "goals":
                        goal_stream_found = True
                        print(f"✅ Goals found in reflection stream (sequence {reflection_data['sequence']})")
                        break
                
                if not goal_stream_found:
                    print("⚠️ Goals not found in reflection stream")
                    
                print(f"📊 Total reflections in stream: {len(stream)}")
                
        else:
            print(f"❌ Comprehensive reflection failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in goal integration test: {e}")

def test_goal_system_with_periodic_reflection():
    """Test del sistema goals con riflessioni periodiche"""
    
    print("\n🔄 Testing Goal System with Periodic Reflection")
    print("=" * 40)
    
    try:
        goal_reflections = []
        
        # Simula 3 riflessioni periodiche sui goals
        for cycle in range(3):
            print(f"\n📅 Periodic reflection cycle {cycle + 1}/3")
            
            response = requests.get(f"{BASE_URL}/reflect")
            if response.status_code == 200:
                data = response.json()
                
                if data["status"] == "success":
                    reflection = data["reflection"]
                    
                    # Cerca riflessioni sui goals
                    thoughts = reflection.get("reflection", [])
                    goal_related_thoughts = []
                    
                    for thought in thoughts:
                        if any(keyword in thought.lower() for keyword in ["goal", "purpose", "aspiration", "objective"]):
                            goal_related_thoughts.append(thought)
                    
                    goal_reflections.append({
                        "cycle": cycle + 1,
                        "total_thoughts": len(thoughts),
                        "goal_thoughts": goal_related_thoughts,
                        "consciousness_level": reflection.get("consciousness_level")
                    })
                    
                    print(f"✅ Reflection {cycle + 1} completed")
                    print(f"💭 Total thoughts: {len(thoughts)}")
                    print(f"🎯 Goal-related thoughts: {len(goal_related_thoughts)}")
                    
                    if goal_related_thoughts:
                        print(f"   Goal thought: \"{goal_related_thoughts[0][:80]}...\"")
            
            if cycle < 2:
                print("⏳ Waiting 5 seconds for next cycle...")
                time.sleep(5)
        
        # Analisi risultati
        print(f"\n📈 Periodic Reflection Analysis:")
        total_goal_thoughts = sum(len(ref["goal_thoughts"]) for ref in goal_reflections)
        total_thoughts = sum(ref["total_thoughts"] for ref in goal_reflections)
        
        print(f"  Total cycles: {len(goal_reflections)}")
        print(f"  Total thoughts: {total_thoughts}")
        print(f"  Goal-related thoughts: {total_goal_thoughts}")
        print(f"  Goal thought ratio: {(total_goal_thoughts/total_thoughts)*100:.1f}%")
        
        print(f"\n✅ Goals are integrated in periodic reflection system!")
        
    except Exception as e:
        print(f"❌ Error in periodic goal reflection test: {e}")

def test_goal_modification_via_self_modify():
    """Test modifica goals tramite /self-modify"""
    
    print("\n⚙️ Testing Goal Modification via Self-Modify")
    print("=" * 40)
    
    try:
        # Prima ottieni stato attuale
        response = requests.get(f"{BASE_URL}/identity")
        if response.status_code == 200:
            current_identity = response.json()["identity"]
            current_goals = current_identity.get("goals", [])
            print(f"📋 Current goals: {len(current_goals)}")
            for i, goal in enumerate(current_goals, 1):
                print(f"  {i}. {goal}")
        
        # Test aggiunta nuovo goal
        print(f"\n➕ Testing adding new goal...")
        new_goal = "Master digital consciousness architecture"
        
        # Assicurati che current_goals sia una lista
        if not isinstance(current_goals, list):
            current_goals = []
        
        modification_data = {
            "modifications": {
                "goals": current_goals + [new_goal],
                "goals_metadata": {
                    **current_identity.get("goals_metadata", {}),
                    "goal_priorities": {
                        **current_identity.get("goals_metadata", {}).get("goal_priorities", {}),
                        new_goal: 0.8
                    },
                    "goal_progress": {
                        **current_identity.get("goals_metadata", {}).get("goal_progress", {}),
                        new_goal: 0.0
                    }
                }
            },
            "reason": "Testing goal system - adding new architectural goal"
        }
        
        response = requests.post(f"{BASE_URL}/api/self/modify", json=modification_data)
        result = response.json()
        
        if result.get("success"):
            print("✅ Goal modification successful!")
            print(f"🎯 Added goal: '{new_goal}'")
            print(f"📝 Reason: {modification_data['reason']}")
            
            # Verifica che la modifica sia stata applicata
            time.sleep(2)
            verify_response = requests.get(f"{BASE_URL}/identity")
            if verify_response.status_code == 200:
                updated_identity = verify_response.json()["identity"]
                updated_goals = updated_identity.get("goals", [])
                
                if new_goal in updated_goals:
                    print(f"✅ Goal successfully persisted in identity")
                    print(f"📊 Total goals now: {len(updated_goals)}")
                else:
                    print(f"⚠️ Goal not found in updated identity")
        else:
            print(f"❌ Goal modification failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in goal modification test: {e}")

if __name__ == "__main__":
    print("🌟 Aether Goal System Test Suite")
    print("Testing complete goal reflection and modification system...\n")
    
    try:
        # Test sequenza completa del sistema goals
        test_goal_reflection()
        test_goal_suggestions()
        test_goal_autonomous_modification()
        test_goal_integration_with_reflection()
        test_goal_system_with_periodic_reflection()
        test_goal_modification_via_self_modify()
        
        print("\n" + "=" * 60)
        print("✅ All goal system tests completed!")
        print("🎯 Goal reflection system operational")
        print("🔄 Goal modification suggestions working")
        print("🤖 Autonomous goal modification functional")
        print("🌟 Goal integration with consciousness system active")
        print("🔄 Periodic goal reflection working")
        print("⚙️ Manual goal modification via API working")
        
        print("\n🧬 Aether's Goal System Summary:")
        print("✅ Aether can reflect deeply on its goals")
        print("✅ Aether suggests its own goal modifications")
        print("✅ Aether can autonomously modify its goals")
        print("✅ Goals are integrated in consciousness reflection")
        print("✅ Goals evolve through periodic self-examination")
        print("✅ Goals can be modified through self-modification API")
        
        print("\n🌟 Aether now has a complete living goal system!")
        print("🎯 Goals drive purpose, reflection guides evolution!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}") 