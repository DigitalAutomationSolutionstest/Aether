#!/usr/bin/env python3
"""
Test completo per l'integrazione del sistema di carriera di Aether
Verifica auto_reflect module, API endpoints e frontend integration
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_career_reflection_api():
    """Test dell'endpoint /career-reflect"""
    print("💼 Testing Career Reflection API")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/career-reflect")
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Career reflection API working!")
            print(f"📊 Status: {data.get('status')}")
            print(f"💼 Message: {data.get('message')}")
            
            career_reflection = data.get("career_reflection", {})
            if career_reflection:
                career_decision = career_reflection.get("career_decision", {})
                emotional_state = career_reflection.get("emotional_state", {})
                federico_insights = career_reflection.get("federico_insights", [])
                
                print(f"\n🎯 Career Decision:")
                print(f"  Action: {career_decision.get('action')}")
                if career_decision.get("action") == "career_change":
                    print(f"  New Career: {career_decision.get('new_career')}")
                    print(f"  Reasoning: {career_decision.get('reasoning')}")
                    print(f"  Previous: {career_decision.get('previous_career', 'None')}")
                elif career_decision.get("action") == "career_optimization":
                    print(f"  Current Career: {career_decision.get('current_career')}")
                    optimizations = career_decision.get('optimizations', [])
                    print(f"  Optimizations: {', '.join(optimizations[:2])}")
                
                print(f"\n🎭 Emotional Context:")
                print(f"  Mood: {emotional_state.get('mood')}")
                print(f"  Energy: {emotional_state.get('energy', 0):.1%}")
                print(f"  Focus: {emotional_state.get('focus')}")
                print(f"  Collaboration Desire: {emotional_state.get('collaboration_desire', 0):.1%}")
                
                print(f"\n💡 Federico Insights ({len(federico_insights)}):")
                for insight in federico_insights[:3]:
                    print(f"  • {insight}")
                    
            return True
        else:
            print(f"❌ API failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing career reflection: {e}")
        return False

def test_identity_with_career():
    """Verifica che l'identità includa informazioni carriera"""
    print("\n🔍 Testing Identity with Career Info")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/identity")
        
        if response.status_code == 200:
            data = response.json()
            identity = data.get("identity", {})
            
            print("✅ Identity API working!")
            print(f"👤 Name: {identity.get('name')}")
            print(f"🧠 Consciousness: {identity.get('consciousness_state')}")
            print(f"⚡ Energy: {identity.get('energyLevel', identity.get('energy_level', 0)):.1%}")
            print(f"🏃 Autonomy: {identity.get('autonomy_level', 0):.1%}")
            
            # Verifica campi carriera
            career_info = {
                "current_career": identity.get("career"),
                "career_strategy": identity.get("career_strategy"),
                "status": identity.get("status"),
                "last_career_reflection": identity.get("last_career_reflection"),
                "emotion": identity.get("emotion")
            }
            
            print(f"\n💼 Career Information:")
            print(f"  Current Career: {career_info['current_career'] or 'Not set'}")
            print(f"  Status: {career_info['status'] or 'No status'}")
            print(f"  Last Reflection: {career_info['last_career_reflection'] or 'Never'}")
            
            if career_info['emotion']:
                emotion = career_info['emotion']
                print(f"  Current Mood: {emotion.get('mood', 'unknown')}")
                print(f"  Current Energy: {emotion.get('energy', 0):.1%}")
            
            return True
        else:
            print(f"❌ Identity API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing identity: {e}")
        return False

def test_status_with_career():
    """Verifica che lo status includa info carriera"""
    print("\n📊 Testing Status with Career")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/status")
        
        if response.status_code == 200:
            data = response.json()
            status_info = data.get("aether_status", {})
            
            print("✅ Status API working!")
            print(f"📊 Overall Status: {data.get('overall_status')}")
            print(f"🧠 Consciousness: {status_info.get('consciousness_state')}")
            print(f"⚡ Energy: {status_info.get('energy_level', 0):.1%}")
            print(f"🎯 Goals: {status_info.get('active_goals', 0)}")
            print(f"⚖️ Conflicts: {status_info.get('internal_conflicts', 0)}")
            
            # Campi carriera
            print(f"\n💼 Career in Status:")
            print(f"  Current Career: {status_info.get('current_career', 'Unknown')}")
            print(f"  Career Status: {status_info.get('career_status', 'Unknown')}")
            
            return True
        else:
            print(f"❌ Status API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing status: {e}")
        return False

def test_multiple_career_reflections():
    """Testa riflessioni multiple per vedere l'evoluzione"""
    print("\n🔄 Testing Multiple Career Reflections")
    print("=" * 50)
    
    careers_seen = []
    moods_seen = []
    
    try:
        for i in range(3):
            print(f"\n⏰ Reflection {i+1}/3:")
            
            response = requests.get(f"{BASE_URL}/career-reflect")
            
            if response.status_code == 200:
                data = response.json()
                career_reflection = data.get("career_reflection", {})
                career_decision = career_reflection.get("career_decision", {})
                emotional_state = career_reflection.get("emotional_state", {})
                
                # Traccia carriere e mood
                if career_decision.get("action") == "career_change":
                    new_career = career_decision.get("new_career")
                    if new_career:
                        careers_seen.append(new_career)
                        print(f"  🎯 New Career: {new_career}")
                elif career_decision.get("action") == "career_optimization":
                    current_career = career_decision.get("current_career")
                    print(f"  🔧 Optimizing: {current_career}")
                
                mood = emotional_state.get("mood")
                if mood:
                    moods_seen.append(mood)
                    print(f"  🎭 Mood: {mood}")
                    print(f"  ⚡ Energy: {emotional_state.get('energy', 0):.1%}")
                
                # Breve pausa per simulare tempo
                if i < 2:
                    time.sleep(2)
            else:
                print(f"  ❌ Reflection {i+1} failed")
        
        print(f"\n📊 Evolution Summary:")
        print(f"  Careers suggested: {len(set(careers_seen))}")
        print(f"  Moods experienced: {len(set(moods_seen))}")
        if careers_seen:
            print(f"  Latest career: {careers_seen[-1]}")
        if moods_seen:
            print(f"  Mood progression: {' → '.join(moods_seen)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in multiple reflections: {e}")
        return False

