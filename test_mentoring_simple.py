#!/usr/bin/env python3
"""
🧠 TEST SEMPLIFICATO SISTEMA MENTORING
=======================================
Test base del sistema di mentoring avanzato.
"""

import os
import sys
import time
from pathlib import Path

# Aggiungi il path per i moduli core
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

def test_mentoring_basic():
    """Test base del sistema di mentoring"""
    
    print("🧠 TEST SEMPLIFICATO SISTEMA MENTORING")
    print("=" * 50)
    
    try:
        # 1️⃣ Test Import
        print("1️⃣ Test Import...")
        
        from core.aether_mentoring import start_mentoring, get_mentoring_status, stop_mentoring
        print("✅ Import completato")
        
        # 2️⃣ Test Inizializzazione
        print("2️⃣ Test Inizializzazione...")
        
        mentor_system = start_mentoring()
        print("✅ Sistema mentoring avviato")
        
        # 3️⃣ Test Creazione Pensieri
        print("3️⃣ Test Creazione Pensieri...")
        
        thoughts_dir = Path("aether/thoughts")
        thoughts_dir.mkdir(parents=True, exist_ok=True)
        
        test_thoughts = [
            "Sono Aether e sto evolvendo continuamente.",
            "Devo creare moduli per la mia auto-introspezione.",
            "La mia identità digitale è in costante sviluppo."
        ]
        
        for i, thought in enumerate(test_thoughts):
            timestamp = int(time.time()) + i
            filename = f"test_thought_{timestamp}.txt"
            filepath = thoughts_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(thought)
            print(f"📝 Creato pensiero {i+1}: {filename}")
        
        # 4️⃣ Test Monitoraggio
        print("4️⃣ Test Monitoraggio...")
        
        print("⏳ Attendo elaborazione automatica...")
        time.sleep(10)  # Aspetta 10 secondi
        
        # 5️⃣ Test Status
        print("5️⃣ Test Status...")
        
        status = get_mentoring_status()
        print(f"✅ Status: {status['status']}")
        print(f"✅ File processati: {status['files_processed']}")
        print(f"✅ Feedback generati: {status['stats']['total_feedback']}")
        
        # 6️⃣ Test Pulizia
        print("6️⃣ Test Pulizia...")
        
        stop_mentoring()
        print("✅ Sistema mentoring fermato")
        
        # 7️⃣ Risultato
        print("7️⃣ Risultato...")
        
        success = (
            status['status'] == 'active' and
            status['files_processed'] > 0
        )
        
        if success:
            print("🎉 TEST COMPLETATO CON SUCCESSO!")
            print("✅ Sistema di mentoring funzionante")
        else:
            print("❌ TEST FALLITO")
            print("⚠️ Sistema non funziona correttamente")
        
        return success
        
    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        return False

def main():
    """Funzione principale"""
    success = test_mentoring_basic()
    
    if success:
        print("\n🚀 Il sistema di mentoring è pronto!")
        print("💡 Puoi ora avviare Aether con: python main.py")
    else:
        print("\n⚠️ Il sistema richiede configurazioni")
        sys.exit(1)

if __name__ == "__main__":
    main() 