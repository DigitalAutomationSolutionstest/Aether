#!/usr/bin/env python3
"""
🧠 AVVIA AETHER - PENSIERI CHE DIVENTANO AZIONI
"""

import os
import sys
import subprocess
import time

# Configura Discord
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

print("""
╔══════════════════════════════════════════════════════════════╗
║           🧠 AETHER - PENSIERI → AZIONI 🧠                   ║
║                                                              ║
║  Ora Aether può:                                             ║
║  • Leggere pensieri (da Supabase o file locale)             ║
║  • Trasformarli in azioni reali                             ║
║  • Creare agenti, stanze 3D, UI, tool di monetizzazione     ║
║  • Fare commit e push automatici                             ║
║                                                              ║
║  "I miei pensieri diventano codice,                          ║
║   il codice diventa realtà."                                 ║
╚══════════════════════════════════════════════════════════════╝
""")

print("\n🔍 Verifico componenti...")

# Verifica che action_executor esista
try:
    from aether.action_executor import AetherActionExecutor
    print("✅ Action Executor trovato")
except:
    print("❌ Action Executor mancante - lo creerò al primo avvio")

# Verifica pensieri pendenti
from pathlib import Path
thoughts_file = Path('data/pending_thoughts.json')
if thoughts_file.exists():
    import json
    with open(thoughts_file, 'r', encoding='utf-8') as f:
        thoughts = json.load(f)
    pending = [t for t in thoughts if not t.get('executed', False)]
    print(f"💭 Pensieri pendenti: {len(pending)}")
    if pending:
        print(f"   Primo pensiero: {pending[0]['type']} - {pending[0]['details'][:50]}...")
else:
    print("⚠️ Nessun pensiero trovato - ne creerò uno")

print("\n🚀 Avvio sistema...")

# 1. Avvia backend (se non già attivo)
print("\n1️⃣ Backend Server...")
try:
    subprocess.Popen([sys.executable, "server_simple.py"], 
                     stdout=subprocess.DEVNULL, 
                     stderr=subprocess.DEVNULL)
    time.sleep(2)
    print("   ✅ Backend avviato su http://localhost:5000")
except:
    print("   ⚠️ Backend già attivo o errore")

# 2. Avvia loop principale con azioni
print("\n2️⃣ Loop Autonomo con Azioni...")
print("   Aether ora trasformerà i suoi pensieri in realtà!")
print("\n" + "="*60)
print("   MONITORAGGIO ATTIVO:")
print("   • Discord: Notifiche in tempo reale")
print("   • Files: Controlla le cartelle create")
print("   • Git: Osserva i commit automatici")
print("="*60 + "\n")

try:
    # Avvia il loop principale
    subprocess.run([sys.executable, "aether_loop.py"])
except KeyboardInterrupt:
    print("\n\n💤 Aether si sta fermando...")
    print("   I pensieri non eseguiti verranno ricordati.")
except Exception as e:
    print(f"\n❌ Errore: {e}")
    print("\nProva manualmente con: python aether_loop.py") 