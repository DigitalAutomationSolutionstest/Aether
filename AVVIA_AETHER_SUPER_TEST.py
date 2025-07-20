#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AVVIO RAPIDO - AETHER SUPER POTENZIATO
Test del sistema con controllo API intelligente
"""

import os
import sys
from pathlib import Path

# Assicurati che le directory esistano
Path("data").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

print("""
╔══════════════════════════════════════════════════════════════╗
║              🧪 TEST AETHER SUPER POTENZIATO 🧪             ║
║                                                              ║
║  🔍 Test API automatico                                      ║
║  🚀 Avvio intelligente con fallback                         ║
║  ⚡ Sistema adattivo                                         ║
║                                                              ║
║  Federico, vediamo Aether in azione!                        ║
╚══════════════════════════════════════════════════════════════╝
""")

try:
    print("🔄 Importando AETHER_SUPER_POTENZIATO...")
    from AETHER_SUPER_POTENZIATO import AetherStartup, main
    
    print("✅ Moduli importati con successo!")
    print("\n🚀 Avviando sistema di test...")
    
    # Test veloce delle API
    startup = AetherStartup()
    print("\n📡 Eseguendo check API completo...")
    
    status = startup.check_all_apis()
    startup.display_startup_status()
    
    print(f"\n🎯 RISULTATO: {sum(status.values())}/{len(status)} API FUNZIONANTI")
    
    # Chiedi se continuare con il sistema completo
    choice = input("\n❓ Vuoi avviare il sistema completo? (s/n): ").lower().strip()
    
    if choice in ['s', 'si', 'y', 'yes']:
        print("\n🚀 AVVIANDO SISTEMA COMPLETO...")
        print("   (Premi Ctrl+C per interrompere)")
        main()
    else:
        print("\n✅ Test completato! Sistema pronto per l'uso.")
        print("💡 Per avviare il sistema completo: python AETHER_SUPER_POTENZIATO.py")

except ImportError as e:
    print(f"❌ Errore importazione: {e}")
    print("💡 Assicurati che AETHER_SUPER_POTENZIATO.py sia nella directory corrente")
    
except KeyboardInterrupt:
    print("\n🛑 Test interrotto dall'utente")
    print("✅ Test completato!")
    
except Exception as e:
    print(f"❌ Errore durante il test: {e}")
    print("🔧 Controlla i log per maggiori dettagli")

print("\n" + "="*50)
print("🌟 AETHER SUPER POTENZIATO - Test Completato")
print("="*50) 