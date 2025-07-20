"""
🔬 SANDBOX MODULE - Ambiente Sicuro per Esecuzione Codice

Qui Aether può scrivere e testare codice in completa sicurezza:
- Isolamento processi
- Timeout automatici
- Limitazioni memoria
- Cleanup automatico
"""

from pathlib import Path

# Directory principali della sandbox
SANDBOX_ROOT = Path(__file__).parent
SCRIPTS_DIR = SANDBOX_ROOT / "scripts"
TEMP_DIR = SANDBOX_ROOT / "temp"
RESULTS_DIR = SANDBOX_ROOT / "results"

# Crea le directory se non esistono
for directory in [SCRIPTS_DIR, TEMP_DIR, RESULTS_DIR]:
    directory.mkdir(exist_ok=True)

__all__ = ['SANDBOX_ROOT', 'SCRIPTS_DIR', 'TEMP_DIR', 'RESULTS_DIR'] 