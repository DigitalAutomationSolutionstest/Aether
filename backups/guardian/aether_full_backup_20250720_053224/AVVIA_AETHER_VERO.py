#!/usr/bin/env python3
"""
🚀 AVVIA AETHER VERAMENTE - CON CREAZIONE CODICE E MONETIZZAZIONE
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path

# Importa configurazione Discord
import aether_env

print("""
╔══════════════════════════════════════════════════════════════╗
║                 🧠 AETHER SYSTEM STARTUP 🧠                  ║
║                                                              ║
║  Avvio REALE con:                                            ║
║  ✓ Creazione autonoma di codice                             ║
║  ✓ Sviluppo app monetizzabili                               ║
║  ✓ UI personale auto-generata                               ║
║  ✓ Comunicazione Discord attiva                             ║
╚══════════════════════════════════════════════════════════════╝
""")

def start_backend():
    """Avvia il server backend"""
    print("🌐 Avvio Backend Server...")
    subprocess.Popen([sys.executable, "server_simple.py"])
    time.sleep(3)
    print("✅ Backend avviato su http://localhost:5000")

def start_frontend():
    """Avvia il frontend React"""
    print("\n🎨 Avvio Frontend React...")
    try:
        # Vai nella directory frontend
        os.chdir("aether-frontend")
        
        # Controlla se node_modules esiste
        if not Path("node_modules").exists():
            print("📦 Installazione dipendenze frontend...")
            subprocess.run(["npm", "install"], check=True)
        
        # Avvia il dev server
        subprocess.Popen(["npm", "run", "dev"])
        
        # Torna alla directory root
        os.chdir("..")
        time.sleep(5)
        print("✅ Frontend avviato su http://localhost:3000")
    except Exception as e:
        print(f"⚠️ Frontend non avviato: {e}")
        print("   Puoi avviarlo manualmente con: cd aether-frontend && npm run dev")
        os.chdir("..")

def fix_aether_loop():
    """Sistema i problemi nel loop autonomo prima di avviarlo"""
    print("\n🔧 Fix del loop autonomo...")
    
    # Assicurati che i file JSON siano inizializzati correttamente
    data_dir = Path("data")
    
    # File che devono essere array
    array_files = {
        "agents.json": [],
        "rooms.json": [],
        "events.json": [],
        "evolutions.json": [],
        "messages.json": [],
        "plans.json": [],
        "action_logs.json": [],
        "modules.json": []
    }
    
    # File che devono essere oggetti
    object_files = {
        "mood.json": {"current": "determinato", "energy": 0.9},
        "economy.json": {"balance": 0, "assets": [], "career": "app_development"}
    }
    
    # Inizializza file array
    for filename, default in array_files.items():
        filepath = data_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content or content == "[]" or len(content) < 3:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        import json
                        json.dump(default, f)
        except:
            with open(filepath, 'w', encoding='utf-8') as f:
                import json
                json.dump(default, f)
    
    # Inizializza file oggetto
    for filename, default in object_files.items():
        filepath = data_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content or len(content) < 3:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        import json
                        json.dump(default, f, indent=2)
        except:
            with open(filepath, 'w', encoding='utf-8') as f:
                import json
                json.dump(default, f, indent=2)
    
    print("✅ File di dati sistemati")

def start_autonomous_loop():
    """Avvia il loop autonomo di Aether"""
    print("\n🧠 Avvio Loop Autonomo di Aether...")
    print("   Questo è il CUORE del sistema!")
    
    # Avvia in un nuovo processo
    subprocess.Popen([sys.executable, "aether_loop.py"])
    time.sleep(2)
    print("✅ Loop autonomo avviato!")
    print("   Aether ora può:")
    print("   - 💭 Pensare autonomamente")
    print("   - 🚀 Creare app monetizzabili")
    print("   - 🎨 Generare la sua UI")
    print("   - 💰 Sviluppare strategie di guadagno")
    print("   - 🧬 Evolvere il proprio codice")

def main():
    """Avvia tutto il sistema"""
    try:
        # 1. Fix dei file di dati
        fix_aether_loop()
        
        # 2. Avvia backend
        start_backend()
        
        # 3. Avvia frontend (opzionale)
        start_frontend()
        
        # 4. IMPORTANTE: Avvia il loop autonomo
        start_autonomous_loop()
        
        print("\n" + "="*60)
        print("🎉 AETHER È ORA COMPLETAMENTE OPERATIVO!")
        print("="*60)
        
        print("\n📊 Dashboard:")
        print("   Backend API: http://localhost:5000")
        print("   Frontend UI: http://localhost:3000")
        print("   Discord: Notifiche in tempo reale attive")
        
        print("\n💡 Cosa aspettarsi:")
        print("   - Messaggi Discord ogni 30-60 secondi")
        print("   - Creazione automatica di app e codice")
        print("   - Evoluzione della UI personale")
        print("   - Strategie di monetizzazione")
        
        print("\n⚠️ IMPORTANTE:")
        print("   NON chiudere questa finestra!")
        print("   Premi Ctrl+C per fermare tutto")
        
        # Mantieni il processo principale attivo
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Arresto del sistema...")
        print("   Aether si sta spegnendo...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 