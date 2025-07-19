#!/usr/bin/env python3
"""
Script per testare il logging dell'identità di Invader
"""

import requests
import json
import os

def test_identity_logging():
    """Testa il bootstrap e il logging dell'identità"""
    
    print("🧠 Testing Identity Logging...")
    print("=" * 50)
    
    # Test 1: Bootstrap per creare l'identità
    print("\n1. 🚀 Chiamata Bootstrap...")
    try:
        response = requests.post("http://localhost:8000/bootstrap", json={})
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Bootstrap completato!")
            
            if "identity" in data:
                identity = data["identity"]
                print(f"   Nome: {identity.get('name', 'N/A')}")
                print(f"   Forma: {identity.get('appearance', 'N/A')}")
                print(f"   Personalità: {identity.get('personality', 'N/A')}")
                print(f"   Goal: {identity.get('goal', 'N/A')}")
            
        else:
            print(f"❌ Errore Bootstrap: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Errore connessione Bootstrap: {e}")
    
    # Test 2: Verifica file identity.json
    print("\n2. 📁 Verifica file identity.json...")
    if os.path.exists("identity.json"):
        try:
            with open("identity.json", "r", encoding="utf-8") as f:
                identity = json.load(f)
            print("✅ File identity.json creato!")
            print(json.dumps(identity, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ Errore lettura file: {e}")
    else:
        print("❌ File identity.json non trovato")
    
    # Test 3: Endpoint GET /identity
    print("\n3. 🔍 Test endpoint GET /identity...")
    try:
        response = requests.get("http://localhost:8000/identity")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint /identity funziona!")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   Source: {data.get('source', 'N/A')}")
            
            if "identity" in data:
                identity = data["identity"]
                print("   Identità:")
                for key, value in identity.items():
                    print(f"     {key}: {value}")
            
        else:
            print(f"❌ Errore endpoint: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Errore connessione endpoint: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completati!")

if __name__ == "__main__":
    test_identity_logging() 