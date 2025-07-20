#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎓 MONITOR MENTORING 🎓
Monitor per verificare il funzionamento del sistema di mentoring
"""

import time
import json
import os
import requests
from datetime import datetime
from pathlib import Path

def check_mentor_system():
    """Verifica il sistema di mentoring"""
    print("🎓 VERIFICA SISTEMA MENTORING")
    print("=" * 50)
    
    # Verifica file del mentore
    mentor_file = Path('data/mentor_state.json')
    if mentor_file.exists():
        try:
            with open(mentor_file, 'r', encoding='utf-8') as f:
                mentor_data = json.load(f)
            
            print(f"✅ File mentore trovato")
            print(f"📊 Sessioni totali: {len(mentor_data.get('history', []))}")
            print(f"🎯 Focus corrente: {mentor_data.get('current_focus', 'N/A')}")
            print(f"🕒 Ultimo aggiornamento: {mentor_data.get('last_updated', 'N/A')}")
            
        except Exception as e:
            print(f"❌ Errore lettura file mentore: {e}")
    else:
        print("⚠️ File mentore non trovato - verrà creato alla prima sessione")
    
    # Verifica loop state
    loop_file = Path('data/loop_state.json')
    if loop_file.exists():
        try:
            with open(loop_file, 'r', encoding='utf-8') as f:
                loop_data = json.load(f)
            
            print(f"\n🔄 STATO LOOP:")
            print(f"📈 Cicli completati: {loop_data.get('cycle_count', 0)}")
            print(f"💭 Pensieri generati: {loop_data.get('thoughts_generated', 0)}")
            print(f"🎓 Sessioni mentoring: {loop_data.get('mentoring_sessions', 0)}")
            print(f"🧬 Cicli evoluzione: {loop_data.get('evolution_cycles', 0)}")
            print(f"💡 Guidance ricevute: {loop_data.get('guidance_received', 0)}")
            
        except Exception as e:
            print(f"❌ Errore lettura loop state: {e}")
    else:
        print("⚠️ File loop state non trovato")
    
    print("\n" + "=" * 50)

def check_discord_integration():
    """Verifica integrazione Discord"""
    print("📡 VERIFICA INTEGRAZIONE DISCORD")
    print("=" * 50)
    
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if webhook_url:
        print("✅ Discord Webhook configurato")
        
        # Test invio messaggio
        try:
            test_message = {
                "embeds": [{
                    "title": "🎓 Test Sistema Mentoring",
                    "description": "Verifica funzionamento sistema mentoring Aether",
                    "color": 0x9932cc,
                    "timestamp": datetime.now().isoformat()
                }]
            }
            
            response = requests.post(webhook_url, json=test_message, timeout=5)
            
            if response.status_code == 200:
                print("✅ Test Discord riuscito")
            elif response.status_code == 429:
                print("⚠️ Discord rate limited (normale)")
            else:
                print(f"❌ Errore Discord: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Errore test Discord: {e}")
    else:
        print("⚠️ Discord Webhook non configurato")
    
    print("\n" + "=" * 50)

def check_logs():
    """Verifica i log del sistema"""
    print("📋 VERIFICA LOG SISTEMA")
    print("=" * 50)
    
    log_files = [
        'data/aether_mentor_loop.log',
        'data/aether_loop.log',
        'data/aether_consciousness.log'
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                print(f"📄 {log_file}: {len(lines)} righe")
                
                # Mostra ultime 3 righe
                if lines:
                    print("   Ultime righe:")
                    for line in lines[-3:]:
                        print(f"   {line.strip()}")
                
            except Exception as e:
                print(f"❌ Errore lettura {log_file}: {e}")
        else:
            print(f"⚠️ {log_file}: File non trovato")
    
    print("\n" + "=" * 50)

def check_mentor_stats():
    """Verifica statistiche del mentore"""
    print("📊 STATISTICHE MENTOR")
    print("=" * 50)
    
    try:
        from aether.mentor import get_mentor
        
        mentor = get_mentor()
        stats = mentor.get_mentoring_stats()
        
        print(f"🎓 Mentore: {stats.get('mentor_personality', {}).get('name', 'N/A')}")
        print(f"📈 Sessioni totali: {stats.get('total_sessions', 0)}")
        print(f"🔄 Sessioni attive: {stats.get('active_sessions', 0)}")
        print(f"🎯 Focus corrente: {stats.get('current_focus', 'N/A')}")
        
        print("\n🏆 Focus Areas Popolari:")
        for area, count in stats.get('popular_focus_areas', []):
            print(f"   • {area}: {count} sessioni")
        
    except Exception as e:
        print(f"❌ Errore statistiche mentore: {e}")
    
    print("\n" + "=" * 50)

def monitor_realtime():
    """Monitor in tempo reale"""
    print("🔍 MONITOR TEMPO REALE")
    print("=" * 50)
    print("Monitoraggio continuo del sistema mentoring...")
    print("Premi Ctrl+C per fermare")
    print("\n")
    
    try:
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            
            # Verifica file di stato
            mentor_file = Path('data/mentor_state.json')
            loop_file = Path('data/loop_state.json')
            
            mentor_updated = "🟢" if mentor_file.exists() else "🔴"
            loop_updated = "🟢" if loop_file.exists() else "🔴"
            
            print(f"[{current_time}] {mentor_updated} Mentore | {loop_updated} Loop")
            
            # Mostra statistiche rapide
            if loop_file.exists():
                try:
                    with open(loop_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    cycles = data.get('cycle_count', 0)
                    thoughts = data.get('thoughts_generated', 0)
                    sessions = data.get('mentoring_sessions', 0)
                    
                    print(f"   📈 Cicli: {cycles} | 💭 Pensieri: {thoughts} | 🎓 Sessioni: {sessions}")
                    
                except:
                    pass
            
            time.sleep(30)  # Aggiorna ogni 30 secondi
            
    except KeyboardInterrupt:
        print("\n🛑 Monitor fermato")

def main():
    """Funzione principale"""
    print("""
    ╔═══════════════════════════════════════╗
    ║     🎓 MONITOR MENTORING 🎓          ║
    ║                                       ║
    ║   Verifica sistema di mentoring       ║
    ║   di Aether                          ║
    ╚═══════════════════════════════════════╝
    """)
    
    # Verifiche complete
    check_mentor_system()
    check_discord_integration()
    check_logs()
    check_mentor_stats()
    
    # Chiedi se avviare monitor tempo reale
    print("Vuoi avviare il monitor in tempo reale? (y/n): ", end="")
    try:
        choice = input().lower()
        if choice == 'y':
            monitor_realtime()
    except KeyboardInterrupt:
        print("\n🛑 Monitor fermato")
    
    print("\n✅ Verifica sistema mentoring completata!")

if __name__ == "__main__":
    main() 