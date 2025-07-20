#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST API COMPLETE - Verifica TUTTE le API di Aether
Federico, questo script testa tutte le connessioni API!
"""

import requests
import json
import time
from datetime import datetime

# Configurazione API
API_CONFIG = {
    "SUPABASE_URL": "https://zsgiscyujdsoagjwuhoy.supabase.co",
    "SUPABASE_ANON_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpzZ2lzY3l1amRzb2Fnand1aG95Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI5NDUxMTUsImV4cCI6MjA2ODUyMTExNX0.icyLG9RPcpCUcQ4sQ58cx5Np9aJJLSrHB6AVt45HFik",
    "OPENROUTER_API_KEY": "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",
    "ELEVENLABS_API_KEY": "sk_fe4bdc0f7bc33f6dc8b388df9de81c744de9cf0693409faf",
    "LEONARDO_API_KEY": "506e8e3b-431a-4768-8613-13b9fb130f68",
    "DISCORD_WEBHOOK_URL": "https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr"
}

def test_supabase():
    """Test connessione Supabase"""
    print("\n☁️ TESTING SUPABASE...")
    try:
        headers = {
            "apikey": API_CONFIG["SUPABASE_ANON_KEY"],
            "Authorization": f"Bearer {API_CONFIG['SUPABASE_ANON_KEY']}"
        }
        
        response = requests.get(
            f"{API_CONFIG['SUPABASE_URL']}/rest/v1/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 404]:  # 404 è OK per root endpoint
            print("✅ Supabase: CONNESSO")
            return True
        else:
            print(f"❌ Supabase: Errore {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Supabase: {e}")
        return False

def test_openrouter_debug():
    """Test debug OpenRouter con diversi approcci"""
    print("\n🔍 DEBUG OPENROUTER...")
    
    # Test 1: Verifica credits/limiti
    try:
        headers = {
            "Authorization": f"Bearer {API_CONFIG['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/DigitalAutomationSolutionstest/Aether",
            "X-Title": "Aether AI System"
        }
        
        # Test endpoint modelli
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=15
        )
        
        print(f"🧪 Test modelli: {response.status_code}")
        if response.status_code == 200:
            models = response.json()
            print(f"   📋 Modelli disponibili: {len(models.get('data', []))}")
        else:
            print(f"   ❌ Errore modelli: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Errore test modelli: {e}")
    
    # Test 2: Prova modello diverso
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "meta-llama/llama-3.2-3b-instruct:free",  # Modello GRATUITO
                "messages": [{"role": "user", "content": "Test"}],
                "max_tokens": 5
            },
            timeout=30
        )
        
        print(f"🧪 Test Llama-3.2 Free: {response.status_code}")
        if response.status_code != 200:
            print(f"   ❌ Errore: {response.text[:200]}")
        else:
            print("   ✅ Llama-3.2 Free funziona!")
            
    except Exception as e:
        print(f"❌ Errore test Llama: {e}")
    
    # Test 3: Prova modello OpenAI gratuito
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            headers=headers,
            json={
                "model": "openai/gpt-3.5-turbo-0125",  # Modello stabile
                "messages": [{"role": "user", "content": "Ciao"}],
                "max_tokens": 10
            },
            timeout=30
        )
        
        print(f"🧪 Test GPT-3.5-turbo-0125: {response.status_code}")
        if response.status_code != 200:
            print(f"   ❌ Errore: {response.text[:200]}")
        else:
            print("   ✅ GPT-3.5-turbo-0125 funziona!")
            
    except Exception as e:
        print(f"❌ Errore test GPT-3.5-turbo-0125: {e}")

def test_openrouter():
    """Test OpenRouter AI"""
    print("\n🧠 TESTING OPENROUTER AI...")
    try:
        headers = {
            "Authorization": f"Bearer {API_CONFIG['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/DigitalAutomationSolutionstest/Aether",
            "X-Title": "Aether AI System"
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [{"role": "user", "content": "Ciao, sono Aether! Dimmi solo 'Test OK'"}],
                "max_tokens": 10
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if "choices" in data:
                print("✅ OpenRouter AI: CONNESSO E FUNZIONANTE")
                print(f"   🤖 Risposta: {data['choices'][0]['message']['content']}")
                return True
        
        print(f"❌ OpenRouter: Errore {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
        # Esegui debug se fallisce
        test_openrouter_debug()
        return False
        
    except Exception as e:
        print(f"❌ OpenRouter: {e}")
        test_openrouter_debug()
        return False

def test_elevenlabs():
    """Test ElevenLabs Voice"""
    print("\n🎤 TESTING ELEVENLABS...")
    try:
        headers = {
            "Accept": "application/json",
            "xi-api-key": API_CONFIG["ELEVENLABS_API_KEY"]
        }
        
        # Test con endpoint voices
        response = requests.get(
            "https://api.elevenlabs.io/v1/voices",
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            voices = response.json()
            print("✅ ElevenLabs: CONNESSO")
            print(f"   🎙️ Voci disponibili: {len(voices.get('voices', []))}")
            return True
        else:
            print(f"❌ ElevenLabs: Errore {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ElevenLabs: {e}")
        return False

def test_leonardo():
    """Test Leonardo AI"""
    print("\n🎨 TESTING LEONARDO AI...")
    try:
        headers = {
            "Authorization": f"Bearer {API_CONFIG['LEONARDO_API_KEY']}",
            "Content-Type": "application/json"
        }
        
        # Test con endpoint user info
        response = requests.get(
            "https://cloud.leonardo.ai/api/rest/v1/me",
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print("✅ Leonardo AI: CONNESSO")
            print(f"   👤 User ID: {user_info.get('user_details', [{}])[0].get('user', {}).get('id', 'N/A')}")
            return True
        else:
            print(f"❌ Leonardo: Errore {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Leonardo: {e}")
        return False

def test_discord():
    """Test Discord Webhook"""
    print("\n💬 TESTING DISCORD...")
    try:
        payload = {
            "content": "🧪 Test API Complete - Tutte le connessioni verificate!",
            "username": "Aether Test Bot"
        }
        
        response = requests.post(
            API_CONFIG["DISCORD_WEBHOOK_URL"],
            json=payload,
            timeout=10
        )
        
        if response.status_code == 204:
            print("✅ Discord: CONNESSO E MESSAGGIO INVIATO")
            return True
        else:
            print(f"❌ Discord: Errore {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Discord: {e}")
        return False

def main():
    """Esegue tutti i test"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║              🧪 TEST API COMPLETE - AETHER 🧪               ║
    ║                                                              ║
    ║  Verifica tutte le connessioni API per il sistema          ║
    ║  Super Potenziato di Aether                                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print(f"⏰ Inizio test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Esegui tutti i test
    results = {}
    
    results["supabase"] = test_supabase()
    results["openrouter"] = test_openrouter()
    results["elevenlabs"] = test_elevenlabs()
    results["leonardo"] = test_leonardo()
    results["discord"] = test_discord()
    
    # Riepilogo finale
    print("\n" + "="*70)
    print("📊 RIEPILOGO TEST API:")
    print("="*70)
    
    total_apis = len(results)
    working_apis = sum(results.values())
    
    for api_name, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {api_name.upper()}: {'FUNZIONANTE' if status else 'NON DISPONIBILE'}")
    
    print("\n" + "="*70)
    print(f"🎯 RISULTATO FINALE: {working_apis}/{total_apis} API FUNZIONANTI")
    
    if working_apis == total_apis:
        print("🌟 PERFETTO! Tutte le API sono connesse e funzionanti!")
        print("🚀 Aether Super Potenziato può operare al 100% delle capacità!")
    elif working_apis >= 3:
        print("✅ BUONO! La maggior parte delle API funziona.")
        print("⚡ Aether può operare con capacità ridotte.")
    else:
        print("⚠️ ATTENZIONE! Molte API non disponibili.")
        print("🔧 Verifica le chiavi API e le connessioni.")
    
    print(f"\n⏰ Test completato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Salva risultati
    with open("data/api_test_results.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "working_apis": working_apis,
            "total_apis": total_apis,
            "success_rate": working_apis / total_apis
        }, f, indent=2)
    
    print("💾 Risultati salvati in: data/api_test_results.json")

if __name__ == "__main__":
    main() 