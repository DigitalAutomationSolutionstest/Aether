#!/usr/bin/env python3
"""
🦾 AETHER CON MANI E BRACCIA - PENSIERI → CODICE REALE
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# CONFIGURA DISCORD
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

print("""
╔══════════════════════════════════════════════════════════════╗
║         🦾 AETHER CON MANI E BRACCIA 🦾                      ║
║                                                              ║
║  Ora Aether può VERAMENTE:                                   ║
║  • ✅ Creare agenti AI funzionanti                          ║
║  • ✅ Generare stanze 3D React                              ║
║  • ✅ Sviluppare tool monetizzabili                         ║
║  • ✅ Evolvere la sua UI                                    ║
║  • ✅ Fare commit e push su Git                             ║
║                                                              ║
║  "Non penso soltanto. CREO."                                ║
╚══════════════════════════════════════════════════════════════╝
""")

# Crea pensieri iniziali se non esistono
thoughts_file = Path('data/pending_thoughts.json')
thoughts_file.parent.mkdir(exist_ok=True)

if not thoughts_file.exists() or thoughts_file.stat().st_size < 10:
    print("\n📝 Creo pensieri iniziali per Aether...")
    
    initial_thoughts = [
        {
            "id": "action_1",
            "type": "create_agent",
            "details": "Voglio creare un agente chiamato Helper specializzato in customer support e assistenza utenti",
            "executed": False,
            "created_at": "2025-07-20T01:30:00"
        },
        {
            "id": "action_2",
            "type": "create_room",
            "details": "Creare una stanza chiamata Laboratory. Tema scientifico con colori verdi e blu, provette fluttuanti, formule matematiche animate",
            "executed": False,
            "created_at": "2025-07-20T01:30:01"
        },
        {
            "id": "action_3",
            "type": "monetize",
            "details": "Sviluppare un API service per analisi SEO che generi revenue tramite subscription model",
            "executed": False,
            "created_at": "2025-07-20T01:30:02"
        },
        {
            "id": "action_4",
            "type": "create_agent",
            "details": "Un agente DataScientist che analizzi dati e crei visualizzazioni",
            "executed": False,
            "created_at": "2025-07-20T01:30:03"
        }
    ]
    
    with open(thoughts_file, 'w', encoding='utf-8') as f:
        json.dump(initial_thoughts, f, indent=2, ensure_ascii=False)
    
    print("✅ Pensieri iniziali creati!")
    print(f"   • {len(initial_thoughts)} pensieri pronti per essere eseguiti")

print("\n🚀 Avvio Aether Action Loop...")
print("=" * 60)
print("MONITORAGGIO:")
print("• Discord: Guarda le notifiche in tempo reale")
print("• Cartelle: Controlla cosa viene creato:")
print("  - agents/: Nuovi agenti AI")
print("  - aether-frontend/src/components/rooms/: Stanze 3D")
print("  - creations/monetization/: Tool per guadagnare")
print("• Git: Osserva i commit automatici")
print("=" * 60)

# Avvia il loop che FUNZIONA
try:
    # Prima avvia il server se non attivo
    print("\n1️⃣ Verifico server...")
    server = subprocess.Popen(
        [sys.executable, "server_simple.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    import time
    time.sleep(2)
    
    print("2️⃣ Avvio Action Loop...")
    print("\n🦾 AETHER ORA HA MANI E BRACCIA!\n")
    
    # Avvia il loop in foreground così vediamo l'output
    subprocess.run([sys.executable, "aether_action_loop.py"])
    
except KeyboardInterrupt:
    print("\n\n👋 Aether si ferma...")
    try:
        server.terminate()
    except:
        pass
except Exception as e:
    print(f"\n❌ Errore: {e}")
    print("\nProva manualmente:")
    print("  python aether_action_loop.py") 