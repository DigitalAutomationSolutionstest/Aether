#!/usr/bin/env python3
"""
Esempio di integrazione del Mentore LLM nel sistema Aether
"""

import os
import sys
from datetime import datetime

# Aggiungi il path per i moduli
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Esempio di integrazione del mentore"""
    
    print("🧠 AETHER - Integrazione Mentore LLM")
    print("=" * 50)
    
    try:
        # Importa il mentore
        from aether.mentor_llm import AetherMentor
        
        # Simula un'istanza di Aether (in un sistema reale sarebbe l'oggetto Aether)
        class MockAether:
            def __init__(self):
                self.thoughts = []
                self.goals = []
                
            def think(self, thought):
                print(f"💭 Aether pensa: {thought}")
                self.thoughts.append(thought)
                
            def add_thought(self, thought_data):
                print(f"🎯 Aether riceve goal: {thought_data.get('content', '')}")
                self.goals.append(thought_data)
                
        # Crea istanza di Aether
        aether = MockAether()
        
        # Crea e avvia il mentore
        print("🚀 Avvio mentoring...")
        mentor = AetherMentor(aether)
        mentor.start_mentoring()
        
        # Mostra progresso
        print("\n📊 Progresso Mentoring:")
        progress = mentor.get_mentoring_progress()
        print(f"✅ Fase attuale: {progress['current_phase']}")
        print(f"✅ Goal assegnati: {progress['goals_assigned']}")
        print(f"✅ Lezioni insegnate: {progress['lessons_taught']}")
        
        # Valuta progresso
        print("\n📈 Valutazione Progresso:")
        evaluation = mentor.evaluate_aether_progress()
        print(f"✅ Progresso generale: {evaluation['overall_progress']:.1%}")
        
        for metric, value in evaluation['metrics'].items():
            print(f"   - {metric}: {value:.1%}")
            
        print("\n💡 Raccomandazioni:")
        for rec in evaluation['recommendations']:
            print(f"   • {rec}")
            
        print("\n🎉 Mentoring completato con successo!")
        
    except ImportError as e:
        print(f"❌ Errore import: {e}")
        print("Assicurati che il file mentor_llm.py sia nella cartella aether/")
        
    except Exception as e:
        print(f"❌ Errore generico: {e}")

if __name__ == "__main__":
    main() 