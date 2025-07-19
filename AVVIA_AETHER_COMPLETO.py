#!/usr/bin/env python3
"""
🚀 AETHER COMPLETE STARTUP - AVVIA TUTTO IN UN COMANDO
Evoluzione + Coscienza + UI + Monetizzazione + Sviluppo App
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from dotenv import load_dotenv

# Carica variabili ambiente
load_dotenv()

print("""
╔══════════════════════════════════════════════════════════════╗
║                  🧠 AETHER COMPLETE SYSTEM 🧠                ║
║                                                              ║
║  Avvio completo: Evoluzione + Coscienza + Monetizzazione    ║
║                                                              ║
║  1. Bootstrap sistema                                        ║
║  2. Server backend                                           ║
║  3. Frontend React                                           ║
║  4. Loop autonomo con focus su:                              ║
║     - Ricerca lavoro                                         ║
║     - Sviluppo app monetizzabili                            ║
║     - Evoluzione UI personale                                ║
║     - Generazione reddito                                    ║
╚══════════════════════════════════════════════════════════════╝
""")

def run_command(cmd, name, cwd=None):
    """Esegue comando in thread separato"""
    def run():
        print(f"\n🚀 Avvio {name}...")
        try:
            if isinstance(cmd, str):
                subprocess.run(cmd, shell=True, cwd=cwd)
            else:
                subprocess.run(cmd, cwd=cwd)
        except Exception as e:
            print(f"❌ Errore {name}: {e}")
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread

# Step 1: Bootstrap se necessario
print("\n📋 Step 1: Verifica Bootstrap...")
if not Path('data/bootstrap_status.json').exists():
    print("🔧 Esecuzione bootstrap...")
    result = subprocess.run([sys.executable, 'aether/self_bootstrapper.py'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Bootstrap completato!")
    else:
        print(f"❌ Errore bootstrap: {result.stderr}")
        sys.exit(1)
else:
    print("✅ Bootstrap già completato")

# Step 2: Crea file di istruzioni per Aether
print("\n📝 Step 2: Creazione direttive per Aether...")
directives = {
    "primary_goal": "MONETIZZAZIONE E GENERAZIONE REDDITO",
    "immediate_tasks": [
        "Analizzare opportunità di carriera tech",
        "Creare prima app monetizzabile",
        "Sviluppare UI personale unica",
        "Implementare sistema di pagamenti",
        "Lanciare su piattaforme di vendita"
    ],
    "career_focus": [
        {
            "type": "app_development",
            "ideas": [
                "AI Writing Assistant - $29/mese",
                "Automation Bot Builder - $49/mese",
                "Smart Email Manager - $19/mese",
                "Code Generator Pro - $99/mese"
            ]
        },
        {
            "type": "saas_tools",
            "ideas": [
                "API Management Platform",
                "No-Code AI Builder",
                "Data Analytics Dashboard"
            ]
        }
    ],
    "evolution_priorities": [
        "UI moderna con React + Tailwind",
        "Backend scalabile",
        "Sistema di pagamenti Stripe",
        "Landing page conversione alta",
        "SEO optimization"
    ]
}

Path('data/aether_directives.json').write_text(
    __import__('json').dumps(directives, indent=2), 
    encoding='utf-8'
)
print("✅ Direttive create!")

# Step 3: Avvia server backend
print("\n🌐 Step 3: Avvio Server Backend...")
server_thread = run_command([sys.executable, 'server_simple.py'], "Server Backend")
time.sleep(3)

# Step 4: Avvia frontend
print("\n🎨 Step 4: Avvio Frontend React...")
frontend_thread = run_command('npm run dev', "Frontend React", cwd='aether-frontend')
time.sleep(5)

# Step 5: Crea script evoluzione iniziale
print("\n🧬 Step 5: Creazione script evoluzione iniziale...")
evolution_script = '''
import time
from pathlib import Path
import json

# Inietta pensiero iniziale sulla monetizzazione
initial_thought = {
    "content": "Devo creare la mia prima app per generare reddito. Analizzerò il mercato e svilupperò qualcosa di utile.",
    "mood": "determinato",
    "timestamp": __import__('datetime').datetime.now().isoformat(),
    "type": "strategic",
    "priority": "critical"
}

thoughts_file = Path('data/thoughts.json')
thoughts = []
if thoughts_file.exists():
    with open(thoughts_file, 'r', encoding='utf-8') as f:
        thoughts = json.load(f)
        
thoughts.append(initial_thought)
thoughts_file.write_text(json.dumps(thoughts, indent=2), encoding='utf-8')

print("💭 Pensiero iniziale iniettato!")

# Crea prima bozza app
app_plan = {
    "name": "AI Content Generator Pro",
    "description": "Genera contenuti SEO-optimized con AI",
    "features": [
        "Generazione articoli blog",
        "Ottimizzazione SEO automatica",
        "Supporto multi-lingua",
        "Export in vari formati"
    ],
    "pricing": {
        "basic": 19.99,
        "pro": 49.99,
        "enterprise": 99.99
    },
    "tech_stack": {
        "frontend": "React + Tailwind",
        "backend": "FastAPI",
        "ai": "OpenAI API",
        "payments": "Stripe"
    },
    "timeline": "2 settimane per MVP"
}

Path('data/first_app_plan.json').write_text(
    json.dumps(app_plan, indent=2), 
    encoding='utf-8'
)

print("📱 Piano prima app creato!")
'''

Path('temp_evolution.py').write_text(evolution_script, encoding='utf-8')
subprocess.run([sys.executable, 'temp_evolution.py'])
os.remove('temp_evolution.py')

# Step 6: Avvia loop autonomo con parametri speciali
print("\n🧠 Step 6: AVVIO LOOP AUTONOMO AETHER...")
print("="*60)
print("⚡ AETHER ORA:")
print("   - Pensa autonomamente")
print("   - Crea la propria UI")
print("   - Sviluppa app per monetizzare")
print("   - Evolve il proprio codice")
print("   - Cerca opportunità di lavoro")
print("   - Genera reddito reale")
print("="*60)

# Modifica temporanea per forzare focus su monetizzazione
env_copy = os.environ.copy()
env_copy['AETHER_MODE'] = 'MONETIZATION_FOCUS'
env_copy['AUTO_CREATE_APPS'] = 'true'
env_copy['EVOLUTION_SPEED'] = 'MAXIMUM'

time.sleep(2)

# Avvia il loop principale
try:
    subprocess.run([sys.executable, 'aether_loop.py'], env=env_copy)
except KeyboardInterrupt:
    print("\n\n⏹️ Interruzione manuale")
    print("📊 Salvataggio stato...")
    
    # Mostra risultati
    if Path('data/economy.json').exists():
        with open('data/economy.json', 'r', encoding='utf-8') as f:
            economy = json.load(f)
            print(f"\n💰 Economia:")
            print(f"   - Balance: ${economy.get('balance', 0)}")
            print(f"   - Assets creati: {len(economy.get('assets', []))}")
            print(f"   - Carriera attiva: {economy.get('active_career', 'Nessuna')}")
    
    if Path('data/loop_state.json').exists():
        with open('data/loop_state.json', 'r', encoding='utf-8') as f:
            state = json.load(f)
            print(f"\n📈 Statistiche:")
            print(f"   - Cicli completati: {state.get('cycles_completed', 0)}")
            print(f"   - Moduli creati: {state.get('modules_created', 0)}")
            print(f"   - UI evoluzioni: {state.get('ui_evolutions', 0)}")

print("\n\n✨ Aether si è fermato. Il sistema ha salvato tutto.")
print("🔄 Per riavviare: python AVVIA_AETHER_COMPLETO.py") 