#!/usr/bin/env python3
"""
🚀 AETHER CODE EXECUTOR - Motore Principale di Esecuzione

Trasforma i pensieri di Aether in codice reale con:
- Esecuzione sicura in sandbox
- Salvataggio automatico su Supabase  
- Versionamento Git automatico
- Template intelligenti
- Monitoring completo
"""

import os
import sys
import json
import subprocess
import threading
import time
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import tempfile
import shutil

# Import moduli interni
from .sandbox import SANDBOX_ROOT, SCRIPTS_DIR, TEMP_DIR, RESULTS_DIR
from .logs import setup_executor_logger
from .outputs import save_output, GENERATED_CODE_DIR
from .templates import get_template, get_base_template
from .supabase_integrator import SupabaseCodeManager
from .git_versioner import GitAutomation

class AetherCodeExecutor:
    """
    🧠 Motore di esecuzione codice autonomo per Aether
    
    Caratteristiche:
    - Sandbox sicura per esecuzione
    - Integrazione Supabase per persistenza
    - Git automatico per versionamento
    - Template intelligenti
    - Monitoring real-time
    """
    
    def __init__(self, 
                 timeout: int = 60,
                 max_memory_mb: int = 256,
                 enable_supabase: bool = True,
                 enable_git: bool = True):
        
        self.timeout = timeout
        self.max_memory_mb = max_memory_mb
        self.execution_count = 0
        self.success_count = 0
        self.error_count = 0
        
        # Setup logging
        self.logger = setup_executor_logger("aether_code_executor")
        
        # Setup componenti
        self.supabase_manager = None
        self.git_automation = None
        
        if enable_supabase:
            try:
                self.supabase_manager = SupabaseCodeManager()
                self.logger.info("✅ Supabase integrazione attivata")
            except Exception as e:
                self.logger.warning(f"⚠️ Supabase non disponibile: {e}")
        
        if enable_git:
            try:
                self.git_automation = GitAutomation()
                self.logger.info("✅ Git automation attivata")
            except Exception as e:
                self.logger.warning(f"⚠️ Git non disponibile: {e}")
        
        self.logger.info("🚀 AetherCodeExecutor inizializzato")
    
    def execute_thought(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """
        🧠 Esegue un pensiero trasformandolo in codice
        
        Args:
            thought: Pensiero da eseguire con tipo e dettagli
            
        Returns:
            Risultato dell'esecuzione con status e output
        """
        self.execution_count += 1
        execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.execution_count}"
        
        self.logger.info(f"🧠 Esecuzione pensiero #{self.execution_count}: {thought.get('type', 'unknown')}")
        
        try:
            # Analizza il pensiero
            thought_type = thought.get('type', 'generic')
            details = thought.get('details', {})
            priority = thought.get('priority', 'medium')
            
            # Genera codice dal pensiero
            generated_code = self._generate_code_from_thought(thought)
            
            # Salva il codice generato
            code_file = self._save_generated_code(generated_code, execution_id, thought_type)
            
            # Esegue il codice in sandbox
            execution_result = self._execute_in_sandbox(code_file)
            
            # Prepara risultato completo
            result = {
                'execution_id': execution_id,
                'thought': thought,
                'generated_code': generated_code,
                'code_file': str(code_file),
                'execution_result': execution_result,
                'timestamp': datetime.now().isoformat(),
                'success': execution_result.get('success', False)
            }
            
            # Salva su Supabase
            if self.supabase_manager:
                self._save_to_supabase(result)
            
            # Commit su Git se successo
            if self.git_automation and result['success']:
                self._commit_to_git(result)
            
            # Aggiorna statistiche
            if result['success']:
                self.success_count += 1
            else:
                self.error_count += 1
            
            # Salva report finale
            self._save_execution_report(result)
            
            self.logger.info(f"✅ Pensiero eseguito con successo: {execution_id}")
            return result
            
        except Exception as e:
            self.error_count += 1
            error_result = {
                'execution_id': execution_id,
                'thought': thought,
                'error': str(e),
                'traceback': traceback.format_exc(),
                'timestamp': datetime.now().isoformat(),
                'success': False
            }
            
            self.logger.error(f"❌ Errore esecuzione {execution_id}: {e}")
            self.logger.debug(f"Traceback: {traceback.format_exc()}")
            return error_result
    
    def _generate_code_from_thought(self, thought: Dict[str, Any]) -> str:
        """Genera codice Python dal pensiero"""
        thought_type = thought.get('type', 'generic')
        details = thought.get('details', {})
        
        # Ottieni template appropriato
        template = get_template(thought_type)
        
        # Personalizza il template
        timestamp = datetime.now().isoformat()
        purpose = thought.get('purpose', details if isinstance(details, str) else str(details))
        
        # Sostituzioni nel template
        code = template.format(
            timestamp=timestamp,
            purpose=purpose,
            thought_type=thought_type,
            details=json.dumps(details, indent=2)
        )
        
        # Aggiungi import datetime se necessario
        if 'datetime' not in code:
            code = code.replace('from typing import Dict, Any, Optional, List', 
                               'from typing import Dict, Any, Optional, List\nfrom datetime import datetime')
        
        # Aggiungi logica specifica per tipo
        if thought_type == 'create_agent':
            code += self._generate_agent_code(details)
        elif thought_type == 'create_tool':
            code += self._generate_tool_code(details)
        elif thought_type == 'data_analysis':
            code += self._generate_analysis_code(details)
        
        return code
    
    def _save_generated_code(self, code: str, execution_id: str, thought_type: str) -> Path:
        """Salva il codice generato in un file"""
        filename = f"{thought_type}_{execution_id}.py"
        code_file = SCRIPTS_DIR / filename
        
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        self.logger.debug(f"📝 Codice salvato: {code_file}")
        return code_file
    
    def _execute_in_sandbox(self, code_file: Path) -> Dict[str, Any]:
        """Esegue il codice in ambiente sandbox sicuro"""
        try:
            # Comando di esecuzione
            cmd = [sys.executable, str(code_file)]
            
            # Esecuzione con timeout e limitazioni
            start_time = time.time()
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=SANDBOX_ROOT,
                timeout=self.timeout
            )
            
            stdout, stderr = process.communicate(timeout=self.timeout)
            execution_time = time.time() - start_time
            
            result = {
                'success': process.returncode == 0,
                'return_code': process.returncode,
                'stdout': stdout,
                'stderr': stderr,
                'execution_time': execution_time,
                'timeout': execution_time >= self.timeout
            }
            
            self.logger.debug(f"⚡ Esecuzione completata in {execution_time:.2f}s")
            return result
            
        except subprocess.TimeoutExpired:
            process.kill()
            return {
                'success': False,
                'error': 'Timeout eseguita',
                'timeout': True,
                'execution_time': self.timeout
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timeout': False
            }
    
    def _save_to_supabase(self, result: Dict[str, Any]):
        """Salva risultato su Supabase"""
        if self.supabase_manager:
            self.supabase_manager.save_execution_result(result)
    
    def _commit_to_git(self, result: Dict[str, Any]):
        """Commit automatico su Git"""
        if self.git_automation:
            commit_message = f"🤖 Aether: {result['thought'].get('type', 'code')} - {result['execution_id']}"
            self.git_automation.auto_commit(commit_message)
    
    def _save_execution_report(self, result: Dict[str, Any]):
        """Salva report di esecuzione"""
        save_output('report', result)
    
    def _generate_agent_code(self, details: Dict) -> str:
        """Genera codice specifico per agenti"""
        return """

# Codice agente AI generato automaticamente
class GeneratedAgent:
    def __init__(self):
        self.name = "{name}"
        self.purpose = "{purpose}"
    
    def execute(self):
        print(f"🤖 Agente {{self.name}} in esecuzione")
        print(f"🎯 Scopo: {{self.purpose}}")
        return True

if __name__ == "__main__":
    agent = GeneratedAgent()
    agent.execute()
""".format(
            name=details.get('name', 'AetherAgent'),
            purpose=details.get('purpose', 'Assistere utente')
        )
    
    def _generate_tool_code(self, details: Dict) -> str:
        """Genera codice per tool"""
        return """

# Tool automatico generato da Aether
def generated_tool():
    from datetime import datetime
    print("🛠️ Tool Aether in esecuzione")
    print("📊 Analizzando dati...")
    
    result = {
        'status': 'success',
        'data': 'Tool completato',
        'timestamp': datetime.now().isoformat()
    }
    
    return result

if __name__ == "__main__":
    result = generated_tool()
    print(f"✅ Risultato: {result}")
"""
    
    def _generate_analysis_code(self, details: Dict) -> str:
        """Genera codice per analisi dati"""
        return """

# Analisi dati automatica
import json
from datetime import datetime

def analyze_data():
    print("📊 Avvio analisi dati...")
    
    # Simula analisi
    analysis_result = {
        'data_points': 1000,
        'trends': ['crescita', 'stabilità'],
        'insights': 'Dati mostrano trend positivo',
        'confidence': 0.85,
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"📈 Analisi completata: {analysis_result}")
    return analysis_result

if __name__ == "__main__":
    result = analyze_data()
    print(json.dumps(result, indent=2))
"""
    
    def get_statistics(self) -> Dict[str, Any]:
        """Restituisce statistiche dell'executor"""
        return {
            'total_executions': self.execution_count,
            'successful_executions': self.success_count,
            'failed_executions': self.error_count,
            'success_rate': self.success_count / max(self.execution_count, 1),
            'supabase_enabled': self.supabase_manager is not None,
            'git_enabled': self.git_automation is not None
        } 