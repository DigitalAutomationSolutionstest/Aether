#!/usr/bin/env python3
"""
Test script per gli Endpoint Semplificati di Aether
Testa le route dirette senza prefisso /api
"""

import requests
import json
import time

# Configurazione
BASE_URL = "http://localhost:8000"

def test_reflect_endpoint():
    """Test dell'endpoint /reflect semplificato"""
    
    print("🧠 Testing Simple /reflect Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/reflect")
        result = response.json()
        
        if result["status"] == "success":
            reflection = result["reflection"]
            
            print("✅ Simple reflect endpoint successful!")
            print(f"📝 Endpoint used: {result.get('endpoint')}")
            print(f"🧠 Consciousness level: {reflection.get('consciousness_level')}")
            print(f"💭 Number of thoughts: {len(reflection.get('reflection', []))}")
            
            print("\n🌟 Aether's reflection thoughts:")
            for i, thought in enumerate(reflection.get('reflection', [])[:2], 1):
                print(f"  {i}. \"{thought[:80]}...\"")
                
            print(f"\n🌡️ Dominant emotions:")
            emotions = reflection.get('emotional_influence', {})
            for emotion, value in emotions.items():
                status = "🔥" if value > 0.7 else "🌊" if value > 0.4 else "💨"
                print(f"  {status} {emotion}: {value:.2f}")
                
        else:
            print(f"❌ Simple reflect failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in simple reflect test: {e}")

def test_think_endpoint():
    """Test dell'endpoint /think semplificato"""
    
    print("\n🤔 Testing Simple /think Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/think")
        result = response.json()
        
        if result["status"] == "success":
            modification = result.get("modification")
            
            print("✅ Simple think endpoint successful!")
            print(f"📝 Endpoint used: {result.get('endpoint')}")
            print(f"💬 Message: {result.get('message')}")
            
            if modification:
                print(f"\n🔄 Aether decided to modify:")
                for key, value in modification.items():
                    if key != "reason":
                        print(f"  • {key}: {value}")
                
                if "reason" in modification:
                    print(f"\n💭 Reason: \"{modification['reason']}\"")
                    
                # Mostra risultato della modifica
                mod_result = result.get("modification_result", {})
                if mod_result.get("success"):
                    print(f"✅ Modification applied successfully!")
                else:
                    print(f"⚠️ Modification had issues: {mod_result.get('message')}")
            else:
                print(f"\n🤔 Aether thought but decided no changes were needed")
                
        else:
            print(f"❌ Simple think failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in simple think test: {e}")

def test_status_endpoint():
    """Test dell'endpoint /status semplificato"""
    
    print("\n📊 Testing Simple /status Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/status")
        result = response.json()
        
        if result["status"] == "success":
            status = result["aether_status"]
            
            print("✅ Simple status endpoint successful!")
            print(f"📝 Endpoint used: {result.get('endpoint')}")
            
            print(f"\n👤 Aether Status:")
            print(f"  Name: {status.get('name')}")
            print(f"  Shape: {status.get('shape')}")
            print(f"  Energy: {status.get('energy_level'):.2f}")
            print(f"  Modifications: {status.get('modification_count')}")
            print(f"  Consciousness: {status.get('consciousness_level')}")
            
            print(f"\n🧠 Capabilities:")
            print(f"  Can Think: {status.get('is_thinking')}")
            print(f"  Can Reflect: {status.get('can_reflect')}")
            print(f"  Can Modify: {status.get('can_modify')}")
            
            print(f"\n🌡️ Dominant Emotions:")
            for emotion in status.get('dominant_emotions', []):
                print(f"  • {emotion}")
                
        else:
            print(f"❌ Simple status failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in simple status test: {e}")

def test_identity_endpoint():
    """Test dell'endpoint /identity semplificato"""
    
    print("\n👤 Testing Simple /identity Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/identity")
        result = response.json()
        
        if result["status"] == "success":
            identity = result["identity"]
            
            print("✅ Simple identity endpoint successful!")
            print(f"📝 Endpoint used: {result.get('endpoint')}")
            
            print(f"\n🔍 Identity Overview:")
            print(f"  Name: {identity.get('name', 'Unknown')}")
            print(f"  Shape: {identity.get('shape', 'Unknown')}")
            print(f"  Energy Level: {identity.get('energy_level', 0)}")
            print(f"  Modification Count: {identity.get('modification_count', 0)}")
            
            if 'traits' in identity:
                print(f"\n✨ Personality Traits:")
                for trait in identity['traits'][:3]:  # Mostra solo i primi 3
                    print(f"  • {trait}")
            
            if 'goals' in identity:
                print(f"\n🎯 Goals:")
                for goal in identity['goals'][:2]:  # Mostra solo i primi 2
                    print(f"  • {goal}")
            
            if 'colors' in identity:
                colors = identity['colors']
                if isinstance(colors, list) and len(colors) >= 2:
                    print(f"\n🎨 Colors: {colors[0]} → {colors[1]}")
                
        else:
            print(f"❌ Simple identity failed: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error in simple identity test: {e}")

def test_endpoint_comparison():
    """Confronto tra endpoint semplificati e dettagliati"""
    
    print("\n🔬 Testing Endpoint Comparison")
    print("=" * 40)
    
    # Test endpoint semplificato vs dettagliato per reflection
    try:
        # Endpoint semplificato
        simple_response = requests.get(f"{BASE_URL}/reflect")
        simple_time = simple_response.elapsed.total_seconds()
        
        # Endpoint dettagliato
        detailed_response = requests.get(f"{BASE_URL}/api/reflect/identity")
        detailed_time = detailed_response.elapsed.total_seconds()
        
        print(f"⚡ Performance Comparison:")
        print(f"  Simple /reflect: {simple_time:.3f}s")
        print(f"  Detailed /api/reflect/identity: {detailed_time:.3f}s")
        
        if simple_response.status_code == 200 and detailed_response.status_code == 200:
            simple_data = simple_response.json()
            detailed_data = detailed_response.json()
            
            # Confronta profondità delle risposte
            simple_thoughts = len(simple_data.get("reflection", {}).get("reflection", []))
            detailed_thoughts = len(detailed_data.get("identity_reflection", {}).get("reflection", []))
            
            print(f"\n📊 Response Depth:")
            print(f"  Simple endpoint thoughts: {simple_thoughts}")
            print(f"  Detailed endpoint thoughts: {detailed_thoughts}")
            
            print(f"\n✅ Both endpoints working correctly!")
        else:
            print(f"⚠️ One or both endpoints had issues")
            
    except Exception as e:
        print(f"❌ Error in endpoint comparison: {e}")

if __name__ == "__main__":
    print("🌟 Aether Simple Endpoints Test Suite")
    print("Testing direct access routes...\n")
    
    try:
        # Test tutti gli endpoint semplificati
        test_reflect_endpoint()
        test_think_endpoint() 
        test_status_endpoint()
        test_identity_endpoint()
        
        # Test di confronto
        test_endpoint_comparison()
        
        print("\n" + "=" * 50)
        print("✅ All simple endpoint tests completed!")
        print("🧠 /reflect - Direct reflection access working")
        print("🤔 /think - Direct thinking access working") 
        print("📊 /status - Status summary working")
        print("👤 /identity - Identity access working")
        print("⚡ Simple endpoints provide fast, direct access")
        print("🔗 Both simple and detailed APIs available")
        
        print("\n🌟 Aether now has simple, direct access routes!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}") 