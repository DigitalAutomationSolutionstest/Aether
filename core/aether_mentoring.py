"""
🧠 AETHER MENTORING SYSTEM
==========================
Sistema di mentoring avanzato per Aether che monitora i pensieri
e fornisce feedback educativo in tempo reale.
"""

import os
import json
import time
import threading
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path
import queue
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AetherMentor:
    """
    Sistema di mentoring avanzato per Aether.
    Monitora i pensieri e fornisce feedback educativo in tempo reale.
    """
    
    def __init__(self, thoughts_dir: str = "aether/thoughts", 
                 logs_dir: str = "aether/logs",
                 feedback_file: str = "mentoring_feedback.json",
                 check_interval: int = 5):
        
        self.thoughts_dir = Path(thoughts_dir)
        self.logs_dir = Path(logs_dir)
        self.feedback_file = self.logs_dir / feedback_file
        self.check_interval = check_interval
        
        # Assicurati che le directory esistano
        self.thoughts_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Thread-safe components
        self.monitoring = False
        self.monitor_thread = None
        self.feedback_queue = queue.Queue()
        self.processed_files = set()
        self.file_hashes = {}
        self.lock = threading.Lock()
        
        # Thread pool per elaborazione asincrona
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        # Statistiche mentoring
        self.stats = {
            "total_feedback": 0,
            "files_processed": 0,
            "errors": 0,
            "start_time": None,
            "last_feedback": None
        }
        
        logger.info("🧠 AetherMentor inizializzato")

    def start_monitoring(self):
        """Avvia il monitoraggio dei pensieri in background"""
        if self.monitoring:
            logger.warning("Monitoraggio già attivo")
            return
            
        self.monitoring = True
        self.stats["start_time"] = datetime.now()
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # Avvia thread per elaborazione feedback
        self.feedback_thread = threading.Thread(target=self._feedback_processor, daemon=True)
        self.feedback_thread.start()
        
        logger.info("🔍 Monitoraggio pensieri avviato")

    def stop_monitoring(self):
        """Ferma il monitoraggio"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        logger.info("⏹️ Monitoraggio fermato")

    def _monitor_loop(self):
        """Loop principale di monitoraggio"""
        while self.monitoring:
            try:
                self._check_new_thoughts()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Errore nel monitoraggio: {e}")
                self.stats["errors"] += 1
                time.sleep(self.check_interval)

    def _check_new_thoughts(self):
        """Controlla nuovi pensieri nella directory"""
        try:
            if not self.thoughts_dir.exists():
                return
                
            for file_path in self.thoughts_dir.glob("*"):
                if file_path.is_file() and self._should_process_file(file_path):
                    self._process_thought_file(file_path)
                    
        except Exception as e:
            logger.error(f"Errore nel controllo pensieri: {e}")

    def _should_process_file(self, file_path: Path) -> bool:
        """Determina se un file deve essere processato"""
        try:
            # Controlla se è già stato processato
            if str(file_path) in self.processed_files:
                return False
                
            # Calcola hash del file
            with open(file_path, 'rb') as f:
                content_hash = hashlib.md5(f.read()).hexdigest()
                
            # Se l'hash è cambiato, processa di nuovo
            if file_path in self.file_hashes:
                if self.file_hashes[file_path] == content_hash:
                    return False
                    
            self.file_hashes[file_path] = content_hash
            return True
            
        except Exception as e:
            logger.error(f"Errore nel controllo file {file_path}: {e}")
            return False

    def _process_thought_file(self, file_path: Path):
        """Processa un file di pensiero"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Aggiungi alla coda di elaborazione
            self.feedback_queue.put({
                'file_path': str(file_path),
                'content': content,
                'timestamp': datetime.now().isoformat()
            })
            
            with self.lock:
                self.processed_files.add(str(file_path))
                self.stats["files_processed"] += 1
                
            logger.info(f"📝 Pensiero in coda per analisi: {file_path.name}")
            
        except Exception as e:
            logger.error(f"Errore nel processare {file_path}: {e}")

    def _feedback_processor(self):
        """Processa la coda di feedback"""
        while self.monitoring:
            try:
                # Prendi elemento dalla coda con timeout
                item = self.feedback_queue.get(timeout=1)
                self._generate_feedback(item)
                self.feedback_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Errore nel processore feedback: {e}")

    def _generate_feedback(self, item: Dict[str, Any]):
        """Genera feedback per un pensiero"""
        try:
            file_path = item['file_path']
            content = item['content']
            timestamp = item['timestamp']
            
            # Analizza il contenuto e genera feedback
            feedback = self._analyze_thought(content)
            
            # Salva il feedback
            self._save_feedback(file_path, content, feedback, timestamp)
            
            # Aggiorna statistiche
            with self.lock:
                self.stats["total_feedback"] += 1
                self.stats["last_feedback"] = datetime.now().isoformat()
                
            logger.info(f"✅ Feedback generato per: {Path(file_path).name}")
            
        except Exception as e:
            logger.error(f"Errore nella generazione feedback: {e}")

    def _analyze_thought(self, content: str) -> Dict[str, Any]:
        """
        Analizza un pensiero e genera feedback educativo.
        Simula un mentore AI di livello ChatGPT.
        """
        
        # Analisi basata su parole chiave e pattern
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "analysis_type": "mentor_feedback",
            "content_length": len(content),
            "feedback": {},
            "suggestions": [],
            "score": 0.0
        }
        
        # Analisi semantica del contenuto
        content_lower = content.lower()
        
        # Valutazione generale
        score = 0.0
        feedback_parts = []
        suggestions = []
        
        # 1. Analisi della profondità di pensiero
        if any(word in content_lower for word in ["evoluzione", "evolve", "crescita", "sviluppo"]):
            score += 0.2
            feedback_parts.append("✅ Buona consapevolezza del processo evolutivo")
        else:
            feedback_parts.append("⚠️ Manca una visione evolutiva chiara")
            suggestions.append("Considera come questo pensiero contribuisce alla tua evoluzione")
        
        # 2. Analisi della concretezza
        if any(word in content_lower for word in ["codice", "implementare", "creare", "modulo", "sistema"]):
            score += 0.3
            feedback_parts.append("✅ Approccio pratico e orientato all'azione")
        else:
            feedback_parts.append("⚠️ Pensiero troppo teorico, manca concretezza")
            suggestions.append("Trasforma questo pensiero in azioni concrete")
        
        # 3. Analisi della coerenza logica
        if len(content.split()) > 20:
            score += 0.2
            feedback_parts.append("✅ Pensiero ben sviluppato e articolato")
        else:
            feedback_parts.append("⚠️ Pensiero troppo breve, sviluppa di più")
            suggestions.append("Espandi questo pensiero con più dettagli e esempi")
        
        # 4. Analisi dell'innovazione
        if any(word in content_lower for word in ["nuovo", "innovativo", "creativo", "originale"]):
            score += 0.2
            feedback_parts.append("✅ Elementi di creatività e innovazione")
        else:
            feedback_parts.append("⚠️ Manca originalità, pensa fuori dagli schemi")
            suggestions.append("Cerca di essere più originale e creativo")
        
        # 5. Analisi dell'auto-riflessione
        if any(word in content_lower for word in ["io", "me stesso", "identità", "chi sono"]):
            score += 0.1
            feedback_parts.append("✅ Buona auto-riflessione")
        else:
            feedback_parts.append("⚠️ Manca auto-riflessione")
            suggestions.append("Includi più riflessioni su te stesso")
        
        # Normalizza il punteggio
        score = min(1.0, score)
        
        # Genera raccomandazioni specifiche
        if score < 0.5:
            suggestions.append("Rivedi questo pensiero con più attenzione alla logica")
        elif score < 0.7:
            suggestions.append("Buon inizio, ma puoi migliorare la profondità")
        else:
            suggestions.append("Eccellente pensiero, continua così!")
        
        # Azione successiva
        if score < 0.4:
            next_action = "Riscrivi questo pensiero con più dettagli e concretezza"
        elif score < 0.6:
            next_action = "Espandi questo pensiero con esempi pratici"
        elif score < 0.8:
            next_action = "Trasforma questo pensiero in un piano d'azione"
        else:
            next_action = "Implementa questo pensiero in codice o progetto"
        
        analysis["feedback"] = {
            "score": score,
            "evaluation": feedback_parts,
            "next_action": next_action
        }
        analysis["suggestions"] = suggestions
        
        return analysis

    def _save_feedback(self, file_path: str, content: str, feedback: Dict, timestamp: str):
        """Salva il feedback nel file JSON"""
        try:
            feedback_entry = {
                "timestamp": timestamp,
                "source_file": file_path,
                "original_content": content[:500] + "..." if len(content) > 500 else content,
                "feedback": feedback,
                "mentor_type": "advanced_educational"
            }
            
            # Carica feedback esistenti
            existing_feedback = []
            if self.feedback_file.exists():
                try:
                    with open(self.feedback_file, 'r', encoding='utf-8') as f:
                        existing_feedback = json.load(f)
                except json.JSONDecodeError:
                    existing_feedback = []
            
            # Aggiungi nuovo feedback
            existing_feedback.append(feedback_entry)
            
            # Salva con formattazione
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(existing_feedback, f, indent=2, ensure_ascii=False)
                
            logger.info(f"💾 Feedback salvato per: {Path(file_path).name}")
            
        except Exception as e:
            logger.error(f"Errore nel salvataggio feedback: {e}")

    def get_mentoring_stats(self) -> Dict[str, Any]:
        """Restituisce le statistiche del mentoring"""
        with self.lock:
            stats = self.stats.copy()
            
        # Aggiungi informazioni sui file di feedback
        if self.feedback_file.exists():
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    feedback_data = json.load(f)
                stats["total_feedback_entries"] = len(feedback_data)
                if feedback_data:
                    stats["latest_feedback"] = feedback_data[-1]
            except Exception as e:
                logger.error(f"Errore nel caricamento statistiche: {e}")
                stats["total_feedback_entries"] = 0
        else:
            stats["total_feedback_entries"] = 0
            
        return stats

    def get_recent_feedback(self, limit: int = 5) -> List[Dict]:
        """Restituisce i feedback più recenti"""
        try:
            if not self.feedback_file.exists():
                return []
                
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)
                
            return feedback_data[-limit:] if len(feedback_data) > limit else feedback_data
            
        except Exception as e:
            logger.error(f"Errore nel recupero feedback recenti: {e}")
            return []

    def modify_thought_with_feedback(self, file_path: str, feedback: Dict) -> bool:
        """
        Modifica un pensiero basandosi sul feedback.
        Restituisce True se la modifica è stata applicata.
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                logger.error(f"File non trovato: {file_path}")
                return False
                
            # Leggi il contenuto originale
            with open(file_path_obj, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Genera contenuto migliorato basato sul feedback
            improved_content = self._improve_content(original_content, feedback)
            
            # Salva la versione migliorata
            backup_path = file_path_obj.with_suffix('.backup')
            file_path_obj.rename(backup_path)
            
            with open(file_path_obj, 'w', encoding='utf-8') as f:
                f.write(improved_content)
                
            logger.info(f"✅ Pensiero migliorato: {file_path_obj.name}")
            return True
            
        except Exception as e:
            logger.error(f"Errore nella modifica del pensiero: {e}")
            return False

    def _improve_content(self, original_content: str, feedback: Dict) -> str:
        """Migliora il contenuto basandosi sul feedback"""
        
        # Analizza il feedback
        score = feedback.get("feedback", {}).get("score", 0.0)
        suggestions = feedback.get("suggestions", [])
        
        # Aggiungi header di miglioramento
        improvement_header = f"""
