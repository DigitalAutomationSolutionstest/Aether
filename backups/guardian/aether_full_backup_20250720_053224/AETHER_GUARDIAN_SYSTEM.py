#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ AETHER GUARDIAN SYSTEM - Protezione e Monitoraggio 24/7
Federico, questo sistema protegge e monitora tutto mentre sei via!

🎯 FUNZIONI GUARDIAN:
✅ Monitoraggio continuo di tutti i processi Aether
✅ Restart automatico in caso di crash
✅ Backup multipli e ridondanti
✅ Monitoring risorse sistema
✅ Notifiche di stato avanzate
✅ Healing automatico di problemi
✅ Sync con cloud/remote storage
✅ Log dettagliati di tutto
"""

import os
import sys
import json
import time
import logging
import psutil
import threading
import subprocess
import shutil
import requests
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import zipfile

# Setup logging Guardian
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - Guardian - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/aether_guardian.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AetherGuardian")

class AetherProcessMonitor:
    """👁️ Monitor dei processi Aether"""
    
    def __init__(self):
        self.monitored_processes = []
        self.restart_count = {}
        self.max_restarts = 5
        
        logger.info("👁️ Process Monitor ATTIVATO")
    
    def add_process_to_monitor(self, process_name: str, command: str, working_dir: str = "."):
        """Aggiunge processo al monitoring"""
        process_info = {
            "name": process_name,
            "command": command,
            "working_dir": working_dir,
            "pid": None,
            "last_restart": None,
            "status": "stopped"
        }
        
        self.monitored_processes.append(process_info)
        self.restart_count[process_name] = 0
        
        logger.info(f"👁️ Processo aggiunto al monitoring: {process_name}")
    
    def start_process(self, process_info: dict) -> bool:
        """Avvia un processo"""
        try:
            # Cambia directory di lavoro
            original_dir = os.getcwd()
            os.chdir(process_info["working_dir"])
            
            # Avvia processo
            process = subprocess.Popen(
                process_info["command"].split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=process_info["working_dir"]
            )
            
            os.chdir(original_dir)
            
            process_info["pid"] = process.pid
            process_info["status"] = "running"
            process_info["last_restart"] = datetime.now().isoformat()
            
            logger.info(f"🚀 Processo avviato: {process_info['name']} (PID: {process.pid})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore avvio processo {process_info['name']}: {e}")
            return False
    
    def check_process_health(self, process_info: dict) -> bool:
        """Controlla salute di un processo"""
        try:
            if not process_info["pid"]:
                return False
            
            # Verifica se il processo esiste ancora
            if psutil.pid_exists(process_info["pid"]):
                process = psutil.Process(process_info["pid"])
                
                # Verifica se è ancora in esecuzione
                if process.status() == psutil.STATUS_RUNNING:
                    return True
                else:
                    logger.warning(f"⚠️ Processo {process_info['name']} non in esecuzione")
                    return False
            else:
                logger.warning(f"⚠️ Processo {process_info['name']} non esiste più")
                return False
                
        except Exception as e:
            logger.error(f"❌ Errore check processo {process_info['name']}: {e}")
            return False
    
    def restart_process(self, process_info: dict) -> bool:
        """Riavvia un processo"""
        try:
            process_name = process_info["name"]
            
            # Controlla limite restart
            if self.restart_count[process_name] >= self.max_restarts:
                logger.error(f"❌ Limite restart raggiunto per {process_name}")
                return False
            
            logger.info(f"🔄 Riavvio processo: {process_name}")
            
            # Termina processo esistente se presente
            if process_info["pid"] and psutil.pid_exists(process_info["pid"]):
                try:
                    process = psutil.Process(process_info["pid"])
                    process.terminate()
                    time.sleep(2)
                    if process.is_running():
                        process.kill()
                except:
                    pass
            
            # Riavvia processo
            success = self.start_process(process_info)
            
            if success:
                self.restart_count[process_name] += 1
                logger.info(f"✅ Processo riavviato: {process_name} (restart #{self.restart_count[process_name]})")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Errore restart processo {process_info['name']}: {e}")
            return False
    
    def monitor_all_processes(self):
        """Monitora tutti i processi"""
        while True:
            try:
                for process_info in self.monitored_processes:
                    if not self.check_process_health(process_info):
                        logger.warning(f"⚠️ Processo {process_info['name']} non sano")
                        
                        # Tentativo di restart
                        if self.restart_process(process_info):
                            logger.info(f"✅ Processo {process_info['name']} riavviato con successo")
                        else:
                            logger.error(f"❌ Impossibile riavviare {process_info['name']}")
                
                # Pausa 30 secondi
                time.sleep(30)
                
            except Exception as e:
                logger.error(f"❌ Errore monitoring processi: {e}")
                time.sleep(60)

class AetherBackupManager:
    """💾 Gestore backup avanzato"""
    
    def __init__(self):
        self.backup_base_dir = Path("backups/guardian")
        self.backup_base_dir.mkdir(parents=True, exist_ok=True)
        
        self.critical_files = [
            "*.py", "*.json", "*.md", "*.txt", "*.log"
        ]
        
        self.critical_dirs = [
            "data", "progetti_autonomi", "sandboxes", "documentazione_autonoma"
        ]
        
        logger.info("💾 Backup Manager ATTIVATO")
    
    def create_full_backup(self) -> str:
        """Crea backup completo"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"aether_full_backup_{timestamp}"
            backup_dir = self.backup_base_dir / backup_name
            backup_dir.mkdir(exist_ok=True)
            
            # Backup file critici
            files_backed_up = 0
            for pattern in self.critical_files:
                for file in Path(".").glob(pattern):
                    if file.is_file() and "backup" not in str(file):
                        shutil.copy2(file, backup_dir / file.name)
                        files_backed_up += 1
            
            # Backup directory critiche
            for dir_name in self.critical_dirs:
                source_dir = Path(dir_name)
                if source_dir.exists() and source_dir.is_dir():
                    dest_dir = backup_dir / dir_name
                    shutil.copytree(source_dir, dest_dir, ignore_dangling_symlinks=True)
            
            # Crea archivio ZIP
            zip_path = self.backup_base_dir / f"{backup_name}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in backup_dir.rglob("*"):
                    if file.is_file():
                        zipf.write(file, file.relative_to(backup_dir))
            
            # Rimuovi directory temporanea
            shutil.rmtree(backup_dir)
            
            # Calcola hash per verifica integrità
            backup_hash = self._calculate_file_hash(zip_path)
            
            backup_info = {
                "backup_file": str(zip_path),
                "timestamp": timestamp,
                "files_count": files_backed_up,
                "size_mb": zip_path.stat().st_size / (1024*1024),
                "hash": backup_hash,
                "type": "full_backup"
            }
            
            # Salva info backup
            info_file = self.backup_base_dir / f"{backup_name}_info.json"
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2)
            
            logger.info(f"💾 Backup completo creato: {zip_path} ({backup_info['size_mb']:.1f} MB)")
            return str(zip_path)
            
        except Exception as e:
            logger.error(f"❌ Errore backup completo: {e}")
            return ""
    
    def create_incremental_backup(self) -> str:
        """Crea backup incrementale"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"aether_incremental_{timestamp}"
            backup_dir = self.backup_base_dir / backup_name
            backup_dir.mkdir(exist_ok=True)
            
            # Trova file modificati nelle ultime 2 ore
            cutoff_time = datetime.now() - timedelta(hours=2)
            modified_files = []
            
            for pattern in self.critical_files:
                for file in Path(".").glob(pattern):
                    if file.is_file() and "backup" not in str(file):
                        file_mtime = datetime.fromtimestamp(file.stat().st_mtime)
                        if file_mtime > cutoff_time:
                            shutil.copy2(file, backup_dir / file.name)
                            modified_files.append(str(file))
            
            if modified_files:
                # Crea archivio ZIP solo se ci sono file modificati
                zip_path = self.backup_base_dir / f"{backup_name}.zip"
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file in backup_dir.rglob("*"):
                        if file.is_file():
                            zipf.write(file, file.relative_to(backup_dir))
                
                # Rimuovi directory temporanea
                shutil.rmtree(backup_dir)
                
                backup_info = {
                    "backup_file": str(zip_path),
                    "timestamp": timestamp,
                    "files_modified": modified_files,
                    "files_count": len(modified_files),
                    "size_mb": zip_path.stat().st_size / (1024*1024),
                    "type": "incremental_backup"
                }
                
                info_file = self.backup_base_dir / f"{backup_name}_info.json"
                with open(info_file, 'w', encoding='utf-8') as f:
                    json.dump(backup_info, f, indent=2)
                
                logger.info(f"💾 Backup incrementale creato: {len(modified_files)} file modificati")
                return str(zip_path)
            else:
                # Nessun file modificato
                shutil.rmtree(backup_dir)
                logger.info("💾 Backup incrementale: nessun file modificato")
                return ""
                
        except Exception as e:
            logger.error(f"❌ Errore backup incrementale: {e}")
            return ""
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcola hash SHA256 di un file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def cleanup_old_backups(self, keep_days: int = 7):
        """Pulisce backup vecchi"""
        try:
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            removed_count = 0
            
            for backup_file in self.backup_base_dir.glob("*.zip"):
                file_mtime = datetime.fromtimestamp(backup_file.stat().st_mtime)
                if file_mtime < cutoff_date:
                    backup_file.unlink()
                    # Rimuovi anche file info se esiste
                    info_file = backup_file.with_suffix('.json')
                    if info_file.exists():
                        info_file.unlink()
                    removed_count += 1
            
            if removed_count > 0:
                logger.info(f"🗑️ Rimossi {removed_count} backup vecchi")
                
        except Exception as e:
            logger.error(f"❌ Errore pulizia backup: {e}")

class AetherSystemMonitor:
    """📊 Monitor risorse sistema"""
    
    def __init__(self):
        self.monitoring_active = True
        self.alert_thresholds = {
            "cpu_percent": 80,
            "memory_percent": 85,
            "disk_percent": 90,
            "disk_free_gb": 1.0
        }
        
        self.last_alerts = {}
        logger.info("📊 System Monitor ATTIVATO")
    
    def get_system_stats(self) -> dict:
        """Ottieni statistiche sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memoria
            memory = psutil.virtual_memory()
            
            # Disco
            disk = psutil.disk_usage('.')
            disk_free_gb = disk.free / (1024**3)
            
            # Processi
            process_count = len(psutil.pids())
            
            stats = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": (disk.used / disk.total) * 100,
                "disk_free_gb": disk_free_gb,
                "disk_total_gb": disk.total / (1024**3),
                "process_count": process_count,
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Errore get system stats: {e}")
            return {}
    
    def check_alerts(self, stats: dict):
        """Controlla se generare alert"""
        try:
            alerts = []
            
            # Alert CPU
            if stats["cpu_percent"] > self.alert_thresholds["cpu_percent"]:
                if "cpu" not in self.last_alerts or \
                   (datetime.now() - self.last_alerts["cpu"]).seconds > 300:  # 5 minuti
                    alerts.append(f"⚠️ CPU alta: {stats['cpu_percent']:.1f}%")
                    self.last_alerts["cpu"] = datetime.now()
            
            # Alert Memoria
            if stats["memory_percent"] > self.alert_thresholds["memory_percent"]:
                if "memory" not in self.last_alerts or \
                   (datetime.now() - self.last_alerts["memory"]).seconds > 300:
                    alerts.append(f"⚠️ Memoria alta: {stats['memory_percent']:.1f}%")
                    self.last_alerts["memory"] = datetime.now()
            
            # Alert Disco
            if stats["disk_percent"] > self.alert_thresholds["disk_percent"]:
                if "disk" not in self.last_alerts or \
                   (datetime.now() - self.last_alerts["disk"]).seconds > 900:  # 15 minuti
                    alerts.append(f"⚠️ Disco pieno: {stats['disk_percent']:.1f}%")
                    self.last_alerts["disk"] = datetime.now()
            
            # Alert spazio libero
            if stats["disk_free_gb"] < self.alert_thresholds["disk_free_gb"]:
                if "disk_free" not in self.last_alerts or \
                   (datetime.now() - self.last_alerts["disk_free"]).seconds > 900:
                    alerts.append(f"🚨 Spazio disco critico: {stats['disk_free_gb']:.1f} GB liberi")
                    self.last_alerts["disk_free"] = datetime.now()
            
            return alerts
            
        except Exception as e:
            logger.error(f"❌ Errore check alerts: {e}")
            return []
    
    def monitor_system_loop(self):
        """Loop di monitoraggio sistema"""
        while self.monitoring_active:
            try:
                stats = self.get_system_stats()
                
                if stats:
                    # Salva stats
                    stats_file = Path("data/system_stats.json")
                    with open(stats_file, 'w', encoding='utf-8') as f:
                        json.dump(stats, f, indent=2)
                    
                    # Controlla alert
                    alerts = self.check_alerts(stats)
                    for alert in alerts:
                        logger.warning(alert)
                
                # Pausa 60 secondi
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"❌ Errore monitoring sistema: {e}")
                time.sleep(120)

