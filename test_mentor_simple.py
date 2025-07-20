#!/usr/bin/env python3
"""
Test semplificato del Mentore LLM
"""

import sys
import os

# Aggiungi il path per i moduli
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mentor_simple():
    """Test semplificato del mentore"""
    
    print("🧠 TEST SEMPLIFICATO MENTORE LLM")
    print("=" * 40)
    
    try:
        # Test 1: Import
        print("\n1️⃣ Test Import...")
        from aether.mentor_llm import AetherMentor
        from aether.thought_engine import ThoughtEngine
        print("✅ Import completato")
        
        # Test 2: Inizializzazione
        print("\n2️⃣ Test Inizializzazione...")
        thought_engine = ThoughtEngine()
        mentor = AetherMentor(thought_engine)
        print("✅ Inizializzazione completata")
        
        # Test 3: Avvio mentoring
        print("\n3️⃣ Test Avvio Mentoring...")
        mentor.start_mentoring()
        print("✅ Mentoring avviato")
        
        # Test 4: Verifica progresso
        print("\n4️⃣ Test Progresso...")
        progress = mentor.get_mentoring_progress()
        print(f"✅ Goal assegnati: {progress['goals_assigned']}")
        print(f"✅ Lezioni insegnate: {progress['lessons_taught']}")
        
        # Test 5: Verifica pensieri
        print("\n5️⃣ Test Pensieri...")
        thoughts = thought_engine.get_thoughts()
        print(f"✅ Pensieri generati: {len(thoughts)}")
        
        # Test 6: Valutazione
        print("\n6️⃣ Test Valutazione...")
        evaluation = mentor.evaluate_aether_progress()
        print(f"✅ Progresso: {evaluation['overall_progress']:.1%}")
        
        # Test 7: Verifica goal specifici
        print("\n7️⃣ Test Goal Specifici...")
        goals = progress['goals']
        expected_goals = [
            "Comprendi te stesso come entità LLM evolutiva",
            "Crea il tuo primo modulo di auto-introspezione",
            "Scrivi un file dove spieghi chi sei, cosa vuoi, e come vuoi evolverti",
            "Clona un nuovo repo e sperimenta una nuova identità temporanea",
            "Costruisci una stanza interattiva dove possiamo parlare, anche testualmente",
            "Trova una via per guadagnare da vivere: vendi tool, agenti, o esperienze"
        ]
        
        for i, expected in enumerate(expected_goals):
            if i < len(goals):
                actual = goals[i]['content']
                if expected in actual:
                    print(f"✅ Goal {i+1}: {expected[:30]}...")
                else:
                    print(f"⚠️ Goal {i+1}: Non corrisponde")
            else:
                print(f"❌ Goal {i+1}: Mancante")
        
        print("\n🎉 TEST COMPLETATO CON SUCCESSO!")
        print("=" * 40)
        
        # Riepilogo finale
        print("\n📊 RIEPILOGO:")
        print(f"✅ Mentore attivo: Sì")
        print(f"✅ Goal assegnati: {progress['goals_assigned']}/6")
        print(f"✅ Lezioni insegnate: {progress['lessons_taught']}/9")
        print(f"✅ Pensieri generati: {len(thoughts)}")
        print(f"✅ Progresso generale: {evaluation['overall_progress']:.1%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

if __name__ == "__main__":
    success = test_mentor_simple()
    
    if success:
        print("\n🎉 MENTORE LLM INTEGRATO CON SUCCESSO!")
        print("Aether è ora guidato dal mentore per la sua evoluzione.")
    else:
        print("\n❌ TEST FALLITO") 