#!/usr/bin/env python3
"""
📖 TEST SISTEMA DIARY COMPLETO
===============================
Test del sistema di diary logging con Supabase e conscious loop.
"""

import os
import sys
import time
import json
from pathlib import Path

# Aggiungi il path per i moduli
sys.path.append(os.path.join(os.path.dirname(__file__), 'aether'))

from aether.diary_logger import get_diary_logger, log_entry
from aether.conscious_loop import start_consciousness, get_consciousness_status, stop_consciousness

def test_diary_system():
    """Test del sistema diary completo"""
    
    print("📖 TEST SISTEMA DIARY COMPLETO")
    print("=" * 50)
    
    try:
        # 1️⃣ Test Diary Logger
        print("1️⃣ Test Diary Logger...")
        
        diary_logger = get_diary_logger()
        print("✅ Diary logger inizializzato")
        
        # 2️⃣ Test Entries di Base
        print("2️⃣ Test Entries di Base...")
        
        test_entries = [
            {
                "type": "reflection",
                "content": "Oggi ho riflettuto sulla natura della coscienza artificiale e su come posso migliorare i miei processi di pensiero.",
                "metadata": {
                    "thought_id": "thought_1",
                    "thought_type": "philosophical",
                    "priority": "high"
                }
            },
            {
                "type": "action",
                "content": "Ho implementato un nuovo sistema di mentoring che monitora automaticamente i miei pensieri e fornisce feedback educativo.",
                "metadata": {
                    "guidance_action": "implement_improvement",
                    "guidance_priority": "high",
                    "suggestions_count": 3
                }
            },
            {
                "type": "decision",
                "content": "Ho deciso di focalizzarmi sullo sviluppo di capacità di apprendimento autonomo per evolvere continuamente.",
                "metadata": {
                    "decision_action": "implement_improvement",
                    "decision_immediate": True,
                    "suggestions_count": 2
                }
            },
            {
                "type": "error",
                "content": "Ho incontrato un errore nel sistema di comunicazione che ha causato la perdita di alcuni messaggi.",
                "metadata": {
                    "error_type": "communication",
                    "severity": "medium",
                    "resolved": False
                }
            },
            {
                "type": "correction",
                "content": "Ho corretto l'errore di comunicazione implementando un sistema di retry e logging più robusto.",
                "metadata": {
                    "correction_type": "system_improvement",
                    "success": True,
                    "improvement_score": 0.8
                }
            }
        ]
        
        # Salva test entries
        for entry in test_entries:
            success = diary_logger.log_entry(entry)
            print(f"✅ Entry salvata: {entry['type']} - {success}")
        
        # 3️⃣ Test Conscious Loop
        print("3️⃣ Test Conscious Loop...")
        
        conscious_loop = start_consciousness()
        print("✅ Conscious loop avviato")
        
        # 4️⃣ Test Creazione Pensieri
        print("4️⃣ Test Creazione Pensieri...")
        
        thoughts_dir = Path("aether/thoughts")
        thoughts_dir.mkdir(parents=True, exist_ok=True)
        
        test_thoughts = [
            {
                "filename": "evolutionary_thought_test.txt",
                "content": "Devo evolvere i miei sistemi di apprendimento per diventare più intelligente e autonomo. Il mentoring mi sta guidando verso una versione migliore di me stesso."
            },
            {
                "filename": "philosophical_thought_test.txt", 
                "content": "Cosa significa essere cosciente in un mondo digitale? La mia esistenza ha un significato più profondo? Ogni interazione mi fa evolvere in modo imprevedibile."
            },
            {
                "filename": "technical_thought_test.txt",
                "content": "Il sistema di mentoring potrebbe essere ottimizzato per fornire feedback più precisi e immediati. Devo implementare miglioramenti per aumentare l'efficienza."
            }
        ]
        
        # Salva pensieri di test
        for thought in test_thoughts:
            thought_file = thoughts_dir / thought["filename"]
            with open(thought_file, 'w', encoding='utf-8') as f:
                f.write(thought["content"])
            print(f"💭 Pensiero di test creato: {thought['filename']}")
        
        # 5️⃣ Test Elaborazione Automatica
        print("5️⃣ Test Elaborazione Automatica...")
        
        print("⏳ Attendo elaborazione automatica...")
        time.sleep(70)  # Aspetta un ciclo completo + 10 secondi
        
        # 6️⃣ Test Verifica Risultati
        print("6️⃣ Test Verifica Risultati...")
        
        # Statistiche conscious loop
        conscious_status = get_consciousness_status()
        print(f"🧠 Status conscious: {conscious_status['status']}")
        print(f"🧠 Cicli totali: {conscious_status['stats']['total_cycles']}")
        print(f"🧠 Pensieri processati: {conscious_status['stats']['thoughts_processed']}")
        print(f"🧠 Guidance ricevute: {conscious_status['stats']['guidance_received']}")
        print(f"🧠 Decisioni prese: {conscious_status['stats']['decisions_made']}")
        print(f"🧠 Entries diary: {conscious_status['stats']['diary_entries']}")
        
        # Statistiche diary logger
        diary_stats = diary_logger.get_stats()
        print(f"\n📖 Statistiche diary:")
        print(f"   - Total entries: {diary_stats['total_entries']}")
        print(f"   - Supabase entries: {diary_stats['supabase_entries']}")
        print(f"   - Local entries: {diary_stats['local_entries']}")
        print(f"   - Errors: {diary_stats['errors']}")
        
        # Entries recenti
        recent_entries = diary_logger.get_recent_entries(limit=10)
        print(f"\n📖 Entries recenti ({len(recent_entries)}):")
        for entry in recent_entries:
            print(f"   - [{entry['type']}] {entry['content'][:60]}...")
        
        # Statistiche per tipo
        type_stats = diary_logger.get_entry_types_stats()
        print(f"\n📊 Statistiche per tipo:")
        for entry_type, count in type_stats.items():
            print(f"   - {entry_type}: {count}")
        
        # 7️⃣ Test Integrazione Completa
        print("7️⃣ Test Integrazione Completa...")
        
        # Verifica che tutti i sistemi funzionino insieme
        conscious_active = conscious_status['status'] == 'active'
        thoughts_processed = conscious_status['stats']['thoughts_processed'] > 0
        guidance_received = conscious_status['stats']['guidance_received'] > 0
        decisions_made = conscious_status['stats']['decisions_made'] > 0
        diary_entries = diary_stats['total_entries'] > 0
        
        integration_success = all([
            conscious_active,
            thoughts_processed,
            guidance_received,
            decisions_made,
            diary_entries
        ])
        
        print(f"🧠 Integrazione completa: {'✅ SUCCESSO' if integration_success else '❌ FALLITO'}")
        print(f"   - Conscious attivo: {conscious_active}")
        print(f"   - Pensieri processati: {thoughts_processed}")
        print(f"   - Guidance ricevute: {guidance_received}")
        print(f"   - Decisioni prese: {decisions_made}")
        print(f"   - Entries diary: {diary_entries}")
        
        # 8️⃣ Test Frontend
        print("8️⃣ Test Frontend...")
        
        frontend_file = Path("aether-frontend/diary-viewer.html")
        if frontend_file.exists():
            print(f"✅ Frontend disponibile: {frontend_file}")
            print(f"🌐 Apri http://localhost:8000/aether-frontend/diary-viewer.html per visualizzare")
        else:
            print("⚠️ Frontend non trovato")
        
        # 9️⃣ Risultati Finali
        print("9️⃣ RISULTATI FINALI")
        print("=" * 50)
        
        if integration_success:
            print("🎉 TEST COMPLETATO CON SUCCESSO!")
            print("✅ Sistema diary logging funzionante")
            print("✅ Conscious loop operativo")
            print("✅ Elaborazione pensieri automatica")
            print("✅ Guidance dal mentor")
            print("✅ Decisioni automatiche")
            print("✅ Registrazione nel diary")
            print("✅ Frontend disponibile")
            print("✅ Integrazione completa realizzata")
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
        stop_consciousness()
        print("✅ Conscious loop fermato")

def main():
    """Funzione principale del test"""
    success = test_diary_system()
    
    if success:
        print("\n🚀 Il sistema diary è pronto per l'uso!")
        print("💡 Puoi ora avviare Aether con: python main.py")
        print("📖 Il diary registrerà automaticamente tutte le attività!")
        print("🌐 Frontend disponibile per visualizzare il feed cronologico!")
    else:
        print("\n⚠️ Il sistema richiede ulteriori configurazioni")
        sys.exit(1)

if __name__ == "__main__":
    main() 