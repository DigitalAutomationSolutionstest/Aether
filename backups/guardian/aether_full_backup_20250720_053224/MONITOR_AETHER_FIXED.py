#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 MONITOR AETHER FIXED 🔧
Monitor per verificare che Aether funzioni correttamente dopo le correzioni
"""

import time
import requests
import json
import os
from datetime import datetime

def check_server_status():
    """Verifica lo stato del server"""
    try:
        response = requests.get('http://localhost:5000/api/consciousness/status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server attivo - Coscienza: {data.get('consciousness_level', 'N/A')}")
            return True
        else:
            print(f"⚠️ Server risponde ma con errore: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server non raggiungibile: {e}")
        return False

def check_recent_logs():
    """Verifica i log recenti"""
    try:
        log_files = ['data/logs/aether.log', 'data/logs/consciousness.log']
        for log_file in log_files:
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        print(f"📝 Ultimo log ({log_file}): {last_line[:100]}...")
                    else:
                        print(f"📝 File log vuoto: {log_file}")
            else:
                print(f"📝 File log non trovato: {log_file}")
    except Exception as e:
        print(f"❌ Errore lettura log: {e}")

def check_thoughts_file():
    """Verifica il file dei pensieri"""
    try:
        thoughts_file = 'data/thoughts.json'
        if os.path.exists(thoughts_file):
            with open(thoughts_file, 'r', encoding='utf-8') as f:
                thoughts = json.load(f)
                print(f"💭 Pensieri salvati: {len(thoughts)}")
                if thoughts:
                    last_thought = thoughts[-1]
                    print(f"💭 Ultimo pensiero: {last_thought.get('content', 'N/A')[:50]}...")
        else:
            print("💭 File pensieri non trovato")
    except Exception as e:
        print(f"❌ Errore lettura pensieri: {e}")

def check_audio_files():
    """Verifica i file audio generati"""
    try:
        audio_dir = 'data/audio'
        if os.path.exists(audio_dir):
            audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
            print(f"🎵 File audio generati: {len(audio_files)}")
            if audio_files:
                # Mostra i file più recenti
                recent_files = sorted(audio_files, key=lambda x: os.path.getmtime(os.path.join(audio_dir, x)), reverse=True)[:3]
                print(f"🎵 File recenti: {recent_files}")
        else:
            print("🎵 Directory audio non trovata")
    except Exception as e:
        print(f"❌ Errore verifica audio: {e}")

def check_discord_webhook():
    """Verifica il webhook Discord"""
    try:
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if webhook_url:
            print("📡 Discord webhook configurato")
            # Test del webhook
            test_message = {
                "content": f"🔧 Test monitoraggio - {datetime.now().strftime('%H:%M:%S')}",
                "embeds": [{
                    "title": "Monitoraggio Aether",
                    "description": "Sistema funzionante dopo le correzioni",
                    "color": 0x00ff00
                }]
            }
            response = requests.post(webhook_url, json=test_message, timeout=10)
            if response.status_code == 204:
                print("✅ Discord webhook funzionante")
            else:
                print(f"⚠️ Discord webhook errore: {response.status_code}")
        else:
            print("❌ Discord webhook non configurato")
    except Exception as e:
        print(f"❌ Errore test Discord: {e}")

def main():
    """Funzione principale di monitoraggio"""
    print("🔧 MONITOR AETHER FIXED")
    print("=" * 50)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Verifiche
    check_server_status()
    check_recent_logs()
    check_thoughts_file()
    check_audio_files()
    check_discord_webhook()
    
    print("=" * 50)
    print("✅ Monitoraggio completato")
    print("🔄 Esegui questo script ogni minuto per monitorare Aether")
    print("🛑 Premi Ctrl+C per fermare")

if __name__ == "__main__":
    main() 