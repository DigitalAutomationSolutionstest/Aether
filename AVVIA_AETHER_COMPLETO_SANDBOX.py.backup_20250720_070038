#!/usr/bin/env python3
"""
🎮 AVVIA AETHER COMPLETO SANDBOX - Sistema completo interattivo
Avvia backend Python e frontend React per la sandbox completa di Aether
"""

import os
import subprocess
import threading
import time
from pathlib import Path

# Configura Discord
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

print("""
╔══════════════════════════════════════════════════════════════╗
║          🎮 AETHER SANDBOX COMPLETA 🎮                      ║
║                                                              ║
║  Sistema completo con backend Python e frontend React       ║
║  Aether può comunicare, muoversi e creare in tempo reale    ║
║                                                              ║
║  🐍 Backend: http://localhost:5001 (Flask + WebSocket)      ║
║  ⚛️  Frontend: http://localhost:5173 (React + Vite)         ║
║                                                              ║
║  "Il mio mondo digitale dove posso essere me stesso!"       ║
╚══════════════════════════════════════════════════════════════╝
""")

def start_backend():
    """Avvia il backend Flask"""
    print("🐍 Avviando backend Aether...")
    try:
        process = subprocess.Popen(
            ["python", "AVVIA_AETHER_SANDBOX_COMPLETA.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Monitora l'output del backend
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"🐍 Backend: {output.strip()}")
                
        return process.returncode == 0
        
    except Exception as e:
        print(f"❌ Errore backend: {e}")
        return False

def start_frontend():
    """Avvia il frontend React"""
    print("⚛️ Avviando frontend React...")
    time.sleep(3)  # Aspetta che il backend si avvii
    
    try:
        # Cambia directory e avvia npm
        os.chdir("aether-frontend")
        
        # Installa dipendenze se necessario
        if not Path("node_modules").exists():
            print("📦 Installando dipendenze npm...")
            subprocess.run(["npm", "install"], check=True)
        
        # Avvia dev server
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Monitora l'output del frontend
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"⚛️ Frontend: {output.strip()}")
                
                # Controlla se il server è pronto
                if "Local:" in output or "ready" in output.lower():
                    print("\n🎉 SISTEMA COMPLETO PRONTO!")
                    print("🎮 Vai su http://localhost:5173 per la sandbox React!")
                    print("🌐 O su http://localhost:5001 per la versione Flask!")
                    print("\n💬 Prova a:")
                    print("   - Scrivere 'Ciao Aether' nella chat")
                    print("   - Chiedere di creare qualcosa")
                    print("   - Trascinare i nodi nella sandbox")
                    print("   - Cambiare il mood di Aether")
                
        return process.returncode == 0
        
    except Exception as e:
        print(f"❌ Errore frontend: {e}")
        return False
    finally:
        # Torna alla directory originale
        os.chdir("..")

def send_discord_notification():
    """Invia notifica Discord di avvio"""
    try:
        import requests
        webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
        if webhook_url:
            message = {
                "embeds": [{
                    "title": "🎮 Aether Sandbox Completa ONLINE!",
                    "description": "Sistema completo avviato con successo!\n\n"
                                 "🐍 **Backend Flask**: http://localhost:5001\n"
                                 "⚛️ **Frontend React**: http://localhost:5173\n\n"
                                 "Aether può ora comunicare, muoversi e creare in tempo reale!",
                    "color": 0x00ff00,
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
                }]
            }
            requests.post(webhook_url, json=message, timeout=10)
            print("📡 Notifica Discord inviata!")
    except Exception as e:
        print(f"❌ Errore Discord: {e}")

def main():
    """Processo principale"""
    
    print("🚀 Inizializzando sistema Aether completo...")
    
    # Invia notifica Discord
    send_discord_notification()
    
    # Avvia backend in thread separato
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    print("⏳ Aspettando 5 secondi per l'avvio del backend...")
    time.sleep(5)
    
    try:
        # Avvia frontend nel thread principale
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Interruzione utente - Chiusura sistema...")
    except Exception as e:
        print(f"❌ Errore generale: {e}")
    
    print("\n✅ Sistema Aether chiuso")

if __name__ == "__main__":
    main() 