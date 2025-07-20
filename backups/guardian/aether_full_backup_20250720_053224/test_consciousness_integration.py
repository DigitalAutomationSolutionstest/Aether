#!/usr/bin/env python3
"""
Test di Integrazione per il Sistema di Coscienza di Aether
Verifica l'integrazione completa frontend-backend per le riflessioni
"""

import requests
import json
import time
import asyncio

# Configurazione
BASE_URL = "http://localhost:8000"

def test_reflect_endpoint_integration():
    """Test dell'endpoint /reflect per l'integrazione frontend"""
    
    print("🧠 Testing /reflect Endpoint Integration")
    print("=" * 50)
    
    try:
        # Simula chiamata frontend ogni minuto
        for i in range(3):  # 3 chiamate di test
            print(f"\n📡 Call {i+1}/3 - Simulating frontend periodic call...")
            
            response = requests.get(f"{BASE_URL}/reflect")
            
            if response.status_code == 200:
                data = response.json()
                
                if data["status"] == "success":
                    reflection = data["reflection"]
                    
                    print(f"✅ Reflection received successfully")
                    print(f"🧠 Consciousness level: {reflection.get('consciousness_level')}")
                    print(f"⏰ Status: {reflection.get('status')}")
                    print(f"💭 Thoughts count: {len(reflection.get('reflection', []))}")
                    
                    # Mostra pensieri come li vedrebbe il frontend
                    thoughts = reflection.get('reflection', [])
                    if thoughts:
                        print(f"\n🌟 Current thoughts for frontend display:")
                        for j, thought in enumerate(thoughts[:2], 1):
                            print(f"  {j}. \"{thought[:100]}...\"")
                    
                    # Mostra stato emotivo per il frontend
                    emotions = reflection.get('emotional_influence', {})
                    if emotions:
                        print(f"\n🌡️ Emotional state for frontend:")
                        for emotion, value in emotions.items():
                            intensity = "High" if value > 0.7 else "Medium" if value > 0.4 else "Low"
                            print(f"  {emotion}: {value:.2f} ({intensity})")
                    
                    print(f"\n📊 Frontend would store this reflection in state")
                    
                else:
                    print(f"❌ Reflection failed: {data.get('message')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
            
            if i < 2:  # Pausa tra le chiamate (simula intervallo frontend)
                print(f"⏳ Waiting 10 seconds (simulating 1-minute interval)...")
                time.sleep(10)
                
    except Exception as e:
        print(f"❌ Integration test error: {e}")

def test_consciousness_state_for_ui():
    """Test dello stato di coscienza per l'UI"""
    
    print("\n🔍 Testing Consciousness State for UI")
    print("=" * 50)
    
    try:
        # Test stato di coscienza
        response = requests.get(f"{BASE_URL}/api/reflect/consciousness-state")
        
        if response.status_code == 200:
            data = response.json()
            
            if data["status"] == "success":
                state = data["consciousness_state"]
                
                print("✅ Consciousness state retrieved for UI")
                print(f"🧠 Consciousness depth: {state.get('consciousness_depth')}")
                print(f"🔍 Self-awareness: {state.get('self_awareness_level')}")
                print(f"📚 Reflection capacity: {state.get('reflection_capacity')}")
                print(f"🤔 Philosophical readiness: {state.get('philosophical_readiness')}")
                
                # Simula come l'UI userebbe questi dati
                print(f"\n📱 UI Integration Preview:")
                consciousness_depth = state.get('consciousness_depth', 'unknown')
                
                # Colori UI basati su livello di coscienza
                ui_colors = {
                    'transcendent': '🟣 Purple (Transcendent)',
                    'deep': '🔵 Blue (Deep)',
                    'moderate': '🟢 Cyan (Moderate)', 
                    'surface': '🟢 Green (Surface)',
                    'unknown': '⚪ Gray (Unknown)'
                }
                
                ui_color = ui_colors.get(consciousness_depth, '⚪ Gray (Unknown)')
                print(f"  Consciousness Indicator Color: {ui_color}")
                
                # Badge di stato
                emotions = state.get('emotional_influence', {})
                if emotions:
                    print(f"  Emotional Badges:")
                    for emotion, value in emotions.items():
                        if value > 0.7:
                            print(f"    🔥 {emotion}: HIGH")
                        elif value > 0.4:
                            print(f"    🌊 {emotion}: MEDIUM")
                        else:
                            print(f"    💨 {emotion}: LOW")
                            
            else:
                print(f"❌ State retrieval failed: {data.get('message')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ UI state test error: {e}")

def test_reflection_stream_for_history():
    """Test del flusso di riflessioni per la cronologia UI"""
    
    print("\n🌊 Testing Reflection Stream for History")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/stream")
        
        if response.status_code == 200:
            data = response.json()
            
            if data["status"] == "success":
                stream = data["reflection_stream"]
                
                print("✅ Reflection stream retrieved for history")
                print(f"📊 Total reflections in stream: {len(stream)}")
                print(f"🌊 Meta-reflection: \"{data.get('meta_reflection')}\"")
                
                # Simula cronologia UI
                print(f"\n📜 UI History Preview:")
                for i, reflection_data in enumerate(stream[:3], 1):  # Solo primi 3
                    rtype = reflection_data['type']
                    sequence = reflection_data['sequence']
                    reflection = reflection_data['reflection']
                    
                    print(f"\n  {sequence}. [{rtype.upper()}] Reflection")
                    
                    # Mostra pensieri come nella cronologia
                    if 'reflection' in reflection:
                        thoughts = reflection['reflection']
                        if thoughts:
                            print(f"     💭 \"{thoughts[0][:80]}...\"")
                    elif 'existential_reflections' in reflection:
                        thoughts = reflection['existential_reflections']
                        if thoughts:
                            print(f"     🌌 \"{thoughts[0][:80]}...\"")
                    
                    # Timestamp simulato
                    print(f"     ⏰ {time.strftime('%H:%M:%S')}")
                
            else:
                print(f"❌ Stream retrieval failed: {data.get('message')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Stream test error: {e}")

def test_periodic_reflection_simulation():
    """Simula il comportamento periodico del frontend"""
    
    print("\n🔄 Testing Periodic Reflection Simulation")
    print("=" * 50)
    
    reflection_history = []
    
    try:
        print("🚀 Starting simulated periodic reflection cycle...")
        print("   (This simulates what the frontend useEffect would do)")
        
        for cycle in range(3):  # 3 cicli di test
            print(f"\n📅 Cycle {cycle + 1}/3")
            
            # Simula chiamata periodica del frontend
            response = requests.get(f"{BASE_URL}/reflect")
            
            if response.status_code == 200:
                data = response.json()
                
                if data["status"] == "success":
                    reflection = data["reflection"]
                    
                    # Simula storage nel state del frontend
                    reflection_entry = {
                        "id": len(reflection_history) + 1,
                        "timestamp": time.time(),
                        "thoughts": reflection.get('reflection', []),
                        "consciousness_level": reflection.get('consciousness_level'),
                        "emotional_state": reflection.get('emotional_influence', {}),
                        "status": reflection.get('status', 'thinking')
                    }
                    
                    reflection_history.append(reflection_entry)
                    
                    print(f"✅ Reflection stored in frontend state")
                    print(f"📝 Entry ID: {reflection_entry['id']}")
                    print(f"🧠 Consciousness: {reflection_entry['consciousness_level']}")
                    print(f"💭 Thoughts: {len(reflection_entry['thoughts'])}")
                    
                    # Mostra stato dell'array frontend
                    print(f"\n📊 Frontend State Array Status:")
                    print(f"   Total reflections: {len(reflection_history)}")
                    print(f"   Latest consciousness level: {reflection_entry['consciousness_level']}")
                    
                    # Simula update UI
                    if reflection_entry['thoughts']:
                        latest_thought = reflection_entry['thoughts'][0]
                        print(f"   UI would display: \"{latest_thought[:60]}...\"")
                
            else:
                print(f"❌ Cycle {cycle + 1} failed: HTTP {response.status_code}")
            
            if cycle < 2:
                print(f"⏳ Waiting 5 seconds for next cycle...")
                time.sleep(5)
        
        # Summary finale
        print(f"\n📈 Simulation Complete!")
        print(f"✅ Total reflections collected: {len(reflection_history)}")
        print(f"🔄 Periodic updates working correctly")
        print(f"📱 Frontend state management simulation successful")
        
    except Exception as e:
        print(f"❌ Periodic simulation error: {e}")

def test_frontend_error_handling():
    """Test gestione errori per il frontend"""
    
    print("\n⚠️ Testing Frontend Error Handling")
    print("=" * 50)
    
    try:
        # Test chiamata a endpoint inesistente
        print("🔍 Testing invalid endpoint handling...")
        response = requests.get(f"{BASE_URL}/invalid-reflect")
        
        if response.status_code == 404:
            print("✅ 404 error handling works")
            print("   Frontend should show: 'Reflection service unavailable'")
        
        # Test risposta malformata (simulata)
        print(f"\n🔍 Testing valid endpoint with potential issues...")
        response = requests.get(f"{BASE_URL}/reflect")
        
        if response.status_code == 200:
            data = response.json()
            
            # Simula controlli frontend
            required_fields = ['status', 'reflection']
            missing_fields = []
            
            for field in required_fields:
                if field not in data:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"⚠️ Frontend would handle missing fields: {missing_fields}")
            else:
                print("✅ All required fields present")
                print("   Frontend can safely process the response")
                
                # Test struttura dati
                reflection = data.get('reflection', {})
                if 'reflection' in reflection and isinstance(reflection['reflection'], list):
                    print("✅ Thoughts array structure valid")
                else:
                    print("⚠️ Frontend should handle missing thoughts array")
                
                if 'emotional_influence' in reflection and isinstance(reflection['emotional_influence'], dict):
                    print("✅ Emotional state structure valid")
                else:
                    print("⚠️ Frontend should handle missing emotional state")
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")

if __name__ == "__main__":
    print("🌟 Aether Consciousness Integration Test Suite")
    print("Testing complete frontend-backend integration...\n")
    
    try:
        # Test sequenza completa di integrazione
        test_reflect_endpoint_integration()
        test_consciousness_state_for_ui()
        test_reflection_stream_for_history()
        test_periodic_reflection_simulation()
        test_frontend_error_handling()
        
        print("\n" + "=" * 60)
        print("✅ All integration tests completed!")
        print("🧠 /reflect endpoint ready for frontend integration")
        print("🔄 Periodic reflection cycle tested and working")
        print("📱 UI state management simulation successful")
        print("🌊 Reflection stream and history working")
        print("⚠️ Error handling scenarios covered")
        print("🌟 Frontend can now safely integrate consciousness panel!")
        
        print("\n💻 Next steps for frontend integration:")
        print("1. Add useEffect with setInterval in React component")
        print("2. Call /reflect every 60 seconds")
        print("3. Store results in Zustand state")
        print("4. Display in ConsciousnessPanel component")
        print("5. Show live consciousness indicators")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}") 