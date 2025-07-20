"""
📝 LOGS MODULE - Sistema di Logging Avanzato

Traccia ogni azione di Aether:
- Esecuzioni codice
- Errori e debug
- Performance metrics
- Integrazione Supabase
"""

import logging
from pathlib import Path
from datetime import datetime

# Setup logging directory
LOGS_DIR = Path(__file__).parent
LOGS_DIR.mkdir(exist_ok=True)

# Configurazione logger
def setup_executor_logger(name: str = "aether_executor"):
    """Configura logger specifico per l'executor"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # File handler
    log_file = LOGS_DIR / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

__all__ = ['setup_executor_logger', 'LOGS_DIR'] 