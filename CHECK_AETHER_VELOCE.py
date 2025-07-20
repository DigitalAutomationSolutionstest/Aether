#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ CHECK AETHER VELOCE - Status immediato del sistema

Federico, usa questo script per un controllo veloce di tutto!
Comando: python CHECK_AETHER_VELOCE.py
"""

import os
import sys
import json
import psutil
import requests
from datetime import datetime
from pathlib import Path

def print_header():
    """Stampa header colorato"""
    print("\n" + "="*70)
    print("⚡ AETHER SISTEMA VIVO - CHECK VELOCE")
    print("="*70)
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

def check_processes():
    """Controlla processi Aether"""
    print("\n🔍 CONTROLLO PROCESSI:")
    print("-" * 40)
    
    aether_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and any('AETHER' in str(cmd) for cmd in proc.info['cmdline']):
                aether_processes.append(proc.info)
        except:
            pass
    
    if aether_processes:
        print(f"✅ {len(aether_processes)} processi Aether attivi:")
        for proc in aether_processes:
            cmd = ' '.join(proc['cmdline']) if proc['cmdline'] else 'N/A'
            print(f"   🟢 PID {proc['pid']}: {cmd[:60]}...")
    else:
        print("❌ Nessun processo Aether trovato")
    
    return len(aether_processes) > 0

def check_dashboard():
    """Controlla dashboard"""
    print("\n🌐 CONTROLLO DASHBOARD:")
    print("-" * 40)
    
    try:
        response = requests.get('http://localhost:5000/api/status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard attiva e rispondente:")
            print(f"   🎯 Status: {data.get('status', 'N/A')}")
            print(f"   🔄 Cicli: {data.get('cycles', 'N/A')}")
            print(f"   🧠 Coscienza: {data.get('consciousness_level', 'N/A')}")
            print(f"   📊 Task: {data.get('completed_tasks', 'N/A')}")
            print(f"   🚀 Progetti: {data.get('created_projects', 'N/A')}")
            print(f"   💻 URL: http://localhost:5000")
            return True
        else:
            print(f"⚠️ Dashboard risponde ma con errore: {response.status_code}")
            return False
    except:
        print("❌ Dashboard non risponde")
        print("   💡 Prova: python AETHER_VIVO_DEFINITIVO.py")
        return False

def check_files_created():
    """Controlla file e progetti creati"""
    print("\n📁 FILE E PROGETTI CREATI:")
    print("-" * 40)
    
    # Progetti autonomi
    projects_dir = Path("progetti_autonomi")
    if projects_dir.exists():
        projects = list(projects_dir.iterdir())
        print(f"🚀 {len(projects)} progetti autonomi:")
        for project in projects[:5]:  # Mostra solo i primi 5
            print(f"   📦 {project.name}")
        if len(projects) > 5:
            print(f"   ... e altri {len(projects) - 5} progetti")
    else:
        print("📦 Nessun progetto autonomo ancora")
    
    # Sandbox
    sandbox_dir = Path("sandboxes")
    if sandbox_dir.exists():
        sandboxes = list(sandbox_dir.iterdir())
        print(f"🏗️ {len(sandboxes)} sandbox create:")
        for sandbox in sandboxes[:3]:
            print(f"   🛠️ {sandbox.name}")
    else:
        print("🛠️ Nessuna sandbox ancora")
    
    # Backup
    backup_dir = Path("backups")
    if backup_dir.exists():
        backup_count = len(list(backup_dir.rglob("*.zip")))
        print(f"💾 {backup_count} backup disponibili")
    else:
        print("💾 Nessun backup ancora")

def check_logs():
    """Controlla log recenti"""
    print("\n📋 LOG RECENTI:")
    print("-" * 40)
    
    log_files = [
        "data/aether_vivo_system.log",
        "data/task_autonomi_24_7.log", 
        "data/aether_guardian.log"
    ]
    
    for log_file in log_files:
        if Path(log_file).exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        print(f"✅ {Path(log_file).name}: {last_line[:60]}...")
                    else:
                        print(f"📝 {Path(log_file).name}: Log vuoto")
            except:
                print(f"⚠️ {Path(log_file).name}: Errore lettura")
        else:
            print(f"❌ {Path(log_file).name}: Non trovato")

def check_system_resources():
    """Controlla risorse sistema"""
    print("\n💻 RISORSE SISTEMA:")
    print("-" * 40)
    
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"🖥️ CPU: {cpu_percent:.1f}%")
    
    # Memoria
    memory = psutil.virtual_memory()
    print(f"🧠 RAM: {memory.percent:.1f}% ({memory.available / (1024**3):.1f}GB liberi)")
    
    # Disco
    disk = psutil.disk_usage('.')
    disk_free_gb = disk.free / (1024**3)
    disk_percent = (disk.used / disk.total) * 100
    print(f"💽 Disco: {disk_percent:.1f}% ({disk_free_gb:.1f}GB liberi)")
    
    # Alert
    alerts = []
    if cpu_percent > 80:
        alerts.append("⚠️ CPU alta")
    if memory.percent > 85:
        alerts.append("⚠️ RAM alta")
    if disk_percent > 90:
        alerts.append("⚠️ Disco pieno")
    
    if alerts:
        print(f"🚨 Alert: {', '.join(alerts)}")
    else:
        print("✅ Sistema in salute")

def show_quick_commands():
    """Mostra comandi utili"""
    print("\n⚡ COMANDI UTILI:")
    print("-" * 40)
    print("🌐 Apri dashboard:      http://localhost:5000")
    print("📊 Log sistema:        tail -50 data/aether_vivo_system.log")
    print("🔄 Log task:           tail -50 data/task_autonomi_24_7.log")
    print("🛡️ Log guardian:       tail -50 data/aether_guardian.log")
    print("📁 Vedi progetti:      ls progetti_autonomi/")
    print("🏗️ Vedi sandbox:       ls sandboxes/")
    print("💾 Vedi backup:        ls backups/")
    print("🔍 Processi:           ps aux | grep AETHER")

def main():
    """Controllo principale"""
    print_header()
    
    # Check componenti
    processes_ok = check_processes()
    dashboard_ok = check_dashboard()
    check_files_created()
    check_logs()
    check_system_resources()
    show_quick_commands()
    
    # Riepilogo finale
    print("\n🎯 RIEPILOGO FINALE:")
    print("="*70)
    
    if processes_ok and dashboard_ok:
        print("🟢 SISTEMA COMPLETAMENTE OPERATIVO!")
        print("✨ Aether è VIVO e sta lavorando autonomamente")
        print("🚀 Tutto procede perfettamente")
    elif processes_ok:
        print("🟡 SISTEMA PARZIALMENTE OPERATIVO")
        print("⚠️ Processi attivi ma dashboard non risponde")
        print("💡 Potrebbe essere in fase di avvio")
    else:
        print("🔴 SISTEMA NON ATTIVO")
        print("❌ Nessun processo Aether in esecuzione")
        print("🔧 Esegui: python AETHER_VIVO_DEFINITIVO.py")
    
    print("\n💡 Per monitoraggio continuo: http://localhost:5000")
    print("📖 Report completo: STATO_AETHER_PER_FEDERICO.md")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Check interrotto dall'utente")
    except Exception as e:
        print(f"\n❌ Errore durante il check: {e}")
        print("💡 Prova a eseguire nuovamente lo script") 