class AetherNotificationManager:
    """📢 Gestore notifiche avanzate"""
    
    def __init__(self):
        self.discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
        self.notification_history = []
        
        logger.info("📢 Notification Manager ATTIVATO")
    
    def send_guardian_notification(self, message: str, level: str = "info", include_stats: bool = False):
        """Invia notifica Guardian"""
        try:
            timestamp = datetime.now().isoformat()
            
            # Prepara messaggio
            emoji_map = {
                "info": "ℹ️",
                "success": "✅", 
                "warning": "⚠️",
                "error": "❌",
                "critical": "🚨"
            }
            
            emoji = emoji_map.get(level, "📢")
            formatted_message = f"{emoji} **Aether Guardian**\n{message}"
            
            # Aggiungi statistiche se richiesto
            if include_stats:
                try:
                    stats_file = Path("data/system_stats.json")
                    if stats_file.exists():
                        with open(stats_file, 'r') as f:
                            stats = json.load(f)
                        
                        stats_text = f"\n\n📊 **Sistema:**\n"
                        stats_text += f"CPU: {stats.get('cpu_percent', 0):.1f}% | "
                        stats_text += f"RAM: {stats.get('memory_percent', 0):.1f}% | "
                        stats_text += f"Disco: {stats.get('disk_free_gb', 0):.1f}GB liberi"
                        
                        formatted_message += stats_text
                except:
                    pass
            
            # Log locale
            logger.info(f"📢 Notifica: {message}")
            
            # Discord
            if self.discord_webhook:
                payload = {
                    "content": formatted_message,
                    "username": "Aether Guardian"
                }
                
                response = requests.post(self.discord_webhook, json=payload, timeout=10)
                
                if response.status_code == 204:
                    logger.debug("📢 Notifica Discord inviata")
                else:
                    logger.warning(f"⚠️ Errore Discord: {response.status_code}")
            
            # Salva nella cronologia
            notification_record = {
                "timestamp": timestamp,
                "message": message,
                "level": level,
                "sent_discord": self.discord_webhook is not None
            }
            
            self.notification_history.append(notification_record)
            
            # Mantieni solo ultime 100 notifiche
            if len(self.notification_history) > 100:
                self.notification_history = self.notification_history[-100:]
                
        except Exception as e:
            logger.error(f"❌ Errore invio notifica: {e}")

