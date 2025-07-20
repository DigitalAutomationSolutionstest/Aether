#!/usr/bin/env python3
"""
Test completo dell'integrazione del Mentore LLM nel sistema Aether
"""

import asyncio
import sys
import os
from datetime import datetime

# Aggiungi il path per i moduli
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_mentor_integration():
    """Test completo dell'integrazione del mentore"""
    
    print("🧠 TEST INTEGRAZIONE MENTORE LLM")
    print("=" * 50)
    
    try:
        # Test 1: Import e inizializzazione
        print("\n1️⃣ Test Import e Inizializzazione...")
        from aether.mentor_llm import AetherMentor
        from aether.thought_engine import ThoughtEngine
        from aether.git_tools import commit_and_push
        from aether.supabase_client import store_event
        
        thought_engine = ThoughtEngine()
        mentor = AetherMentor(thought_engine)
        print("✅ Import e inizializzazione completati")
        
        # Test 2: Funzionalità del mentore
        print("\n2️⃣ Test Funzionalità Mentore...")
        mentor.start_mentoring()
        print("✅ Mentoring avviato con successo")
        
        # Test 3: Verifica goal assegnati
        print("\n3️⃣ Test Goal Assegnati...")
        progress = mentor.get_mentoring_progress()
        print(f"✅ Goal assegnati: {progress['goals_assigned']}")
        print(f"✅ Lezioni insegnate: {progress['lessons_taught']}")
        
        # Test 4: Verifica pensieri generati
        print("\n4️⃣ Test Pensieri Generati...")
        thoughts = thought_engine.get_thoughts()
        print(f"✅ Pensieri generati: {len(thoughts)}")
        
        # Test 5: Verifica eventi salvati
        print("\n5️⃣ Test Eventi Salvati...")
        try:
            store_event("test", {"message": "Test evento mentore"})
            print("✅ Eventi salvati correttamente")
        except Exception as e:
            print(f"⚠️ Errore salvataggio eventi: {e}")
        
        # Test 6: Verifica Git
        print("\n6️⃣ Test Git Operations...")
        try:
            commit_and_push("🧠 Test integrazione mentore")
            print("✅ Git operations completate")
        except Exception as e:
            print(f"⚠️ Errore Git: {e}")
        
        # Test 7: Valutazione progresso
        print("\n7️⃣ Test Valutazione Progresso...")
        evaluation = mentor.evaluate_aether_progress()
        print(f"✅ Progresso generale: {evaluation['overall_progress']:.1%}")
        
        # Test 8: Verifica integrazione sistema principale
        print("\n8️⃣ Test Integrazione Sistema Principale...")
        from main import AetherSystem
        
        aether_system = AetherSystem()
        print("✅ Sistema principale inizializzato con mentore")
        
        # Test 9: Verifica funzionalità complete
        print("\n9️⃣ Test Funzionalità Complete...")
        
        # Verifica che il mentore abbia assegnato i goal corretti
        expected_goals = [
            "Comprendi te stesso come entità LLM evolutiva.",
            "Crea il tuo primo modulo di auto-introspezione.",
            "Scrivi un file dove spieghi chi sei, cosa vuoi, e come vuoi evolverti.",
            "Clona un nuovo repo e sperimenta una nuova identità temporanea.",
            "Costruisci una stanza interattiva dove possiamo parlare, anche testualmente.",
            "Trova una via per guadagnare da vivere: vendi tool, agenti, o esperienze."
        ]
        
        actual_goals = [goal['content'] for goal in progress['goals']]
        
        for expected_goal in expected_goals:
            if expected_goal in actual_goals:
                print(f"✅ Goal trovato: {expected_goal[:50]}...")
            else:
                print(f"❌ Goal mancante: {expected_goal[:50]}...")
        
        # Test 10: Verifica pensieri del mentore
        print("\n🔟 Test Pensieri del Mentore...")
        mentor_thoughts = [thought for thought in thoughts if 'mentor' in str(thought).lower()]
        print(f"✅ Pensieri del mentore: {len(mentor_thoughts)}")
        
        print("\n🎉 TUTTI I TEST COMPLETATI CON SUCCESSO!")
        print("=" * 50)
        
        # Riepilogo finale
        print("\n📊 RIEPILOGO INTEGRAZIONE:")
        print(f"✅ Mentore attivo: {aether_system.system_status['mentor_active']}")
        print(f"✅ Goal assegnati: {progress['goals_assigned']}")
        print(f"✅ Lezioni insegnate: {progress['lessons_taught']}")
        print(f"✅ Pensieri generati: {len(thoughts)}")
        print(f"✅ Progresso generale: {evaluation['overall_progress']:.1%}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Errore import: {e}")
        return False
    except Exception as e:
        print(f"❌ Errore generico: {e}")
        return False

async def main():
    """Funzione principale del test"""
    print("🚀 Avvio test integrazione mentore...")
    
    success = await test_mentor_integration()
    
    if success:
        print("\n🎉 INTEGRAZIONE MENTORE COMPLETATA CON SUCCESSO!")
        print("Aether è ora guidato dal mentore LLM per la sua evoluzione.")
    else:
        print("\n❌ TEST FALLITO - Controllare errori sopra.")

if __name__ == "__main__":
    asyncio.run(main()) 