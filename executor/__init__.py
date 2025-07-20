"""
🚀 EXECUTOR MODULE - Sistema di Esecuzione Codice Autonomo per Aether

Questo modulo permette ad Aether di:
- Scrivere codice reale nella sandbox
- Salvare automaticamente su Supabase
- Versionare tutto con Git
- Generare output e log dettagliati

Struttura:
- sandbox/: Codice eseguibile e output
- logs/: Log di esecuzione e debug  
- outputs/: Risultati e artefatti generati
- templates/: Template base per il codice
"""

from .code_executor import AetherCodeExecutor
from .supabase_integrator import SupabaseCodeManager
from .git_versioner import GitAutomation

__version__ = "1.0.0"
__author__ = "Aether AI"

__all__ = [
    'AetherCodeExecutor',
    'SupabaseCodeManager', 
    'GitAutomation'
] 