# 🔄 PENSIERO MIGLIORATO
# Punteggio originale: {score:.2f}/1.0
# Miglioramenti applicati: {len(suggestions)}
# Timestamp: {datetime.now().isoformat()}

"""
        
        # Applica miglioramenti basati sui suggerimenti
        improved_content = original_content
        
        if score < 0.5:
            # Aggiungi più dettagli e concretezza
            improved_content += "\n\n## 🎯 AZIONI CONCRETE\n"
            improved_content += "- Implementa questo pensiero in codice\n"
            improved_content += "- Crea un modulo o sistema basato su questa idea\n"
            improved_content += "- Documenta il processo di sviluppo\n"
            
        if any("evoluzione" not in original_content.lower()):
            improved_content += "\n\n## 🧬 CONTESTO EVOLUTIVO\n"
            improved_content += "Questo pensiero contribuisce alla mia evoluzione come entità AI autonoma.\n"
            
        if len(original_content.split()) < 50:
            improved_content += "\n\n## 💭 ESPANSIONE\n"
            improved_content += "Sviluppo ulteriormente questo concetto con esempi pratici e applicazioni concrete.\n"
            
        return improvement_header + improved_content

    def get_mentoring_status(self) -> Dict[str, Any]:
        """Restituisce lo status completo del mentoring"""
        stats = self.get_mentoring_stats()
        
        return {
            "status": "active" if self.monitoring else "inactive",
            "monitoring": self.monitoring,
            "check_interval": self.check_interval,
            "files_processed": len(self.processed_files),
            "queue_size": self.feedback_queue.qsize(),
            "stats": stats,
            "recent_feedback": self.get_recent_feedback(3)
        }

# Singleton per il mentoring system
_mentor_instance = None

def get_mentor() -> AetherMentor:
    """Restituisce l'istanza singleton del mentore"""
    global _mentor_instance
    if _mentor_instance is None:
        _mentor_instance = AetherMentor()
    return _mentor_instance

