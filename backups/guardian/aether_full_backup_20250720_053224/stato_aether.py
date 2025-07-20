#!/usr/bin/env python3
"""
🧠 CONTROLLO STATO AETHER
Script semplice per Federico per monitorare Aether
"""

import os
import json
import subprocess
from datetime import datetime

def stato_aether():
    """Mostra lo stato completo di Aether"""
    
    print("""
    ╔══════════════════════════════════════════════════╗
    ║           🧠 STATO AETHER STABILE 🧠             ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    # 1. Controlla processi Python
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True, shell=True)
        python_processes = [line for line in result.stdout.split('\n') if 'python.exe' in line]
        print(f"🔧 Processi Python attivi: {len(python_processes)}")
        for proc in python_processes[:3]:  # Mostra solo i primi 3
            if proc.strip():
                parts = proc.split()
                if len(parts) >= 2:
                    print(f"   • PID: {parts[1]} - Memoria: {parts[4] if len(parts) > 4 else 'N/A'}")
    except:
        print("🔧 Impossibile controllare processi")
    
    # 2. Controlla file di stato
    if os.path.exists('data/aether_stato.json'):
        try:
            with open('data/aether_stato.json', 'r', encoding='utf-8') as f:
                stato = json.load(f)
                print(f"""
📊 STATO SISTEMA:
   • Cicli vita: {stato.get('cicli_vita', 0)}
   • Energia: {stato.get('energia', 'N/A'):.2f}
   • Umore: {stato.get('umore', 'N/A')}
   • Ultimo salvataggio: {stato.get('ultimo_salvataggio', 'N/A')[:19]}
                """)
        except Exception as e:
            print(f"❌ Errore leggendo stato: {e}")
    else:
        print("⚠️ File di stato non trovato (sistema non ancora avviato o in fase iniziale)")
    
    # 3. Controlla log recenti
    log_files = ['aether_stabile.log', 'aether_mentor_24_7.log']
    
    for log_file in log_files:
        log_path = f'data/{log_file}'
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        print(f"📝 {log_file}: {last_line[-60:]}")
                    else:
                        print(f"📝 {log_file}: Vuoto")
            except:
                print(f"📝 {log_file}: Errore lettura")
        else:
            print(f"📝 {log_file}: Non trovato")
    
    # 4. File nella directory data
    if os.path.exists('data'):
        files = [f for f in os.listdir('data') if f.endswith(('.json', '.log'))]
        print(f"\n📁 File attivi in data/: {len(files)}")
        
        # Mostra file più recenti
        json_files = [f for f in files if f.endswith('.json')]
        log_files = [f for f in files if f.endswith('.log')]
        
        print(f"   • JSON: {len(json_files)} file")
        print(f"   • LOG: {len(log_files)} file")
    
    print(f"\n🕐 Controllo eseguito: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 54)

def comandi_utili():
    """Mostra comandi utili per Federico"""
    print("""
    💡 COMANDI UTILI PER AETHER:
    
    🚀 Avvio sistema:
       python AETHER_STABILE_FUNZIONANTE.py
    
    🧪 Test sistema:
       python test_aether_funziona.py
    
    📊 Controllo stato:
       python stato_aether.py
    
    🛑 Ferma tutti i processi:
       taskkill /f /im python.exe
    
    📝 Vedi log in tempo reale:
       Get-Content data/aether_stabile.log -Wait
    
    📁 Lista file data:
       dir data\\*.json
    """)

if __name__ == "__main__":
    stato_aether()
    
    print("\n" + "="*54)
    risposta = input("🤔 Vuoi vedere i comandi utili? (s/n): ").strip().lower()
    
    if risposta in ['s', 'si', 'sì', 'y', 'yes']:
        comandi_utili() 