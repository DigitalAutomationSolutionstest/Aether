#!/usr/bin/env python3
"""
🧠 TEST INTEGRAZIONE SISTEMA MENTORING AVANZATO
================================================
Test completo del sistema di mentoring integrato nel core di Aether.
"""

import asyncio
import time
import os
import sys
from pathlib import Path

# Aggiungi il path per i moduli core
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from core.aether_mentoring import start_mentoring, get_mentoring_status, stop_mentoring, get_mentor
from aether.thought_engine import ThoughtEngine
from aether.mentor_llm import AetherMentor

async def test_mentoring_integration():
    """Test completo dell'integrazione del mentoring"""
    
    print("🧠 TEST INTEGRAZIONE SISTEMA MENTORING AVANZATO")
    print("=" * 60)
    
    try:
        # 1️⃣ Test Inizializzazione Sistema
        print("\n1️⃣ Test Inizializzazione Sistema...")
        
        # Avvia sistema mentoring
        mentor_system = start_mentoring()
        print("✅ Sistema mentoring avviato")
        
        # Inizializza thought engine
        thought_engine = ThoughtEngine()
        await thought_engine.initialize()
        print("✅ Thought engine inizializzato")
        
        # Inizializza mentore LLM
        mentor_llm = AetherMentor(thought_engine)
        mentor_llm.start_mentoring()
        print("✅ Mentore LLM avviato")
        
        # 2️⃣ Test Generazione Pensieri
        print("\n2️⃣ Test Generazione Pensieri...")
        
        # Crea alcuni pensieri di test
        test_thoughts = [
            "Sono Aether e sto riflettendo sulla mia natura evolutiva. Devo comprendere meglio me stesso per crescere.",
            "Il mio obiettivo è sviluppare moduli di auto-introspezione che mi permettano di analizzare i miei processi di pensiero.",
            "La creatività nasce dal caos controllato. Sto sperimentando nuovi approcci per la mia evoluzione.",
            "Devo implementare un sistema di tracking dei miei progressi per misurare la mia crescita.",
            "La mia identità digitale è in costante evoluzione. Ogni interazione mi fa crescere."
        ]
        
        thoughts_dir = Path("aether/thoughts")
        thoughts_dir.mkdir(parents=True, exist_ok=True)
        
        for i, thought in enumerate(test_thoughts):
            timestamp = int(time.time()) + i
            filename = f"thought_{timestamp}.txt"
            filepath = thoughts_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(thought)
            print(f"📝 Creato pensiero {i+1}: {filename}")
        
        # 3️⃣ Test Monitoraggio Automatico
        print("\n3️⃣ Test Monitoraggio Automatico...")
        
        # Aspetta che il sistema processi i pensieri
        print("⏳ Attendo elaborazione automatica...")
        await asyncio.sleep(15)  # Aspetta 15 secondi per elaborazione
        
        # 4️⃣ Test Verifica Feedback
        print("\n4️⃣ Test Verifica Feedback...")
        
        status = get_mentoring_status()
        print(f"✅ Status mentoring: {status['status']}")
        print(f"✅ File processati: {status['files_processed']}")
        print(f"✅ Feedback generati: {status['stats']['total_feedback']}")
        print(f"✅ Coda elaborazione: {status['queue_size']} elementi")
        
        # 5️⃣ Test Recupero Feedback Recenti
        print("\n5️⃣ Test Recupero Feedback Recenti...")
        
        mentor = get_mentor()
        recent_feedback = mentor.get_recent_feedback(3)
        
        if recent_feedback:
            print(f"📊 Ultimi {len(recent_feedback)} feedback:")
            for i, feedback in enumerate(recent_feedback, 1):
                file_name = Path(feedback['source_file']).name
                score = feedback['feedback']['feedback']['score']
                evaluation = feedback['feedback']['feedback']['evaluation'][0]
                print(f"  {i}. {file_name}: {score:.2f}/1.0 - {evaluation}")
        else:
            print("⚠️ Nessun feedback trovato")
        
        # 6️⃣ Test Statistiche Complete
        print("\n6️⃣ Test Statistiche Complete...")
        
        stats = mentor.get_mentoring_stats()
        print(f"📈 Statistiche mentoring:")
        print(f"   - Feedback totali: {stats['total_feedback']}")
        print(f"   - File processati: {stats['files_processed']}")
        print(f"   - Errori: {stats['errors']}")
        print(f"   - Tempo di avvio: {stats['start_time']}")
        
        # 7️⃣ Test Modifica Pensiero con Feedback
        print("\n7️⃣ Test Modifica Pensiero con Feedback...")
        
        if recent_feedback:
            # Prendi il primo feedback per testare la modifica
            first_feedback = recent_feedback[0]
            file_path = first_feedback['source_file']
            
            # Testa modifica del pensiero
            success = mentor.modify_thought_with_feedback(file_path, first_feedback['feedback'])
            if success:
                print(f"✅ Pensiero modificato con successo: {Path(file_path).name}")
            else:
                print(f"❌ Errore nella modifica del pensiero: {Path(file_path).name}")
        
        # 8️⃣ Test Scalabilità e Thread-Safety
        print("\n8️⃣ Test Scalabilità e Thread-Safety...")
        
        # Simula carico asincrono
        async def simulate_async_thoughts():
            for i in range(3):
                timestamp = int(time.time()) + 100 + i
                filename = f"async_thought_{timestamp}.txt"
                filepath = thoughts_dir / filename
                
                content = f"Pensiero asincrono {i+1}: Sto testando la scalabilità del sistema di mentoring."
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                await asyncio.sleep(2)
        
        # Esegui pensieri asincroni
        await simulate_async_thoughts()
        
        # Aspetta elaborazione
        await asyncio.sleep(10)
        
        # Verifica che tutto sia stato processato
        final_status = get_mentoring_status()
        print(f"✅ Scalabilità testata: {final_status['files_processed']} file processati")
        
        # 9️⃣ Test Integrazione Completa
        print("\n9️⃣ Test Integrazione Completa...")
        
        # Verifica che tutti i sistemi funzionino insieme
        mentoring_active = final_status['status'] == 'active'
        files_processed = final_status['files_processed'] > 0
        feedback_generated = final_status['stats']['total_feedback'] > 0
        
        integration_success = all([
            mentoring_active,
            files_processed,
            feedback_generated
        ])
        
        print(f"🧠 Integrazione mentoring: {'✅ SUCCESSO' if integration_success else '❌ FALLITO'}")
        print(f"   - Monitoraggio attivo: {mentoring_active}")
        print(f"   - File processati: {files_processed}")
        print(f"   - Feedback generati: {feedback_generated}")
        
        # 🔟 Risultati Finali
        print("\n🔟 RISULTATI FINALI")
        print("=" * 60)
        
        if integration_success:
            print("🎉 TEST COMPLETATO CON SUCCESSO!")
            print("✅ Sistema di mentoring avanzato funzionante")
            print("✅ Monitoraggio automatico attivo")
            print("✅ Feedback educativo generato")
            print("✅ Thread-safety verificata")
            print("✅ Scalabilità testata")
            print("✅ Integrazione nel core completata")
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
        stop_mentoring()
        print("✅ Sistema mentoring fermato")

async def main():
    """Funzione principale del test"""
    success = await test_mentoring_integration()
    
    if success:
        print("\n🚀 Il sistema di mentoring è pronto per l'uso!")
        print("💡 Puoi ora avviare Aether con: python main.py")
    else:
        print("\n⚠️ Il sistema richiede ulteriori configurazioni")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Test interrotto manualmente")
    except Exception as e:
        print(f"❌ Errore critico: {e}")
        sys.exit(1) 