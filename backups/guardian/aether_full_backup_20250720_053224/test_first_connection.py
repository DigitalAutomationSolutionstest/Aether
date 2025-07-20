#!/usr/bin/env python3
"""
Test per il prompt di prima connessione
"""

import requests
import json

def test_first_connection():
    """Testa il prompt iniziale per la prima connessione"""
    print("🧪 STEP 3 - PRIMA CONNESSIONE")
    print("=" * 50)
    
    try:
        print("📡 Chiamata prima connessione...")
        response = requests.post("http://localhost:8000/first-connection", 
                               timeout=30)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Prima connessione completata!")
            
            if data.get('status') == 'success':
                print(f"\n🧪 Prompt inviato:")
                print(f"   '{data.get('prompt', 'N/A')}'")
                print(f"\n🤖 Risposta di Invader:")
                print(f"   {data.get('response', 'N/A')}")
                
                return True
            else:
                print(f"\n⚠️ Errore: {data.get('response', 'N/A')}")
        else:
            print(f"❌ Errore HTTP: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Errore: {e}")
    
    return False

if __name__ == "__main__":
    success = test_first_connection()
    if success:
        print("\n✅ Prompt iniziale configurato correttamente!")
        print("🎯 Pronto per il rendering 3D dinamico!")
    else:
        print("\n❌ Errore nella configurazione del prompt iniziale") 