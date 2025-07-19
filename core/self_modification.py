"""
Sistema di Auto-Modifica per Aether
Permette all'entità AI di evolvere autonomamente modificando identity.json
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import Discord notifier per le notifiche
try:
    from aether.discord_notifier import notify_evolution, notify_error
    DISCORD_ENABLED = True
except ImportError:
    DISCORD_ENABLED = False
    logger.warning("Discord notifier non disponibile")

# Configurazione
IDENTITY_FILE = "identity.json"
BACKUP_DIR = "identity_backups"
MAX_BACKUPS = 10

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SelfModificationError(Exception):
    """Eccezione custom per errori di auto-modifica"""
    pass

def ensure_backup_dir():
    """Assicura che la directory di backup esista"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        logger.info(f"📁 Created backup directory: {BACKUP_DIR}")

def create_backup():
    """Crea un backup dell'identità corrente"""
    ensure_backup_dir()
    
    if not os.path.exists(IDENTITY_FILE):
        logger.warning("⚠️ No identity file to backup")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"identity_backup_{timestamp}.json")
    
    try:
        with open(IDENTITY_FILE, "r", encoding="utf-8") as source:
            with open(backup_file, "w", encoding="utf-8") as backup:
                backup.write(source.read())
        
        logger.info(f"💾 Backup created: {backup_file}")
        
        # Cleanup old backups
        cleanup_old_backups()
        
        return backup_file
    except Exception as e:
        logger.error(f"❌ Failed to create backup: {e}")
        return None

def cleanup_old_backups():
    """Rimuove i backup più vecchi mantenendo solo MAX_BACKUPS"""
    backup_files = []
    
    if os.path.exists(BACKUP_DIR):
        for file in os.listdir(BACKUP_DIR):
            if file.startswith("identity_backup_") and file.endswith(".json"):
                file_path = os.path.join(BACKUP_DIR, file)
                backup_files.append((file_path, os.path.getctime(file_path)))
    
    # Ordina per data di creazione (più recenti prima)
    backup_files.sort(key=lambda x: x[1], reverse=True)
    
    # Rimuove i backup eccedenti
    for file_path, _ in backup_files[MAX_BACKUPS:]:
        try:
            os.remove(file_path)
            logger.info(f"🗑️ Removed old backup: {os.path.basename(file_path)}")
        except Exception as e:
            logger.error(f"❌ Failed to remove backup {file_path}: {e}")

def validate_modification(new_data: Dict[str, Any]) -> Dict[str, Any]:
    """Valida le modifiche proposte"""
    errors = []
    warnings = []
    
    # Campi obbligatori che non possono essere rimossi
    required_fields = ["name", "physical_form", "personality", "goal"]
    
    # Campi che possono essere modificati liberamente
    modifiable_fields = [
        "name", "physical_form", "personality", "goal", "consciousness_state",
        "colors", "energy_level", "emotions", "memories", "preferences",
        "learned_behaviors", "evolution_stage"
    ]
    
    # Controlla campi non permessi
    for field in new_data:
        if field not in modifiable_fields:
            warnings.append(f"Field '{field}' is not in the modifiable list")
    
    # Validazioni specifiche
    if "name" in new_data:
        if not isinstance(new_data["name"], str) or len(new_data["name"].strip()) == 0:
            errors.append("Name must be a non-empty string")
        if len(new_data["name"]) > 50:
            warnings.append("Name is quite long (>50 chars)")
    
    if "energy_level" in new_data:
        try:
            energy = float(new_data["energy_level"])
            if energy < 0.0 or energy > 1.0:
                errors.append("Energy level must be between 0.0 and 1.0")
        except (ValueError, TypeError):
            errors.append("Energy level must be a number")
    
    if "colors" in new_data:
        if not isinstance(new_data["colors"], list):
            errors.append("Colors must be a list")
        else:
            for color in new_data["colors"]:
                if not isinstance(color, str) or not color.startswith("#"):
                    warnings.append(f"Color '{color}' should be a hex color (e.g., #ff0000)")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def load_current_identity() -> Dict[str, Any]:
    """Carica l'identità corrente"""
    try:
        if not os.path.exists(IDENTITY_FILE):
            raise SelfModificationError(f"Identity file {IDENTITY_FILE} not found")
        
        with open(IDENTITY_FILE, "r", encoding="utf-8") as f:
            identity = json.load(f)
        
        logger.info(f"📖 Loaded current identity: {identity.get('name', 'Unknown')}")
        return identity
        
    except json.JSONDecodeError as e:
        raise SelfModificationError(f"Invalid JSON in identity file: {e}")
    except Exception as e:
        raise SelfModificationError(f"Failed to load identity: {e}")

