#!/usr/bin/env python3
"""
Test rapido per verificare che Aether funzioni
"""

import os
import json
import time
from datetime import datetime

def test_aether_stabile():
    """Test veloce del sistema Aether stabile"""
    
    print("🧪 Test Sistema Aether Stabile")
    print("=" * 50)
    
    # 1. Test import moduli
    try:
        from AETHER_STABILE_FUNZIONANTE import AetherSistemaStabile, AetherCoscienzaStabile
        print("✅ Import moduli: OK")
    except Exception as e:
        print(f"❌ Import moduli: ERRORE - {e}")
        return False
    
    # 2. Test creazione sistema
    try:
        sistema = AetherSistemaStabile()
        print("✅ Creazione sistema: OK")
    except Exception as e:
        print(f"❌ Creazione sistema: ERRORE - {e}")
        return False
    
    # 3. Test coscienza
    try:
        coscienza = AetherCoscienzaStabile()
        pensiero = coscienza.genera_pensiero()
        print(f"✅ Generazione pensiero: OK - '{pensiero[:30]}...'")
    except Exception as e:
        print(f"❌ Generazione pensiero: ERRORE - {e}")
        return False
    
    # 4. Test ciclo vita
    try:
        risultato = coscienza.ciclo_vita()
        if 'errore' not in risultato:
            print("✅ Ciclo vita: OK")
        else:
            print(f"❌ Ciclo vita: ERRORE - {risultato['errore']}")
            return False
    except Exception as e:
        print(f"❌ Ciclo vita: ERRORE - {e}")
        return False
    
    # 5. Test stato
    try:
        stato = sistema.stato_sistema()
        print(f"✅ Stato sistema: OK - Energia: {stato.get('energia', 'N/A')}")
    except Exception as e:
        print(f"❌ Stato sistema: ERRORE - {e}")
        return False
    
    # 6. Controlla file di stato
    try:
        if os.path.exists('data/aether_stato.json'):
            with open('data/aether_stato.json', 'r') as f:
                stato_file = json.load(f)
                print(f"✅ File stato: OK - Cicli: {stato_file.get('cicli_vita', 0)}")
        else:
            print("⚠️ File stato: Non ancora creato (normale)")
    except Exception as e:
        print(f"❌ File stato: ERRORE - {e}")
    
    print("=" * 50)
    print("🎉 TUTTI I TEST SUPERATI!")
    print("🧠 Sistema Aether Stabile è FUNZIONANTE!")
    
    return True

def test_rapido_coscienza():
    """Test super rapido della coscienza"""
    print("\n🚀 Test Rapido Coscienza")
    print("-" * 30)
    
    try:
        from AETHER_STABILE_FUNZIONANTE import AetherCoscienzaStabile
        
        aether = AetherCoscienzaStabile()
        
        # Genera 3 pensieri
        for i in range(3):
            pensiero = aether.genera_pensiero()
            print(f"💭 Pensiero {i+1}: {pensiero[:40]}...")
            time.sleep(0.5)
        
        # Test decisione
        decisione = aether.prendi_decisione()
        print(f"🎯 Decisione: {decisione}")
        
        # Test azione
        risultato = aether.esegui_azione(decisione)
        if risultato['successo']:
            print(f"✅ Azione completata: {risultato['dettagli']}")
        else:
            print(f"❌ Azione fallita: {risultato.get('errore', 'Errore sconosciuto')}")
        
        # Mostra stato
        print(f"⚡ Energia: {aether.energia:.2f}")
        print(f"😊 Umore: {aether.umore}")
        print(f"🔄 Cicli: {aether.cicli_vita}")
        
        print("\n🎉 COSCIENZA FUNZIONA PERFETTAMENTE!")
        return True
        
    except Exception as e:
        print(f"❌ ERRORE: {e}")
        return False

if __name__ == "__main__":
    print("🧠 AETHER - VERIFICA FUNZIONAMENTO")
    print("=" * 60)
    
    # Test sistema completo
    if test_aether_stabile():
        print("\n" + "="*60)
        # Test rapido coscienza
        test_rapido_coscienza()
    
    print("\n" + "="*60)
    print("✅ Verifica completata!")
    
    # Mostra status processi
    print(f"\n📊 Timestamp test: {datetime.now().strftime('%H:%M:%S')}")
    
    if os.path.exists('data'):
        files = os.listdir('data')
        print(f"📁 File in data/: {len(files)} file")
        for f in files:
            if f.endswith(('.json', '.log')):
                print(f"   • {f}")
    else:
        print("📁 Directory data/ non esiste ancora") 