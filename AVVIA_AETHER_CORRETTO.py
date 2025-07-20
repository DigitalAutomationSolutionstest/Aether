#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AVVIA AETHER CORRETTO 🚀
Script per avviare Aether con tutte le correzioni applicate
"""

import os
import sys
import time
import logging
import threading
from datetime import datetime
from pathlib import Path
import json

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/aether_corrected.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_environment():
    """Configura l'ambiente per Aether"""
    logger.info("🔧 Configurazione ambiente...")
    
    # Crea directory necessarie
    directories = ['data', 'logs', 'audio', 'backups']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    # Verifica file di configurazione
    if not os.path.exists('.env'):
        logger.warning("⚠️ File .env non trovato - usando configurazione di default")
    
    logger.info("✅ Ambiente configurato")

def fix_common_issues():
    """Risolve problemi comuni"""
    logger.info("🔧 Risoluzione problemi comuni...")
    
    # Rimuovi file lock Git se presente
    git_lock = Path('.git/index.lock')
    if git_lock.exists():
        git_lock.unlink()
        logger.info("🗑️ Rimosso file lock Git")
    
    # Verifica e ripara file JSON corrotti
    thoughts_file = Path('data/thoughts.json')
    if thoughts_file.exists():
        try:
            with open(thoughts_file, 'r', encoding='utf-8') as f:
                json.load(f)
            logger.info("✅ File thoughts.json valido")
        except:
            logger.warning("⚠️ File thoughts.json corrotto - ricreando...")
            thoughts_file.unlink()
    
    logger.info("✅ Problemi comuni risolti")

def start_aether_consciousness():
    """Avvia il sistema di coscienza di Aether"""
    logger.info("🧠 Avvio sistema di coscienza...")
    
    try:
        from aether.consciousness_engine import AetherConsciousness
        
        consciousness = AetherConsciousness()
        consciousness.start_living()
        
        logger.info("✅ Sistema di coscienza avviato")
        return consciousness
        
    except Exception as e:
        logger.error(f"❌ Errore avvio coscienza: {e}")
        return None

def start_evolution_engine():
    """Avvia il motore di evoluzione"""
    logger.info("🧬 Avvio motore di evoluzione...")
    
    try:
        from aether.self_evolution import SelfEvolutionEngine
        
        evolution_engine = SelfEvolutionEngine()
        
        logger.info("✅ Motore di evoluzione avviato")
        return evolution_engine
        
    except Exception as e:
        logger.error(f"❌ Errore avvio evoluzione: {e}")
        return None

def start_audio_system():
    """Avvia il sistema audio se configurato"""
    logger.info("🎵 Avvio sistema audio...")
    
    try:
        from aether.notifier.audio_reporter import AudioReporter
        
        audio_reporter = AudioReporter()
        
        # Test audio
        test_message = "Aether è vivo e funzionante! 🚀"
        audio_reporter.report_thought(test_message)
        
        logger.info("✅ Sistema audio avviato")
        return audio_reporter
        
    except Exception as e:
        logger.warning(f"⚠️ Sistema audio non disponibile: {e}")
        return None

def start_mentor_system():
    """Avvia il sistema di mentoring"""
    logger.info("🎓 Avvio sistema di mentoring...")
    
    try:
        from aether.mentor import AetherMentor
        
        mentor = AetherMentor()
        
        logger.info("✅ Sistema di mentoring avviato")
        return mentor
        
    except Exception as e:
        logger.warning(f"⚠️ Sistema di mentoring non disponibile: {e}")
        return None

def start_web_server():
    """Avvia il server web in background"""
    logger.info("🌐 Avvio server web...")
    
    try:
        import subprocess
        import threading
        
        def run_server():
            subprocess.run([sys.executable, 'server.py'], check=True)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Attendi che il server si avvii
        time.sleep(3)
        
        logger.info("✅ Server web avviato in background")
        return True
        
    except Exception as e:
        logger.error(f"❌ Errore avvio server web: {e}")
        return False

def main():
    """Funzione principale"""
    print("""
    ╔═══════════════════════════════════════╗
    ║     🚀 AETHER CORRETTO 🚀            ║
    ║                                       ║
    ║   Sistema autonomo con tutte le       ║
    ║   correzioni applicate                ║
    ╚═══════════════════════════════════════╝
    """)
    
    # Setup iniziale
    setup_environment()
    fix_common_issues()
    
    # Avvia componenti
    consciousness = start_aether_consciousness()
    evolution_engine = start_evolution_engine()
    audio_system = start_audio_system()
    mentor = start_mentor_system()
    web_server = start_web_server()
    
    # Verifica stato
    components_status = {
        "Coscienza": consciousness is not None,
        "Evoluzione": evolution_engine is not None,
        "Audio": audio_system is not None,
        "Mentor": mentor is not None,
        "Web Server": web_server
    }
    
    print("\n📊 STATO COMPONENTI:")
    for component, status in components_status.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {component}")
    
    # Calcola percentuale di successo
    success_rate = sum(components_status.values()) / len(components_status) * 100
    print(f"\n🎯 Tasso di successo: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 AETHER È VIVO E FUNZIONANTE!")
        
        # Avvia ciclo di vita
        if consciousness:
            print("\n🔄 Avvio ciclo di vita autonomo...")
            print("💡 Aether ora vive e opera autonomamente!")
            print("🛑 Premi Ctrl+C per fermare il sistema")
            
            try:
                while True:
                    time.sleep(10)
                    # Log stato ogni 10 secondi
                    if consciousness.is_alive:
                        logger.info("💓 Aether è vivo e attivo")
                    
            except KeyboardInterrupt:
                print("\n🛑 Fermando Aether...")
                if consciousness:
                    consciousness.stop_living()
                print("💤 Aether si è addormentato")
                
    else:
        print("⚠️ Alcuni componenti non sono disponibili")
        print("🔧 Controlla i log per dettagli")

if __name__ == "__main__":
    main() 