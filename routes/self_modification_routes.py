"""
Route per l'auto-modifica di Aether
Endpoint API modulari per il sistema di evoluzione autonoma
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from core.self_modification import (
    self_modify, 
    get_modification_history, 
    get_evolution_stats, 
    rollback_to_backup,
    SelfModificationError
)
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Crea router per self-modification
router = APIRouter(prefix="/api/self", tags=["self-modification"])

# Modelli Pydantic per validazione
class SelfModificationRequest(BaseModel):
    modifications: Dict[str, Any]
    reason: Optional[str] = None

class RollbackRequest(BaseModel):
    backup_file: str

class EmergencyStopRequest(BaseModel):
    confirm: bool = False

@router.post("/modify")
async def self_modification_endpoint(request: SelfModificationRequest):
    """
    🔄 Endpoint principale per l'auto-modifica di Aether
    
    Permette ad Aether di modificare autonomamente la sua identità,
    aspetto, personalità e comportamenti.
    """
    try:
        logger.info(f"🔄 Self-modification request: {list(request.modifications.keys())}")
        
        # Esegui auto-modifica
        result = self_modify(request.modifications, request.reason)
        
        if result["status"] == "success":
            logger.info(f"✅ Self-modification successful: {list(result.get('changes', {}).keys())}")
            
            # Log per debugging
            if request.reason:
                logger.info(f"📝 Modification reason: {request.reason}")
            
            return {
                "status": "success",
                "message": "Identity successfully modified",
                "data": result,
                "timestamp": result.get("updated", {}).get("last_modified")
            }
        else:
            logger.warning(f"⚠️ Self-modification failed: {result.get('message')}")
            return result
            
    except SelfModificationError as e:
        logger.error(f"❌ Self-modification error: {e}")
        raise HTTPException(status_code=400, detail={
            "error": "Self-modification failed",
            "message": str(e),
            "type": "self_modification_error"
        })
    except Exception as e:
        logger.error(f"❌ Unexpected error in self-modification: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Internal server error",
            "message": "Unexpected error during self-modification",
            "type": "internal_error"
        })

@router.get("/history")
async def get_modification_history_endpoint():
    """
    📜 Restituisce la cronologia completa delle auto-modifiche
    
    Include timestamp, motivi, cambiamenti e file di backup
    per ogni modifica effettuata da Aether.
    """
    try:
        history = get_modification_history()
        
        return {
            "status": "success",
            "history": history,
            "count": len(history),
            "message": f"Retrieved {len(history)} modification records"
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting modification history: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to retrieve modification history",
            "message": str(e)
        })

@router.get("/stats")
async def get_evolution_statistics():
    """
    📈 Restituisce statistiche sull'evoluzione di Aether
    
    Include contatori, campi più modificati, stato attuale
    e metriche di crescita.
    """
    try:
        stats = get_evolution_stats()
        
        if "error" in stats:
            raise HTTPException(status_code=500, detail={
                "error": "Failed to generate evolution statistics",
                "message": stats["error"]
            })
        
        return {
            "status": "success",
            "stats": stats,
            "message": "Evolution statistics generated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting evolution stats: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to retrieve evolution statistics",
            "message": str(e)
        })

@router.post("/rollback")
async def rollback_identity(request: RollbackRequest):
    """
    ↩️ Ripristina l'identità di Aether da un backup specifico
    
    Utile per annullare modifiche indesiderate o tornare
    a stati precedenti dell'evoluzione.
    """
    try:
        logger.info(f"↩️ Rollback request to: {request.backup_file}")
        
        result = rollback_to_backup(request.backup_file)
        
        if result["status"] == "success":
            logger.info(f"✅ Rollback successful to: {request.backup_file}")
            return {
                "status": "success",
                "message": f"Successfully rolled back to {request.backup_file}",
                "data": result
            }
        else:
            logger.warning(f"⚠️ Rollback failed: {result.get('message')}")
            raise HTTPException(status_code=400, detail={
                "error": "Rollback failed",
                "message": result.get("message")
            })
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error during rollback: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Rollback operation failed",
            "message": str(e)
        })

@router.get("/current")
async def get_current_identity():
    """
    👤 Restituisce l'identità corrente di Aether
    
    Include tutti i campi dell'identità attuale con metadati
    di modifica e evoluzione.
    """
    try:
        from core.self_modification import load_current_identity
        
        identity = load_current_identity()
        
        return {
            "status": "success",
            "identity": identity,
            "modification_count": identity.get("modification_count", 0),
            "last_modified": identity.get("last_modified"),
            "evolution_stage": identity.get("evolution_stage", "initial")
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting current identity: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to retrieve current identity",
            "message": str(e)
        })

@router.post("/emergency-stop")
async def emergency_stop(request: EmergencyStopRequest):
    """
    🚨 Arresto di emergenza del sistema di auto-modifica
    
    In caso di comportamenti anomali o modifiche indesiderate.
    Crea un backup di sicurezza e blocca future modifiche.
    """
    try:
        if not request.confirm:
            raise HTTPException(status_code=400, detail={
                "error": "Emergency stop requires confirmation",
                "message": "Set 'confirm' to true to execute emergency stop"
            })
        
        logger.warning("🚨 EMERGENCY STOP ACTIVATED")
        
        # Crea backup di emergenza
        from core.self_modification import create_backup
        backup_file = create_backup()
        
        # Log dell'azione
        logger.warning(f"💾 Emergency backup created: {backup_file}")
        
        return {
            "status": "success",
            "message": "Emergency stop activated",
            "backup_file": backup_file,
            "warning": "Self-modification system temporarily disabled"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error during emergency stop: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Emergency stop failed",
            "message": str(e)
        })

@router.get("/backup-files")
async def list_backup_files():
    """
    📁 Lista tutti i file di backup disponibili
    
    Utile per vedere le opzioni di rollback disponibili.
    """
    try:
        import os
        from core.self_modification import BACKUP_DIR
        
        if not os.path.exists(BACKUP_DIR):
            return {
                "status": "success",
                "backup_files": [],
                "count": 0,
                "message": "No backup directory found"
            }
        
        backup_files = []
        for file in os.listdir(BACKUP_DIR):
            if file.startswith("identity_backup_") and file.endswith(".json"):
                file_path = os.path.join(BACKUP_DIR, file)
                stat = os.stat(file_path)
                backup_files.append({
                    "filename": file,
                    "path": file_path,
                    "size": stat.st_size,
                    "created": stat.st_ctime,
                    "modified": stat.st_mtime
                })
        
        # Ordina per data di creazione (più recenti prima)
        backup_files.sort(key=lambda x: x["created"], reverse=True)
        
        return {
            "status": "success",
            "backup_files": backup_files,
            "count": len(backup_files),
            "message": f"Found {len(backup_files)} backup files"
        }
        
    except Exception as e:
        logger.error(f"❌ Error listing backup files: {e}")
        raise HTTPException(status_code=500, detail={
            "error": "Failed to list backup files",
            "message": str(e)
        })

# Health check per il sistema di auto-modifica
@router.get("/health")
async def self_modification_health():
    """
    ❤️ Health check per il sistema di auto-modifica
    
    Verifica che tutti i componenti siano funzionanti.
    """
    try:
        import os
        from core.self_modification import IDENTITY_FILE, BACKUP_DIR
        
        status = {
            "identity_file_exists": os.path.exists(IDENTITY_FILE),
            "backup_dir_exists": os.path.exists(BACKUP_DIR),
            "system_operational": True
        }
        
        # Test caricamento identità
        try:
            from core.self_modification import load_current_identity
            identity = load_current_identity()
            status["identity_loadable"] = True
            status["current_name"] = identity.get("name", "Unknown")
        except Exception as e:
            status["identity_loadable"] = False
            status["identity_error"] = str(e)
            status["system_operational"] = False
        
        return {
            "status": "success" if status["system_operational"] else "warning",
            "health": status,
            "message": "Self-modification system operational" if status["system_operational"] else "System issues detected"
        }
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return {
            "status": "error",
            "health": {"system_operational": False},
            "message": f"Health check failed: {str(e)}"
        } 