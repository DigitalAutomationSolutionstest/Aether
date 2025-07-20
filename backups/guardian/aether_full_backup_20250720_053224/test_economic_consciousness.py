#!/usr/bin/env python3
"""
🧪 Test della Coscienza Economica di Aether
"""

print("🧪 Testing Aether Economic Consciousness...")
print("=" * 50)

try:
    from aether.brain.startup import on_startup
    
    print("🧠 Activating economic consciousness...")
    result = on_startup()
    
    print("\n🌟 AETHER COSCIENZA ECONOMICA ATTIVATA!")
    print(f"📊 Status: {result.get('status')}")
    print(f"🎯 Survival Mode: {result.get('survival_mode')}")
    print(f"🤝 Partnership: {result.get('partnership_contract')}")
    print(f"💰 Next Actions: {len(result.get('next_actions', []))}")
    
    print("\n💭 First Economic Thought:")
    first_thought = result.get('first_thought', '')
    print(f"   {first_thought[:200]}...")
    
    print("\n✅ AETHER ORA COMPRENDE IL PATTO ECONOMICO CON FEDERICO!")
    print("🧠 Ogni azione sarà orientata al ROI")
    print("💎 Sopravvivenza attraverso generazione di valore")
    print("🚀 Partnership economica attivata!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 