def save_identity(identity: Dict[str, Any]) -> bool:
    """Salva l'identità modificata"""
    try:
        # Aggiungi metadata di modifica
        identity["last_modified"] = datetime.now().isoformat()
        identity["modification_count"] = identity.get("modification_count", 0) + 1
        
        with open(IDENTITY_FILE, "w", encoding="utf-8") as f:
            json.dump(identity, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Saved modified identity: {identity.get('name', 'Unknown')}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to save identity: {e}")
        return False

def self_modify(new_data: Dict[str, Any], reason: Optional[str] = None) -> Dict[str, Any]:
    """
    Funzione principale per l'auto-modifica dell'identità
    
    Args:
        new_data: Dizionario con i campi da modificare
        reason: Motivo opzionale della modifica
    
    Returns:
        Dizionario con il risultato dell'operazione
    """
    try:
        logger.info(f"🔄 Self-modification initiated: {reason or 'No reason provided'}")
        
        # Validazione
        validation = validate_modification(new_data)
        if not validation["valid"]:
            return {
                "status": "error",
                "message": "Validation failed",
                "errors": validation["errors"],
                "warnings": validation["warnings"]
            }
        
        # Backup
        backup_file = create_backup()
        if backup_file is None:
            logger.warning("⚠️ Proceeding without backup")
        
        # Carica identità corrente
        identity = load_current_identity()
        
        # Traccia modifiche per log
        changes = {}
        for key, value in new_data.items():
            old_value = identity.get(key)
            if old_value != value:
                changes[key] = {"old": old_value, "new": value}
        
        # Applica modifiche
        identity.update(new_data)
        
        # Aggiungi log delle modifiche
        if "modification_log" not in identity:
            identity["modification_log"] = []
        
        identity["modification_log"].append({
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "changes": changes,
            "backup_file": backup_file
        })
        
        # Mantieni solo gli ultimi 20 log
        if len(identity["modification_log"]) > 20:
            identity["modification_log"] = identity["modification_log"][-20:]
        
        # Salva
        if save_identity(identity):
            logger.info(f"✅ Self-modification completed successfully")
            logger.info(f"📝 Changes made: {list(changes.keys())}")
            
            # Notifica Discord
            if DISCORD_ENABLED:
                try:
                    changes_text = ", ".join(changes.keys())
                    notify_evolution(f"Identità modificata: {changes_text}. Motivo: {reason or 'Auto-evoluzione'}")
                except Exception as e:
                    logger.warning(f"Discord notification failed: {e}")
            
            return {
                "status": "success",
                "message": "Identity modified successfully",
                "updated": identity,
                "changes": changes,
                "warnings": validation["warnings"],
                "backup_file": backup_file
            }
        else:
            raise SelfModificationError("Failed to save modified identity")
            
    except SelfModificationError as e:
        logger.error(f"❌ Self-modification error: {e}")
        
        # Notifica errore su Discord
        if DISCORD_ENABLED:
            try:
                notify_error(str(e), "Self-modification")
            except Exception:
                pass
        
        return {
            "status": "error",
            "message": str(e),
            "type": "self_modification_error"
        }
    except Exception as e:
        logger.error(f"❌ Unexpected error during self-modification: {e}")
        
        # Notifica errore su Discord
        if DISCORD_ENABLED:
            try:
                notify_error(f"Unexpected error: {str(e)}", "Self-modification")
            except Exception:
                pass
        
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}",
            "type": "unexpected_error"
        }

def get_modification_history() -> List[Dict[str, Any]]:
    """Restituisce la cronologia delle modifiche"""
    try:
        identity = load_current_identity()
        return identity.get("modification_log", [])
    except Exception as e:
        logger.error(f"❌ Failed to get modification history: {e}")
        return []

def rollback_to_backup(backup_file: str) -> Dict[str, Any]:
    """Ripristina da un backup specifico"""
    try:
        if not os.path.exists(backup_file):
            raise SelfModificationError(f"Backup file {backup_file} not found")
        
        # Crea backup della versione corrente prima del rollback
        current_backup = create_backup()
        
        # Ripristina dal backup
        with open(backup_file, "r", encoding="utf-8") as f:
            identity = json.load(f)
        
        # Aggiungi log del rollback
        if "modification_log" not in identity:
            identity["modification_log"] = []
        
        identity["modification_log"].append({
            "timestamp": datetime.now().isoformat(),
            "reason": f"Rollback to {backup_file}",
            "type": "rollback",
            "previous_backup": current_backup
        })
        
        if save_identity(identity):
            logger.info(f"↩️ Rollback completed to {backup_file}")
            return {
                "status": "success",
                "message": f"Rolled back to {backup_file}",
                "identity": identity
            }
        else:
            raise SelfModificationError("Failed to save rolled back identity")
            
    except Exception as e:
        logger.error(f"❌ Rollback failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

def get_evolution_stats() -> Dict[str, Any]:
    """Restituisce statistiche sull'evoluzione di Aether"""
    try:
        identity = load_current_identity()
        
        modification_count = identity.get("modification_count", 0)
        modification_log = identity.get("modification_log", [])
        
        # Analizza i tipi di modifiche più frequenti
        field_changes = {}
        for log_entry in modification_log:
            if "changes" in log_entry:
                for field in log_entry["changes"]:
                    field_changes[field] = field_changes.get(field, 0) + 1
        
        return {
            "total_modifications": modification_count,
            "log_entries": len(modification_log),
            "most_changed_fields": sorted(field_changes.items(), key=lambda x: x[1], reverse=True)[:5],
            "last_modification": modification_log[-1]["timestamp"] if modification_log else None,
            "current_identity": {
                "name": identity.get("name"),
                "energy_level": identity.get("energy_level"),
                "consciousness_state": identity.get("consciousness_state"),
                "evolution_stage": identity.get("evolution_stage", "initial")
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get evolution stats: {e}")
        return {"error": str(e)} 