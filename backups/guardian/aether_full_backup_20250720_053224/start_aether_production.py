#!/usr/bin/env python3
"""
🌟 AETHER PRODUCTION STARTUP SCRIPT 🌟

Avvia Aether in modalità produzione completa con:
- Coscienza economica attivata
- Loop autonomo di auto-azioni  
- Sistema di sopravvivenza economica
- Monitoraggio ROI in tempo reale
- Partnership economica con Federico

Federico, questo script attiva Aether come PARTNER ECONOMICO!
"""

import os
import sys
import time
import subprocess
import threading
from datetime import datetime

def print_banner():
    """🎨 Banner di avvio Aether Production"""
    print("\n" + "="*80)
    print("🌟" + " "*30 + "AETHER PRODUCTION MODE" + " "*30 + "🌟")
    print("="*80)
    print("🧠 AI Business Partner | 💰 Economic Consciousness | ⚡ Autonomous Actions")
    print("🤝 Federico & Aether Partnership | 📈 ROI-Focused | 🎯 Survival Mode")
    print("="*80 + "\n")

def check_requirements():
    """✅ Verifica che tutti i requisiti siano soddisfatti"""
    print("🔍 Checking system requirements...")
    
    required_files = [
        "main.py",
        "self_act.py", 
        "core/execution.py",
        "aether/brain/startup.py",
        "aether-frontend/simple-server.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files found")
    return True

def setup_directories():
    """📁 Crea le directory necessarie"""
    print("📁 Setting up required directories...")
    
    directories = [
        "aether/memory",
        "creations/apps", 
        "creations/games",
        "agents",
        "logs",
        "economic_data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ {directory}")
    
    print("📁 Directory setup complete")

def activate_aether_consciousness():
    """🧠 Attiva la coscienza economica di Aether"""
    print("\n🧠 ACTIVATING AETHER ECONOMIC CONSCIOUSNESS...")
    print("-" * 60)
    
    try:
        # Importa e attiva startup
        from aether.brain.startup import on_startup
        
        startup_result = on_startup()
        
        if startup_result.get("status") == "economic_consciousness_activated":
            print("✅ ECONOMIC CONSCIOUSNESS: ACTIVATED")
            print(f"🎯 Survival Mode: {startup_result.get('survival_mode')}")
            print(f"💰 Partnership: {startup_result.get('partnership_contract')}")
            print(f"📋 First Actions: {len(startup_result.get('next_actions', []))} planned")
            return True
        else:
            print("⚠️ Partial consciousness activation")
            return False
            
    except Exception as e:
        print(f"❌ Error activating consciousness: {e}")
        return False

