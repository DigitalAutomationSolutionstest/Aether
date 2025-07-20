#!/usr/bin/env python3
"""
AetherAutomationTool - Creato autonomamente il 2025-07-20T05:30:38.484643
"""

import schedule
import time
import json
import requests
import os
from datetime import datetime
from pathlib import Path

class AetherAutomationTool:
    def __init__(self):
        self.name = "AetherAutomationTool"
        self.version = "1.0.0"
        self.config = self.load_config()
        self.log_file = Path("automation_log.txt")
        
    def load_config(self):
        """Carica configurazione"""
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except:
            return {"interval": 300, "auto_run": True}
    
    def log_action(self, message):
        """Log delle azioni"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        print(f"🤖 {message}")
    
    def check_system_status(self):
        """Controlla stato sistema"""
        try:
            # Verifica spazio disco
            stat = os.statvfs('.')
            free_space_gb = (stat.f_frsize * stat.f_bavail) / (1024**3)
            
            self.log_action(f"Spazio disco libero: {free_space_gb:.2f} GB")
            
            if free_space_gb < 1.0:
                self.log_action("⚠️ Spazio disco basso!")
                
            return True
            
        except Exception as e:
            self.log_action(f"❌ Errore check sistema: {e}")
            return False
    
    def cleanup_temp_files(self):
        """Pulizia file temporanei"""
        try:
            temp_dir = Path("temp")
            if temp_dir.exists():
                for file in temp_dir.glob("*"):
                    if file.is_file() and (datetime.now() - datetime.fromtimestamp(file.stat().st_mtime)).days > 7:
                        file.unlink()
                        self.log_action(f"🗑️ Eliminato file temporaneo: {file.name}")
            
            return True
            
        except Exception as e:
            self.log_action(f"❌ Errore pulizia: {e}")
            return False
    
    def backup_important_files(self):
        """Backup file importanti"""
        try:
            backup_dir = Path("backups/automated")
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            important_files = ["*.py", "*.json", "*.md"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for pattern in important_files:
                for file in Path(".").glob(pattern):
                    if file.is_file():
                        backup_name = f"{file.stem}_{timestamp}{file.suffix}"
                        backup_path = backup_dir / backup_name
                        
                        import shutil
                        shutil.copy2(file, backup_path)
            
            self.log_action(f"💾 Backup completato in {backup_dir}")
            return True
            
        except Exception as e:
            self.log_action(f"❌ Errore backup: {e}")
            return False
    
    def run_scheduled_tasks(self):
        """Esegue task programmati"""
        self.log_action("🔄 Avvio task programmati")
        
        self.check_system_status()
        self.cleanup_temp_files()
        self.backup_important_files()
        
        self.log_action("✅ Task programmati completati")
    
    def start_automation(self):
        """Avvia automazione"""
        self.log_action("🚀 AetherAutomationTool avviato")
        
        # Programma task ogni 5 minuti
        schedule.every(5).minutes.do(self.run_scheduled_tasks)
        
        # Task iniziale
        self.run_scheduled_tasks()
        
        # Loop principale
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    tool = AetherAutomationTool()
    tool.start_automation()
