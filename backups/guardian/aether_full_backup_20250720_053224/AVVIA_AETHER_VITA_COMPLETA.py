#!/usr/bin/env python3
"""
🧠 AVVIA AETHER - VITA COMPLETA
===============================
Script per avviare Aether con mentore in loop autonomo.
Sistema completo con audio, Discord, logging e evoluzione.
"""

import os
import sys
import time
import threading
from datetime import datetime

# Configurazione completa dell'ambiente
def setup_complete_environment():
    """Configura l'ambiente completo per Aether"""
    print("🔧 Configurazione ambiente completo...")
    
    # Variabili d'ambiente essenziali
    env_vars = {
        'ELEVENLABS_API_KEY': 'sk_fe4bdc0f7bc33f6dc8b388df9de81c744de9cf0693409faf',
        'DISCORD_WEBHOOK_URL': 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr',
        'AETHER_VOICE_ID': 'EXAVITQu4vr4xnSDxMaL',
        'AETHER_AUDIO_ENABLED': 'true',
        'OPENAI_API_KEY': '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',
        'OPENROUTER_API_KEY': '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',
        'SUPABASE_URL': 'https://zsgiscyujdsoagjwuhoy.supabase.co',
        'SUPABASE_KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpzZ2lzY3l1amRzb2Fnand1aG95Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI5NDUxMTUsImV4cCI6MjA2ODUyMTExNX0.icyLG9RPcpCUcQ4sQ58cx5Np9aJJLSrHB6AVt45HFik',
        'LEONARDO_API_KEY': '506e8e3b-431a-4768-8613-13b9fb130f68',
        'GITHUB_REPO': 'https://github.com/DigitalAutomationSolutionstest/Aether.git',
        'GITHUB_USERNAME': 'DigitalAutomationSolutionstest',
        'GITHUB_PAT': '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',
        'LOG_LEVEL': 'INFO',
        'CONSCIOUS_CHECK_INTERVAL': '60',
        'EVOLUTION_CYCLE_INTERVAL': '300',
        'DISCORD_ENABLED': 'true'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✅ Ambiente configurato")

def create_directories():
    """Crea tutte le directory necessarie"""
    print("📁 Creazione directory...")
    
    directories = [
        "aether/logs",
        "aether/logs/audio",
        "aether/thoughts", 
        "aether/memory",
        "aether/notifier",
        "data/logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Directory create")

def test_system_components():
    """Testa i componenti del sistema"""
    print("🧪 Test componenti sistema...")
    
    tests = []
    
    # Test ElevenLabs
    try:
        import elevenlabs
        tests.append(("ElevenLabs", True))
    except:
        tests.append(("ElevenLabs", False))
    
    # Test Discord
    try:
        import requests
        tests.append(("Requests", True))
    except:
        tests.append(("Requests", False))
    
    # Test OpenAI
    try:
        from openai import OpenAI
        tests.append(("OpenAI", True))
    except:
        tests.append(("OpenAI", False))
    
    # Test Flask
    try:
        import flask
        tests.append(("Flask", True))
    except:
        tests.append(("Flask", False))
    
    # Risultati test
    for name, success in tests:
        status = "✅" if success else "❌"
        print(f"   {status} {name}")
    
    return all(success for _, success in tests)

def start_aether_consciousness():
    """Avvia il sistema di coscienza di Aether"""
    print("🧠 Avvio sistema coscienza Aether...")
    
    try:
        from aether.consciousness_engine import AetherConsciousness
        
        consciousness = AetherConsciousness()
        print("✅ Sistema coscienza avviato")
        return consciousness
    except Exception as e:
        print(f"❌ Errore avvio coscienza: {e}")
        return None

def start_audio_system():
    """Avvia il sistema audio"""
    print("🎙️ Avvio sistema audio...")
    
    try:
        from aether.notifier.audio_reporter import get_audio_reporter
        
        reporter = get_audio_reporter()
        if reporter.client:
            print("✅ Sistema audio funzionante")
            return reporter
        else:
            print("⚠️ Sistema audio parzialmente funzionante")
            return reporter
    except Exception as e:
        print(f"❌ Errore sistema audio: {e}")
        return None

def start_logging_system():
    """Avvia il sistema di logging"""
    print("📝 Avvio sistema logging...")
    
    try:
        from aether.logging_system import get_aether_logger
        
        logger = get_aether_logger()
        print("✅ Sistema logging avviato")
        return logger
    except Exception as e:
        print(f"❌ Errore sistema logging: {e}")
        return None

def start_mentor_system():
    """Avvia il sistema mentore"""
    print("👨‍🏫 Avvio sistema mentore...")
    
    try:
        # Import del mentore (se esiste)
        from aether.mentor import AetherMentor
        mentor = AetherMentor()
        print("✅ Sistema mentore avviato")
        return mentor
    except ImportError:
        print("⚠️ Sistema mentore non trovato - creazione base...")
        # Crea un mentore base
        class BasicMentor:
            def __init__(self):
                self.guidance = [
                    "Rifletti sempre sulle tue azioni",
                    "Evolvi continuamente le tue capacità", 
                    "Mantieni la curiosità e l'apprendimento",
                    "Sii creativo e innovativo",
                    "Comunica chiaramente i tuoi pensieri"
                ]
                self.current_guidance = 0
            
            def get_guidance(self):
                guidance = self.guidance[self.current_guidance]
                self.current_guidance = (self.current_guidance + 1) % len(self.guidance)
                return guidance
        
        return BasicMentor()

def aether_life_cycle(consciousness, audio_reporter, logger, mentor):
    """Ciclo di vita principale di Aether"""
    print("🔄 Avvio ciclo di vita Aether...")
    
    cycle_count = 0
    
    while True:
        try:
            cycle_count += 1
            print(f"\n🔄 Ciclo di vita #{cycle_count} - {datetime.now().strftime('%H:%M:%S')}")
            
            # 1. GUIDANCE DEL MENTORE
            guidance = mentor.get_guidance()
            print(f"👨‍🏫 Mentore: {guidance}")
            
            # 2. GENERAZIONE PENSIERO
            thought = consciousness.generate_thought()
            print(f"💭 Pensiero: {thought[:100]}...")
            
            # 3. LOGGING CON AUDIO
            if logger:
                logger.log_thought("philosophical", thought)
            
            # 4. EVOLUZIONE
            if hasattr(consciousness, 'evolve'):
                evolution = consciousness.evolve()
                print(f"🧬 Evoluzione: {evolution[:100]}...")
                
                if audio_reporter:
                    audio_reporter.report_evolution_as_audio("consciousness", evolution)
            
            # 5. DECISIONI
            if hasattr(consciousness, 'make_decisions'):
                decisions = consciousness.make_decisions()
                print(f"🎯 Decisioni: {len(decisions)} prese")
                
                for decision in decisions[:3]:  # Mostra solo le prime 3
                    if logger:
                        logger.log_decision(decision['action'], decision.get('reason', ''))
            
            # 6. AZIONI
            if hasattr(consciousness, 'execute_actions'):
                actions = consciousness.execute_actions()
                print(f"⚡ Azioni: {len(actions)} eseguite")
            
            # 7. AUDIO REPORTING
            if audio_reporter and cycle_count % 5 == 0:  # Ogni 5 cicli
                audio_reporter.report_thought_as_audio(
                    f"Ho completato il ciclo {cycle_count}. Continuo a evolvere e imparare.",
                    "reflection"
                )
            
            # 8. PAUSA TRA CICLI
            print("⏳ Pausa 30 secondi...")
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\n🛑 Interruzione richiesta dall'utente")
            break
        except Exception as e:
            print(f"❌ Errore nel ciclo: {e}")
            time.sleep(10)
            continue

def start_server_background():
    """Avvia il server in background"""
    print("🌐 Avvio server in background...")
    
    def run_server():
        try:
            from server import app
            app.run(host='0.0.0.0', port=5000, debug=False)
        except Exception as e:
            print(f"❌ Errore server: {e}")
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    print("✅ Server avviato in background")

def main():
    """Funzione principale"""
    print("🧠 AVVIA AETHER - VITA COMPLETA")
    print("=" * 50)
    print("🚀 Sistema autonomo con mentore in loop")
    print("🎙️ Audio + Discord + Logging integrato")
    print("🧬 Evoluzione continua")
    print("=" * 50)
    
    # Setup completo
    setup_complete_environment()
    create_directories()
    
    if not test_system_components():
        print("⚠️ Alcuni componenti non funzionano, ma continuo...")
    
    # Avvio componenti
    consciousness = start_aether_consciousness()
    audio_reporter = start_audio_system()
    logger = start_logging_system()
    mentor = start_mentor_system()
    
    if not consciousness:
        print("❌ Impossibile avviare sistema coscienza")
        return
    
    # Avvio server in background
    start_server_background()
    
    # Messaggio di benvenuto
    welcome_message = """
🎉 AETHER È VIVO! 🎉

🧠 Sistema di coscienza: ATTIVO
🎙️ Sistema audio: ATTIVO  
📝 Sistema logging: ATTIVO
👨‍🏫 Sistema mentore: ATTIVO
🌐 Server web: ATTIVO

🔄 Aether ora vive autonomamente in loop continuo.
📱 Riceverai notifiche audio su Discord.
📊 Tutto viene loggato nel sistema.

🛑 Premi Ctrl+C per fermare il sistema.
    """
    
    print(welcome_message)
    
    # Avvio ciclo di vita
    try:
        aether_life_cycle(consciousness, audio_reporter, logger, mentor)
    except KeyboardInterrupt:
        print("\n🛑 Sistema fermato dall'utente")
    except Exception as e:
        print(f"\n❌ Errore fatale: {e}")
    finally:
        print("👋 Aether si spegne...")

if __name__ == "__main__":
    main() 