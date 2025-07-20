#!/usr/bin/env python3
"""
Test finale per verificare il sistema bootstrap completo
"""

import requests
import json
import time

def test_final_system():
    """Test completo del sistema"""
    print("🧩 PASSO 3 - LOGGING INTERNO")
    print("=" * 50)
    
    # Aspetta che il server sia pronto
    print("Aspetto che il server sia pronto...")
    time.sleep(2)
    
    try:
        # Test bootstrap
        print("\n🚀 Chiamata Bootstrap per generare identità...")
        response = requests.post("http://localhost:8000/bootstrap", 
                               json={}, timeout=30)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Bootstrap completato!")
            print(f"Status: {data.get('status', 'N/A')}")
            
            if data.get('status') == 'success' and 'identity' in data:
                identity = data['identity']
                print("\n🆔 IDENTITÀ GENERATA:")
                print(f"   Nome: {identity.get('name', 'N/A')}")
                print(f"   Aspetto: {identity.get('appearance', 'N/A')}")
                print(f"   Genere: {identity.get('gender', 'N/A')}")
                print(f"   Personalità: {identity.get('personality', 'N/A')}")
                print(f"   Goal: {identity.get('goal', 'N/A')}")
                
                # Verifica file salvato
                try:
                    with open("identity.json", "r", encoding="utf-8") as f:
                        saved_identity = json.load(f)
                    print("\n📁 File identity.json salvato correttamente:")
                    print(json.dumps(saved_identity, indent=2, ensure_ascii=False))
                except FileNotFoundError:
                    print("\n⚠️ File identity.json non trovato")
                    
            else:
                print(f"\n⚠️ Risposta: {data.get('response', 'N/A')}")
        else:
            print(f"❌ Errore: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore di connessione: {e}")
    except Exception as e:
        print(f"❌ Errore generico: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completato!")

if __name__ == "__main__":
    test_final_system() 