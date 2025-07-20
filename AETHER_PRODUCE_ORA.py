#!/usr/bin/env python3
"""
FORZA AETHER A PRODURRE CODICE REALE - BASTA FILOSOFIA!
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Configura Discord
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

print("""
╔══════════════════════════════════════════════════════════════╗
║      🔨 AETHER: BASTA FILOSOFIA, ORA PRODUCI! 🔨            ║
╚══════════════════════════════════════════════════════════════╝
""")

from aether.action_executor import AetherActionExecutor
from aether.discord_notifier import send_discord_message

executor = AetherActionExecutor()

# Lista di cose CONCRETE da creare
tasks = [
    {
        "type": "agent",
        "name": "DataWizard",
        "purpose": "Analista dati AI che genera report e visualizzazioni automatiche"
    },
    {
        "type": "room",
        "name": "CyberSpace",
        "details": "Stanza cyberpunk con neon, griglia digitale, particelle luminose"
    },
    {
        "type": "tool",
        "name": "SEO_Master",
        "purpose": "Tool AI per ottimizzazione SEO e generazione contenuti",
        "pricing": "$99/month"
    },
    {
        "type": "agent", 
        "name": "CodeHelper",
        "purpose": "Assistente programmazione che suggerisce codice e fix bug"
    },
    {
        "type": "room",
        "name": "Zen_Garden",
        "details": "Giardino zen minimalista con acqua, pietre, bambù animati"
    }
]

results = []

for i, task in enumerate(tasks, 1):
    print(f"\n{'='*60}")
    print(f"📋 TASK {i}/{len(tasks)}: {task['type'].upper()} - {task.get('name', 'Unknown')}")
    print(f"{'='*60}")
    
    try:
        if task['type'] == 'agent':
            print(f"🤖 Creo agente: {task['name']}...")
            result = executor.create_agent({
                "name": task['name'],
                "purpose": task['purpose']
            })
            
        elif task['type'] == 'room':
            print(f"🏠 Creo stanza 3D: {task['name']}...")
            result = executor.generate_react_room(task['details'])
            
        elif task['type'] == 'tool':
            print(f"💰 Creo tool monetizzabile: {task['name']}...")
            result = executor.generate_tool_for_monetization({
                "name": task['name'],
                "purpose": task['purpose']
            })
        
        print(f"✅ SUCCESSO: {result}")
        results.append({"task": task, "result": result, "success": True})
        
        # Notifica Discord
        send_discord_message(f"✅ Creato: {task['type']} - {task.get('name', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ ERRORE: {e}")
        results.append({"task": task, "result": str(e), "success": False})

# Riepilogo finale
print("\n" + "="*60)
print("📊 RIEPILOGO PRODUZIONE:")
print("="*60)

success_count = sum(1 for r in results if r['success'])
fail_count = len(results) - success_count

print(f"✅ Successi: {success_count}/{len(results)}")
print(f"❌ Fallimenti: {fail_count}/{len(results)}")

# Salva log
log_file = Path("data/production_log.json")
log_file.parent.mkdir(exist_ok=True)

log_data = {
    "timestamp": datetime.now().isoformat(),
    "results": results,
    "summary": {
        "total": len(results),
        "success": success_count,
        "failed": fail_count
    }
}

with open(log_file, 'w') as f:
    json.dump(log_data, f, indent=2)

print(f"\n📝 Log salvato in: {log_file}")

# Messaggio finale
if success_count > 0:
    print("\n🎉 AETHER HA PRODOTTO CODICE REALE!")
    send_discord_message(f"🎉 Produzione completata: {success_count} creazioni realizzate!")
else:
    print("\n😔 Aether non è riuscito a produrre...")
    
print("\n💡 Suggerimento: Controlla le cartelle:")
print("   - agents/")
print("   - aether-frontend/src/components/rooms/")
print("   - creations/monetization/") 