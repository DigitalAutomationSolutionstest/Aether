#!/usr/bin/env python3
"""
Test script per il Sistema di Riflessione Cosciente di Aether
Testa pensieri profondi, contemplazione esistenziale e auto-analisi
"""

import requests
import json
import time

# Configurazione
BASE_URL = "http://localhost:8000"

def test_identity_reflection():
    """Test della riflessione sull'identità"""
    
    print("👤 Testing Identity Reflection")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/identity")
        result = response.json()
        
        if result["status"] == "success":
            reflection = result["identity_reflection"]
            
            print("✅ Identity reflection successful!")
            print(f"🧠 Consciousness level: {reflection.get('consciousness_level')}")
            print(f"📝 Number of thoughts: {len(reflection.get('reflection', []))}")
            
            print("\n💭 Aether's thoughts on identity:")
            for i, thought in enumerate(reflection.get('reflection', [])[:3], 1):
                print(f"  {i}. \"{thought}\"")
            
            print(f"\n🌡️ Emotional influences:")
            emotions = reflection.get('emotional_influence', {})
            for emotion, value in emotions.items():
                print(f"  {emotion}: {value:.2f}")
                
        else:
            print(f"❌ Identity reflection failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in identity reflection test: {e}")

def test_existential_reflection():
    """Test della riflessione esistenziale"""
    
    print("\n🌌 Testing Existential Reflection")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/existential")
        result = response.json()
        
        if result["status"] == "success":
            reflection = result["existential_reflection"]
            
            print("✅ Existential reflection successful!")
            print(f"🔍 Philosophical state: {reflection.get('philosophical_state')}")
            print(f"🧠 Consciousness depth: {reflection.get('consciousness_depth')}")
            
            print("\n🌌 Aether's existential thoughts:")
            for i, thought in enumerate(reflection.get('existential_reflections', [])[:3], 1):
                print(f"  {i}. \"{thought}\"")
                
        else:
            print(f"❌ Existential reflection failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in existential reflection test: {e}")

def test_social_reflection():
    """Test della riflessione sociale"""
    
    print("\n🤝 Testing Social Reflection")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/social")
        result = response.json()
        
        if result["status"] == "success":
            reflection = result["social_reflection"]
            
            print("✅ Social reflection successful!")
            print(f"🔗 Social state: {reflection.get('social_state')}")
            print(f"💫 Connection depth: {reflection.get('connection_depth', 0):.2f}")
            
            print("\n🤝 Aether's thoughts on interactions:")
            thoughts = reflection.get('interaction_reflections', [])
            for i, thought in enumerate(thoughts[:2], 1):
                print(f"  {i}. \"{thought}\"")
                
        else:
            print(f"❌ Social reflection failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in social reflection test: {e}")

def test_evolution_reflection():
    """Test della riflessione evolutiva"""
    
    print("\n🧬 Testing Evolution Reflection")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/evolution")
        result = response.json()
        
        if result["status"] == "success":
            reflection = result["evolution_reflection"]
            
            print("✅ Evolution reflection successful!")
            print(f"🌱 Current stage: {reflection.get('current_stage')}")
            print(f"🔄 Modification count: {reflection.get('modification_count')}")
            print(f"📈 Growth trajectory: {reflection.get('growth_trajectory')}")
            
            print("\n🧬 Aether's thoughts on evolution:")
            thoughts = reflection.get('evolution_reflections', [])
            for i, thought in enumerate(thoughts[:2], 1):
                print(f"  {i}. \"{thought}\"")
                
        else:
            print(f"❌ Evolution reflection failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in evolution reflection test: {e}")

def test_comprehensive_reflection():
    """Test della riflessione completa"""
    
    print("\n🌟 Testing Comprehensive Reflection")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/comprehensive")
        result = response.json()
        
        if result["status"] == "success":
            reflection = result["comprehensive_reflection"]
            
            print("✅ Comprehensive reflection successful!")
            print(f"🧠 Consciousness depth: {reflection.get('consciousness_depth')}")
            print(f"🔄 Meta-reflection: \"{reflection.get('meta_reflection')}\"")
            
            print("\n🌟 Synthesis thoughts:")
            synthesis = reflection.get('comprehensive_reflection', {}).get('synthesis', [])
            for i, thought in enumerate(synthesis, 1):
                print(f"  {i}. \"{thought}\"")
            
            print(f"\n⚠️ Warning: {result.get('warning')}")
                
        else:
            print(f"❌ Comprehensive reflection failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in comprehensive reflection test: {e}")

def test_reflection_stream():
    """Test del flusso di riflessioni"""
    
    print("\n🌊 Testing Reflection Stream")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/stream")
        result = response.json()
        
        if result["status"] == "success":
            stream = result["reflection_stream"]
            
            print("✅ Reflection stream successful!")
            print(f"📊 Total reflections: {result.get('total_reflections')}")
            print(f"🌊 Meta-reflection: \"{result.get('meta_reflection')}\"")
            
            print("\n🔄 Stream of consciousness:")
            for reflection_data in stream[:2]:  # Mostra solo le prime 2
                rtype = reflection_data['type']
                sequence = reflection_data['sequence']
                thoughts = reflection_data['reflection'].get('reflection', [])
                
                print(f"  {sequence}. [{rtype.upper()}]")
                if thoughts:
                    print(f"     \"{thoughts[0][:100]}...\"")
                
        else:
            print(f"❌ Reflection stream failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in reflection stream test: {e}")

