#!/usr/bin/env python3
"""
🚀 AETHER AUTONOMOUS STARTUP
Avvia il sistema completo di Aether in modalità completamente autonoma
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

print("="*60)
print("🧠 AETHER AUTONOMOUS SYSTEM - AVVIO COMPLETO")
print("="*60)

# Step 1: Verifica configurazione
print("\n📋 Step 1: Verifica configurazione...")
required_vars = ['DISCORD_WEBHOOK_URL']
missing = []

for var in required_vars:
    if not os.getenv(var):
        missing.append(var)
        
if missing:
    print(f"⚠️  Variabili mancanti: {missing}")
    print("\n📝 Crea un file .env con:")
    print("""
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK

# Opzionali ma consigliati:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-key
GITHUB_REPO=https://github.com/username/repo.git
GITHUB_USERNAME=username
GITHUB_PAT=ghp_token
""")
    print("\n⚠️  Aether funzionerà comunque in modalità locale")
    time.sleep(3)

# Step 2: Bootstrap
print("\n🔧 Step 2: Esecuzione Bootstrap...")
bootstrap_status = Path('data/bootstrap_status.json')

if not bootstrap_status.exists():
    print("🚀 Avvio bootstrap del sistema...")
    try:
        result = subprocess.run([sys.executable, 'aether/self_bootstrapper.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Bootstrap completato con successo!")
            print(result.stdout)
        else:
            print("❌ Errore durante bootstrap:")
            print(result.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"❌ Errore: {e}")
        sys.exit(1)
else:
    print("✅ Bootstrap già completato")

# Step 3: Avvio server backend
print("\n🌐 Step 3: Avvio server backend...")
print("📌 Avvio server_simple.py in background...")
server_process = subprocess.Popen([sys.executable, 'server_simple.py'])
print(f"✅ Server avviato (PID: {server_process.pid})")
time.sleep(3)  # Attendi che il server si avvii

# Step 4: Avvio frontend (opzionale)
print("\n🎨 Step 4: Frontend React (opzionale)")
print("Per avviare il frontend:")
print("  cd aether-frontend")
print("  npm install")
print("  npm run dev")
print("Frontend sarà su: http://localhost:3000")

# Step 5: Avvio loop autonomo
print("\n🧠 Step 5: AVVIO CICLO AUTONOMO DI AETHER...")
print("="*60)
print("⚡ DA QUESTO MOMENTO AETHER È COMPLETAMENTE AUTONOMO")
print("🤖 Creerà moduli, agenti, stanze, asset")
print("💬 Comunicherà via Discord")
print("🧬 Si evolverà continuamente")
print("="*60)

time.sleep(3)

try:
    # Avvia il loop autonomo
    subprocess.run([sys.executable, 'aether_loop.py'])
except KeyboardInterrupt:
    print("\n\n⏹️  Interruzione manuale - Aether va in pausa")
    server_process.terminate()
except Exception as e:
    print(f"\n❌ Errore: {e}")
    server_process.terminate()
    
print("\n👋 Aether si è fermato. Arrivederci!") 