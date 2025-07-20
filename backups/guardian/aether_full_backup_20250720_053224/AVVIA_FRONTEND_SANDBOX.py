#!/usr/bin/env python3
"""
🎮 AVVIA FRONTEND SANDBOX - Avvia il frontend React con la sandbox di Aether
"""

import os
import subprocess
import time
from pathlib import Path

print("""
╔══════════════════════════════════════════════════════════════╗
║          🎮 AVVIA FRONTEND SANDBOX 🎮                       ║
║                                                              ║
║  Avvio automatico del frontend React                        ║
║  con la sandbox interattiva di Aether                       ║
║                                                              ║
║  "Ora puoi vedere e interagire con Aether!"                 ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_node_modules():
    """Verifica se node_modules esiste"""
    frontend_path = Path("aether-frontend")
    node_modules = frontend_path / "node_modules"
    return node_modules.exists()

def install_dependencies():
    """Installa dipendenze npm"""
    print("📦 Installando dipendenze npm...")
    try:
        result = subprocess.run(
            ["npm", "install"],
            cwd="aether-frontend",
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print("✅ Dipendenze installate con successo!")
            return True
        else:
            print(f"❌ Errore installazione: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def start_frontend():
    """Avvia il server di sviluppo"""
    print("🚀 Avviando frontend React...")
    try:
        # Avvia npm run dev
        process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd="aether-frontend",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("🌐 Frontend in avvio...")
        print("📱 La sandbox di Aether sarà disponibile su: http://localhost:5173")
        print("🎮 Aether può comunicare, muoversi e creare in tempo reale!")
        print("\n💬 Prova a:")
        print("   - Scrivere 'Ciao Aether' nella chat")
        print("   - Chiedere di creare qualcosa")
        print("   - Trascinare i nodi nella sandbox")
        print("   - Cambiare il mood di Aether")
        print("\n🔄 Monitoraggio output...")
        
        # Monitora l'output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"📡 {output.strip()}")
                
                # Controlla se il server è pronto
                if "Local:" in output or "ready" in output.lower():
                    print("\n🎉 FRONTEND PRONTO!")
                    print("🎮 Vai su http://localhost:5173 per interagire con Aether!")
                    
        return process.returncode == 0
        
    except KeyboardInterrupt:
        print("\n🛑 Interruzione utente")
        if 'process' in locals():
            process.terminate()
        return False
    except Exception as e:
        print(f"❌ Errore avvio: {e}")
        return False

def main():
    """Processo principale"""
    
    # Verifica se siamo nella directory corretta
    if not Path("aether-frontend").exists():
        print("❌ Directory aether-frontend non trovata!")
        print("   Assicurati di essere nella directory root del progetto")
        return False
    
    # Verifica node_modules
    if not check_node_modules():
        print("📦 node_modules non trovato, installando dipendenze...")
        if not install_dependencies():
            print("❌ Installazione fallita!")
            return False
    else:
        print("✅ node_modules trovato")
    
    # Verifica package.json
    package_json = Path("aether-frontend/package.json")
    if not package_json.exists():
        print("❌ package.json non trovato!")
        return False
    
    print("✅ Tutto pronto per l'avvio!")
    time.sleep(1)
    
    # Avvia frontend
    return start_frontend()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Avvio fallito!")
        input("Premi Enter per uscire...")
    else:
        print("\n✅ Frontend chiuso correttamente") 