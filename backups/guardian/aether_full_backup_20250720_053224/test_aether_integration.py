#!/usr/bin/env python3
"""
Test dell'integrazione Aether + Supabase
Verifica che tutti i sistemi funzionino prima dell'avvio completo
"""

import asyncio
import sys
from datetime import datetime

def test_imports():
    """Test che tutti gli import funzionino"""
    print("🔍 Testing imports...")
    
    try:
        # Test import Supabase
        from config.supabase_config import get_supabase_client, validate_config
        print("✅ Supabase config imports OK")
        
        # Test import Aether brain
        from aether.brain.startup import on_startup, get_economic_consciousness_status
        from aether.brain.memory import save_memory, load_memory
        print("✅ Aether brain imports OK")
        
        # Test import core
        from core.consciousness_cycle import consciousness_cycle
        from core.reflection_engine import reflect
        print("✅ Core modules imports OK")
        
        # Test import main
        from main import AetherSystem
        print("✅ Main system imports OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_supabase_connection():
    """Test connessione Supabase"""
    print("\n🗄️ Testing Supabase connection...")
    
    try:
        from config.supabase_config import get_supabase_client, validate_config
        
        # Valida configurazione
        if not validate_config():
            print("❌ Supabase configuration invalid")
            return False
        
        # Test connessione
        supabase = get_supabase_client()
        if not supabase:
            print("❌ Could not create Supabase client")
            return False
        
        # Test inserimento dati
        test_data = {
            'type': 'integration_test',
            'content': f'Integration test at {datetime.now().isoformat()}',
            'context': {'test': True, 'system': 'aether'}
        }
        
        result = supabase.table('aether_thoughts').insert(test_data).execute()
        if result.data:
            print("✅ Supabase connection and data insertion OK")
            
            # Test lettura dati
            read_result = supabase.table('aether_thoughts').select('*').eq('type', 'integration_test').execute()
            if read_result.data:
                print("✅ Supabase data reading OK")
                return True
        
        print("❌ Supabase data operations failed")
        return False
        
    except Exception as e:
        print(f"❌ Supabase test failed: {e}")
        return False

def test_aether_brain():
    """Test moduli brain di Aether"""
    print("\n🧠 Testing Aether brain modules...")
    
    try:
        from aether.brain.startup import get_economic_consciousness_status
        from aether.brain.memory import save_memory, load_memory
        
        # Test stato coscienza economica
        status = get_economic_consciousness_status()
        print(f"✅ Economic consciousness status: {status.get('status', 'unknown')}")
        
        # Test memoria locale
        test_memory = {"test": "integration_test", "timestamp": datetime.now().isoformat()}
        save_result = save_memory("integration_test", test_memory)
        
        if save_result:
            load_result = load_memory("integration_test")
            if load_result and load_result.get("data", {}).get("test") == "integration_test":
                print("✅ Aether memory system OK")
                return True
        
        print("❌ Aether memory test failed")
        return False
        
    except Exception as e:
        print(f"❌ Aether brain test failed: {e}")
        return False

def test_core_systems():
    """Test sistemi core"""
    print("\n⚙️ Testing core systems...")
    
    try:
        from core.consciousness_cycle import consciousness_cycle
        from core.reflection_engine import reflect
        from core.self_modification import load_current_identity
        
        # Test caricamento identità
        identity = load_current_identity()
        if identity:
            print(f"✅ Identity loaded: {identity.get('name', 'Unknown')}")
        
        # Test stato ciclo coscienza
        cycle_status = consciousness_cycle.get_cycle_status()
        print(f"✅ Consciousness cycle status: {cycle_status.get('is_running', False)}")
        
        # Test riflessione
        reflection_result = reflect()
        if reflection_result:
            print("✅ Reflection system OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Core systems test failed: {e}")
        return False

async def test_main_system():
    """Test sistema principale"""
    print("\n🚀 Testing main system...")
    
    try:
        from main import AetherSystem
        
        # Crea istanza sistema
        aether = AetherSystem()
        print("✅ AetherSystem instance created")
        
        # Test inizializzazione (senza avviare loop)
        print("🔧 Testing initialization components...")
        
        # Test configurazione Supabase nel sistema
        if hasattr(aether, 'system_status'):
            print("✅ System status structure OK")
        
        if hasattr(aether, 'evolution_engine'):
            print("✅ Evolution engine initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Main system test failed: {e}")
        return False

async def run_integration_test():
    """Esegue test completo di integrazione"""
    print("🧪 AETHER + SUPABASE INTEGRATION TEST")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Supabase Connection", test_supabase_connection),
        ("Aether Brain", test_aether_brain),
        ("Core Systems", test_core_systems),
        ("Main System", test_main_system),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Risultati finali
    print("\n📊 TEST RESULTS")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Aether + Supabase integration is ready")
        print("\n🚀 You can now run: python main.py")
        return True
    else:
        print(f"\n⚠️ {total - passed} tests failed")
        print("❌ Please fix issues before running main.py")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(run_integration_test())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite crashed: {e}")
        sys.exit(1) 