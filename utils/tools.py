"""
Tools - Strumenti e utilità per l'applicazione
Fornisce funzioni di utilità, logging e altri strumenti comuni.
"""

import logging
import logging.handlers
import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

class Logger:
    """Sistema di logging avanzato per l'agente."""
    
    def __init__(self, name: str = "InvaderAgent"):
        """Inizializza il logger."""
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Evita duplicazione dei handler
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configura i handler per il logging."""
        # Handler per console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Handler per file
        log_dir = Path("data/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "agent.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log di debug."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log informativo."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log di avvertimento."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log di errore."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critico."""
        self.logger.critical(message)

class DataManager:
    """Gestisce il salvataggio e caricamento dei dati."""
    
    def __init__(self, data_dir: str = "data"):
        """Inizializza il gestore dati."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_data(self, filename: str, data: Any, compress: bool = False):
        """Salva dati su file."""
        file_path = self.data_dir / filename
        
        try:
            if isinstance(data, (dict, list)):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            
            print(f"💾 Dati salvati: {file_path}")
        except Exception as e:
            print(f"⚠️ Errore nel salvataggio dei dati: {e}")
    
    def load_data(self, filename: str, default: Any = None):
        """Carica dati da file."""
        file_path = self.data_dir / filename
        
        if not file_path.exists():
            return default
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Prova a caricare come JSON
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return content
        except Exception as e:
            print(f"⚠️ Errore nel caricamento dei dati: {e}")
            return default
    
    def backup_data(self, filename: str, backup_suffix: str = None):
        """Crea un backup dei dati."""
        if backup_suffix is None:
            backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        source_file = self.data_dir / filename
        backup_file = self.data_dir / f"{filename}.backup_{backup_suffix}"
        
        if source_file.exists():
            try:
                import shutil
                shutil.copy2(source_file, backup_file)
                print(f"💾 Backup creato: {backup_file}")
            except Exception as e:
                print(f"⚠️ Errore nella creazione del backup: {e}")

class PerformanceMonitor:
    """Monitora le performance dell'applicazione."""
    
    def __init__(self):
        """Inizializza il monitor di performance."""
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, name: str):
        """Avvia un timer."""
        self.start_times[name] = time.time()
    
    def end_timer(self, name: str) -> float:
        """Termina un timer e restituisce il tempo trascorso."""
        if name in self.start_times:
            elapsed = time.time() - self.start_times[name]
            self.metrics[name] = elapsed
            del self.start_times[name]
            return elapsed
        return 0.0
    
    def get_metrics(self) -> Dict[str, float]:
        """Restituisce tutte le metriche."""
        return self.metrics.copy()
    
    def reset_metrics(self):
        """Resetta tutte le metriche."""
        self.metrics.clear()
        self.start_times.clear()

class TextProcessor:
    """Processa e analizza il testo."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Pulisce il testo da caratteri speciali."""
        import re
        # Rimuove caratteri speciali ma mantiene spazi e punteggiatura
        cleaned = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        return cleaned.strip()
    
    @staticmethod
    def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
        """Estrae le parole chiave dal testo."""
        import re
        from collections import Counter
        
        # Pulisce il testo
        cleaned_text = TextProcessor.clean_text(text.lower())
        
        # Rimuove parole comuni (stop words)
        stop_words = {
            'il', 'la', 'lo', 'gli', 'le', 'di', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra',
            'a', 'e', 'o', 'ma', 'se', 'che', 'come', 'dove', 'quando', 'perché', 'chi',
            'un', 'una', 'uno', 'questo', 'questa', 'questi', 'queste', 'quello', 'quella',
            'sono', 'è', 'era', 'stato', 'essere', 'avere', 'ha', 'hanno', 'aveva'
        }
        
        # Estrae le parole
        words = re.findall(r'\b\w+\b', cleaned_text)
        
        # Filtra le stop words e parole troppo corte
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Conta le occorrenze
        word_counts = Counter(keywords)
        
        # Restituisce le parole più frequenti
        return [word for word, count in word_counts.most_common(max_keywords)]
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calcola la similarità tra due testi."""
        keywords1 = set(TextProcessor.extract_keywords(text1))
        keywords2 = set(TextProcessor.extract_keywords(text2))
        
        if not keywords1 or not keywords2:
            return 0.0
        
        intersection = len(keywords1.intersection(keywords2))
        union = len(keywords1.union(keywords2))
        
        return intersection / union if union > 0 else 0.0

class ConfigValidator:
    """Valida le configurazioni dell'applicazione."""
    
    @staticmethod
    def validate_config(config: Dict) -> List[str]:
        """Valida una configurazione e restituisce gli errori."""
        errors = []
        
        # Validazioni di base
        if not isinstance(config, dict):
            errors.append("La configurazione deve essere un dizionario")
            return errors
        
        # Validazioni specifiche per sezioni
        if "memory" in config:
            memory_config = config["memory"]
            if "max_short_term" in memory_config:
                if not isinstance(memory_config["max_short_term"], int) or memory_config["max_short_term"] <= 0:
                    errors.append("max_short_term deve essere un intero positivo")
            
            if "max_long_term" in memory_config:
                if not isinstance(memory_config["max_long_term"], int) or memory_config["max_long_term"] <= 0:
                    errors.append("max_long_term deve essere un intero positivo")
        
        if "brain" in config:
            brain_config = config["brain"]
            if "confidence_threshold" in brain_config:
                threshold = brain_config["confidence_threshold"]
                if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 1:
                    errors.append("confidence_threshold deve essere un numero tra 0 e 1")
        
        return errors
    
    @staticmethod
    def fix_config(config: Dict) -> Dict:
        """Corregge automaticamente una configurazione."""
        fixed_config = config.copy()
        
        # Correzioni automatiche
        if "memory" in fixed_config:
            memory = fixed_config["memory"]
            if "max_short_term" in memory and (not isinstance(memory["max_short_term"], int) or memory["max_short_term"] <= 0):
                memory["max_short_term"] = 100
            
            if "max_long_term" in memory and (not isinstance(memory["max_long_term"], int) or memory["max_long_term"] <= 0):
                memory["max_long_term"] = 1000
        
        if "brain" in fixed_config:
            brain = fixed_config["brain"]
            if "confidence_threshold" in brain:
                threshold = brain["confidence_threshold"]
                if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 1:
                    brain["confidence_threshold"] = 0.7
        
        return fixed_config 