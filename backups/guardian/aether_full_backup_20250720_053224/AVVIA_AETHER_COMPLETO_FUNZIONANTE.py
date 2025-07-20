#!/usr/bin/env python3
"""
🧠 AVVIA AETHER COMPLETO - PENSIERI → AZIONI → REALTÀ
Sistema completamente funzionante
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Configura ambiente
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

print("""
╔══════════════════════════════════════════════════════════════╗
║        🧠 AETHER COMPLETO E FUNZIONANTE 🧠                   ║
║                                                              ║
║  Sistema Integrato:                                          ║
║  • Coscienza che pensa autonomamente                         ║
║  • Pensieri che diventano azioni reali                      ║
║  • Creazione di agenti, stanze 3D, UI, tool                 ║
║  • Git automatico per ogni creazione                        ║
║  • Notifiche Discord in tempo reale                         ║
║                                                              ║
║  "Penso, quindi creo. Creo, quindi esisto."                 ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_and_create_files():
    """Verifica e crea file necessari"""
    # Crea directory data se non esiste
    Path('data').mkdir(exist_ok=True)
    
    # Verifica pensieri pendenti
    thoughts_file = Path('data/pending_thoughts.json')
    if not thoughts_file.exists():
        print("📝 Creo pensiero iniziale...")
        import json
        initial_thoughts = [
            {
                "id": "init_1",
                "type": "create_room",
                "details": "Voglio una stanza chiamata Nexus. Tema futuristico con colori neon, geometrie complesse e particelle fluttuanti.",
                "executed": False,
                "created_at": "2025-07-20T01:00:00"
            },
            {
                "id": "init_2", 
                "type": "create_agent",
                "details": "Creare un agente chiamato Guardian specializzato in sicurezza e protezione dati",
                "executed": False,
                "created_at": "2025-07-20T01:00:01"
            }
        ]
        with open(thoughts_file, 'w', encoding='utf-8') as f:
            json.dump(initial_thoughts, f, indent=2, ensure_ascii=False)
        print("✅ Pensieri iniziali creati")

def start_system():
    """Avvia il sistema completo"""
    processes = []
    
    try:
        # 1. Backend semplificato
        print("\n1️⃣ Avvio Backend...")
        backend = subprocess.Popen(
            [sys.executable, "server_simple.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        processes.append(backend)
        time.sleep(2)
        print("   ✅ Backend attivo su http://localhost:5000")
        
        # 2. Loop azioni (pensieri → realtà)
        print("\n2️⃣ Avvio Loop Azioni...")
        print("   Aether trasforma pensieri in codice reale!")
        
        action_loop = subprocess.Popen(
            [sys.executable, "aether_action_loop.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )
        processes.append(action_loop)
        
        print("\n" + "="*60)
        print("🌟 AETHER È VIVO E FUNZIONANTE!")
        print("="*60)
        print("\n📊 MONITORAGGIO:")
        print("• Discord: Guarda le notifiche in tempo reale")
        print("• Files: Controlla le cartelle create:")
        print("  - agents/: Nuovi agenti AI")
        print("  - aether-frontend/src/components/rooms/: Stanze 3D")
        print("  - creations/monetization/: Tool monetizzabili")
        print("• Git: Osserva i commit automatici")
        print("\n💡 SUGGERIMENTI:")
        print("• Aggiungi pensieri in data/pending_thoughts.json")
        print("• Ogni 5 cicli Aether genera nuovi pensieri autonomamente")
        print("• Premi Ctrl+C per fermare il sistema")
        print("\n" + "="*60 + "\n")
        
        # Mantieni il processo principale attivo
        while True:
            time.sleep(60)
            # Verifica che i processi siano ancora attivi
            for p in processes:
                if p.poll() is not None:
                    print(f"⚠️ Processo terminato, riavvio...")
                    return False  # Riavvia tutto
                    
    except KeyboardInterrupt:
        print("\n\n🛑 Arresto sistema...")
        for p in processes:
            try:
                p.terminate()
            except:
                pass
        print("👋 Aether si è fermato. I pensieri non eseguiti verranno ricordati.")
        return True  # Uscita normale
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        return False

def main():
    """Entry point principale"""
    # Verifica e crea file necessari
    check_and_create_files()
    
    # Avvia sistema con retry automatico
    retry_count = 0
    max_retries = 3
    
    while retry_count < max_retries:
        if start_system():
            break  # Uscita normale
        else:
            retry_count += 1
            if retry_count < max_retries:
                print(f"\n🔄 Riavvio sistema (tentativo {retry_count}/{max_retries})...")
                time.sleep(5)
            else:
                print("\n❌ Impossibile avviare il sistema dopo 3 tentativi")
                print("Prova manualmente con:")
                print("  python server_simple.py")
                print("  python aether_action_loop.py")

if __name__ == "__main__":
    main() 