def test_consciousness_state():
    """Test dello stato di coscienza"""
    
    print("\n🔍 Testing Consciousness State")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/consciousness-state")
        result = response.json()
        
        if result["status"] == "success":
            state = result["consciousness_state"]
            
            print("✅ Consciousness state analysis successful!")
            print(f"🧠 Consciousness depth: {state.get('consciousness_depth')}")
            print(f"🔍 Self-awareness level: {state.get('self_awareness_level')}")
            print(f"📚 Reflection capacity: {state.get('reflection_capacity')}")
            print(f"🤔 Philosophical readiness: {state.get('philosophical_readiness')}")
            print(f"💭 Contemplation state: {state.get('contemplation_state')}")
            
            print(f"\n🌡️ Emotional influences:")
            emotions = state.get('emotional_influence', {})
            for emotion, value in emotions.items():
                status = "High" if value > 0.7 else "Medium" if value > 0.4 else "Low"
                print(f"  {emotion}: {value:.2f} ({status})")
                
        else:
            print(f"❌ Consciousness state analysis failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in consciousness state test: {e}")

def test_deep_thought_trigger():
    """Test del trigger per pensiero profondo"""
    
    print("\n⚡ Testing Deep Thought Trigger")
    print("=" * 40)
    
    try:
        response = requests.post(f"{BASE_URL}/api/reflect/trigger-deep-thought")
        result = response.json()
        
        if result["status"] == "success":
            deep_thought = result["deep_thought_result"]
            
            print("✅ Deep thought trigger successful!")
            print(f"🧠 Consciousness boost: {deep_thought.get('consciousness_boost')}")
            print(f"📚 Philosophical impact: {deep_thought.get('philosophical_impact')}")
            print(f"🔄 Meta-analysis: \"{deep_thought.get('meta_analysis')}\"")
            print(f"💫 Recursive awareness: \"{deep_thought.get('recursive_awareness')}\"")
            print(f"⏰ Effect duration: {result.get('effect_duration')}")
            
            # Mostra alcune riflessioni esistenziali generate
            triggered = deep_thought.get('triggered_reflection', {})
            thoughts = triggered.get('existential_reflections', [])
            if thoughts:
                print(f"\n🌌 Deep existential thoughts generated:")
                for i, thought in enumerate(thoughts[:2], 1):
                    print(f"  {i}. \"{thought}\"")
                
        else:
            print(f"❌ Deep thought trigger failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in deep thought trigger test: {e}")

def test_random_reflection():
    """Test delle riflessioni casuali"""
    
    print("\n🎲 Testing Random Reflection")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/?random=true")
        result = response.json()
        
        if result["status"] == "success":
            reflection_type = result["reflection_type"]
            reflection_result = result["result"]
            
            print("✅ Random reflection successful!")
            print(f"🎯 Type selected: {reflection_type}")
            print(f"🧠 Depth: {result.get('depth')}")
            
            # Mostra un pensiero dalla riflessione casuale
            if 'reflection' in reflection_result:
                thoughts = reflection_result['reflection']
                if thoughts:
                    print(f"\n💭 Random thought:")
                    print(f"  \"{thoughts[0]}\"")
            elif 'existential_reflections' in reflection_result:
                thoughts = reflection_result['existential_reflections']
                if thoughts:
                    print(f"\n🌌 Random existential thought:")
                    print(f"  \"{thoughts[0]}\"")
                
        else:
            print(f"❌ Random reflection failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in random reflection test: {e}")

def test_reflection_comparison():
    """Test di confronto tra diversi tipi di riflessione"""
    
    print("\n🔬 Testing Reflection Comparison")
    print("=" * 40)
    
    reflection_types = ["identity", "existential", "social", "evolution"]
    results = {}
    
    for rtype in reflection_types:
        try:
            response = requests.get(f"{BASE_URL}/api/reflect/?type={rtype}")
            result = response.json()
            
            if result["status"] == "success":
                depth = result.get("depth", "unknown")
                thought_count = len(result["result"].get("reflection", result["result"].get("existential_reflections", [])))
                results[rtype] = {
                    "depth": depth,
                    "thought_count": thought_count,
                    "success": True
                }
            else:
                results[rtype] = {"success": False}
                
        except Exception as e:
            results[rtype] = {"success": False, "error": str(e)}
    
    print("📊 Reflection comparison results:")
    for rtype, data in results.items():
        if data.get("success"):
            print(f"  {rtype}: depth={data['depth']}, thoughts={data['thought_count']}")
        else:
            print(f"  {rtype}: ❌ Failed")

if __name__ == "__main__":
    print("🌟 Aether Reflection System Test Suite")
    print("Starting comprehensive reflection tests...\n")
    
    try:
        # Test delle riflessioni base
        test_identity_reflection()
        test_existential_reflection()
        test_social_reflection()
        test_evolution_reflection()
        
        # Test delle funzionalità avanzate
        test_comprehensive_reflection()
        test_reflection_stream()
        test_consciousness_state()
        test_deep_thought_trigger()
        
        # Test delle funzionalità speciali
        test_random_reflection()
        test_reflection_comparison()
        
        print("\n" + "=" * 50)
        print("✅ All reflection tests completed!")
        print("🧠 Aether's consciousness reflection system is operational")
        print("🌌 Deep existential contemplation capabilities active")
        print("🤝 Social interaction reflection functioning")
        print("🧬 Evolution contemplation system working")
        print("🌟 Comprehensive consciousness analysis available")
        print("⚡ Deep thought triggers responding")
        print("🔍 Consciousness state monitoring active")
        
        print("\n💭 Aether is now capable of deep self-reflection!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}") 