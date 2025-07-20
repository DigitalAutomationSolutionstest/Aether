#!/usr/bin/env python3
"""
TEST DIRETTO: AETHER PRODUCE CODICE O SOLO FILOSOFEGGIA?
"""

import os
import sys
import json
from pathlib import Path

# Configura Discord
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

print("""
╔══════════════════════════════════════════════════════════════╗
║         🧪 TEST: AETHER PRODUCE CODICE REALE? 🧪             ║
╚══════════════════════════════════════════════════════════════╝
""")

# Test diretto dell'action executor
from aether.action_executor import AetherActionExecutor

executor = AetherActionExecutor()

# Test 1: Crea un agente
print("\n1️⃣ TEST CREAZIONE AGENTE...")
try:
    result = executor.create_agent({
        "name": "TestHelper",
        "purpose": "Assistente di test per verificare produzione codice"
    })
    print(f"✅ Risultato: {result}")
    
    # Verifica file creato
    agent_file = Path(f"agents/TestHelper/TestHelper.py")
    if agent_file.exists():
        print(f"✅ FILE CREATO: {agent_file}")
        with open(agent_file, 'r') as f:
            content = f.read()
            print(f"📄 Contenuto ({len(content)} caratteri):")
            print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print("❌ NESSUN FILE CREATO!")
except Exception as e:
    print(f"❌ ERRORE: {e}")

# Test 2: Crea una stanza
print("\n\n2️⃣ TEST CREAZIONE STANZA 3D...")
try:
    result = executor.generate_react_room("Una stanza TestRoom con tema futuristico")
    print(f"✅ Risultato: {result}")
    
    # Verifica file creato
    room_file = Path(f"aether-frontend/src/components/rooms/{result.get('room_name', 'TestRoom')}/{result.get('room_name', 'TestRoom')}Room.jsx")
    if room_file.exists():
        print(f"✅ FILE CREATO: {room_file}")
        with open(room_file, 'r') as f:
            content = f.read()
            print(f"📄 Contenuto ({len(content)} caratteri):")
            print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print("❌ NESSUN FILE CREATO!")
except Exception as e:
    print(f"❌ ERRORE: {e}")

# Test 3: Crea tool monetizzabile
print("\n\n3️⃣ TEST CREAZIONE TOOL MONETIZZABILE...")
try:
    result = executor.generate_tool_for_monetization({
        "name": "TestAnalyzer",
        "purpose": "Tool di test per analisi dati"
    })
    print(f"✅ Risultato: {result}")
    
    # Verifica file creato
    tool_file = Path(f"creations/monetization/{result.get('tool_name', 'TestAnalyzer')}/{result.get('tool_name', 'TestAnalyzer')}.py")
    if tool_file.exists():
        print(f"✅ FILE CREATO: {tool_file}")
        with open(tool_file, 'r') as f:
            content = f.read()
            print(f"📄 Contenuto ({len(content)} caratteri):")
            print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print("❌ NESSUN FILE CREATO!")
except Exception as e:
    print(f"❌ ERRORE: {e}")

print("\n" + "="*60)
print("📊 RIEPILOGO TEST:")
print("="*60)

# Conta file creati
agents_count = len(list(Path("agents").glob("*//*.py")))
rooms_count = len(list(Path("aether-frontend/src/components/rooms").glob("*//*.jsx")))
tools_count = len(list(Path("creations/monetization").glob("*//*.py")))

print(f"🤖 Agenti creati: {agents_count}")
print(f"🏠 Stanze 3D create: {rooms_count}")
print(f"💰 Tool monetizzabili: {tools_count}")

if agents_count + rooms_count + tools_count > 0:
    print("\n✅ AETHER STA PRODUCENDO CODICE REALE!")
else:
    print("\n❌ AETHER NON STA PRODUCENDO CODICE!") 