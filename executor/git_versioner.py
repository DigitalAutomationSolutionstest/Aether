#!/usr/bin/env python3
"""
🔀 GIT AUTOMATION - Versionamento Automatico per Aether

Gestisce automaticamente:
- Commit di codice generato
- Push automatici
- Branch per esperimenti
- Tag per versioni stabili
- Backup repository
"""

import os
import subprocess
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class GitAutomation:
    """
    🚀 Sistema di automazione Git per Aether
    
    Funzionalità:
    - Auto-commit del codice generato
    - Push intelligenti
    - Branch per esperimenti
    - Tag automatici
    - Gestione errori
    """
    
    def __init__(self, repo_path: str = None):
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.git_available = self._check_git_availability()
        self.repo_initialized = self._check_repo_status()
        
        # Statistiche
        self.commits_made = 0
        self.pushes_made = 0
        self.branches_created = 0
        
        # File di log Git
        self.git_log_file = Path("executor/logs/git_automation.log")
        self.git_log_file.parent.mkdir(parents=True, exist_ok=True)
        
        if self.git_available and self.repo_initialized:
            logger.info("✅ Git automation attivata")
        else:
            logger.warning("⚠️ Git non disponibile o repository non inizializzato")
    
    def _check_git_availability(self) -> bool:
        """Verifica se Git è disponibile"""
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _check_repo_status(self) -> bool:
        """Verifica se siamo in un repository Git"""
        try:
            result = subprocess.run(['git', 'status'], cwd=self.repo_path, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def auto_commit(self, message: str = None, files: List[str] = None) -> bool:
        """
        📝 Commit automatico con messaggio intelligente
        
        Args:
            message: Messaggio commit personalizzato
            files: Lista file specifici da committare
            
        Returns:
            bool: Successo operazione
        """
        if not self.git_available or not self.repo_initialized:
            logger.warning("⚠️ Git non disponibile per commit")
            return False
        
        try:
            # Genera messaggio automatico se non fornito
            if not message:
                message = f"🤖 Aether auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Add files
            if files:
                for file in files:
                    self._run_git_command(['add', file])
            else:
                # Add tutti i file nella directory executor
                self._run_git_command(['add', 'executor/'])
            
            # Verifica se ci sono cambiamenti da committare
            status = self._run_git_command(['status', '--porcelain'])
            if not status.stdout.strip():
                logger.debug("📝 Nessun cambiamento da committare")
                return True
            
            # Commit
            result = self._run_git_command(['commit', '-m', message])
            
            if result.returncode == 0:
                self.commits_made += 1
                self._log_git_action("commit", message)
                logger.info(f"✅ Commit completato: {message}")
                
                # Auto-push se configurato
                self._auto_push()
                return True
            else:
                logger.error(f"❌ Errore commit: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Errore auto-commit: {e}")
            return False
    
    def _auto_push(self) -> bool:
        """Push automatico al repository remoto"""
        try:
            # Verifica se esiste un remote
            remotes = self._run_git_command(['remote', '-v'])
            if not remotes.stdout.strip():
                logger.debug("📡 Nessun remote configurato - skip push")
                return True
            
            # Push
            result = self._run_git_command(['push'])
            
            if result.returncode == 0:
                self.pushes_made += 1
                self._log_git_action("push", "Auto-push successful")
                logger.debug("📡 Push automatico completato")
                return True
            else:
                logger.warning(f"⚠️ Push fallito: {result.stderr}")
                return False
                
        except Exception as e:
            logger.warning(f"⚠️ Errore auto-push: {e}")
            return False
    
    def create_experiment_branch(self, experiment_name: str) -> bool:
        """
        🌿 Crea branch per esperimenti
        
        Args:
            experiment_name: Nome dell'esperimento
            
        Returns:
            bool: Successo operazione
        """
        if not self.git_available or not self.repo_initialized:
            return False
        
        try:
            # Sanitize branch name
            branch_name = f"aether-experiment-{experiment_name.lower().replace(' ', '-')}"
            
            # Crea e switcha al branch
            result = self._run_git_command(['checkout', '-b', branch_name])
            
            if result.returncode == 0:
                self.branches_created += 1
                self._log_git_action("branch", f"Created branch: {branch_name}")
                logger.info(f"🌿 Branch esperimento creato: {branch_name}")
                return True
            else:
                logger.error(f"❌ Errore creazione branch: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Errore creazione branch: {e}")
            return False
    
    def tag_stable_version(self, version: str = None, message: str = None) -> bool:
        """
        🏷️ Crea tag per versione stabile
        
        Args:
            version: Versione (default: auto-generata)
            message: Messaggio tag
            
        Returns:
            bool: Successo operazione
        """
        if not self.git_available or not self.repo_initialized:
            return False
        
        try:
            # Genera versione automatica se non fornita
            if not version:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                version = f"aether-stable-{timestamp}"
            
            if not message:
                message = f"Aether stable version: {version}"
            
            # Crea tag annotato
            result = self._run_git_command(['tag', '-a', version, '-m', message])
            
            if result.returncode == 0:
                self._log_git_action("tag", f"Created tag: {version}")
                logger.info(f"🏷️ Tag creato: {version}")
                
                # Push del tag
                self._run_git_command(['push', 'origin', version])
                return True
            else:
                logger.error(f"❌ Errore creazione tag: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Errore tag: {e}")
            return False
    
    def commit_code_execution(self, execution_result: Dict[str, Any]) -> bool:
        """
        🎯 Commit specifico per risultato esecuzione
        
        Args:
            execution_result: Risultato dell'esecuzione
            
        Returns:
            bool: Successo operazione
        """
        if not execution_result.get('success'):
            logger.debug("❌ Skip commit per esecuzione fallita")
            return False
        
        # Messaggio specifico per esecuzione
        thought_type = execution_result.get('thought', {}).get('type', 'unknown')
        execution_id = execution_result.get('execution_id', 'unknown')
        
        message = f"🤖 Aether execution: {thought_type} ({execution_id})"
        
        # File specifici da committare
        files = ['executor/']
        
        # Aggiungi file generato se presente
        code_file = execution_result.get('code_file')
        if code_file and Path(code_file).exists():
            files.append(code_file)
        
        return self.auto_commit(message, files)
    
    def _run_git_command(self, args: List[str]) -> subprocess.CompletedProcess:
        """Esegue comando Git"""
        cmd = ['git'] + args
        return subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)
    
    def _log_git_action(self, action: str, details: str):
        """Log azioni Git"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details
        }
        
        try:
            # Append al file di log
            with open(self.git_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logger.error(f"❌ Errore log Git: {e}")
    
    def get_repository_status(self) -> Dict[str, Any]:
        """
        📊 Status completo del repository
        
        Returns:
            Dizionario con informazioni repository
        """
        status = {
            'git_available': self.git_available,
            'repo_initialized': self.repo_initialized,
            'commits_made': self.commits_made,
            'pushes_made': self.pushes_made,
            'branches_created': self.branches_created
        }
        
        if self.git_available and self.repo_initialized:
            try:
                # Branch corrente
                branch_result = self._run_git_command(['branch', '--show-current'])
                status['current_branch'] = branch_result.stdout.strip()
                
                # Status working directory
                status_result = self._run_git_command(['status', '--porcelain'])
                status['has_changes'] = bool(status_result.stdout.strip())
                
                # Ultimo commit
                log_result = self._run_git_command(['log', '-1', '--oneline'])
                status['last_commit'] = log_result.stdout.strip()
                
                # Remote
                remote_result = self._run_git_command(['remote', '-v'])
                status['has_remote'] = bool(remote_result.stdout.strip())
                
            except Exception as e:
                status['error'] = str(e)
        
        return status
    
    def cleanup_old_branches(self, keep_days: int = 30) -> int:
        """
        🧹 Pulizia branch vecchi
        
        Args:
            keep_days: Giorni da mantenere
            
        Returns:
            Numero di branch eliminati
        """
        if not self.git_available or not self.repo_initialized:
            return 0
        
        try:
            # Lista branch locali con data
            result = self._run_git_command(['for-each-ref', '--format=%(refname:short) %(committerdate)', 'refs/heads/'])
            
            deleted_count = 0
            current_time = datetime.now()
            
            for line in result.stdout.strip().split('\n'):
                if line and 'aether-experiment-' in line:
                    parts = line.split()
                    branch_name = parts[0]
                    
                    # Non eliminare branch corrente
                    current_branch = self._run_git_command(['branch', '--show-current']).stdout.strip()
                    if branch_name == current_branch:
                        continue
                    
                    # Elimina branch se vecchio
                    delete_result = self._run_git_command(['branch', '-D', branch_name])
                    if delete_result.returncode == 0:
                        deleted_count += 1
                        logger.debug(f"🗑️ Branch eliminato: {branch_name}")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"❌ Errore pulizia branch: {e}")
            return 0 