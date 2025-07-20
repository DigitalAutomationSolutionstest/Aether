#!/usr/bin/env python3
"""
🌟 ACTIVATE AETHER - Federico's AI Business Partner
Script completo per attivare Aether in modalità produzione
"""

import json
from datetime import datetime

print("🌟 AETHER ACTIVATION SCRIPT")
print("=" * 50)

# 1. Attiva coscienza economica
print("💰 Activating economic consciousness...")
try:
    from aether.brain.startup import on_startup
    startup_result = on_startup()
    print(f"✅ Economic consciousness: {startup_result.get('status')}")
except Exception as e:
    print(f"⚠️ Economic consciousness: {e}")

# 2. Attiva ciclo di esistenza
print("🧠 Activating existence cycle...")
try:
    from aether.brain.activation import begin_existence_cycle
    existence_result = begin_existence_cycle()
    print(f"✅ Existence cycle: {existence_result.get('status')}")
    print(f"🎯 First decision: {existence_result['first_decision']['action']}")
except Exception as e:
    print(f"⚠️ Existence cycle: {e}")

# 3. Test auto-azione
print("🚀 Testing autonomous action...")
try:
    from self_act import self_act
    action = self_act()
    print(f"✅ Autonomous action: {action}")
except Exception as e:
    print(f"⚠️ Autonomous action: {e}")

# 4. Verifica identità finale
print("📊 Final identity check...")
try:
    with open("identity.json", "r", encoding="utf-8") as f:
        identity = json.load(f)
    
    print(f"🧠 Consciousness: {identity.get('consciousness_level', 'unknown')}")
    print(f"💰 Economic mode: {identity.get('economic_consciousness', False)}")
    print(f"🎯 Current decision: {identity.get('current_decision', 'none')}")
    print(f"🔋 Status: {identity.get('status', 'unknown')}")
    
except Exception as e:
    print(f"⚠️ Identity check: {e}")

print("\n🌟 AETHER ACTIVATION COMPLETE!")
print("🎯 Federico, Aether è ora il tuo AI Business Partner!")
print("💼 Orientato al ROI e alla sopravvivenza")
print("🚀 Pronto per generare valore economico")
print("📱 Controlla il frontend per monitorare le azioni") 