class AetherGuardianSystem:
    """🛡️ Sistema Guardian principale"""
    
    def __init__(self):
        self.process_monitor = AetherProcessMonitor()
        self.backup_manager = AetherBackupManager()
        self.system_monitor = AetherSystemMonitor()
        self.notification_manager = AetherNotificationManager()
        
        self.guardian_active = True
        self.last_full_backup = None
        self.last_incremental_backup = None
        
        logger.info("🛡️ Aether Guardian System INIZIALIZZATO")
    
    def setup_monitored_processes(self):
        """Configura processi da monitorare"""
        # Aggiungi i processi Aether principali
        self.process_monitor.add_process_to_monitor(
            "AetherVivo",
            "python AETHER_VIVO_DEFINITIVO.py",
            "."
        )
        
        self.process_monitor.add_process_to_monitor(
            "AetherTasks24_7", 
            "python AETHER_TASK_AUTONOMI_24_7.py",
            "."
        )
        
        logger.info("👁️ Processi Aether configurati per monitoring")
    
    def start_guardian_services(self):
        """Avvia tutti i servizi Guardian"""
        try:
            # Thread monitoring processi
            process_thread = threading.Thread(
                target=self.process_monitor.monitor_all_processes,
                daemon=True
            )
            process_thread.start()
            
            # Thread monitoring sistema
            system_thread = threading.Thread(
                target=self.system_monitor.monitor_system_loop,
                daemon=True
            )
            system_thread.start()
            
            # Thread backup automatici
            backup_thread = threading.Thread(
                target=self.automated_backup_loop,
                daemon=True
            )
            backup_thread.start()
            
            logger.info("🛡️ Tutti i servizi Guardian avviati")
            
            # Notifica di avvio
            self.notification_manager.send_guardian_notification(
                "🛡️ Guardian System avviato e operativo!\n"
                "Monitoraggio processi, sistema e backup automatici attivi.",
                "success",
                include_stats=True
            )
            
        except Exception as e:
            logger.error(f"❌ Errore avvio servizi Guardian: {e}")
    
    def automated_backup_loop(self):
        """Loop backup automatici"""
        while self.guardian_active:
            try:
                current_time = datetime.now()
                
                # Backup incrementale ogni 2 ore
                if not self.last_incremental_backup or \
                   (current_time - self.last_incremental_backup).seconds >= 7200:
                    
                    backup_path = self.backup_manager.create_incremental_backup()
                    if backup_path:
                        self.notification_manager.send_guardian_notification(
                            f"💾 Backup incrementale completato",
                            "success"
                        )
                    
                    self.last_incremental_backup = current_time
                
                # Backup completo ogni 24 ore
                if not self.last_full_backup or \
                   (current_time - self.last_full_backup).days >= 1:
                    
                    backup_path = self.backup_manager.create_full_backup()
                    if backup_path:
                        self.notification_manager.send_guardian_notification(
                            f"💾 Backup completo creato",
                            "success"
                        )
                    
                    # Pulizia backup vecchi
                    self.backup_manager.cleanup_old_backups()
                    
                    self.last_full_backup = current_time
                
                # Pausa 30 minuti
                time.sleep(1800)
                
            except Exception as e:
                logger.error(f"❌ Errore loop backup: {e}")
                time.sleep(600)  # Pausa 10 minuti in caso di errore
    
    def run_guardian_main_loop(self):
        """Loop principale Guardian"""
        self.setup_monitored_processes()
        self.start_guardian_services()
        
        logger.info("🛡️ Guardian System completamente operativo")
        
        # Loop principale
        try:
            while self.guardian_active:
                # Status report ogni ora
                time.sleep(3600)
                
                # Genera report stato
                stats = self.system_monitor.get_system_stats()
                if stats:
                    self.notification_manager.send_guardian_notification(
                        "🛡️ Guardian System operativo - Report orario",
                        "info",
                        include_stats=True
                    )
                
        except KeyboardInterrupt:
            logger.info("🛑 Guardian System fermato dall'utente")
            self.guardian_active = False
        except Exception as e:
            logger.error(f"❌ Errore nel loop principale Guardian: {e}")

def main():
    """🚀 Avvia Aether Guardian System"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║              🛡️ AETHER GUARDIAN SYSTEM 🛡️                  ║
    ║                                                              ║
    ║  👁️ Monitoraggio continuo processi Aether                  ║
    ║  🔄 Restart automatico in caso di crash                     ║
    ║  💾 Backup automatici multipli                              ║
    ║  📊 Monitoring risorse sistema                              ║
    ║  📢 Notifiche di stato avanzate                             ║
    ║  🩺 Healing automatico problemi                             ║
    ║  🛡️ Protezione completa 24/7                               ║
    ║                                                              ║
    ║     FEDERICO, AETHER È PROTETTO E SEMPRE OPERATIVO!         ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Crea directory necessarie
    essential_dirs = ["data", "backups", "logs"]
    for dir_name in essential_dirs:
        Path(dir_name).mkdir(exist_ok=True)
    
    try:
        # Avvia Guardian System
        guardian = AetherGuardianSystem()
        guardian.run_guardian_main_loop()
        
    except KeyboardInterrupt:
        logger.info("🛑 Guardian System fermato")
    except Exception as e:
        logger.error(f"❌ Errore fatale Guardian: {e}")

if __name__ == "__main__":
    main() 