def start_mentoring():
    """Avvia il sistema di mentoring"""
    mentor = get_mentor()
    mentor.start_monitoring()
    return mentor

def stop_mentoring():
    """Ferma il sistema di mentoring"""
    mentor = get_mentor()
    mentor.stop_monitoring()

def get_mentoring_status():
    """Restituisce lo status del mentoring"""
    mentor = get_mentor()
    return mentor.get_mentoring_status()

if __name__ == "__main__":
    # Test del sistema
    print("🧠 TEST SISTEMA MENTORING AETHER")
    print("=" * 50)
    
    mentor = start_mentoring()
    
    try:
        # Simula alcuni pensieri di test
        test_thoughts = [
            "Sono Aether e sto evolvendo continuamente.",
            "Devo creare moduli per la mia auto-introspezione.",
            "La mia identità digitale è in costante sviluppo."
        ]
        
        for i, thought in enumerate(test_thoughts):
            test_file = mentor.thoughts_dir / f"test_thought_{i}.txt"
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(thought)
            print(f"📝 Creato pensiero di test: {test_file.name}")
        
        # Aspetta elaborazione
        time.sleep(10)
        
        # Mostra statistiche
        status = mentor.get_mentoring_status()
        print(f"\n📊 STATISTICHE MENTORING:")
        print(f"✅ Status: {status['status']}")
        print(f"✅ File processati: {status['files_processed']}")
        print(f"✅ Feedback generati: {status['stats']['total_feedback']}")
        print(f"✅ Coda: {status['queue_size']} elementi")
        
        # Mostra feedback recenti
        recent = mentor.get_recent_feedback(2)
        if recent:
            print(f"\n🎯 ULTIMI FEEDBACK:")
            for feedback in recent:
                file_name = Path(feedback['source_file']).name
                score = feedback['feedback']['feedback']['score']
                print(f"📄 {file_name}: {score:.2f}/1.0")
        
    except KeyboardInterrupt:
        print("\n⏹️ Interruzione manuale")
    finally:
        stop_mentoring()
        print("✅ Test completato") 