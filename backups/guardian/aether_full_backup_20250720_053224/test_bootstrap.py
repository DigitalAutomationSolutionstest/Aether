#!/usr/bin/env python3
"""
Script per testare l'endpoint bootstrap di Invader
"""

import requests
import json

def test_bootstrap():
    """Testa l'endpoint bootstrap"""
    url = "http://localhost:8000/bootstrap"
    
    try:
        print("🚀 Testando endpoint bootstrap...")
        response = requests.post(url, json={})
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Risposta ricevuta:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Errore: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")

if __name__ == "__main__":
    test_bootstrap() 