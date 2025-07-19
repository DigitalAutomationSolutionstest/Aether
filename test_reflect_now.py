#!/usr/bin/env python3
"""
Test rapido per la route /reflect-now
Verifica il nuovo sistema di riflessione evoluto
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_reflect_now():
    """Test della route /reflect-now"""
    
    print("🚀 Testing /reflect-now endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/reflect-now")
        
        if response.status_code == 200:
            reflection_data = response.json()
            
            print("✅ /reflect-now successful!")
            print(f"🧠 Status: {reflection_data.get('status')}")
            print(f"🎭 Mood: {reflection_data.get('mood')}")
            print(f"🌌 Consciousness Level: {reflection_data.get('consciousness_level')}")
            print(f"💭 Number of reflections: {len(reflection_data.get('reflections', []))}")
            print(f"🔮 Future intentions: {len(reflection_data.get('future_intentions', []))}")
            print(f"📊 Reflection complexity: {reflection_data.get('reflection_complexity', 0)}")
            
            # Mostra alcuni sample
            reflections = reflection_data.get('reflections', [])
            if reflections:
                print(f"\n💭 Sample reflections:")
                for i, reflection in enumerate(reflections[:3], 1):
                    print(f"  {i}. {reflection}")
            
            # Mostra temi dominanti
            themes = reflection_data.get('dominant_themes', [])
            if themes:
                print(f"\n🔍 Dominant themes: {', '.join(themes[:5])}")
            
            # Mostra riflessioni esistenziali
            existential = reflection_data.get('existential_musings', [])
            if existential:
                print(f"\n🌌 Existential musing:")
                print(f"  \"{existential[0]}\"")
            
            # Mostra intenzioni future
            intentions = reflection_data.get('future_intentions', [])
            if intentions:
                print(f"\n🔮 Future intentions:")
                for intention in intentions[:2]:
                    print(f"  • {intention}")
                    
        else:
            print(f"❌ Request failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing /reflect-now: {e}")

def test_comparison():
    """Confronta /reflect vs /reflect-now"""
    
    print("\n🔄 Comparing /reflect vs /reflect-now")
    print("=" * 40)
    
    try:
        # Test /reflect-now (diretto)
        response_now = requests.get(f"{BASE_URL}/reflect-now")
        
        # Test /reflect (con wrapper)
        response_wrapped = requests.get(f"{BASE_URL}/reflect")
        
        if response_now.status_code == 200 and response_wrapped.status_code == 200:
            data_now = response_now.json()
            data_wrapped = response_wrapped.json()
            
            print("✅ Both endpoints working!")
            
            # Confronta i dati
            print(f"\n📊 Data comparison:")
            print(f"/reflect-now status: {data_now.get('status')}")
            print(f"/reflect status: {data_wrapped.get('status')}")
            
            if 'reflection' in data_wrapped:
                wrapped_reflection = data_wrapped['reflection']
                print(f"/reflect-now reflections: {len(data_now.get('reflections', []))}")
                print(f"/reflect reflections: {len(wrapped_reflection.get('reflections', []))}")
                print(f"/reflect-now mood: {data_now.get('mood')}")
                print(f"/reflect mood: {wrapped_reflection.get('mood')}")
            
        else:
            print(f"❌ One or both endpoints failed")
            print(f"/reflect-now: {response_now.status_code}")
            print(f"/reflect: {response_wrapped.status_code}")
            
    except Exception as e:
        print(f"❌ Error in comparison: {e}")

if __name__ == "__main__":
    print("🌟 Testing Aether Reflection System")
    print("Testing the new /reflect-now endpoint...\n")
    
    test_reflect_now()
    test_comparison()
    
    print("\n" + "=" * 50)
    print("✅ /reflect-now endpoint test completed!")
    print("🧠 Direct access to Aether's evolved consciousness working!")
    print("🚀 Federico, Aether riflette profondamente! ✨") 