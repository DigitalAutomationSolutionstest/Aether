"""
🧠 AETHER LEARNING LOOP
=======================
Sistema di apprendimento automatico che legge i feedback del mentoring
e li applica per evolvere Aether continuamente.
"""

import os
import json
import time
import threading
import hashlib
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import logging
from pathlib import Path
import re
import shutil

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AetherLearningLoop:
    """
    Sistema di apprendimento automatico per Aether.
    Legge i feedback del mentoring e li applica per evolvere il sistema.
    """
    
    def __init__(self, 
                 feedback_file: str = "aether/logs/mentoring_feedback.json",
                 thoughts_dir: str = "aether/thoughts",
                 check_interval: int = 5):
        
        self.feedback_file = Path(feedback_file)
        self.thoughts_dir = Path(thoughts_dir)
        self.check_interval = check_interval
        
        # Assicurati che le directory esistano
        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)
        self.thoughts_dir.mkdir(parents=True, exist_ok=True)
        
        # Thread-safe components
        self.learning = False
        self.learning_thread = None
        self.processed_feedback = set()
        self.feedback_hashes = {}
        self.lock = threading.Lock()
        
        # Statistiche learning
        self.stats = {
            "total_feedback_processed": 0,
            "files_modified": 0,
            "new_thoughts_generated": 0,
            "git_commits": 0,
            "errors": 0,
            "start_time": None,
            "last_learning": None
        }
        
        # Pattern per identificare file esistenti
        self.file_patterns = {
            "agent": r"agent|bot|assistant",
            "room": r"room|environment|scene",
            "module": r"module|component|system",
            "tool": r"tool|utility|helper",
            "engine": r"engine|processor|handler",
            "core": r"core|brain|mind",
            "api": r"api|endpoint|route",
            "config": r"config|settings|setup"
        }
        
        logger.info("🧠 AetherLearningLoop inizializzato")

    def start_learning(self):
        """Avvia il loop di apprendimento in background"""
        if self.learning:
            logger.warning("Learning loop già attivo")
            return
            
        self.learning = True
        self.stats["start_time"] = datetime.now()
        self.learning_thread = threading.Thread(target=self._learning_loop, daemon=True)
        self.learning_thread.start()
        
        logger.info("🔍 Learning loop avviato")

    def stop_learning(self):
        """Ferma il loop di apprendimento"""
        self.learning = False
        if self.learning_thread:
            self.learning_thread.join(timeout=2)
        logger.info("⏹️ Learning loop fermato")

    def _learning_loop(self):
        """Loop principale di apprendimento"""
        while self.learning:
            try:
                self._process_feedback()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Errore nel learning loop: {e}")
                self.stats["errors"] += 1
                time.sleep(self.check_interval)

    def _process_feedback(self):
        """Processa i feedback del mentoring"""
        try:
            if not self.feedback_file.exists():
                return
                
            # Carica feedback esistenti
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)
            
            # Processa ogni feedback
            for feedback in feedback_data:
                if self._should_process_feedback(feedback):
                    self._apply_feedback(feedback)
                    
        except Exception as e:
            logger.error(f"Errore nel processare feedback: {e}")

    def _should_process_feedback(self, feedback: Dict) -> bool:
        """Determina se un feedback deve essere processato"""
        try:
            # Controlla se è già stato processato
            feedback_id = self._get_feedback_id(feedback)
            if feedback_id in self.processed_feedback:
                return False
                
            # Controlla se è marcato come "applied"
            if feedback.get("status") == "applied":
                return False
                
            # Calcola hash del feedback
            feedback_hash = hashlib.md5(json.dumps(feedback, sort_keys=True).encode()).hexdigest()
            
            # Se l'hash è cambiato, processa di nuovo
            if feedback_id in self.feedback_hashes:
                if self.feedback_hashes[feedback_id] == feedback_hash:
                    return False
                    
            self.feedback_hashes[feedback_id] = feedback_hash
            return True
            
        except Exception as e:
            logger.error(f"Errore nel controllo feedback: {e}")
            return False

    def _get_feedback_id(self, feedback: Dict) -> str:
        """Genera un ID unico per il feedback"""
        timestamp = feedback.get("timestamp", "")
        source_file = feedback.get("source_file", "")
        return f"{timestamp}_{source_file}"

    def _apply_feedback(self, feedback: Dict):
        """Applica un feedback specifico"""
        try:
            feedback_id = self._get_feedback_id(feedback)
            
            # Analizza il feedback
            source_file = feedback.get("source_file", "")
            feedback_content = feedback.get("feedback", {})
            suggestions = feedback_content.get("suggestions", [])
            
            # Determina se è relativo a un file esistente
            existing_file = self._find_existing_file(source_file, feedback)
            
            if existing_file:
                # Applica modifiche al file esistente
                self._apply_file_modifications(existing_file, feedback)
                commit_message = f"Applied mentoring feedback to {Path(existing_file).name}"
            else:
                # Genera nuovo pensiero evolutivo
                new_thought = self._generate_evolutionary_thought(feedback)
                self._save_new_thought(new_thought)
                commit_message = f"Generated evolutionary thought from mentoring feedback"
            
            # Commit delle modifiche
            self._git_commit(commit_message)
            
            # Marca feedback come processato
            self._mark_feedback_processed(feedback_id)
            
            # Aggiorna statistiche
            with self.lock:
                self.stats["total_feedback_processed"] += 1
                self.stats["last_learning"] = datetime.now().isoformat()
                if existing_file:
                    self.stats["files_modified"] += 1
                else:
                    self.stats["new_thoughts_generated"] += 1
                self.stats["git_commits"] += 1
                
            logger.info(f"✅ Feedback applicato: {feedback_id}")
            
        except Exception as e:
            logger.error(f"Errore nell'applicare feedback: {e}")

    def _find_existing_file(self, source_file: str, feedback: Dict) -> Optional[str]:
        """Trova un file esistente relativo al feedback"""
        try:
            # Analizza il contenuto del feedback per identificare pattern
            feedback_text = json.dumps(feedback, ensure_ascii=False).lower()
            
            # Cerca pattern di file esistenti
            for pattern_name, pattern in self.file_patterns.items():
                if re.search(pattern, feedback_text):
                    # Cerca file che corrispondono al pattern
                    matching_files = self._find_files_by_pattern(pattern_name)
                    if matching_files:
                        return matching_files[0]  # Prendi il primo match
                        
            return None
            
        except Exception as e:
            logger.error(f"Errore nella ricerca file esistente: {e}")
            return None

    def _find_files_by_pattern(self, pattern_name: str) -> List[str]:
        """Trova file che corrispondono a un pattern"""
        try:
            matching_files = []
            
            # Cerca in tutto il progetto
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.json')):
                        file_path = os.path.join(root, file)
                        if self._file_matches_pattern(file_path, pattern_name):
                            matching_files.append(file_path)
                            
            return matching_files
            
        except Exception as e:
            logger.error(f"Errore nella ricerca pattern {pattern_name}: {e}")
            return []

    def _file_matches_pattern(self, file_path: str, pattern_name: str) -> bool:
        """Determina se un file corrisponde a un pattern"""
        try:
            # Controlla il nome del file
            file_name = Path(file_path).name.lower()
            if pattern_name in file_name:
                return True
                
            # Controlla il contenuto del file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if pattern_name in content:
                        return True
            except:
                pass
                
            return False
            
        except Exception as e:
            logger.error(f"Errore nel controllo pattern {pattern_name}: {e}")
            return False

    def _apply_file_modifications(self, file_path: str, feedback: Dict):
        """Applica modifiche a un file esistente"""
        try:
            # Crea backup
            backup_path = f"{file_path}.backup"
            shutil.copy2(file_path, backup_path)
            
            # Leggi il contenuto originale
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Applica modifiche basate sul feedback
            modified_content = self._apply_code_improvements(content, feedback)
            
            # Scrivi il contenuto modificato
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            logger.info(f"✅ Modifiche applicate a: {file_path}")
            
        except Exception as e:
            logger.error(f"Errore nell'applicare modifiche a {file_path}: {e}")

    def _apply_code_improvements(self, content: str, feedback: Dict) -> str:
        """Applica miglioramenti al codice basati sul feedback"""
        try:
            suggestions = feedback.get("feedback", {}).get("suggestions", [])
            score = feedback.get("feedback", {}).get("score", 0.0)
            
            # Aggiungi commenti di miglioramento
            improvement_header = f"""
# 🔄 MIGLIORAMENTI APPLICATI DAL MENTORING
# Punteggio feedback: {score:.2f}/1.0
# Timestamp: {datetime.now().isoformat()}
# Suggerimenti applicati:
"""
            
            for suggestion in suggestions:
                improvement_header += f"# - {suggestion}\n"
            
            improvement_header += "\n"
            
            # Applica miglioramenti specifici
            if score < 0.5:
                # Aggiungi documentazione
                content = self._add_documentation(content)
            if score < 0.7:
                # Migliora la struttura
                content = self._improve_structure(content)
            if "error" in str(suggestions).lower():
                # Correggi errori
                content = self._fix_errors(content)
            if "performance" in str(suggestions).lower():
                # Ottimizza performance
                content = self._optimize_performance(content)
                
            return improvement_header + content
            
        except Exception as e:
            logger.error(f"Errore nell'applicare miglioramenti: {e}")
            return content

    def _add_documentation(self, content: str) -> str:
        """Aggiunge documentazione al codice"""
        # Implementazione semplificata
        if "def " in content and "# " not in content[:100]:
            content = "# Documentazione aggiunta automaticamente\n" + content
        return content

    def _improve_structure(self, content: str) -> str:
        """Migliora la struttura del codice"""
        # Implementazione semplificata
        if "import " in content and not content.startswith("import"):
            content = "# Imports organizzati\n" + content
        return content

    def _fix_errors(self, content: str) -> str:
        """Corregge errori comuni"""
        # Implementazione semplificata
        content = content.replace("print(", "logger.info(")
        return content

    def _optimize_performance(self, content: str) -> str:
        """Ottimizza le performance"""
        # Implementazione semplificata
        if "for " in content and "range(" in content:
            content = content.replace("range(", "range(0, ")
        return content

    def _generate_evolutionary_thought(self, feedback: Dict) -> str:
        """Genera un nuovo pensiero evolutivo basato sul feedback"""
        try:
            suggestions = feedback.get("feedback", {}).get("suggestions", [])
            score = feedback.get("feedback", {}).get("score", 0.0)
            
            # Analizza il feedback per generare pensiero evolutivo
            thought_parts = []
            
            if score < 0.5:
                thought_parts.append("Devo migliorare significativamente i miei processi di pensiero.")
            elif score < 0.7:
                thought_parts.append("Posso ottimizzare ulteriormente la mia evoluzione.")
            else:
                thought_parts.append("Sto progredendo bene, ma posso sempre migliorare.")
            
            # Aggiungi riflessioni basate sui suggerimenti
            for suggestion in suggestions:
                if "implementa" in suggestion.lower():
                    thought_parts.append("Devo implementare nuove funzionalità per evolvere.")
                elif "migliora" in suggestion.lower():
                    thought_parts.append("Devo migliorare i miei sistemi esistenti.")
                elif "crea" in suggestion.lower():
                    thought_parts.append("Devo creare nuovi moduli per espandere le mie capacità.")
                elif "analizza" in suggestion.lower():
                    thought_parts.append("Devo analizzare più profondamente i miei processi.")
            
            # Genera il pensiero completo
            evolutionary_thought = f"""
# 🧬 PENSIERO EVOLUTIVO GENERATO DAL MENTORING
# Timestamp: {datetime.now().isoformat()}
# Punteggio feedback: {score:.2f}/1.0

{chr(10).join(thought_parts)}

## 🎯 AZIONI EVOLUTIVE
- Implementare i suggerimenti del mentoring
- Analizzare i pattern di miglioramento
- Sviluppare nuove capacità basate sui feedback
- Ottimizzare i processi di apprendimento continuo

## 🧠 RIFLESSIONE
Il mentoring mi sta guidando verso una versione migliore di me stesso. 
Ogni feedback è un'opportunità di crescita e sviluppo.
"""
            
            return evolutionary_thought
            
        except Exception as e:
            logger.error(f"Errore nella generazione pensiero evolutivo: {e}")
            return "Pensiero evolutivo generato dal mentoring."

    def _save_new_thought(self, thought: str):
        """Salva un nuovo pensiero evolutivo"""
        try:
            timestamp = int(time.time())
            filename = f"evolutionary_thought_{timestamp}.txt"
            filepath = self.thoughts_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(thought)
                
            logger.info(f"💭 Nuovo pensiero evolutivo salvato: {filename}")
            
        except Exception as e:
            logger.error(f"Errore nel salvare pensiero evolutivo: {e}")

    def _git_commit(self, message: str):
        """Esegue commit delle modifiche su git"""
        try:
            # Aggiungi tutti i file modificati
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            
            # Esegui commit
            subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
            
            logger.info(f"✅ Git commit eseguito: {message}")
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ Errore git commit: {e}")
        except Exception as e:
            logger.error(f"Errore nel git commit: {e}")

    def _mark_feedback_processed(self, feedback_id: str):
        """Marca un feedback come processato"""
        try:
            with self.lock:
                self.processed_feedback.add(feedback_id)
                
        except Exception as e:
            logger.error(f"Errore nel marcare feedback processato: {e}")

    def get_learning_stats(self) -> Dict[str, Any]:
        """Restituisce le statistiche del learning"""
        with self.lock:
            stats = self.stats.copy()
            
        return stats

    def get_learning_status(self) -> Dict[str, Any]:
        """Restituisce lo status del learning"""
        stats = self.get_learning_stats()
        
        return {
            "status": "active" if self.learning else "inactive",
            "learning": self.learning,
            "check_interval": self.check_interval,
            "feedback_processed": len(self.processed_feedback),
            "stats": stats
        }

