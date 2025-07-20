#!/usr/bin/env python3
"""
🎙️ TEST SISTEMA AUDIO AETHER
=============================
Script di test per verificare il sistema audio con ElevenLabs
"""

import os
import sys

# Imposta le variabili d'ambiente
os.environ['ELEVENLABS_API_KEY'] = 'sk_fe4bdc0f7bc33f6dc8b388df9de81c744de9cf0693409faf'
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'
os.environ['AETHER_VOICE_ID'] = 'EXAVITQu4vr4xnSDxMaL'
os.environ['AETHER_AUDIO_ENABLED'] = 'true'

def test_elevenlabs_import():
    """Testa l'import di ElevenLabs"""
    print("🧪 Test import ElevenLabs...")
    
    try:
        import elevenlabs
        print(f"✅ ElevenLabs importato - versione: {elevenlabs.__version__}")
        
        # Test import funzioni specifiche
        from elevenlabs import text_to_speech, save, set_api_key
        print("✅ Funzioni ElevenLabs importate correttamente")
        
        return True
    except ImportError as e:
        print(f"❌ Errore import ElevenLabs: {e}")
        return False

def test_audio_generation():
    """Testa la generazione audio"""
    print("\n🎙️ Test generazione audio...")
    
    try:
        from elevenlabs import text_to_speech, save, set_api_key
        
        # Imposta API key
        set_api_key(os.environ['ELEVENLABS_API_KEY'])
        print("✅ API key impostata")
        
        # Genera audio di test
        text = "Ciao, sono Aether. Questo è un test del sistema audio."
        voice_id = os.environ['AETHER_VOICE_ID']
        
        print(f"🎵 Generando audio per: '{text[:50]}...'")
        audio = text_to_speech(text=text, voice=voice_id)
        print("✅ Audio generato con successo")
        
        # Salva file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            save(audio, f.name)
            print(f"✅ Audio salvato: {f.name}")
            return f.name
            
    except Exception as e:
        print(f"❌ Errore generazione audio: {e}")
        return None

def test_discord_upload():
    """Testa l'invio su Discord"""
    print("\n📡 Test invio Discord...")
    
    try:
        import requests
        
        # Crea un file di test
        test_message = "🧪 **Test Sistema Audio Aether**\nSistema audio funzionante!"
        
        webhook_url = os.environ['DISCORD_WEBHOOK_URL']
        
        # Invia messaggio di test
        response = requests.post(webhook_url, json={'content': test_message})
        
        if response.status_code == 200:
            print("✅ Messaggio di test inviato su Discord")
            return True
        else:
            print(f"❌ Errore invio Discord: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Errore test Discord: {e}")
        return False

def test_audio_reporter():
    """Testa il modulo audio_reporter"""
    print("\n🎯 Test AetherAudioReporter...")
    
    try:
        # Import del nostro modulo
        sys.path.append('.')
        from aether.notifier.audio_reporter import get_audio_reporter
        
        reporter = get_audio_reporter()
        print(f"✅ AetherAudioReporter creato")
        print(f"   - ElevenLabs configurato: {reporter.elevenlabs_key is not None}")
        print(f"   - Discord configurato: {reporter.webhook_url is not None}")
        print(f"   - Voice ID: {reporter.voice_id}")
        
        # Test generazione e invio
        success = reporter.report_thought_as_audio(
            "Questo è un test del sistema audio di Aether. Il sistema funziona correttamente!",
            "test"
        )
        
        if success:
            print("✅ Test audio completo riuscito!")
        else:
            print("⚠️ Test audio parzialmente riuscito")
            
        return success
        
    except Exception as e:
        print(f"❌ Errore test audio reporter: {e}")
        return False

def test_integrated_system():
    """Testa il sistema integrato di logging"""
    print("\n🔗 Test sistema integrato...")
    
    try:
        from aether.logging_system import get_aether_logger
        
        logger = get_aether_logger()
        print("✅ AetherLogger creato")
        
        # Test logging con audio
        logger.log_thought(
            "philosophical", 
            "Riflessione profonda: L'audio permette una connessione più umana con gli utenti.",
            {"test": True}
        )
        print("✅ Pensiero loggato con audio")
        
        logger.log_decision(
            "Implementare sistema audio",
            "Per migliorare l'interazione e l'engagement degli utenti"
        )
        print("✅ Decisione loggata con audio")
        
        # Mostra statistiche
        stats = logger.get_stats()
        print(f"📊 Statistiche:")
        print(f"   - Audio messages: {stats['audio_messages']}")
        print(f"   - Discord messages: {stats['discord_messages']}")
        print(f"   - Total entries: {stats['total_entries']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore test sistema integrato: {e}")
        return False

def main():
    """Funzione principale di test"""
    print("🎙️ TEST COMPLETO SISTEMA AUDIO AETHER")
    print("=" * 50)
    
    results = {
        "elevenlabs_import": test_elevenlabs_import(),
        "audio_generation": test_audio_generation() is not None,
        "discord_upload": test_discord_upload(),
        "audio_reporter": test_audio_reporter(),
        "integrated_system": test_integrated_system()
    }
    
    print("\n📊 RISULTATI FINALI:")
    print("=" * 30)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n🎯 TOTALE: {passed}/{total} test passati")
    
    if passed == total:
        print("🎉 Tutti i test sono passati! Sistema audio completamente funzionante!")
    elif passed >= total * 0.7:
        print("⚠️ La maggior parte dei test è passata. Sistema parzialmente funzionante.")
    else:
        print("❌ Molti test falliti. Controllare configurazione.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 