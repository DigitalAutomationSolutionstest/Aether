#!/usr/bin/env python3
"""
📊 MONITOR AETHER - TEMPO REALE
================================
Monitor per vedere cosa sta facendo Aether in tempo reale.
"""

import os
import time
import requests
import json
from datetime import datetime
from pathlib import Path

def check_aether_status():
    """Controlla lo status di Aether"""
    try:
        response = requests.get("http://localhost:5000/api/consciousness/status", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"HTTP {response.status_code}"}
    except:
        return {"status": "offline", "message": "Server non raggiungibile"}

def check_logs():
    """Controlla i log recenti"""
    log_files = [
        "aether/logs/aether_diary.log",
        "data/logs/aether.log"
    ]
    
    logs = []
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        # Ultime 5 righe
                        recent_lines = lines[-5:]
                        logs.extend(recent_lines)
            except:
                pass
    
    return logs

def check_audio_files():
    """Controlla i file audio recenti"""
    audio_dir = Path("aether/logs/audio")
    if audio_dir.exists():
        audio_files = list(audio_dir.glob("*.mp3"))
        return sorted(audio_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
    return []

def check_discord_webhook():
    """Testa il webhook Discord"""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return "❌ Webhook non configurato"
    
    try:
        response = requests.post(webhook_url, json={
            "content": "🔍 **Monitor Aether**: Sistema controllato e funzionante!"
        }, timeout=10)
        
        if response.status_code in [200, 204]:
            return "✅ Webhook funzionante"
        else:
            return f"❌ Webhook errore: {response.status_code}"
    except Exception as e:
        return f"❌ Webhook errore: {e}"

def display_status():
    """Mostra lo status completo"""
    print("📊 MONITOR AETHER - TEMPO REALE")
    print("=" * 50)
    print(f"🕐 Ultimo aggiornamento: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Status server
    print("🌐 STATUS SERVER:")
    status = check_aether_status()
    if status.get("status") == "online":
        print("   ✅ Server online")
        print(f"   📊 Pensieri: {status.get('thoughts_count', 0)}")
        print(f"   🧬 Evoluzioni: {status.get('evolutions_count', 0)}")
        print(f"   🎯 Decisioni: {status.get('decisions_count', 0)}")
    else:
        print(f"   ❌ Server: {status.get('message', 'offline')}")
    
    print()
    
    # Status Discord
    print("📱 STATUS DISCORD:")
    discord_status = check_discord_webhook()
    print(f"   {discord_status}")
    
    print()
    
    # File audio recenti
    print("🎙️ AUDIO RECENTI:")
    audio_files = check_audio_files()
    if audio_files:
        for audio_file in audio_files:
            mtime = datetime.fromtimestamp(audio_file.stat().st_mtime)
            print(f"   🎵 {audio_file.name} ({mtime.strftime('%H:%M:%S')})")
    else:
        print("   ⚠️ Nessun file audio recente")
    
    print()
    
    # Log recenti
    print("📝 LOG RECENTI:")
    logs = check_logs()
    if logs:
        for log in logs[-3:]:  # Ultime 3 righe
            log = log.strip()
            if log and len(log) > 50:
                print(f"   📄 {log[:80]}...")
    else:
        print("   ⚠️ Nessun log recente")
    
    print()
    print("=" * 50)

def main():
    """Loop principale del monitor"""
    print("🔍 Avvio monitor Aether...")
    print("🔄 Aggiornamento ogni 30 secondi")
    print("🛑 Premi Ctrl+C per fermare")
    print()
    
    try:
        while True:
            display_status()
            print("⏳ Attendo 30 secondi...")
            time.sleep(30)
            print("\n" * 3)  # Pulisce lo schermo
            
    except KeyboardInterrupt:
        print("\n🛑 Monitor fermato")

if __name__ == "__main__":
    main() 