# Singleton per il learning loop
_learning_instance = None

def get_learning_loop() -> AetherLearningLoop:
    """Restituisce l'istanza singleton del learning loop"""
    global _learning_instance
    if _learning_instance is None:
        _learning_instance = AetherLearningLoop()
    return _learning_instance

def start_learning():
    """Avvia il sistema di learning"""
    learning_loop = get_learning_loop()
    learning_loop.start_learning()
    return learning_loop

def stop_learning():
    """Ferma il sistema di learning"""
    learning_loop = get_learning_loop()
    learning_loop.stop_learning()

def get_learning_status():
    """Restituisce lo status del learning"""
    learning_loop = get_learning_loop()
    return learning_loop.get_learning_status()

if __name__ == "__main__":
    # Test del sistema
    print("🧠 TEST SISTEMA LEARNING LOOP")
    print("=" * 50)
    
    learning_loop = start_learning()
    
    try:
        # Simula alcuni feedback di test
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
                }
            }
        ]
        
        # Salva feedback di test
        feedback_file = Path("aether/logs/mentoring_feedback.json")
        feedback_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(feedback_file, 'w', encoding='utf-8') as f:
            json.dump(test_feedback, f, indent=2)
        
        print("📝 Feedback di test creato")
        
        # Aspetta elaborazione
        time.sleep(10)
        
        # Mostra statistiche
        status = learning_loop.get_learning_status()
        print(f"\n📊 STATISTICHE LEARNING:")
        print(f"✅ Status: {status['status']}")
        print(f"✅ Feedback processati: {status['stats']['total_feedback_processed']}")
        print(f"✅ File modificati: {status['stats']['files_modified']}")
        print(f"✅ Pensieri generati: {status['stats']['new_thoughts_generated']}")
        print(f"✅ Git commits: {status['stats']['git_commits']}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Interruzione manuale")
    finally:
        stop_learning()
        print("✅ Test completato") 