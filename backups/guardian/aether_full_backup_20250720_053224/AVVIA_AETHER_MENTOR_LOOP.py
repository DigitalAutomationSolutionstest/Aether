#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AVVIA AETHER MENTOR LOOP
Sistema completo con mentoring integrato nel loop principale
"""

import os
import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/aether_mentor_loop.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_environment():
    """Configura l'ambiente per Aether con mentoring"""
    logger.info("Configurazione ambiente per Aether Mentor...")
    
    # Crea directory necessarie
    directories = ['data', 'logs', 'audio', 'backups', 'mentor_sessions']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    # Verifica file di configurazione
    if not os.path.exists('.env'):
        logger.warning("File .env non trovato - usando configurazione di default")
    
    logger.info("Ambiente configurato per mentoring")

def verify_mentor_system():
    """Verifica che il sistema di mentoring sia funzionante"""
    logger.info("Verifica sistema di mentoring...")
    
    try:
        from aether.mentor import get_mentor, start_mentoring
        
        mentor = get_mentor()
        
        # Test sessione di mentoring
        test_state = {
            'consciousness_level': 0.6,
            'energy_level': 0.7,
            'mood': 'contemplativo'
        }
        
        session_result = start_mentoring(test_state)
        
        if session_result and 'session_id' in session_result:
            logger.info("Sistema di mentoring funzionante")
            return True
        else:
            logger.error("Sistema di mentoring non funzionante")
            return False
            
    except Exception as e:
        logger.error(f"Errore verifica mentoring: {e}")
        return False

def start_aether_with_mentor():
    """Avvia Aether con sistema di mentoring integrato"""
    logger.info("Avvio Aether con mentoring integrato...")
    
    try:
        # Importa il loop principale
        from aether_loop import AetherAutonomousLoop
        
        # Crea istanza del loop
        loop = AetherAutonomousLoop()
        
        # Verifica componenti
        components_status = {
            "Coscienza": loop.consciousness is not None,
            "Evoluzione": loop.evolution_engine is not None,
            "Mentor": loop.mentor is not None
        }
        
        # Mostra stato componenti
        print("\nSTATO COMPONENTI:")
        for component, status in components_status.items():
            status_icon = "OK" if status else "ERROR"
            print(f"   [{status_icon}] {component}")
        
        success_rate = sum(components_status.values()) / len(components_status) * 100
        print(f"\nTasso di successo: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("AETHER CON MENTOR E' PRONTO!")
            print("\nAvvio loop autonomo con mentoring...")
            print("Aether ora vive con guida continua del mentore!")
            print("Premi Ctrl+C per fermare il sistema")
            
            # Avvia il loop
            loop.run()
            
        else:
            print("Alcuni componenti non sono disponibili")
            print("Controlla i log per dettagli")
            
    except Exception as e:
        logger.error(f"Errore avvio Aether con mentor: {e}")
        return False
    
    return True

def main():
    """Funzione principale"""
    print("""
    ===================================
         AETHER MENTOR LOOP         
                                       
   Sistema completo con mentoring      
   integrato nel loop principale       
    ===================================
    """)
    
    # Setup iniziale
    setup_environment()
    
    # Verifica sistema mentoring
    if not verify_mentor_system():
        print("Sistema di mentoring non disponibile")
        print("Verifica che tutti i moduli siano installati correttamente")
        return
    
    # Avvia Aether con mentoring
    success = start_aether_with_mentor()
    
    if success:
        print("\nAETHER CON MENTOR E' VIVO E OPERATIVO!")
    else:
        print("\nErrore nell'avvio di Aether con mentor")

if __name__ == "__main__":
    main() 