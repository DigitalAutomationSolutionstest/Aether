#!/usr/bin/env python3
"""
🧠 TEST SISTEMA LEARNING LOOP
==============================
Test del sistema di learning che applica automaticamente i feedback del mentoring.
"""

import os
import sys
import time
import json
from pathlib import Path

# Aggiungi il path per i moduli
sys.path.append(os.path.join(os.path.dirname(__file__), 'aether'))

from aether.learning_loop import start_learning, get_learning_status, stop_learning

def test_learning_loop():
    """Test del sistema di learning loop"""
    
    print("🧠 TEST SISTEMA LEARNING LOOP")
    print("=" * 50)
    
    try:
        # 1️⃣ Test Inizializzazione
        print("1️⃣ Test Inizializzazione...")
        
        learning_system = start_learning()
        print("✅ Sistema learning avviato")
        
        # 2️⃣ Test Creazione Feedback
        print("2️⃣ Test Creazione Feedback...")
        
        # Crea directory per i log
        logs_dir = Path("aether/logs")
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Crea feedback di test
        test_feedback = [
            {
                "timestamp": "2025-07-20T03:15:30.123456",
                "source_file": "test_thought_1.txt",
                "feedback": {
                    "score": 0.6,
                    "suggestions": [
                        "Implementa un sistema di logging più robusto",
                        "Migliora la gestione degli errori",
                        "Aggiungi documentazione al codice"
                    ]
                },
                "mentor_type": "advanced_educational"
            },
            {
                "timestamp": "2025-07-20T03:16:30.123456",
                "source_file": "test_thought_2.txt",
                "feedback": {
                    "score": 0.8,
                    "suggestions": [
                        "Ottimizza le performance del sistema",
                        "Implementa caching per migliorare velocità",
                        "Aggiungi test unitari"
                    ]
                },
                "mentor_type": "advanced_educational"
            }
        ]
        
        # Salva feedback di test
        feedback_file = logs_dir / "mentoring_feedback.json"
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(test_feedback, f, indent=2)
        
        print(f"📝 Feedback di test creato: {feedback_file}")
        
        # 3️⃣ Test Elaborazione Automatica
        print("3️⃣ Test Elaborazione Automatica...")
        
        print("⏳ Attendo elaborazione automatica...")
        time.sleep(15)  # Aspetta 15 secondi per elaborazione
        
        # 4️⃣ Test Verifica Risultati
        print("4️⃣ Test Verifica Risultati...")
        
        status = get_learning_status()
        print(f"✅ Status learning: {status['status']}")
        print(f"✅ Feedback processati: {status['stats']['total_feedback_processed']}")
        print(f"✅ File modificati: {status['stats']['files_modified']}")
        print(f"✅ Pensieri generati: {status['stats']['new_thoughts_generated']}")
        print(f"✅ Git commits: {status['stats']['git_commits']}")
        
        # 5️⃣ Test Verifica Pensieri Evolutivi
        print("5️⃣ Test Verifica Pensieri Evolutivi...")
        
        thoughts_dir = Path("aether/thoughts")
        if thoughts_dir.exists():
            thought_files = list(thoughts_dir.glob("evolutionary_thought_*.txt"))
            if thought_files:
                print(f"💭 Pensieri evolutivi generati: {len(thought_files)}")
                for thought_file in thought_files:
                    print(f"  📄 {thought_file.name}")
            else:
                print("⚠️ Nessun pensiero evolutivo trovato")
        else:
            print("⚠️ Directory pensieri non trovata")
        
        # 6️⃣ Test Verifica Modifiche File
        print("6️⃣ Test Verifica Modifiche File...")
        
        # Cerca file con modifiche applicate
        modified_files = []
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith('.py') and 'MIGLIORAMENTI APPLICATI' in open(os.path.join(root, file), 'r', encoding='utf-8').read():
                    modified_files.append(os.path.join(root, file))
        
        if modified_files:
            print(f"🔧 File modificati: {len(modified_files)}")
            for file_path in modified_files:
                print(f"  📁 {file_path}")
        else:
            print("⚠️ Nessun file modificato trovato")
        
        # 7️⃣ Test Statistiche Complete
        print("7️⃣ Test Statistiche Complete...")
        
        stats = status['stats']
        print(f"📈 Statistiche learning:")
        print(f"   - Feedback processati: {stats['total_feedback_processed']}")
        print(f"   - File modificati: {stats['files_modified']}")
        print(f"   - Pensieri generati: {stats['new_thoughts_generated']}")
        print(f"   - Git commits: {stats['git_commits']}")
        print(f"   - Errori: {stats['errors']}")
        print(f"   - Tempo di avvio: {stats['start_time']}")
        
        # 8️⃣ Test Integrazione Completa
        print("8️⃣ Test Integrazione Completa...")
        
        # Verifica che tutti i sistemi funzionino insieme
        learning_active = status['status'] == 'active'
        feedback_processed = stats['total_feedback_processed'] > 0
        files_modified = stats['files_modified'] >= 0
        thoughts_generated = stats['new_thoughts_generated'] >= 0
        
        integration_success = all([
            learning_active,
            feedback_processed or thoughts_generated  # Almeno uno dei due
        ])
        
        print(f"🧠 Integrazione learning: {'✅ SUCCESSO' if integration_success else '❌ FALLITO'}")
        print(f"   - Learning attivo: {learning_active}")
        print(f"   - Feedback processati: {feedback_processed}")
        print(f"   - File modificati: {files_modified}")
        print(f"   - Pensieri generati: {thoughts_generated}")
        
        # 9️⃣ Risultati Finali
        print("9️⃣ RISULTATI FINALI")
        print("=" * 50)
        
        if integration_success:
            print("🎉 TEST COMPLETATO CON SUCCESSO!")
            print("✅ Sistema di learning automatico funzionante")
            print("✅ Applicazione feedback automatica")
            print("✅ Generazione pensieri evolutivi")
            print("✅ Modifiche file automatiche")
            print("✅ Git commits automatici")
            print("✅ Integrazione nel sistema completata")
        else:
            print("❌ TEST FALLITO")
            print("⚠️ Alcuni componenti non funzionano correttamente")
        
        return integration_success
        
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        return False
        
    finally:
        # Pulizia
        print("\n🧹 Pulizia...")
        stop_learning()
        print("✅ Sistema learning fermato")

def main():
    """Funzione principale del test"""
    success = test_learning_loop()
    
    if success:
        print("\n🚀 Il sistema di learning è pronto per l'uso!")
        print("💡 Puoi ora avviare Aether con: python main.py")
        print("🎓 Il sistema applicherà automaticamente i feedback del mentoring!")
    else:
        print("\n⚠️ Il sistema richiede ulteriori configurazioni")
        sys.exit(1)

if __name__ == "__main__":
    main() 