# aether/git_tools.py

import subprocess
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def commit_and_push(message: str):
    """Committa e pusha le modifiche su Git"""
    try:
        # Aggiungi tutti i file
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Committa con il messaggio
        subprocess.run(['git', 'commit', '-m', message], check=True)
        
        # Pusha le modifiche
        subprocess.run(['git', 'push'], check=True)
        
        logger.info(f"✅ Git: {message}")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Errore Git: {e}")
    except Exception as e:
        logger.error(f"❌ Errore Git: {e}")

def get_git_status():
    """Restituisce lo status di Git"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        logger.error(f"❌ Errore nel controllare status Git: {e}")
        return ""

def get_last_commit():
    """Restituisce l'ultimo commit"""
    try:
        result = subprocess.run(['git', 'log', '-1', '--oneline'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        logger.error(f"❌ Errore nel controllare ultimo commit: {e}")
        return "" 