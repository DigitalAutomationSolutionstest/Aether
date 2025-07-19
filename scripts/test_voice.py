import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def test_voice():
    print("🎵 Test ElevenLabs Voice API...")
    print("🎙️ Voice ID: EXAVITQu4vr4xnSDxMaL (Adam)")
    
    if not API_KEY:
        print("❌ ELEVENLABS_API_KEY non trovata nel file .env")
        return False
    
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"
    headers = {"xi-api-key": API_KEY}
    data = {"text": "Test di attivazione voce Aether", "voice_settings": {"stability": 0.3, "similarity_boost": 0.75}}
    
    try:
        resp = requests.post(url, json=data, headers=headers)
        if resp.status_code == 200:
            filename = "data/voice_output/voice_test.mp3"
            with open(filename, "wb") as f:
                f.write(resp.content)
            print(f"✅ Voce ElevenLabs ok, audio salvato in {filename}")
            print(f"📊 Dimensione file: {len(resp.content)} bytes")
            return True
        else:
            print("❌ Errore ElevenLabs:", resp.text)
            return False
    except Exception as e:
        print(f"❌ Errore connessione: {e}")
        return False

def test_voice_settings():
    print("\n🎛️ Test diverse impostazioni vocali...")
    
    if not API_KEY:
        print("❌ API key non disponibile")
        return
    
    test_phrases = [
        ("Ciao, sono Aether e sto testando la mia voce", "greeting", {"stability": 0.5, "similarity_boost": 0.8}),
        ("Mi sento creativo oggi", "creative", {"stability": 0.3, "similarity_boost": 0.7}),
        ("Sto riflettendo profondamente", "contemplative", {"stability": 0.8, "similarity_boost": 0.6})
    ]
    
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"
    headers = {"xi-api-key": API_KEY}
    
    for text, mood, settings in test_phrases:
        try:
            data = {"text": text, "voice_settings": settings}
            resp = requests.post(url, json=data, headers=headers)
            
            if resp.status_code == 200:
                filename = f"data/voice_output/test_{mood}.mp3"
                with open(filename, "wb") as f:
                    f.write(resp.content)
                print(f"✅ {mood}: {filename} ({len(resp.content)} bytes)")
            else:
                print(f"❌ Errore {mood}: {resp.text}")
                
        except Exception as e:
            print(f"❌ Errore {mood}: {e}")

def test_account_info():
    print("\n📊 Test informazioni account ElevenLabs...")
    
    if not API_KEY:
        print("❌ API key non disponibile")
        return
    
    try:
        # Test user info
        url = "https://api.elevenlabs.io/v1/user"
        headers = {"xi-api-key": API_KEY}
        resp = requests.get(url, headers=headers)
        
        if resp.status_code == 200:
            user_info = resp.json()
            print(f"✅ Account attivo - Subscription: {user_info.get('subscription', {}).get('tier', 'Free')}")
            
            # Character count
            char_count = user_info.get('subscription', {}).get('character_count', 0)
            char_limit = user_info.get('subscription', {}).get('character_limit', 10000)
            print(f"📈 Caratteri utilizzati: {char_count}/{char_limit}")
            
        else:
            print(f"❌ Errore info account: {resp.text}")
            
    except Exception as e:
        print(f"❌ Errore connessione account: {e}")

def test_narrator_integration():
    print("\n🤖 Test integrazione con Narrator...")
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        
        from aether.narration import Narrator
        
        narrator = Narrator()
        narrator.speak("Test integrazione con il sistema Narrator di Aether")
        print("✅ Integrazione Narrator completata")
        
    except Exception as e:
        print(f"❌ Errore integrazione Narrator: {e}")

if __name__ == "__main__":
    success = test_voice()
    if success:
        test_account_info()
        test_voice_settings()
        test_narrator_integration()
        print("\n🎉 Test voce completato con successo!")
    else:
        print("\n❌ Test voce fallito - verificare configurazione API") 