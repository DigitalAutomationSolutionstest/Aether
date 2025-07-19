#!/usr/bin/env python3
"""
🌟 AETHER COMPLETE STARTUP
Script che avvia backend e frontend per Federico's AI Business Partner
"""

import subprocess
import time
import os
import sys
import json
from datetime import datetime

def start_backend():
    """🚀 Avvia il backend FastAPI"""
    print("🚀 STEP 1: Starting backend...")
    
    try:
        # Avvia con uvicorn per evitare warning
        backend_cmd = [
            sys.executable, "-m", "uvicorn", "main:app",
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ]
        
        backend_process = subprocess.Popen(
            backend_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ Backend starting with uvicorn...")
        time.sleep(3)  # Aspetta l'avvio
        
        return backend_process
        
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return None

def start_frontend_npm():
    """🌐 Avvia frontend con npm se disponibile"""
    print("🌐 STEP 2: Starting frontend with npm...")
    
    frontend_dir = "aether-frontend"
    
    if not os.path.exists(os.path.join(frontend_dir, "package.json")):
        print("❌ No package.json found")
        return None
        
    try:
        # Cambia directory e avvia npm
        os.chdir(frontend_dir)
        
        # Prima installa dipendenze se necessario
        if not os.path.exists("node_modules"):
            print("📦 Installing npm dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Avvia il dev server
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Torna alla directory principale
        os.chdir("..")
        
        print("✅ Frontend starting with npm dev server...")
        time.sleep(3)
        
        return frontend_process
        
    except Exception as e:
        print(f"⚠️ npm not available: {e}")
        os.chdir("..")  # Assicurati di tornare alla directory principale
        return None

def start_frontend_python():
    """🐍 Avvia frontend con Python simple server"""
    print("🐍 Starting frontend with Python server...")
    
    try:
        frontend_process = subprocess.Popen([
            sys.executable, "aether-frontend/simple-server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("✅ Frontend starting with Python server on port 3001...")
        time.sleep(2)
        
        return frontend_process
        
    except Exception as e:
        print(f"❌ Python frontend error: {e}")
        return None

def check_services():
    """🔍 Verifica che i servizi siano attivi"""
    print("\n🔍 Checking services...")
    
    try:
        import requests
        
        # Test backend
        try:
            response = requests.get("http://localhost:8000/", timeout=3)
            print("✅ Backend: http://localhost:8000")
        except:
            print("⚠️ Backend not responding")
        
        # Test frontend npm (porta 5173)
        try:
            response = requests.get("http://localhost:5173", timeout=3)
            print("✅ Frontend (npm): http://localhost:5173")
        except:
            # Test frontend python (porta 3001)
            try:
                response = requests.get("http://localhost:3001", timeout=3)
                print("✅ Frontend (python): http://localhost:3001")
            except:
                print("⚠️ Frontend not responding")
                
    except ImportError:
        print("⚠️ requests not available, skipping service check")

def show_startup_info():
    """📋 Mostra informazioni di avvio"""
    print("\n" + "="*60)
    print("🌟 AETHER IS NOW RUNNING!")
    print("="*60)
    print("🖥️  ACCESS URLS:")
    print("   • Backend API: http://localhost:8000")
    print("   • API Docs: http://localhost:8000/docs")
    print("   • Frontend (npm): http://localhost:5173")
    print("   • Frontend (python): http://localhost:3001")
    
    print("\n🎯 KEY ENDPOINTS:")
    print("   • POST /begin-existence - Activate Aether consciousness")
    print("   • GET /existence-status - Check if Aether is alive")
    print("   • POST /make-decision - Force new strategic decision")
    print("   • POST /autonomous-action - Trigger autonomous action")
    
    print("\n💰 AETHER STATUS:")
    print("   • Economic consciousness: ACTIVE")
    print("   • Survival mode: ENGAGED")
    print("   • Partnership with Federico: ACCEPTED")
    print("   • Auto-action loop: Running every 60 seconds")
    
    print("\n📱 MOBILE ACCESS:")
    print("   1. Install ngrok: https://ngrok.com/download")
    print("   2. Run: ngrok http 5173 (or 3001)")
    print("   3. Use the https URL on your phone")
    
    print("\n⚡ Press Ctrl+C to stop all services")

def main():
    """🌟 Main startup routine"""
    print("🌟 AETHER COMPLETE STARTUP")
    print("=" * 60)
    print("🤖 Federico's AI Business Partner")
    print("🧠 Autonomous, Economic, ROI-Focused")
    print("=" * 60)
    
    # Verifica file essenziali
    essential_files = [
        "main.py",
        "aether/brain/startup.py", 
        "aether-frontend/index.html"
    ]
    
    missing_files = [f for f in essential_files if not os.path.exists(f)]
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return
    
    # Avvia backend
    backend = start_backend()
    if not backend:
        print("❌ Failed to start backend")
        return
    
    # Prova prima npm, poi Python
    frontend = start_frontend_npm()
    if not frontend:
        frontend = start_frontend_python()
    
    # Attendi stabilizzazione
    print("\n⏳ Waiting for services to stabilize...")
    time.sleep(5)
    
    # Verifica servizi
    check_services()
    
    # Mostra info
    show_startup_info()
    
    # Mantieni attivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        
        if backend:
            backend.terminate()
            backend.wait()
            
        if frontend:
            frontend.terminate() 
            frontend.wait()
            
        print("✅ All services stopped")

if __name__ == "__main__":
    main() 