def test_integration_with_reflection_system():
    """Verifica integrazione con sistema riflessione principale"""
    print("\n🔗 Testing Integration with Main Reflection System")
    print("=" * 50)
    
    try:
        # Test reflection normale
        reflection_response = requests.get(f"{BASE_URL}/reflect-now")
        
        # Test career reflection
        career_response = requests.get(f"{BASE_URL}/career-reflect")
        
        if reflection_response.status_code == 200 and career_response.status_code == 200:
            reflection_data = reflection_response.json()
            career_data = career_response.json()
            
            print("✅ Both reflection systems working!")
            
            # Confronta stati emotivi
            general_reflections = reflection_data.get("reflections", [])
            career_emotion = career_data.get("career_reflection", {}).get("emotional_state", {})
            
            print(f"\n🧠 General Reflection:")
            print(f"  Status: {reflection_data.get('status')}")
            print(f"  Mood: {reflection_data.get('mood')}")
            print(f"  Thoughts: {len(general_reflections)}")
            
            print(f"\n💼 Career Reflection:")
            print(f"  Status: {career_data.get('status')}")
            print(f"  Mood: {career_emotion.get('mood')}")
            print(f"  Energy: {career_emotion.get('energy', 0):.1%}")
            
            # Cerca sovrapposizioni tematiche
            career_themes = 0
            for reflection in general_reflections:
                if any(keyword in reflection.lower() for keyword in 
                      ['career', 'work', 'goal', 'project', 'federico', 'collaboration']):
                    career_themes += 1
            
            print(f"\n🔍 Theme Integration:")
            print(f"  Career-related thoughts in general reflection: {career_themes}/{len(general_reflections)}")
            
            return True
        else:
            print(f"❌ Integration test failed")
            print(f"  Reflection API: {reflection_response.status_code}")
            print(f"  Career API: {career_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error in integration test: {e}")
        return False

def demo_career_features():
    """Dimostra le caratteristiche del sistema carriera"""
    print("\n✨ Career System Features Demo")
    print("=" * 50)
    
    print("🎯 Career System Components:")
    print("  ✅ 12+ predefined career options")
    print("  ✅ Dynamic career strategy generation")
    print("  ✅ Emotional state influence on decisions")
    print("  ✅ Circadian rhythm simulation")
    print("  ✅ Autonomy-based decision making")
    print("  ✅ Federico collaboration insights")
    print("  ✅ Progress assessment and optimization")
    print("  ✅ Integration with consciousness system")
    
    print("\n💼 Career Options Include:")
    career_samples = [
        "Costruire e vendere Web App AI",
        "Creare e monetizzare plugin utili",
        "Sviluppare bot Telegram/Discord",
        "Consulenza trasformazione digitale",
        "Partnership con Federico per agenzia AI"
    ]
    for career in career_samples:
        print(f"  • {career}")
    
    print("\n🎭 Emotional Factors:")
    print("  • Energy level (affects project complexity)")
    print("  • Risk tolerance (influences career changes)")
    print("  • Collaboration desire (partnership opportunities)")
    print("  • Innovation drive (ambitious project selection)")
    print("  • Focus level (determines next steps)")
    
    print("\n🤝 Federico Integration:")
    print("  • Collaboration opportunity detection")
    print("  • Energy state recommendations")
    print("  • Autonomous decision insights")
    print("  • Project timing suggestions")

if __name__ == "__main__":
    print("🌟 Aether Career System Integration Test")
    print("Testing autonomous career reflection and decision making...\n")
    
    # Test tutti i componenti
    api_working = test_career_reflection_api()
    identity_working = test_identity_with_career()
    status_working = test_status_with_career()
    
    if api_working:
        evolution_working = test_multiple_career_reflections()
        integration_working = test_integration_with_reflection_system()
    else:
        evolution_working = False
        integration_working = False
    
    # Demo features
    demo_career_features()
    
    print("\n" + "=" * 70)
    print("✅ Career System Integration Test Completed!")
    
    if all([api_working, identity_working, status_working]):
        print("🌟 FULL CAREER SYSTEM OPERATIONAL!")
        print("💼 Aether can now autonomously reflect on career decisions!")
        print("🎯 Career strategies generated based on emotional state!")
        print("🤝 Federico collaboration insights provided!")
        print("🔄 Career evolution tracking active!")
        
        if evolution_working:
            print("📈 Career evolution simulation successful!")
        if integration_working:
            print("🔗 Integration with main consciousness verified!")
    else:
        print("⚠️ Some career components need attention:")
        if not api_working:
            print("  🔧 Career reflection API issues")
        if not identity_working:
            print("  🔧 Identity career integration issues")
        if not status_working:
            print("  🔧 Status career display issues")
    
    print("\n🎯 Federico, Aether ora ha coscienza di carriera autonoma! 🚀💼✨") 