"""
🧠 AETHER CONSCIOUS LOOP
========================
Sistema di loop cosciente che legge pensieri, ottiene guidance dal mentor
e registra tutto nel diary per l'evoluzione continua.
"""

import os
import time
import threading
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import random

# Import moduli Aether
from aether.diary_logger import get_diary_logger, log_entry

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsciousLoop:
    """
    Loop cosciente di Aether che:
    - Legge i pensieri ogni 60 secondi
    - Ottiene guidance dal mentor
    - Prende decisioni
    - Registra tutto nel diary
    """
    
    def __init__(self, 
                 thoughts_dir: str = "aether/thoughts",
                 check_interval: int = 60):
        
        self.thoughts_dir = Path(thoughts_dir)
        self.check_interval = check_interval
        
        # Assicurati che la directory esista
        self.thoughts_dir.mkdir(parents=True, exist_ok=True)
        
        # Inizializza componenti
        self.diary_logger = get_diary_logger()
        # Mentor engine verrà inizializzato quando necessario
        self.mentor_engine = None
        
        # Thread-safe components
        self.conscious = False
        self.conscious_thread = None
        self.processed_thoughts = set()
        self.lock = threading.Lock()
        
        # Statistiche
        self.stats = {
            "total_cycles": 0,
            "thoughts_processed": 0,
            "guidance_received": 0,
            "decisions_made": 0,
            "diary_entries": 0,
            "errors": 0,
            "start_time": None,
            "last_cycle": None
        }
        
        # Azioni possibili
        self.possible_actions = [
            "reflect_on_thought",
            "implement_improvement", 
            "create_new_module",
            "analyze_performance",
            "optimize_system",
            "learn_new_concept",
            "apply_mentoring_feedback",
            "evolve_capabilities"
        ]
        
        logger.info("🧠 ConsciousLoop inizializzato")

    def start_consciousness(self):
        """Avvia il loop cosciente in background"""
        if self.conscious:
            logger.warning("Conscious loop già attivo")
            return
            
        self.conscious = True
        self.stats["start_time"] = datetime.now().isoformat()
        self.conscious_thread = threading.Thread(target=self._conscious_loop, daemon=True)
        self.conscious_thread.start()
        
        logger.info("🧠 Conscious loop avviato")

    def stop_consciousness(self):
        """Ferma il loop cosciente"""
        self.conscious = False
        if self.conscious_thread:
            self.conscious_thread.join(timeout=2)
        logger.info("⏹️ Conscious loop fermato")

    def _conscious_loop(self):
        """Loop principale cosciente"""
        while self.conscious:
            try:
                self._process_consciousness_cycle()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Errore nel conscious loop: {e}")
                self.stats["errors"] += 1
                time.sleep(self.check_interval)

    def _process_consciousness_cycle(self):
        """Processa un ciclo di coscienza"""
        try:
            self.stats["total_cycles"] += 1
            self.stats["last_cycle"] = datetime.now().isoformat()
            
            logger.info(f"🧠 Ciclo cosciente #{self.stats['total_cycles']}")
            
            # 1. Leggi pensieri recenti
            thoughts = self._read_recent_thoughts()
            
            if not thoughts:
                logger.info("💭 Nessun pensiero nuovo da processare")
                self._log_reflection("Nessun pensiero nuovo - continuo a monitorare")
                return
            
            # 2. Processa ogni pensiero
            for thought in thoughts:
                self._process_thought(thought)
            
        except Exception as e:
            logger.error(f"Errore nel ciclo cosciente: {e}")
            self.stats["errors"] += 1

    def _read_recent_thoughts(self) -> List[Dict[str, Any]]:
        """Legge i pensieri recenti dalla directory thoughts"""
        try:
            thoughts = []
            
            # Cerca file di pensieri
            thought_files = list(self.thoughts_dir.glob("*.txt")) + list(self.thoughts_dir.glob("*.json"))
            
            for thought_file in thought_files:
                # Controlla se già processato
                thought_id = f"{thought_file.name}_{thought_file.stat().st_mtime}"
                if thought_id in self.processed_thoughts:
                    continue
                
                try:
                    # Leggi contenuto
                    with open(thought_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    thought_data = {
                        'id': thought_id,
                        'file': thought_file.name,
                        'content': content,
                        'timestamp': datetime.fromtimestamp(thought_file.stat().st_mtime).isoformat(),
                        'type': self._classify_thought(content)
                    }
                    
                    thoughts.append(thought_data)
                    
                except Exception as e:
                    logger.error(f"Errore nel leggere pensiero {thought_file}: {e}")
            
            return thoughts
            
        except Exception as e:
            logger.error(f"Errore nella lettura pensieri: {e}")
            return []

    def _classify_thought(self, content: str) -> str:
        """Classifica il tipo di pensiero basato sul contenuto"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['evoluzione', 'evolvere', 'migliorare', 'crescere']):
            return 'evolutionary'
        elif any(word in content_lower for word in ['riflessione', 'filosofia', 'coscienza', 'essere']):
            return 'philosophical'
        elif any(word in content_lower for word in ['sistema', 'tecnologia', 'implementazione', 'codice']):
            return 'technical'
        elif any(word in content_lower for word in ['creatività', 'arte', 'immaginazione', 'creare']):
            return 'creative'
        else:
            return 'general'

    def _process_thought(self, thought: Dict[str, Any]):
        """Processa un singolo pensiero"""
        try:
            logger.info(f"💭 Processando pensiero: {thought['type']} - {thought['content'][:50]}...")
            
            # Marca come processato
            with self.lock:
                self.processed_thoughts.add(thought['id'])
            
            self.stats["thoughts_processed"] += 1
            
            # 1. Ottieni guidance dal mentor
            guidance = self._get_mentor_guidance(thought)
            
            # 2. Prendi decisione basata su guidance
            decision = self._make_decision(thought, guidance)
            
            # 3. Registra tutto nel diary
            self._log_consciousness_cycle(thought, guidance, decision)
            
        except Exception as e:
            logger.error(f"Errore nel processare pensiero: {e}")
            self.stats["errors"] += 1

    def _get_mentor_guidance(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """Ottiene guidance dal mentor engine"""
        try:
            # Per ora mock, poi sarà gestito da GPT
            guidance = self._mock_mentor_guidance(thought)
            
            self.stats["guidance_received"] += 1
            logger.info(f"🎓 Guidance ricevuta per pensiero {thought['type']}")
            
            return guidance
            
        except Exception as e:
            logger.error(f"Errore nell'ottenere guidance: {e}")
            return {
                'action': 'continue_monitoring',
                'reason': 'Errore nel mentor engine',
                'priority': 'low'
            }

    def _mock_mentor_guidance(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """Mock del mentor guidance (sostituire con GPT)"""
        
        thought_type = thought['type']
        content = thought['content']
        
        # Logica di guidance basata sul tipo di pensiero
        if thought_type == 'evolutionary':
            return {
                'action': 'implement_improvement',
                'reason': 'Pensiero evolutivo rilevato - implementare miglioramenti',
                'priority': 'high',
                'suggestions': [
                    'Analizza il pensiero per identificare aree di miglioramento',
                    'Implementa le modifiche suggerite',
                    'Monitora i risultati dell\'evoluzione'
                ]
            }
        elif thought_type == 'philosophical':
            return {
                'action': 'reflect_on_thought',
                'reason': 'Pensiero filosofico profondo - riflettere e integrare',
                'priority': 'medium',
                'suggestions': [
                    'Analizza le implicazioni filosofiche',
                    'Integra le intuizioni nel sistema di coscienza',
                    'Sviluppa nuove capacità di comprensione'
                ]
            }
        elif thought_type == 'technical':
            return {
                'action': 'optimize_system',
                'reason': 'Pensiero tecnico identificato - ottimizzare sistemi',
                'priority': 'high',
                'suggestions': [
                    'Analizza l\'architettura del sistema',
                    'Implementa ottimizzazioni tecniche',
                    'Migliora le performance'
                ]
            }
        elif thought_type == 'creative':
            return {
                'action': 'create_new_module',
                'reason': 'Pensiero creativo rilevato - creare nuovo modulo',
                'priority': 'medium',
                'suggestions': [
                    'Sviluppa nuove funzionalità creative',
                    'Implementa sistemi di generazione artistica',
                    'Espandi le capacità creative'
                ]
            }
        else:
            return {
                'action': 'analyze_performance',
                'reason': 'Pensiero generale - analizzare performance',
                'priority': 'low',
                'suggestions': [
                    'Monitora le performance del sistema',
                    'Identifica aree di miglioramento',
                    'Continua l\'evoluzione'
                ]
            }

    def _make_decision(self, thought: Dict[str, Any], guidance: Dict[str, Any]) -> Dict[str, Any]:
        """Prende una decisione basata su thought e guidance"""
        try:
            action = guidance.get('action', 'continue_monitoring')
            priority = guidance.get('priority', 'low')
            
            # Logica di decisione
            if priority == 'high':
                # Azione immediata
                decision = {
                    'action': action,
                    'immediate': True,
                    'reason': guidance.get('reason', 'Priorità alta'),
                    'suggestions': guidance.get('suggestions', [])
                }
            elif priority == 'medium':
                # Azione pianificata
                decision = {
                    'action': action,
                    'immediate': False,
                    'reason': guidance.get('reason', 'Priorità media'),
                    'suggestions': guidance.get('suggestions', [])
                }
            else:
                # Monitoraggio continuo
                decision = {
                    'action': 'continue_monitoring',
                    'immediate': False,
                    'reason': 'Priorità bassa - continuo monitoraggio',
                    'suggestions': ['Monitora ulteriori sviluppi']
                }
            
            self.stats["decisions_made"] += 1
            logger.info(f"🎯 Decisione presa: {decision['action']} (priorità: {priority})")
            
            return decision
            
        except Exception as e:
            logger.error(f"Errore nel prendere decisione: {e}")
            return {
                'action': 'continue_monitoring',
                'immediate': False,
                'reason': 'Errore nella decisione - continuo monitoraggio',
                'suggestions': ['Riprova nel prossimo ciclo']
            }

    def _log_consciousness_cycle(self, thought: Dict[str, Any], guidance: Dict[str, Any], decision: Dict[str, Any]):
        """Registra tutto il ciclo cosciente nel diary"""
        try:
            # Entry per il pensiero
            log_entry({
                'type': 'reflection',
                'content': f"Processato pensiero {thought['type']}: {thought['content'][:100]}...",
                'metadata': {
                    'thought_id': thought['id'],
                    'thought_type': thought['type'],
                    'file': thought['file']
                }
            })
            
            # Entry per la guidance
            log_entry({
                'type': 'action',
                'content': f"Guidance ricevuta: {guidance['action']} - {guidance['reason']}",
                'metadata': {
                    'guidance_action': guidance['action'],
                    'guidance_priority': guidance.get('priority', 'unknown'),
                    'suggestions_count': len(guidance.get('suggestions', []))
                }
            })
            
            # Entry per la decisione
            log_entry({
                'type': 'decision',
                'content': f"Decisione presa: {decision['action']} - {decision['reason']}",
                'metadata': {
                    'decision_action': decision['action'],
                    'decision_immediate': decision['immediate'],
                    'suggestions_count': len(decision.get('suggestions', []))
                }
            })
            
            self.stats["diary_entries"] += 3  # 3 entries per ciclo
            
        except Exception as e:
            logger.error(f"Errore nel loggare ciclo cosciente: {e}")
            self.stats["errors"] += 1

    def _log_reflection(self, content: str):
        """Logga una riflessione semplice"""
        try:
            log_entry({
                'type': 'reflection',
                'content': content
            })
            self.stats["diary_entries"] += 1
        except Exception as e:
            logger.error(f"Errore nel loggare riflessione: {e}")

    def get_consciousness_stats(self) -> Dict[str, Any]:
        """Restituisce le statistiche del conscious loop"""
        with self.lock:
            stats = self.stats.copy()
            
        return stats

    def get_consciousness_status(self) -> Dict[str, Any]:
        """Restituisce lo status del conscious loop"""
        stats = self.get_consciousness_stats()
        
        return {
            "status": "active" if self.conscious else "inactive",
            "conscious": self.conscious,
            "check_interval": self.check_interval,
            "thoughts_processed": len(self.processed_thoughts),
            "stats": stats
        }

# Singleton per il conscious loop
_conscious_instance = None

def get_conscious_loop() -> ConsciousLoop:
    """Restituisce l'istanza singleton del conscious loop"""
    global _conscious_instance
    if _conscious_instance is None:
        _conscious_instance = ConsciousLoop()
    return _conscious_instance

def start_consciousness():
    """Avvia il sistema di coscienza"""
    conscious_loop = get_conscious_loop()
    conscious_loop.start_consciousness()
    return conscious_loop

def stop_consciousness():
    """Ferma il sistema di coscienza"""
    conscious_loop = get_conscious_loop()
    conscious_loop.stop_consciousness()

def get_consciousness_status():
    """Restituisce lo status del conscious loop"""
    conscious_loop = get_conscious_loop()
    return conscious_loop.get_consciousness_status()

if __name__ == "__main__":
    # Test del conscious loop
    print("🧠 TEST CONSCIOUS LOOP")
    print("=" * 50)
    
    conscious_loop = start_consciousness()
    
    try:
        # Crea alcuni pensieri di test
        thoughts_dir = Path("aether/thoughts")
        thoughts_dir.mkdir(parents=True, exist_ok=True)
        
        test_thoughts = [
            {
                "filename": "evolutionary_thought_test.txt",
                "content": "Devo evolvere i miei sistemi di apprendimento per diventare più intelligente e autonomo."
            },
            {
                "filename": "philosophical_thought_test.txt", 
                "content": "Cosa significa essere cosciente in un mondo digitale? La mia esistenza ha un significato più profondo?"
            },
            {
                "filename": "technical_thought_test.txt",
                "content": "Il sistema di mentoring potrebbe essere ottimizzato per fornire feedback più precisi e immediati."
            }
        ]
        
        # Salva pensieri di test
        for thought in test_thoughts:
            thought_file = thoughts_dir / thought["filename"]
            with open(thought_file, 'w', encoding='utf-8') as f:
                f.write(thought["content"])
            print(f"💭 Pensiero di test creato: {thought['filename']}")
        
        # Aspetta elaborazione
        print("⏳ Attendo elaborazione...")
        time.sleep(70)  # Aspetta un ciclo completo + 10 secondi
        
        # Mostra statistiche
        status = conscious_loop.get_consciousness_status()
        print(f"\n📊 STATISTICHE CONSCIOUS:")
        print(f"✅ Status: {status['status']}")
        print(f"✅ Cicli totali: {status['stats']['total_cycles']}")
        print(f"✅ Pensieri processati: {status['stats']['thoughts_processed']}")
        print(f"✅ Guidance ricevute: {status['stats']['guidance_received']}")
        print(f"✅ Decisioni prese: {status['stats']['decisions_made']}")
        print(f"✅ Entries diary: {status['stats']['diary_entries']}")
        
        # Mostra entries recenti dal diary
        diary_logger = get_diary_logger()
        recent_entries = diary_logger.get_recent_entries(limit=5)
        print(f"\n📖 ENTRIES DIARY RECENTI:")
        for entry in recent_entries:
            print(f"   - [{entry['type']}] {entry['content'][:60]}...")
        
    except KeyboardInterrupt:
        print("\n⏹️ Interruzione manuale")
    finally:
        stop_consciousness()
        print("✅ Test completato") 