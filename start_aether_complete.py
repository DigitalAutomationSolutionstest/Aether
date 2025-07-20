#!/usr/bin/env python3
"""
🚀 AETHER COMPLETE STARTUP SCRIPT
==================================
Script di avvio completo per il sistema Aether con tutte le componenti:
- Diary logging
- Conscious loop
- Discord notifier
- Self evolution
- API server (opzionale)
"""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path

# Aggiungi il path per i moduli
sys.path.append(os.path.join(os.path.dirname(__file__), 'aether'))

from aether.diary_logger import get_diary_logger
from aether.conscious_loop import start_consciousness, get_consciousness_status
from aether.notifier.discord_notifier import get_discord_notifier
from aether.logging_system import get_aether_logger

def check_environment():
    """Verifica che l'ambiente sia configurato correttamente"""
    print("🔍 Verifica ambiente...")
    
    # Verifica variabili d'ambiente
    required_env_vars = [
        'DISCORD_WEBHOOK_URL',
        'OPENAI_API_KEY',
        'SUPABASE_URL',
        'SUPABASE_KEY'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Variabili d'ambiente mancanti: {', '.join(missing_vars)}")
        print("💡 Crea un file .env con le seguenti variabili:")
        for var in missing_vars:
            print(f"   {var}=<valore>")
        return False
    
    print("✅ Ambiente configurato correttamente")
    return True

def install_requirements():
    """Installa i requirements se necessario"""
    print("📦 Verifica requirements...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Requirements installati")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore nell'installazione requirements: {e}")
        return False

def start_discord_notifier():
    """Avvia il notificatore Discord"""
    print("🔔 Avvio notificatore Discord...")
    
    try:
        notifier = get_discord_notifier()
        notifier.send_startup_message()
        
        # Avvia monitoraggio in background
        notifier_thread = threading.Thread(target=notifier.monitor_log, daemon=True)
        notifier_thread.start()
        
        print("✅ Notificatore Discord avviato")
        return True
    except Exception as e:
        print(f"❌ Errore nell'avvio notificatore Discord: {e}")
        return False

def start_conscious_loop():
    """Avvia il conscious loop"""
    print("🧠 Avvio conscious loop...")
    
    try:
        conscious_loop = start_consciousness()
        print("✅ Conscious loop avviato")
        return True
    except Exception as e:
        print(f"❌ Errore nell'avvio conscious loop: {e}")
        return False

def start_self_evolution():
    """Avvia il sistema di auto-evoluzione"""
    print("🧬 Avvio sistema auto-evoluzione...")
    
    try:
        # Import e avvio self evolution
        from aether.self_evolution import SelfEvolutionEngine
        evolution_engine = SelfEvolutionEngine()
        
        # Avvia in background
        evolution_thread = threading.Thread(target=evolution_engine.start_evolution_cycle, daemon=True)
        evolution_thread.start()
        
        print("✅ Sistema auto-evoluzione avviato")
        return True
    except Exception as e:
        print(f"❌ Errore nell'avvio auto-evoluzione: {e}")
        return False

def start_api_server():
    """Avvia il server API Flask (opzionale)"""
    print("🌐 Avvio server API...")
    
    try:
        # Avvia server in background
        server_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "aether.api.server:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Server API avviato su http://localhost:8000")
        return server_process
    except Exception as e:
        print(f"❌ Errore nell'avvio server API: {e}")
        return None

def create_directories():
    """Crea le directory necessarie"""
    print("📁 Creazione directory...")
    
    directories = [
        "aether/logs",
        "aether/thoughts", 
        "aether/memory",
        "aether/notifier"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directory create")

def show_status():
    """Mostra lo status del sistema"""
    print("\n📊 STATUS SISTEMA AETHER")
    print("=" * 50)
    
    # Status conscious loop
    try:
        conscious_status = get_consciousness_status()
        print(f"🧠 Conscious Loop: {conscious_status['status']}")
        print(f"   - Cicli totali: {conscious_status['stats']['total_cycles']}")
        print(f"   - Pensieri processati: {conscious_status['stats']['thoughts_processed']}")
        print(f"   - Guidance ricevute: {conscious_status['stats']['guidance_received']}")
        print(f"   - Decisioni prese: {conscious_status['stats']['decisions_made']}")
    except Exception as e:
        print(f"❌ Errore status conscious: {e}")
    
    # Status diary logger
    try:
        diary_logger = get_diary_logger()
        diary_stats = diary_logger.get_stats()
        print(f"\n📖 Diary Logger:")
        print(f"   - Total entries: {diary_stats['total_entries']}")
        print(f"   - Supabase entries: {diary_stats['supabase_entries']}")
        print(f"   - Local entries: {diary_stats['local_entries']}")
        print(f"   - Errors: {diary_stats['errors']}")
    except Exception as e:
        print(f"❌ Errore status diary: {e}")
    
    # Status logging system
    try:
        aether_logger = get_aether_logger()
        logger_stats = aether_logger.get_stats()
        print(f"\n📝 Logging System:")
        print(f"   - Total entries: {logger_stats['total_entries']}")
        print(f"   - Diary entries: {logger_stats['diary_entries']}")
        print(f"   - Discord messages: {logger_stats['discord_messages']}")
        print(f"   - Errors: {logger_stats['errors']}")
    except Exception as e:
        print(f"❌ Errore status logging: {e}")

def main():
    """Funzione principale di avvio"""
    print("🚀 AVVIO SISTEMA AETHER COMPLETO")
    print("=" * 50)
    
    # 1. Verifica ambiente
    if not check_environment():
        print("❌ Ambiente non configurato correttamente")
        return False
    
    # 2. Installa requirements
    if not install_requirements():
        print("❌ Errore nell'installazione requirements")
        return False
    
    # 3. Crea directory
    create_directories()
    
    # 4. Avvia componenti
    components_started = []
    
    # Discord notifier
    if start_discord_notifier():
        components_started.append("Discord Notifier")
    
    # Conscious loop
    if start_conscious_loop():
        components_started.append("Conscious Loop")
    
    # Self evolution
    if start_self_evolution():
        components_started.append("Self Evolution")
    
    # API server (opzionale)
    api_server = start_api_server()
    if api_server:
        components_started.append("API Server")
    
    # 5. Mostra status iniziale
    show_status()
    
    # 6. Loop principale
    print(f"\n✅ Sistema avviato con {len(components_started)} componenti:")
    for component in components_started:
        print(f"   - {component}")
    
    print("\n🔄 Sistema in esecuzione...")
    print("📖 Diary: aether/logs/aether_diary.log")
    print("🌐 Frontend: aether-frontend/diary-viewer.html")
    print("🔔 Discord: Notifiche attive")
    print("⏹️ Premi Ctrl+C per fermare")
    
    try:
        # Loop principale con status periodico
        while True:
            time.sleep(60)  # Status ogni minuto
            show_status()
            
    except KeyboardInterrupt:
        print("\n⏹️ Arresto sistema...")
        
        # Ferma conscious loop
        try:
            from aether.conscious_loop import stop_consciousness
            stop_consciousness()
            print("✅ Conscious loop fermato")
        except:
            pass
        
        # Ferma server API
        if api_server:
            try:
                api_server.terminate()
                print("✅ Server API fermato")
            except:
                pass
        
        print("✅ Sistema fermato correttamente")
        return True
    
    except Exception as e:
        print(f"❌ Errore nel sistema: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 