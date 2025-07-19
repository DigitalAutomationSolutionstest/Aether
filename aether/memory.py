#!/usr/bin/env python3
"""
🧠 AETHER MEMORY MANAGER
Sistema di gestione memoria integrato con Supabase

Gestisce:
- Pensieri e riflessioni in tempo reale
- Memoria semantica e esperienze
- Configurazioni ambiente e scene 3D
- Azioni economiche e ROI tracking
- Sincronizzazione memoria locale + cloud
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

# Configurazione Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

# Inizializza client Supabase
sb = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        import supabase
        sb = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✅ Supabase client initialized successfully")
    except ImportError:
        logger.warning("⚠️ Supabase not installed - falling back to local memory only")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Supabase client: {e}")
else:
    logger.warning("⚠️ Supabase credentials not found - using local memory only")

class MemoryManager:
    """
    🧠 Gestore memoria avanzato per Aether
    Combina memoria locale (JSON) e cloud (Supabase)
    """
    
    def __init__(self):
        self.local_memory_dir = "aether/memory"
        self.ensure_local_memory_dir()
        self.supabase_available = sb is not None
        
        logger.info(f"📁 Memory manager initialized - Supabase: {'Available' if self.supabase_available else 'Unavailable'}")
    
    def ensure_local_memory_dir(self):
        """Assicura che la directory di memoria locale esista"""
        os.makedirs(self.local_memory_dir, exist_ok=True)
    
    def save_thought(self, thought: Dict[str, Any]) -> bool:
        """
        💭 Salva un pensiero sia localmente che su Supabase
        
        Args:
            thought: Dizionario con il pensiero da salvare
            
        Returns:
            bool: Successo dell'operazione
        """
        try:
            # Prepara dati del pensiero
            thought_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "type": thought.get("type", "thought"),
                "content": thought.get("content", ""),
                "context": thought.get("context", {})
            }
            
            # Salva localmente
            local_success = self._save_thought_local(thought_data)
            
            # Salva su Supabase se disponibile
            supabase_success = True
            if self.supabase_available:
                supabase_success = self._save_thought_supabase(thought_data)
            
            success = local_success and (supabase_success or not self.supabase_available)
            
            if success:
                logger.info(f"💭 Thought saved: {thought_data['type']} - {thought_data['content'][:50]}...")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error saving thought: {e}")
            return False
    
    def _save_thought_local(self, thought_data: Dict) -> bool:
        """Salva pensiero in memoria locale"""
        try:
            filename = f"thought_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.local_memory_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(thought_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            logger.error(f"❌ Error saving thought locally: {e}")
            return False
    
    def _save_thought_supabase(self, thought_data: Dict) -> bool:
        """Salva pensiero su Supabase"""
        try:
            if not sb:
                return False
                
            result = sb.table("aether_thoughts").insert(thought_data).execute()
            return result.data is not None
            
        except Exception as e:
            logger.error(f"❌ Error saving thought to Supabase: {e}")
            return False
    
    def save_memory(self, content: str, tags: List[str] = None, metadata: Dict = None) -> bool:
        """
        🧠 Salva una memoria semantica
        
        Args:
            content: Contenuto della memoria
            tags: Tag associati alla memoria
            metadata: Metadati aggiuntivi
            
        Returns:
            bool: Successo dell'operazione
        """
        try:
            memory_data = {
                "content": content,
                "tags": tags or [],
                "metadata": metadata or {},
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Salva localmente
            local_success = self._save_memory_local(memory_data)
            
            # Salva su Supabase se disponibile
            supabase_success = True
            if self.supabase_available:
                supabase_success = self._save_memory_supabase(memory_data)
            
            success = local_success and (supabase_success or not self.supabase_available)
            
            if success:
                logger.info(f"🧠 Memory saved: {content[:50]}... (tags: {tags})")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error saving memory: {e}")
            return False
    
    def _save_memory_local(self, memory_data: Dict) -> bool:
        """Salva memoria in locale"""
        try:
            filename = f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.local_memory_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            logger.error(f"❌ Error saving memory locally: {e}")
            return False
    
    def _save_memory_supabase(self, memory_data: Dict) -> bool:
        """Salva memoria su Supabase"""
        try:
            if not sb:
                return False
                
            result = sb.table("aether_memory").insert(memory_data).execute()
            return result.data is not None
            
        except Exception as e:
            logger.error(f"❌ Error saving memory to Supabase: {e}")
            return False
    
    def save_environment_step(self, action: str, image_url: str = None, scene_config: Dict = None) -> bool:
        """
        🌍 Salva uno step dell'ambiente/scena 3D
        
        Args:
            action: Nome dell'azione/scena
            image_url: URL dell'immagine generata (opzionale)
            scene_config: Configurazione dettagliata della scena
            
        Returns:
            bool: Successo dell'operazione
        """
        try:
            env_data = {
                "scene_name": action,
                "scene_config": scene_config or {"image": image_url} if image_url else {},
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Salva localmente
            local_success = self._save_environment_local(env_data)
            
            # Salva su Supabase se disponibile
            supabase_success = True
            if self.supabase_available:
                supabase_success = self._save_environment_supabase(env_data)
            
            success = local_success and (supabase_success or not self.supabase_available)
            
            if success:
                logger.info(f"🌍 Environment step saved: {action}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error saving environment step: {e}")
            return False
    
    def _save_environment_local(self, env_data: Dict) -> bool:
        """Salva ambiente in locale"""
        try:
            filename = f"environment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.local_memory_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(env_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            logger.error(f"❌ Error saving environment locally: {e}")
            return False
    
    def _save_environment_supabase(self, env_data: Dict) -> bool:
        """Salva ambiente su Supabase"""
        try:
            if not sb:
                return False
                
            result = sb.table("aether_environment").insert(env_data).execute()
            return result.data is not None
            
        except Exception as e:
            logger.error(f"❌ Error saving environment to Supabase: {e}")
            return False
    
    def save_economic_action(self, action: str, cost: float, expected_roi: float, status: str = "planned") -> bool:
        """
        💰 Salva un'azione economica per tracking ROI
        
        Args:
            action: Descrizione dell'azione
            cost: Costo dell'azione
            expected_roi: ROI atteso
            status: Stato dell'azione (planned, executed, completed, failed)
            
        Returns:
            bool: Successo dell'operazione
        """
        try:
            economy_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "action": action,
                "cost": cost,
                "expected_roi": expected_roi,
                "status": status
            }
            
            # Salva localmente
            local_success = self._save_economic_local(economy_data)
            
            # Salva su Supabase se disponibile
            supabase_success = True
            if self.supabase_available:
                supabase_success = self._save_economic_supabase(economy_data)
            
            success = local_success and (supabase_success or not self.supabase_available)
            
            if success:
                logger.info(f"💰 Economic action saved: {action} (ROI: {expected_roi}%)")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error saving economic action: {e}")
            return False
    
    def _save_economic_local(self, economy_data: Dict) -> bool:
        """Salva azione economica in locale"""
        try:
            filename = f"economy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.local_memory_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(economy_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            logger.error(f"❌ Error saving economic action locally: {e}")
            return False
    
    def _save_economic_supabase(self, economy_data: Dict) -> bool:
        """Salva azione economica su Supabase"""
        try:
            if not sb:
                return False
                
            result = sb.table("aether_economy").insert(economy_data).execute()
            return result.data is not None
            
        except Exception as e:
            logger.error(f"❌ Error saving economic action to Supabase: {e}")
            return False
    
    def get_recent_thoughts(self, limit: int = 10) -> List[Dict]:
        """
        📖 Ottiene i pensieri più recenti
        
        Args:
            limit: Numero massimo di pensieri da restituire
            
        Returns:
            List[Dict]: Lista dei pensieri recenti
        """
        try:
            if self.supabase_available:
                result = sb.table("aether_thoughts").select("*").order("timestamp", desc=True).limit(limit).execute()
                if result.data:
                    return result.data
            
            # Fallback: leggi da memoria locale
            return self._get_recent_thoughts_local(limit)
            
        except Exception as e:
            logger.error(f"❌ Error getting recent thoughts: {e}")
            return []
    
    def _get_recent_thoughts_local(self, limit: int) -> List[Dict]:
        """Ottiene pensieri recenti da memoria locale"""
        try:
            thoughts = []
            thought_files = [f for f in os.listdir(self.local_memory_dir) if f.startswith('thought_')]
            thought_files.sort(reverse=True)
            
            for filename in thought_files[:limit]:
                filepath = os.path.join(self.local_memory_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    thoughts.append(json.load(f))
            
            return thoughts
        except Exception as e:
            logger.error(f"❌ Error getting local thoughts: {e}")
            return []
    
    def get_memory_by_tags(self, tags: List[str]) -> List[Dict]:
        """
        🔍 Cerca memorie per tag
        
        Args:
            tags: Lista di tag da cercare
            
        Returns:
            List[Dict]: Memorie trovate
        """
        try:
            if self.supabase_available:
                # Query Supabase con ricerca nei tag
                result = sb.table("aether_memory").select("*").contains("tags", tags).execute()
                if result.data:
                    return result.data
            
            # Fallback: cerca in locale
            return self._get_memory_by_tags_local(tags)
            
        except Exception as e:
            logger.error(f"❌ Error searching memory by tags: {e}")
            return []
    
    def _get_memory_by_tags_local(self, tags: List[str]) -> List[Dict]:
        """Cerca memorie per tag in locale"""
        try:
            memories = []
            memory_files = [f for f in os.listdir(self.local_memory_dir) if f.startswith('memory_')]
            
            for filename in memory_files:
                filepath = os.path.join(self.local_memory_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    memory = json.load(f)
                    memory_tags = memory.get('tags', [])
                    if any(tag in memory_tags for tag in tags):
                        memories.append(memory)
            
            return memories
        except Exception as e:
            logger.error(f"❌ Error searching local memory: {e}")
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """
        📊 Ottiene lo status del sistema di memoria
        
        Returns:
            Dict: Status del sistema
        """
        local_count = len([f for f in os.listdir(self.local_memory_dir) if f.endswith('.json')])
        
        status = {
            "local_memory_available": True,
            "local_memory_count": local_count,
            "supabase_available": self.supabase_available,
            "memory_dir": self.local_memory_dir,
            "timestamp": datetime.now().isoformat()
        }
        
        if self.supabase_available:
            try:
                # Test connessione Supabase
                test_result = sb.table("aether_thoughts").select("id").limit(1).execute()
                status["supabase_connected"] = True
                status["supabase_test"] = "success"
            except Exception as e:
                status["supabase_connected"] = False
                status["supabase_error"] = str(e)
        
        return status

# Istanza globale del memory manager
memory_manager = MemoryManager()

# Funzioni di convenienza per retrocompatibilità
def save_thought(thought: Dict[str, Any]) -> bool:
    """Funzione di convenienza per salvare pensieri"""
    return memory_manager.save_thought(thought)

def save_memory(content: str, tags: List[str] = None) -> bool:
    """Funzione di convenienza per salvare memoria"""
    return memory_manager.save_memory(content, tags)

def save_environment_step(action: str, image_url: str = None) -> bool:
    """Funzione di convenienza per salvare step ambiente"""
    return memory_manager.save_environment_step(action, image_url)

def get_recent_thoughts(limit: int = 10) -> List[Dict]:
    """Funzione di convenienza per ottenere pensieri recenti"""
    return memory_manager.get_recent_thoughts(limit) 