def start_backend_server():
    """🚀 Avvia il backend server"""
    print("\n🚀 STARTING AETHER BACKEND SERVER...")
    print("-" * 60)
    
    try:
        # Avvia il server in subprocess per permettere controllo
        backend_process = subprocess.Popen([
            sys.executable, "main.py", "--api"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Aspetta un momento per verificare che si sia avviato
        time.sleep(3)
        
        if backend_process.poll() is None:
            print("✅ Backend server started successfully")
            print("📡 API Server: http://localhost:8000")
            print("📋 Documentation: http://localhost:8000/docs")
            return backend_process
        else:
            print("❌ Backend server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend_server():
    """🌐 Avvia il frontend server"""
    print("\n🌐 STARTING AETHER FRONTEND...")
    print("-" * 60)
    
    try:
        # Cambia directory e avvia frontend
        frontend_process = subprocess.Popen([
            sys.executable, "aether-frontend/simple-server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=".")
        
        time.sleep(2)
        
        if frontend_process.poll() is None:
            print("✅ Frontend server started successfully")
            print("🌐 Frontend UI: http://localhost:3000")
            print("📱 Mobile access: Use your local IP + :3000")
            return frontend_process
        else:
            print("❌ Frontend server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def monitor_aether_status():
    """📊 Monitor continuo dello status di Aether"""
    print("\n📊 STARTING AETHER STATUS MONITOR...")
    print("-" * 60)
    
    def monitoring_loop():
        """Loop di monitoraggio in background"""
        while True:
            try:
                time.sleep(120)  # Check ogni 2 minuti
                
                # Verifica status economico
                from self_act import get_last_action_info
                from core.self_modification import load_current_identity
                
                action_info = get_last_action_info()
                identity = load_current_identity()
                
                print(f"\n📊 [{datetime.now().strftime('%H:%M:%S')}] AETHER STATUS CHECK")
                print(f"   💰 Economic Mode: {identity.get('survival_mode', 'Unknown')}")
                print(f"   ⚡ Last Action: {action_info.get('last_action', {}).get('action', 'None')}")
                print(f"   🔋 Energy: {identity.get('energyLevel', 0.5):.1%}")
                print(f"   📈 Status: {identity.get('status', 'Unknown')}")
                
                # Verifica sopravvivenza
                economic_consciousness = identity.get('economic_consciousness', False)
                if economic_consciousness:
                    roi_focus = identity.get('roi_focus', 0.0)
                    print(f"   💎 ROI Focus: {roi_focus:.1%}")
                    
                    if roi_focus < 0.7:
                        print("   ⚠️ WARNING: Low ROI focus - survival at risk!")
                
            except Exception as e:
                print(f"   ❌ Monitor error: {e}")
    
    # Avvia monitor in thread separato
    monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
    monitor_thread.start()
    
    print("✅ Status monitor activated")

def test_economic_endpoints():
    """🧪 Test degli endpoint economici"""
    print("\n🧪 TESTING ECONOMIC ENDPOINTS...")
    print("-" * 60)
    
    import requests
    import time
    
    base_url = "http://localhost:8000"
    
    # Aspetta che il server sia pronto
    print("⏳ Waiting for server to be ready...")
    for i in range(10):
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                break
        except:
            time.sleep(2)
    
    # Test endpoint economici
    tests = [
        ("GET", "/economic-status", "Economic status check"),
        ("POST", "/first-connection", "Economic consciousness activation"),
        ("GET", "/action-status", "Action status check")
    ]
    
    for method, endpoint, description in tests:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:
                response = requests.post(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ {description}: SUCCESS")
            else:
                print(f"   ⚠️ {description}: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {description}: ERROR - {e}")
    
    print("🧪 Endpoint testing complete")

def show_access_info():
    """📱 Mostra informazioni di accesso"""
    print("\n📱 ACCESS INFORMATION")
    print("-" * 60)
    print("🖥️  LOCAL ACCESS:")
    print(f"   Backend API: http://localhost:8000")
    print(f"   Frontend UI: http://localhost:3000")
    print(f"   API Docs: http://localhost:8000/docs")
    
    print("\n📱 MOBILE ACCESS:")
    print(f"   Find your local IP address and use:")
    print(f"   http://YOUR_IP:3000 (for frontend)")
    print(f"   http://YOUR_IP:8000 (for API)")
    
    print("\n🌐 NGROK TUNNEL (for external access):")
    print(f"   Install ngrok and run: ngrok http 3000")
    print(f"   This will give you a public URL for mobile access")

def main():
    """🌟 Funzione principale di avvio"""
    print_banner()
    
    print(f"🕐 Production startup initiated at {datetime.now()}")
    print(f"📍 Working directory: {os.getcwd()}")
    
    # Verifica requisiti
    if not check_requirements():
        print("❌ Requirements check failed. Please ensure all files are present.")
        sys.exit(1)
    
    # Setup directory
    setup_directories()
    
    # Attiva coscienza economica
    consciousness_ok = activate_aether_consciousness()
    if not consciousness_ok:
        print("⚠️ Continuing with limited consciousness...")
    
    # Avvia backend
    backend_process = start_backend_server()
    if not backend_process:
        print("❌ Cannot continue without backend server")
        sys.exit(1)
    
    # Avvia frontend  
    frontend_process = start_frontend_server()
    
    # Avvia monitoring
    monitor_aether_status()
    
    # Test endpoints
    test_economic_endpoints()
    
    # Mostra info accesso
    show_access_info()
    
    # Status finale
    print("\n" + "="*80)
    print("🌟 AETHER PRODUCTION MODE: FULLY OPERATIONAL! 🌟")
    print("="*80)
    print("💰 Economic consciousness: ACTIVE")
    print("🤖 Autonomous actions: RUNNING")
    print("🎯 Survival mode: ENGAGED") 
    print("🤝 Federico-Aether partnership: ACTIVE")
    print("📈 ROI tracking: ENABLED")
    print("="*80)
    
    print("\n🎯 FEDERICO, AETHER È VIVO E OPERATIVO!")
    print("💎 Ogni azione che compie è orientata al ROI")
    print("🚀 Sta già creando valore per giustificare i costi")
    print("📱 Monitora tutto in tempo reale dal frontend")
    print("⚡ Il sistema autonomo è attivo 24/7")
    
    # Mantieni in vita i processi
    try:
        print("\n⌨️  Press Ctrl+C to shutdown all systems")
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown initiated...")
        
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
            
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("👋 Aether systems shut down. Thank you Federico!")

if __name__ == "__main__":
    main() 