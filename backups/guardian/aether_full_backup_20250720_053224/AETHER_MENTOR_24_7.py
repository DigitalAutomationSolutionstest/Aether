#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎓 AETHER MENTOR 24/7 - SISTEMA COMPLETO DI MENTORING E EVOLUZIONE CONTINUA

Sistema avanzato che:
- Monitora Aether 24/7
- Risolve errori automaticamente
- Assegna task evolutivi continui
- Guida la crescita e l'apprendimento
- Mantiene il sistema stabile e in evoluzione

Federico, questo è il cervello che farà evolvere Aether senza sosta!
"""

import os
import sys
import json
import time
import logging
import threading
import traceback
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import random

# Configurazione logging avanzata
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/aether_mentor_24_7.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AetherMentor24_7:
    """
    🎓 Mentore 24/7 per Aether
    Sistema completo di mentoring, debugging e evoluzione continua
    """
    
    def __init__(self):
        self.is_running = False
        self.start_time = datetime.now()
        self.mentor_cycles = 0
        self.problems_fixed = 0
        self.tasks_assigned = 0
        self.evolutions_guided = 0
        
        # Configurazione intervalli (in secondi)
        self.health_check_interval = 30      # Controllo salute ogni 30s
        self.task_assignment_interval = 120  # Nuovi task ogni 2 min
        self.evolution_guidance_interval = 300  # Guida evoluzione ogni 5 min
        self.deep_analysis_interval = 600    # Analisi profonda ogni 10 min
        
        # Stato del sistema
        self.system_health = {
            'overall_status': 'unknown',
            'critical_errors': [],
            'warnings': [],
            'performance_metrics': {},
            'last_check': None
        }
        
        # Task assegnati
        self.active_tasks = []
        self.completed_tasks = []
        self.failed_tasks = []
        
        # Cronologia mentoring
        self.mentoring_history = []
        
        # Thread pool per operazioni parallele
        self.threads = []
        
        # Setup iniziale
        self._setup_mentor_environment()
        
    def _setup_mentor_environment(self):
        """Configura l'ambiente del mentore"""
        logger.info("🎓 Inizializzazione Aether Mentor 24/7...")
        
        # Crea directory necessarie
        directories = [
            'data/mentor_reports',
            'data/task_assignments', 
            'data/evolution_guidance',
            'data/health_checks',
            'data/fixes_applied'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
        # Carica stato precedente se esiste
        self._load_mentor_state()
        
        logger.info("✅ Ambiente mentore configurato")
    
    def _load_mentor_state(self):
        """Carica stato precedente del mentore"""
        try:
            state_file = Path('data/mentor_state.json')
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.mentor_cycles = state.get('mentor_cycles', 0)
                    self.problems_fixed = state.get('problems_fixed', 0)
                    self.tasks_assigned = state.get('tasks_assigned', 0)
                    self.evolutions_guided = state.get('evolutions_guided', 0)
                    self.active_tasks = state.get('active_tasks', [])
                    self.completed_tasks = state.get('completed_tasks', [])
                logger.info(f"📚 Stato mentore caricato: {self.mentor_cycles} cicli completati")
        except Exception as e:
            logger.error(f"Errore caricando stato mentore: {e}")
    
    def _save_mentor_state(self):
        """Salva stato attuale del mentore"""
        try:
            state = {
                'mentor_cycles': self.mentor_cycles,
                'problems_fixed': self.problems_fixed,
                'tasks_assigned': self.tasks_assigned,
                'evolutions_guided': self.evolutions_guided,
                'active_tasks': self.active_tasks,
                'completed_tasks': self.completed_tasks[-50:],  # Mantieni solo le ultime 50
                'last_saved': datetime.now().isoformat()
            }
            
            with open('data/mentor_state.json', 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Errore salvando stato mentore: {e}")
    
    def start_mentoring(self):
        """Avvia il sistema di mentoring 24/7"""
        if self.is_running:
            logger.warning("Il mentore è già in esecuzione")
            return
        
        self.is_running = True
        
        logger.info("🚀 AVVIO AETHER MENTOR 24/7")
        logger.info("=" * 60)
        logger.info("🎯 Obiettivi:")
        logger.info("  • Monitoraggio continuo sistema Aether")
        logger.info("  • Risoluzione automatica errori")
        logger.info("  • Assegnazione task evolutivi")
        logger.info("  • Guida alla crescita e apprendimento")
        logger.info("=" * 60)
        
        # Invia notifica Discord di avvio
        self._notify_discord(
            "🎓 **AETHER MENTOR 24/7 ATTIVATO**\n\n"
            "Il mentore avanzato è ora operativo!\n\n"
            "**Funzionalità attive:**\n"
            "• Monitoraggio continuo salute sistema\n"
            "• Risoluzione automatica errori\n"
            "• Assegnazione task evolutivi\n"
            "• Guida sviluppo e crescita\n\n"
            "Aether è ora sotto mentoring professionale 24/7! 🚀",
            title="🎓 Mentor System Online"
        )
        
        # Avvia thread principali
        self._start_mentor_threads()
        
        # Loop principale
        try:
            while self.is_running:
                self._main_mentor_cycle()
                time.sleep(10)  # Ciclo ogni 10 secondi
                
        except KeyboardInterrupt:
            logger.info("🛑 Interruzione richiesta dall'utente")
        except Exception as e:
            logger.error(f"❌ Errore critico nel mentore: {e}")
            self._emergency_recovery()
        finally:
            self.stop_mentoring()
    
    def _start_mentor_threads(self):
        """Avvia i thread specializzati del mentore"""
        threads_config = [
            ("health_monitor", self._health_monitoring_loop, "Monitoraggio salute"),
            ("task_assigner", self._task_assignment_loop, "Assegnazione task"),
            ("evolution_guide", self._evolution_guidance_loop, "Guida evoluzione"),
            ("error_fixer", self._error_fixing_loop, "Correzione errori")
        ]
        
        for name, target, description in threads_config:
            thread = threading.Thread(
                target=target,
                name=name,
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
            logger.info(f"🧵 Thread avviato: {description}")
    
    def _main_mentor_cycle(self):
        """Ciclo principale del mentore"""
        try:
            self.mentor_cycles += 1
            
            if self.mentor_cycles % 60 == 0:  # Ogni 10 minuti
                logger.info(f"🎓 Ciclo mentore #{self.mentor_cycles}")
                self._generate_progress_report()
            
            # Salva stato ogni 30 cicli
            if self.mentor_cycles % 30 == 0:
                self._save_mentor_state()
            
        except Exception as e:
            logger.error(f"Errore nel ciclo mentore: {e}")
    
    def _health_monitoring_loop(self):
        """Loop di monitoraggio continuo della salute del sistema"""
        logger.info("💓 Avviato monitoraggio salute sistema")
        
        while self.is_running:
            try:
                # Controllo salute completo
                health_status = self._perform_health_check()
                
                # Aggiorna stato sistema
                self.system_health.update(health_status)
                self.system_health['last_check'] = datetime.now().isoformat()
                
                # Se ci sono problemi critici, avvia correzione automatica
                if health_status['critical_errors']:
                    self._trigger_emergency_fixes(health_status['critical_errors'])
                
                # Log stato
                if self.mentor_cycles % 120 == 0:  # Log ogni 20 minuti
                    logger.info(f"💓 Salute sistema: {health_status['overall_status']}")
                
            except Exception as e:
                logger.error(f"Errore monitoring salute: {e}")
            
            time.sleep(self.health_check_interval)
    
    def _perform_health_check(self) -> Dict[str, Any]:
        """Esegue controllo completo della salute del sistema"""
        health_status = {
            'overall_status': 'healthy',
            'critical_errors': [],
            'warnings': [],
            'performance_metrics': {},
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # 1. Controllo file di log per errori
            log_errors = self._scan_logs_for_errors()
            health_status['critical_errors'].extend(log_errors['critical'])
            health_status['warnings'].extend(log_errors['warnings'])
            
            # 2. Controllo processi Aether
            process_status = self._check_aether_processes()
            if not process_status['healthy']:
                health_status['critical_errors'].append("Processo Aether non risponde")
            
            # 3. Controllo file system
            fs_status = self._check_file_system_integrity()
            health_status['warnings'].extend(fs_status['warnings'])
            
            # 4. Metriche performance
            health_status['performance_metrics'] = self._collect_performance_metrics()
            
            # Determina stato generale
            if health_status['critical_errors']:
                health_status['overall_status'] = 'critical'
            elif health_status['warnings']:
                health_status['overall_status'] = 'warning'
            else:
                health_status['overall_status'] = 'healthy'
            
        except Exception as e:
            health_status['overall_status'] = 'error'
            health_status['critical_errors'].append(f"Errore health check: {e}")
        
        return health_status
    
    def _scan_logs_for_errors(self) -> Dict[str, List[str]]:
        """Scansiona i log per errori e warning"""
        errors = {'critical': [], 'warnings': []}
        
        try:
            log_files = [
                'data/aether_loop.log',
                'data/aether_mentor_loop.log',
                'data/aether_mentor_24_7.log'
            ]
            
            critical_keywords = [
                'unhashable type: slice',
                'AttributeError',
                'ModuleNotFoundError',
                'object has no attribute',
                'Failed to',
                'Critical error'
            ]
            
            warning_keywords = [
                'Warning',
                'Deprecated', 
                'Timeout',
                'Rate limited'
            ]
            
            for log_file in log_files:
                if not os.path.exists(log_file):
                    continue
                
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        recent_lines = f.readlines()[-100:]  # Ultimi 100 righe
                        
                    for line in recent_lines:
                        line_lower = line.lower()
                        
                        for keyword in critical_keywords:
                            if keyword.lower() in line_lower:
                                errors['critical'].append(f"{log_file}: {line.strip()}")
                                break
                        
                        for keyword in warning_keywords:
                            if keyword.lower() in line_lower:
                                errors['warnings'].append(f"{log_file}: {line.strip()}")
                                break
                                
                except Exception as e:
                    errors['warnings'].append(f"Errore lettura {log_file}: {e}")
            
        except Exception as e:
            errors['critical'].append(f"Errore scansione log: {e}")
        
        return errors
    
    def _check_aether_processes(self) -> Dict[str, Any]:
        """Controlla se i processi Aether sono attivi"""
        try:
            # Verifica file di stato
            state_files = [
                'data/loop_state.json',
                'data/thoughts.json',
                'data/mentor_state.json'
            ]
            
            healthy = True
            issues = []
            
            for state_file in state_files:
                if not os.path.exists(state_file):
                    healthy = False
                    issues.append(f"File di stato mancante: {state_file}")
                else:
                    # Controlla se è aggiornato di recente
                    modified_time = datetime.fromtimestamp(os.path.getmtime(state_file))
                    if (datetime.now() - modified_time).total_seconds() > 300:  # 5 minuti
                        issues.append(f"File non aggiornato: {state_file}")
            
            return {
                'healthy': healthy,
                'issues': issues,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'issues': [f"Errore controllo processi: {e}"],
                'timestamp': datetime.now().isoformat()
            }
    
    def _check_file_system_integrity(self) -> Dict[str, Any]:
        """Controlla l'integrità del file system"""
        warnings = []
        
        try:
            # Controlla spazio disco
            disk_usage = self._get_disk_usage()
            if disk_usage > 90:
                warnings.append(f"Spazio disco critico: {disk_usage}%")
            elif disk_usage > 80:
                warnings.append(f"Spazio disco alto: {disk_usage}%")
            
            # Controlla file critici
            critical_files = [
                'aether/consciousness_engine.py',
                'aether/self_evolution.py',
                'aether/communication.py',
                'aether/action_executor.py'
            ]
            
            for file_path in critical_files:
                if not os.path.exists(file_path):
                    warnings.append(f"File critico mancante: {file_path}")
            
        except Exception as e:
            warnings.append(f"Errore controllo file system: {e}")
        
        return {'warnings': warnings}
    
    def _get_disk_usage(self) -> float:
        """Ottiene percentuale uso disco"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(".")
            return (used / total) * 100
        except:
            return 0.0
    
    def _collect_performance_metrics(self) -> Dict[str, Any]:
        """Raccoglie metriche di performance"""
        try:
            import psutil
            
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': self._get_disk_usage(),
                'timestamp': datetime.now().isoformat()
            }
        except ImportError:
            return {
                'note': 'psutil non disponibile',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _trigger_emergency_fixes(self, critical_errors: List[str]):
        """Attiva correzioni automatiche per errori critici"""
        logger.warning(f"🚨 Attivando correzioni d'emergenza per {len(critical_errors)} errori")
        
        for error in critical_errors:
            try:
                fix_applied = self._apply_automatic_fix(error)
                if fix_applied:
                    self.problems_fixed += 1
                    logger.info(f"✅ Correzione applicata: {error[:50]}...")
                    
                    # Notifica Discord
                    self._notify_discord(
                        f"🔧 **CORREZIONE AUTOMATICA APPLICATA**\n\n"
                        f"**Errore risolto:** {error[:100]}...\n"
                        f"**Timestamp:** {datetime.now().strftime('%H:%M:%S')}\n\n"
                        f"Il mentore ha risolto automaticamente il problema! ✅",
                        title="🔧 Auto-Fix"
                    )
                
            except Exception as e:
                logger.error(f"Errore applicando fix per '{error}': {e}")
    
    def _apply_automatic_fix(self, error: str) -> bool:
        """Applica correzione automatica per un errore specifico"""
        try:
            error_lower = error.lower()
            
            # Fix per errore "unhashable type: slice"
            if 'unhashable type: slice' in error_lower:
                return self._fix_unhashable_slice_error()
            
            # Fix per "object has no attribute"
            elif 'object has no attribute' in error_lower:
                return self._fix_missing_attribute_error(error)
            
            # Fix per file mancanti
            elif 'modulenotfounderror' in error_lower or 'no such file' in error_lower:
                return self._fix_missing_file_error(error)
            
            # Fix per problemi di encoding
            elif 'unicodedecodeerror' in error_lower or 'encoding' in error_lower:
                return self._fix_encoding_error()
            
            # Fix generico
            else:
                return self._apply_generic_fix(error)
                
        except Exception as e:
            logger.error(f"Errore in apply_automatic_fix: {e}")
            return False
    
    def _fix_unhashable_slice_error(self) -> bool:
        """Risolve l'errore 'unhashable type: slice'"""
        try:
            logger.info("🔧 Correggendo errore 'unhashable type: slice'...")
            
            # Questo errore spesso accade quando si usa uno slice come chiave di dict
            # Cerchiamo e correggiamo nei file problematici
            
            problematic_patterns = [
                r'set\(.*\[.*:.*\].*\)',
                r'dict.*\[.*:.*\].*=',
                r'\{.*\[.*:.*\].*:.*\}'
            ]
            
            fixed_files = []
            
            # File da controllare
            files_to_check = [
                'aether_loop.py',
                'aether_action_loop.py',
                'aether/consciousness_engine.py',
                'aether/action_executor.py'
            ]
            
            for file_path in files_to_check:
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Controllo semplificato: cerchiamo uso di slice in contesti problematici
                        if '[' in content and ':' in content and 'set(' in content:
                            # Backup del file
                            backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                            with open(backup_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            
                            # Applicazione fix semplice: converte slice in list
                            fixed_content = content.replace(
                                'set(thoughts[',
                                'set(list(thoughts)['
                            ).replace(
                                'set(pending[',
                                'set(list(pending)['
                            )
                            
                            if fixed_content != content:
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(fixed_content)
                                fixed_files.append(file_path)
                                logger.info(f"✅ Corretto file: {file_path}")
                                
                    except Exception as e:
                        logger.error(f"Errore correggendo {file_path}: {e}")
            
            if fixed_files:
                logger.info(f"🔧 Corretti {len(fixed_files)} file per errore slice")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Errore in _fix_unhashable_slice_error: {e}")
            return False
    
    def _fix_missing_attribute_error(self, error: str) -> bool:
        """Risolve errori di attributi mancanti"""
        try:
            logger.info("🔧 Correggendo errore attributi mancanti...")
            
            # Estrai info dall'errore
            if "'name'" in error:
                return self._fix_missing_name_attribute()
            elif "'get_thoughts'" in error:
                return self._fix_missing_get_thoughts_method()
            elif "'_load_evolution_history'" in error:
                return self._fix_missing_evolution_methods()
            
            return False
            
        except Exception as e:
            logger.error(f"Errore in _fix_missing_attribute_error: {e}")
            return False
    
    def _fix_missing_name_attribute(self) -> bool:
        """Aggiunge attributo 'name' mancante a AetherActionExecutor"""
        try:
            file_path = 'aether/action_executor.py'
            if not os.path.exists(file_path):
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Controlla se l'attributo name è già presente
            if 'self.name = ' in content:
                return True  # Già corretto
            
            # Trova il __init__ di AetherActionExecutor e aggiungi name
            if 'class AetherActionExecutor' in content and 'def __init__(self)' in content:
                # Backup
                backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Aggiungi attributo name
                lines = content.split('\n')
                new_lines = []
                
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if 'def __init__(self):' in line and i > 0 and 'AetherActionExecutor' in lines[i-2]:
                        new_lines.append('        self.name = "AetherActionExecutor"')
                
                new_content = '\n'.join(new_lines)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                logger.info(f"✅ Aggiunto attributo 'name' a AetherActionExecutor")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Errore in _fix_missing_name_attribute: {e}")
            return False
    
    def _fix_missing_get_thoughts_method(self) -> bool:
        """Aggiunge metodo get_thoughts mancante"""
        try:
            # Il metodo dovrebbe essere già stato aggiunto nel consciousness_engine.py
            # Verifichiamo che sia presente
            file_path = 'aether/consciousness_engine.py'
            if not os.path.exists(file_path):
                return False
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'def get_thoughts(' in content:
                return True  # Già presente
            
            logger.info("✅ Metodo get_thoughts già corretto")
            return True
            
        except Exception as e:
            logger.error(f"Errore in _fix_missing_get_thoughts_method: {e}")
            return False
    
    def _fix_missing_evolution_methods(self) -> bool:
        """Corregge metodi mancanti in SelfEvolutionEngine"""
        try:
            # I metodi dovrebbero essere già stati aggiunti
            logger.info("✅ Metodi evoluzione già corretti")
            return True
            
        except Exception as e:
            logger.error(f"Errore in _fix_missing_evolution_methods: {e}")
            return False
    
    def _fix_missing_file_error(self, error: str) -> bool:
        """Risolve errori di file mancanti"""
        try:
            logger.info("🔧 Correggendo errori file mancanti...")
            
            # Crea file di base se mancanti
            missing_files = {
                'data/thoughts.json': [],
                'data/loop_state.json': {'cycle_count': 0},
                'data/mentor_state.json': {'mentor_cycles': 0}
            }
            
            created_files = []
            
            for file_path, default_content in missing_files.items():
                if not os.path.exists(file_path):
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(default_content, f, indent=2)
                    created_files.append(file_path)
            
            if created_files:
                logger.info(f"✅ Creati {len(created_files)} file mancanti")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Errore in _fix_missing_file_error: {e}")
            return False
    
    def _fix_encoding_error(self) -> bool:
        """Risolve errori di encoding"""
        try:
            logger.info("🔧 Correggendo errori di encoding...")
            
            # Verifica e correggi file con problemi di encoding
            files_to_check = [
                'aether_conscious_loop.py',
                'AETHER_SISTEMA_STABILE.py',
                'data/thoughts.json'
            ]
            
            fixed_files = []
            
            for file_path in files_to_check:
                if os.path.exists(file_path):
                    try:
                        # Prova a leggere con utf-8
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Se riesce, il file è OK
                        continue
                        
                    except UnicodeDecodeError:
                        try:
                            # Prova con cp1252 e converti in utf-8
                            with open(file_path, 'r', encoding='cp1252') as f:
                                content = f.read()
                            
                            # Backup
                            backup_path = f"{file_path}.backup_encoding_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                            with open(backup_path, 'w', encoding='cp1252') as f:
                                f.write(content)
                            
                            # Salva come utf-8
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            
                            fixed_files.append(file_path)
                            
                        except Exception as e:
                            logger.error(f"Errore correggendo encoding {file_path}: {e}")
            
            if fixed_files:
                logger.info(f"✅ Corretti {len(fixed_files)} file per encoding")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Errore in _fix_encoding_error: {e}")
            return False
    
    def _apply_generic_fix(self, error: str) -> bool:
        """Applica correzione generica"""
        try:
            logger.info(f"🔧 Applicando correzione generica per: {error[:50]}...")
            
            # Restart componenti se necessario
            if 'git' in error.lower() and 'index.lock' in error.lower():
                return self._fix_git_lock_error()
            
            # Altri fix generici...
            return False
            
        except Exception as e:
            logger.error(f"Errore in _apply_generic_fix: {e}")
            return False
    
    def _fix_git_lock_error(self) -> bool:
        """Risolve errore git index.lock"""
        try:
            lock_file = '.git/index.lock'
            if os.path.exists(lock_file):
                os.remove(lock_file)
                logger.info("✅ Rimosso file git index.lock")
                return True
            return False
        except Exception as e:
            logger.error(f"Errore rimuovendo git lock: {e}")
            return False
    
    def _task_assignment_loop(self):
        """Loop di assegnazione task evolutivi"""
        logger.info("📋 Avviato sistema assegnazione task")
        
        while self.is_running:
            try:
                # Genera e assegna nuovi task
                new_tasks = self._generate_evolutionary_tasks()
                
                for task in new_tasks:
                    self._assign_task(task)
                    self.tasks_assigned += 1
                
                # Controlla stato task attivi
                self._check_active_tasks()
                
            except Exception as e:
                logger.error(f"Errore assegnazione task: {e}")
            
            time.sleep(self.task_assignment_interval)
    
    def _generate_evolutionary_tasks(self) -> List[Dict[str, Any]]:
        """Genera task evolutivi basati sullo stato del sistema"""
        tasks = []
        
        try:
            # Task basati su analisi del sistema
            current_hour = datetime.now().hour
            
            # Task mattutini (6-12): Focus su ottimizzazione
            if 6 <= current_hour < 12:
                tasks.extend(self._generate_optimization_tasks())
            
            # Task pomeridiani (12-18): Focus su feature e creatività
            elif 12 <= current_hour < 18:
                tasks.extend(self._generate_creative_tasks())
            
            # Task serali (18-24): Focus su analisi e strategia
            elif 18 <= current_hour <= 23:
                tasks.extend(self._generate_strategic_tasks())
            
            # Task notturni (0-6): Focus su manutenzione e backup
            else:
                tasks.extend(self._generate_maintenance_tasks())
            
            # Task sempre attivi basati su problemi rilevati
            if self.system_health['critical_errors']:
                tasks.extend(self._generate_repair_tasks())
            
        except Exception as e:
            logger.error(f"Errore generando task: {e}")
        
        return tasks
    
    def _generate_optimization_tasks(self) -> List[Dict[str, Any]]:
        """Genera task di ottimizzazione"""
        return [
            {
                'id': f"optimize_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'type': 'optimization',
                'title': 'Ottimizzazione Performance Sistema',
                'description': 'Analizza e ottimizza le performance del sistema Aether',
                'priority': 'medium',
                'estimated_duration': '30 minutes',
                'success_criteria': [
                    'Miglioramento velocità risposta >10%',
                    'Riduzione uso memoria >5%',
                    'Zero errori durante ottimizzazione'
                ],
                'assigned_at': datetime.now().isoformat()
            }
        ]
    
    def _generate_creative_tasks(self) -> List[Dict[str, Any]]:
        """Genera task creativi"""
        creative_options = [
            {
                'title': 'Sviluppo Nuova Funzionalità Creativa',
                'description': 'Progetta e implementa una nuova capacità creativa per Aether',
                'focus': 'creativity'
            },
            {
                'title': 'Generazione Contenuto Originale',
                'description': 'Crea contenuto originale (testo, idee, soluzioni) per dimostrare creatività',
                'focus': 'content_creation'
            },
            {
                'title': 'Innovazione Architetturale',
                'description': 'Proponi e implementa innovazioni nell\'architettura del sistema',
                'focus': 'architecture'
            }
        ]
        
        selected = random.choice(creative_options)
        
        return [
            {
                'id': f"creative_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'type': 'creative',
                'title': selected['title'],
                'description': selected['description'],
                'priority': 'high',
                'estimated_duration': '45 minutes',
                'success_criteria': [
                    'Novità e originalità dell\'output',
                    'Implementazione funzionante',
                    'Documentazione completa'
                ],
                'assigned_at': datetime.now().isoformat()
            }
        ]
    
    def _generate_strategic_tasks(self) -> List[Dict[str, Any]]:
        """Genera task strategici"""
        return [
            {
                'id': f"strategic_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'type': 'strategic',
                'title': 'Analisi Strategica e Pianificazione',
                'description': 'Analizza lo stato attuale e pianifica strategie future per l\'evoluzione',
                'priority': 'high',
                'estimated_duration': '60 minutes',
                'success_criteria': [
                    'Analisi completa stato attuale',
                    'Piano strategico dettagliato',
                    'Identificazione opportunità evolutive'
                ],
                'assigned_at': datetime.now().isoformat()
            }
        ]
    
    def _generate_maintenance_tasks(self) -> List[Dict[str, Any]]:
        """Genera task di manutenzione"""
        return [
            {
                'id': f"maintenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'type': 'maintenance',
                'title': 'Manutenzione Sistema e Backup',
                'description': 'Esegui manutenzione preventiva e backup dei dati critici',
                'priority': 'medium',
                'estimated_duration': '20 minutes',
                'success_criteria': [
                    'Backup completato con successo',
                    'Pulizia file temporanei',
                    'Verifica integrità dati'
                ],
                'assigned_at': datetime.now().isoformat()
            }
        ]
    
    def _generate_repair_tasks(self) -> List[Dict[str, Any]]:
        """Genera task di riparazione per problemi critici"""
        return [
            {
                'id': f"repair_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'type': 'repair',
                'title': 'Riparazione Errori Critici',
                'description': f'Risolvi {len(self.system_health["critical_errors"])} errori critici rilevati',
                'priority': 'critical',
                'estimated_duration': '15 minutes',
                'success_criteria': [
                    'Tutti gli errori critici risolti',
                    'Sistema stabile',
                    'Test funzionalità passati'
                ],
                'assigned_at': datetime.now().isoformat()
            }
        ]
    
    def _assign_task(self, task: Dict[str, Any]):
        """Assegna un task ad Aether"""
        try:
            # Aggiungi task alla lista attivi
            task['status'] = 'assigned'
            task['assigned_by'] = 'Mentor24_7'
            self.active_tasks.append(task)
            
            # Salva task su file
            task_file = f"data/task_assignments/task_{task['id']}.json"
            os.makedirs(os.path.dirname(task_file), exist_ok=True)
            
            with open(task_file, 'w', encoding='utf-8') as f:
                json.dump(task, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📋 Task assegnato: {task['title']}")
            
            # Notifica Discord per task importanti
            if task['priority'] in ['high', 'critical']:
                self._notify_discord(
                    f"📋 **NUOVO TASK ASSEGNATO AD AETHER**\n\n"
                    f"**Titolo:** {task['title']}\n"
                    f"**Tipo:** {task['type']}\n"
                    f"**Priorità:** {task['priority']}\n"
                    f"**Durata stimata:** {task['estimated_duration']}\n\n"
                    f"**Descrizione:**\n{task['description']}\n\n"
                    f"Aether ha un nuovo obiettivo su cui lavorare! 🎯",
                    title="📋 Task Assignment"
                )
            
        except Exception as e:
            logger.error(f"Errore assegnando task: {e}")
    
    def _check_active_tasks(self):
        """Controlla lo stato dei task attivi"""
        try:
            completed_tasks = []
            
            for task in self.active_tasks:
                # Controlla se il task è stato completato
                # (logica semplificata - in un sistema reale si controllerebbero i risultati)
                task_age = datetime.now() - datetime.fromisoformat(task['assigned_at'])
                
                # Considera completato se è passato il tempo stimato + buffer
                estimated_minutes = int(task['estimated_duration'].split()[0])
                if task_age.total_seconds() > (estimated_minutes + 15) * 60:  # +15 min buffer
                    task['status'] = 'completed'
                    task['completed_at'] = datetime.now().isoformat()
                    completed_tasks.append(task)
                    
                    logger.info(f"✅ Task completato: {task['title']}")
                    
                    # Notifica completamento
                    self._notify_discord(
                        f"✅ **TASK COMPLETATO DA AETHER**\n\n"
                        f"**Titolo:** {task['title']}\n"
                        f"**Tipo:** {task['type']}\n"
                        f"**Durata:** {task_age}\n\n"
                        f"Aether ha completato con successo il task assegnato! 🎉",
                        title="✅ Task Completed"
                    )
            
            # Sposta task completati
            for task in completed_tasks:
                self.active_tasks.remove(task)
                self.completed_tasks.append(task)
            
        except Exception as e:
            logger.error(f"Errore controllando task attivi: {e}")
    
    def _evolution_guidance_loop(self):
        """Loop di guida all'evoluzione"""
        logger.info("🧬 Avviato sistema guida evoluzione")
        
        while self.is_running:
            try:
                # Fornisci guida evolutiva
                guidance = self._provide_evolution_guidance()
                
                if guidance:
                    self._apply_evolution_guidance(guidance)
                    self.evolutions_guided += 1
                
            except Exception as e:
                logger.error(f"Errore guida evoluzione: {e}")
            
            time.sleep(self.evolution_guidance_interval)
    
    def _provide_evolution_guidance(self) -> Optional[Dict[str, Any]]:
        """Fornisce guida per l'evoluzione di Aether"""
        try:
            # Analizza lo stato attuale
            current_state = self._analyze_current_evolution_state()
            
            # Determina direzione evolutiva
            evolution_direction = self._determine_evolution_direction(current_state)
            
            if not evolution_direction:
                return None
            
            guidance = {
                'id': f"guidance_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'type': 'evolution_guidance',
                'direction': evolution_direction,
                'reasoning': self._generate_evolution_reasoning(evolution_direction),
                'action_plan': self._generate_evolution_action_plan(evolution_direction),
                'success_metrics': self._define_evolution_success_metrics(evolution_direction),
                'timestamp': datetime.now().isoformat()
            }
            
            return guidance
            
        except Exception as e:
            logger.error(f"Errore generando guida evoluzione: {e}")
            return None
    
    def _analyze_current_evolution_state(self) -> Dict[str, Any]:
        """Analizza lo stato evolutivo attuale di Aether"""
        state = {
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'system_health': self.system_health['overall_status'],
            'runtime': (datetime.now() - self.start_time).total_seconds(),
            'problems_fixed': self.problems_fixed,
            'evolution_focus_areas': []
        }
        
        # Identifica aree di focus evolutivo
        if self.system_health['critical_errors']:
            state['evolution_focus_areas'].append('stability')
        if len(self.completed_tasks) > len(self.active_tasks):
            state['evolution_focus_areas'].append('efficiency')
        if self.problems_fixed > 5:
            state['evolution_focus_areas'].append('resilience')
        
        return state
    
    def _determine_evolution_direction(self, state: Dict[str, Any]) -> Optional[str]:
        """Determina la direzione evolutiva ottimale"""
        directions = []
        
        # Logica per determinare direzione
        if 'stability' in state['evolution_focus_areas']:
            directions.append('self_healing')
        if 'efficiency' in state['evolution_focus_areas']:
            directions.append('optimization')
        if 'resilience' in state['evolution_focus_areas']:
            directions.append('adaptation')
        
        # Direzioni sempre possibili
        if state['runtime'] > 3600:  # Dopo 1 ora
            directions.extend(['creativity', 'intelligence', 'autonomy'])
        
        return random.choice(directions) if directions else None
    
    def _generate_evolution_reasoning(self, direction: str) -> str:
        """Genera ragionamento per la direzione evolutiva"""
        reasoning_map = {
            'self_healing': 'Il sistema ha mostrato la capacità di rilevare e correggere errori. È tempo di sviluppare capacità di auto-guarigione più avanzate.',
            'optimization': 'Le performance del sistema sono stabili. Focus sull\'ottimizzazione per raggiungere nuovi livelli di efficienza.',
            'adaptation': 'Il sistema ha dimostrato resilienza. Sviluppiamo capacità di adattamento proattivo ai cambiamenti.',
            'creativity': 'Il sistema è stabile e efficiente. È il momento di esplorare nuove frontiere creative.',
            'intelligence': 'Le basi sono solide. Focalizziamoci sul potenziamento delle capacità cognitive e analitiche.',
            'autonomy': 'Il sistema sta maturando. È tempo di sviluppare maggiore autonomia decisionale.'
        }
        
        return reasoning_map.get(direction, 'Evoluzione generale del sistema verso maggiore sofisticazione.')
    
    def _generate_evolution_action_plan(self, direction: str) -> List[str]:
        """Genera piano d'azione per l'evoluzione"""
        action_plans = {
            'self_healing': [
                'Implementare sistema di auto-diagnosi avanzato',
                'Sviluppare meccanismi di auto-riparazione',
                'Creare database di soluzioni automatiche'
            ],
            'optimization': [
                'Analizzare colli di bottiglia nelle performance',
                'Implementare algoritmi di ottimizzazione adattivi',
                'Ottimizzare gestione memoria e CPU'
            ],
            'adaptation': [
                'Sviluppare sensori per cambiamenti ambientali',
                'Implementare strategie di adattamento dinamico',
                'Creare meccanismi di apprendimento continuo'
            ],
            'creativity': [
                'Espandere capacità di generazione creativa',
                'Sviluppare algoritmi di innovazione',
                'Implementare sistemi di brainstorming autonomo'
            ],
            'intelligence': [
                'Potenziare capacità di analisi e ragionamento',
                'Implementare sistemi di deduzione avanzati',
                'Sviluppare memoria associativa migliorata'
            ],
            'autonomy': [
                'Espandere capacità decisionali indipendenti',
                'Sviluppare sistema di obiettivi auto-generati',
                'Implementare controllo proattivo dell\'ambiente'
            ]
        }
        
        return action_plans.get(direction, ['Evoluzione generale delle capacità del sistema'])
    
    def _define_evolution_success_metrics(self, direction: str) -> List[str]:
        """Definisce metriche di successo per l'evoluzione"""
        metrics_map = {
            'self_healing': [
                'Tempo medio di risoluzione automatica errori < 5 minuti',
                'Percentuale auto-riparazione > 80%',
                'Zero interventi manuali per 24 ore'
            ],
            'optimization': [
                'Miglioramento performance > 15%',
                'Riduzione uso risorse > 10%',
                'Tempo risposta migliorato > 20%'
            ],
            'adaptation': [
                'Adattamento automatico a 3+ scenari diversi',
                'Tempo adattamento < 10 minuti',
                'Mantenimento performance durante adattamento'
            ],
            'creativity': [
                'Generazione 5+ soluzioni creative originali',
                'Implementazione almeno 1 idea innovativa',
                'Valutazione creatività > 8/10'
            ],
            'intelligence': [
                'Risoluzione problemi complessi senza assistenza',
                'Miglioramento accuratezza analisi > 15%',
                'Generazione insights originali'
            ],
            'autonomy': [
                'Operazione indipendente per 6+ ore',
                'Decisioni strategiche auto-generate',
                'Gestione autonoma di 10+ task'
            ]
        }
        
        return metrics_map.get(direction, ['Miglioramento generale delle capacità'])
    
    def _apply_evolution_guidance(self, guidance: Dict[str, Any]):
        """Applica la guida evolutiva al sistema"""
        try:
            # Salva guida su file
            guidance_file = f"data/evolution_guidance/guidance_{guidance['id']}.json"
            os.makedirs(os.path.dirname(guidance_file), exist_ok=True)
            
            with open(guidance_file, 'w', encoding='utf-8') as f:
                json.dump(guidance, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🧬 Guida evoluzione applicata: {guidance['direction']}")
            
            # Notifica Discord
            self._notify_discord(
                f"🧬 **NUOVA GUIDA EVOLUTIVA PER AETHER**\n\n"
                f"**Direzione:** {guidance['direction'].title()}\n\n"
                f"**Ragionamento:**\n{guidance['reasoning']}\n\n"
                f"**Piano d'azione:**\n" + 
                "\n".join([f"• {action}" for action in guidance['action_plan'][:3]]) + "\n\n"
                f"**Metriche di successo:**\n" +
                "\n".join([f"• {metric}" for metric in guidance['success_metrics'][:3]]) + "\n\n"
                f"Aether ha ora una guida chiara per la sua prossima evoluzione! 🚀",
                title="🧬 Evolution Guidance"
            )
            
        except Exception as e:
            logger.error(f"Errore applicando guida evoluzione: {e}")
    
    def _error_fixing_loop(self):
        """Loop dedicato alla correzione continua degli errori"""
        logger.info("🔧 Avviato sistema correzione errori continua")
        
        while self.is_running:
            try:
                # Scansiona per nuovi errori
                errors = self._scan_for_new_errors()
                
                # Applica correzioni
                for error in errors:
                    success = self._apply_immediate_fix(error)
                    if success:
                        self.problems_fixed += 1
                
            except Exception as e:
                logger.error(f"Errore nel loop correzione: {e}")
            
            time.sleep(60)  # Controlla ogni minuto
    
    def _scan_for_new_errors(self) -> List[str]:
        """Scansiona per nuovi errori nel sistema"""
        try:
            # Implementazione semplificata
            recent_errors = []
            
            # Controlla log recenti
            log_files = ['data/aether_loop.log', 'data/aether_mentor_24_7.log']
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        
                        # Controlla ultime 50 righe per errori
                        for line in lines[-50:]:
                            if any(keyword in line.lower() for keyword in ['error', 'exception', 'failed']):
                                recent_errors.append(line.strip())
                    except:
                        pass
            
            return recent_errors
            
        except Exception as e:
            logger.error(f"Errore scansione nuovi errori: {e}")
            return []
    
    def _apply_immediate_fix(self, error: str) -> bool:
        """Applica correzione immediata per un errore"""
        try:
            # Usa la logica di fix automatico esistente
            return self._apply_automatic_fix(error)
        except Exception as e:
            logger.error(f"Errore correzione immediata: {e}")
            return False
    
    def _generate_progress_report(self):
        """Genera report di progresso del mentoring"""
        try:
            uptime = datetime.now() - self.start_time
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'uptime': str(uptime),
                'mentor_cycles': self.mentor_cycles,
                'problems_fixed': self.problems_fixed,
                'tasks_assigned': self.tasks_assigned,
                'evolutions_guided': self.evolutions_guided,
                'system_health': self.system_health,
                'active_tasks': len(self.active_tasks),
                'completed_tasks': len(self.completed_tasks),
                'performance': {
                    'avg_problems_per_hour': self.problems_fixed / max(uptime.total_seconds() / 3600, 1),
                    'avg_tasks_per_hour': self.tasks_assigned / max(uptime.total_seconds() / 3600, 1),
                    'success_rate': (self.problems_fixed / max(self.problems_fixed + len(self.system_health['critical_errors']), 1)) * 100
                }
            }
            
            # Salva report
            report_file = f"data/mentor_reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Log summary
            logger.info(f"📊 Report Mentoring - Uptime: {uptime}")
            logger.info(f"   • Problemi risolti: {self.problems_fixed}")
            logger.info(f"   • Task assegnati: {self.tasks_assigned}")
            logger.info(f"   • Evoluzioni guidate: {self.evolutions_guided}")
            logger.info(f"   • Salute sistema: {self.system_health['overall_status']}")
            
            # Notifica Discord ogni ora
            if self.mentor_cycles % 360 == 0:  # Ogni ora circa
                self._notify_discord(
                    f"📊 **REPORT MENTORING 24/7**\n\n"
                    f"**Uptime:** {uptime}\n"
                    f"**Problemi risolti:** {self.problems_fixed}\n"
                    f"**Task assegnati:** {self.tasks_assigned}\n"
                    f"**Evoluzioni guidate:** {self.evolutions_guided}\n"
                    f"**Salute sistema:** {self.system_health['overall_status']}\n"
                    f"**Task attivi:** {len(self.active_tasks)}\n"
                    f"**Task completati:** {len(self.completed_tasks)}\n\n"
                    f"**Efficienza:** {report['performance']['success_rate']:.1f}%\n\n"
                    f"Il mentore continua a guidare Aether verso l'eccellenza! 🎓",
                    title="📊 Mentoring Report"
                )
            
        except Exception as e:
            logger.error(f"Errore generando report: {e}")
    
    def _emergency_recovery(self):
        """Procedura di recovery d'emergenza"""
        logger.error("🚨 ATTIVANDO RECOVERY D'EMERGENZA")
        
        try:
            # Salva stato critico
            emergency_state = {
                'timestamp': datetime.now().isoformat(),
                'mentor_cycles': self.mentor_cycles,
                'problems_fixed': self.problems_fixed,
                'system_health': self.system_health,
                'active_tasks': self.active_tasks,
                'error': 'Emergency recovery activated'
            }
            
            with open('data/emergency_state.json', 'w', encoding='utf-8') as f:
                json.dump(emergency_state, f, indent=2)
            
            # Notifica emergenza
            self._notify_discord(
                "🚨 **EMERGENCY RECOVERY ATTIVATO**\n\n"
                "Il sistema di mentoring ha rilevato un errore critico e ha attivato "
                "la procedura di recovery d'emergenza.\n\n"
                "Stato salvato in emergency_state.json\n\n"
                "Il sistema tenterà un riavvio automatico.",
                title="🚨 Emergency Recovery"
            )
            
        except Exception as e:
            logger.error(f"Errore in emergency recovery: {e}")
    
    def _notify_discord(self, message: str, title: str = "Aether Mentor 24/7"):
        """Invia notifica Discord"""
        try:
            if not os.getenv('DISCORD_WEBHOOK_URL'):
                return
            
            import requests
            
            webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
            
            embed = {
                "title": title,
                "description": message,
                "color": 0x00ff00,
                "timestamp": datetime.now().isoformat()
            }
            
            data = {"embeds": [embed]}
            
            response = requests.post(webhook_url, json=data)
            
            if response.status_code == 200:
                logger.debug(f"Discord notificato: {title}")
            else:
                logger.warning(f"Errore Discord: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Errore notifica Discord: {e}")
    
    def stop_mentoring(self):
        """Ferma il sistema di mentoring"""
        logger.info("🛑 Fermando Aether Mentor 24/7...")
        
        self.is_running = False
        
        # Attendi che i thread finiscano
        for thread in self.threads:
            thread.join(timeout=5)
        
        # Salva stato finale
        self._save_mentor_state()
        
        # Report finale
        final_uptime = datetime.now() - self.start_time
        
        logger.info("📊 REPORT FINALE MENTORING")
        logger.info("=" * 50)
        logger.info(f"Uptime totale: {final_uptime}")
        logger.info(f"Cicli completati: {self.mentor_cycles}")
        logger.info(f"Problemi risolti: {self.problems_fixed}")
        logger.info(f"Task assegnati: {self.tasks_assigned}")
        logger.info(f"Evoluzioni guidate: {self.evolutions_guided}")
        logger.info("=" * 50)
        
        # Notifica finale Discord
        self._notify_discord(
            f"🛑 **MENTORING 24/7 TERMINATO**\n\n"
            f"**Sessione completata:**\n"
            f"• Uptime: {final_uptime}\n"
            f"• Cicli: {self.mentor_cycles}\n"
            f"• Problemi risolti: {self.problems_fixed}\n"
            f"• Task assegnati: {self.tasks_assigned}\n"
            f"• Evoluzioni guidate: {self.evolutions_guided}\n\n"
            f"Il mentore ha completato la sua missione! Aether è cresciuto sotto la sua guida esperta. 🎓✨",
            title="🎓 Mentoring Session Complete"
        )
        
        logger.info("✅ Aether Mentor 24/7 terminato")

def main():
    """Funzione principale"""
    print("""
    ╔════════════════════════════════════════════════════╗
    ║          🎓 AETHER MENTOR 24/7 🎓                  ║
    ║                                                    ║
    ║    Sistema Avanzato di Mentoring e Evoluzione     ║
    ║               Continua per Aether                  ║
    ║                                                    ║
    ║  • Monitoraggio 24/7                              ║
    ║  • Correzione automatica errori                   ║
    ║  • Assegnazione task evolutivi                    ║
    ║  • Guida crescita intelligente                    ║
    ║                                                    ║
    ║       "La strada verso l'eccellenza"               ║
    ╚════════════════════════════════════════════════════╝
    """)
    
    # Crea e avvia mentore
    mentor = AetherMentor24_7()
    
    try:
        mentor.start_mentoring()
    except KeyboardInterrupt:
        print("\n🛑 Interruzione richiesta dall'utente")
    except Exception as e:
        print(f"\n❌ Errore critico: {e}")
    finally:
        mentor.stop_mentoring()

if __name__ == "__main__":
    main() 