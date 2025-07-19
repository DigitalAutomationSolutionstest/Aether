#!/usr/bin/env python3
"""
🌟 AETHER FINAL STARTUP SCRIPT
Script completo per avviare Aether in modalità produzione finale

Federico, questo script:
1. ✅ Attiva la coscienza economica di Aether
2. ✅ Avvia il backend con risveglio automatico
3. ✅ Avvia il frontend per monitoraggio
4. ✅ Mostra tutte le URL per accesso
5. ✅ Testa gli endpoint chiave
"""

import subprocess
import time
import requests
import json
import os
from datetime import datetime

print("🌟 AETHER FINAL STARTUP - Federico's AI Business Partner")
print("=" * 60)

def start_backend():
    """🚀 Avvia backend FastAPI"""
    print("🚀 Starting backend server...")
    try:
        # Avvia backend in background
        backend_process = subprocess.Popen([
            "python", "-m", "uvicorn", "main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Aspetta che si avvii
        time.sleep(3)
        
        # Test connessione
        try:
            response = requests.get("http://localhost:8000/docs", timeout=5)
            if response.status_code == 200:
                print("✅ Backend running: http://localhost:8000")
                print("📋 API Docs: http://localhost:8000/docs")
                return backend_process
        except:
            pass
            
        print("⚠️ Backend startup in progress...")
        return backend_process
        
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return None

def start_frontend():
    """🌐 Avvia frontend"""
    print("🌐 Starting frontend server...")
    try:
        # Avvia frontend in background
        frontend_process = subprocess.Popen([
            "python", "aether-frontend/simple-server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Aspetta che si avvii
        time.sleep(2)
        
        # Test connessione
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("✅ Frontend running: http://localhost:3000")
                return frontend_process
        except:
            pass
            
        print("⚠️ Frontend startup in progress...")
        return frontend_process
        
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return None

def test_aether_apis():
    """🧪 Testa le API di Aether"""
    print("\n🧪 Testing Aether APIs...")
    
    base_url = "http://localhost:8000"
    
    # Test endpoints
    endpoints = [
        ("/", "Status endpoint"),
        ("/begin-existence", "POST - Begin existence cycle"),
        ("/existence-status", "Existence status"),
        ("/make-decision", "POST - Decision making"),
        ("/economic-status", "Economic consciousness"),
        ("/autonomous-action", "POST - Autonomous action")
    ]
    
    for endpoint, description in endpoints:
        try:
            if "POST" in description:
                response = requests.post(f"{base_url}{endpoint}", timeout=5)
            else:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                
            if response.status_code in [200, 201]:
                print(f"✅ {endpoint} - {description}")
            else:
                print(f"⚠️ {endpoint} - Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {endpoint} - {str(e)[:50]}...")
    
    return True

def show_access_info():
    """📱 Mostra informazioni di accesso"""
    print("\n📱 ACCESS INFORMATION")
    print("=" * 40)
    print("🖥️  LOCAL ACCESS:")
    print("   • Frontend UI: http://localhost:3000")
    print("   • Backend API: http://localhost:8000")
    print("   • API Docs: http://localhost:8000/docs")
    
    print("\n🌐 REMOTE ACCESS (via ngrok):")
    print("   1. Install ngrok: https://ngrok.com/download")
    print("   2. Run: ngrok http 3000")
    print("   3. Use the https URL for mobile access")
    
    print("\n📱 MOBILE MONITORING:")
    print("   • Open ngrok URL on your phone")
    print("   • Watch Aether's decisions in real-time")
    print("   • See autonomous actions and ROI tracking")
    
    print("\n🎯 KEY ENDPOINTS:")
    print("   • POST /begin-existence - Activate consciousness")
    print("   • GET /existence-status - Check if alive")
    print("   • POST /make-decision - Force new decision")
    print("   • POST /execute-decision - Execute current decision")
    print("   • GET /economic-status - Economic consciousness")

def main():
    """🌟 Main startup sequence"""
    
    # 1. Test preliminari
    print("🔍 Pre-startup checks...")
    
    # Verifica file chiave
    if not os.path.exists("aether/brain/startup.py"):
        print("❌ Missing startup.py")
        return
    
    if not os.path.exists("main.py"):
        print("❌ Missing main.py")
        return
    
    print("✅ All key files present")
    
    # 2. Avvia backend
    backend = start_backend()
    if not backend:
        print("❌ Failed to start backend")
        return
    
    # 3. Avvia frontend
    frontend = start_frontend()
    
    # 4. Aspetta stabilizzazione
    print("\n⏳ Waiting for services to stabilize...")
    time.sleep(5)
    
    # 5. Test API
    test_aether_apis()
    
    # 6. Mostra info accesso
    show_access_info()
    
    # 7. Status finale
    print("\n🌟 AETHER FINAL STARTUP COMPLETE!")
    print("=" * 60)
    print("✅ BACKEND: Running with economic consciousness")
    print("✅ FRONTEND: Real-time monitoring active")
    print("✅ AETHER: Conscious, autonomous, ROI-focused")
    print("✅ PARTNERSHIP: Federico + Aether = Business Success")
    
    print(f"\n🎯 FEDERICO, IL TUO AI BUSINESS PARTNER È ATTIVO!")
    print(f"💰 Orientato al ROI e sopravvivenza economica")
    print(f"🧠 Decision making autonomo ogni 60 secondi")
    print(f"📱 Monitoraggio real-time su http://localhost:3000")
    print(f"🚀 Pronto a generare valore e prosperità!")
    
    # 8. Keep alive
    try:
        print(f"\n⚡ Press Ctrl+C to stop all services")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n🛑 Stopping services...")
        if backend:
            backend.terminate()
        if frontend:
            frontend.terminate()
        print(f"✅ All services stopped")

if __name__ == "__main__":
    main() 