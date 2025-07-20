#!/usr/bin/env python3
"""
🚀 AVVIA AETHER CON DISCORD CONFIGURATO
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
║         🦾 AETHER ATTIVATO CON DISCORD 🦾                    ║
║                                                              ║
║  ✅ Discord Webhook: CONFIGURATO                             ║
║  ✅ Notifiche: ATTIVE                                        ║
║  ✅ Creazione Codice: ABILITATA                              ║
║                                                              ║
║  Ora Aether può:                                             ║
║  • Creare agenti AI                                          ║
║  • Generare stanze 3D                                        ║
║  • Sviluppare tool monetizzabili                             ║
║  • Notificare tutto su Discord                               ║
║                                                              ║
║  "I miei pensieri diventano realtà."                         ║
╚══════════════════════════════════════════════════════════════╝
""")

# Pulisci i pensieri con errori
thoughts_file = Path('data/pending_thoughts.json')
if thoughts_file.exists():
    print("\n🧹 Pulizia pensieri con errori...")
    
    # Crea nuovi pensieri puliti
    clean_thoughts = [
        {
            "id": f"thought_{i}",
            "type": thought_type,
            "details": details,
            "executed": False,
            "created_at": f"2025-07-20T01:30:0{i}"
        }
        for i, (thought_type, details) in enumerate([
            ("create_agent", "Un agente DataAnalyst specializzato in analisi dati e visualizzazioni"),
            ("create_room", "Una stanza Cosmos con tema spaziale, stelle animate e pianeti orbitanti"),
            ("monetize", "Un tool di AI Writing Assistant per contenuti SEO con abbonamento mensile"),
            ("evolve_ui", "Aggiungere animazioni fluide e transizioni smooth all'interfaccia"),
            ("create_agent", "Un agente SecurityExpert per analisi vulnerabilità e sicurezza"),
            ("create_room", "Una stanza Ocean con onde, pesci animati e suoni rilassanti")
        ])
    ]
    
    with open(thoughts_file, 'w', encoding='utf-8') as f:
        json.dump(clean_thoughts, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {len(clean_thoughts)} pensieri pronti per l'esecuzione!")

print("\n📡 Test connessione Discord...")
# Test Discord
try:
    import requests
    webhook_url = os.environ['DISCORD_WEBHOOK_URL']
    response = requests.post(webhook_url, json={
        "content": "🤖 **AETHER ONLINE!**\n\n✨ Sistema attivato con successo\n🧠 Pronto a trasformare pensieri in codice\n🚀 Monitoraggio attivo"
    })
    if response.status_code in [200, 204]:
        print("✅ Discord connesso con successo!")
    else:
        print(f"⚠️ Discord response: {response.status_code}")
except Exception as e:
    print(f"⚠️ Errore Discord: {e}")

print("\n🚀 Avvio sistema Aether...")
print("=" * 60)
print("MONITORAGGIO LIVE:")
print("• Discord: Guarda il canale per notifiche")
print("• Cartelle da controllare:")
print("  - agents/: Nuovi agenti AI")
print("  - aether-frontend/src/components/rooms/: Stanze 3D")
print("  - creations/monetization/: Tool monetizzabili")
print("• File: data/pending_thoughts.json")
print("=" * 60)

# Avvia il server semplice in background
print("\n1️⃣ Avvio server backend...")
server_process = subprocess.Popen(
    [sys.executable, "server_simple.py"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

import time
time.sleep(2)

# Avvia il loop azioni
print("2️⃣ Avvio Action Loop con Discord...")
print("\n🦾 AETHER È VIVO E CREA!\n")

try:
    subprocess.run([sys.executable, "aether_action_loop.py"])
except KeyboardInterrupt:
    print("\n\n👋 Aether si ferma...")
    server_process.terminate()
except Exception as e:
    print(f"\n❌ Errore: {e}")
    server_process.terminate() 