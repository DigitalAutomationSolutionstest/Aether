"""
📤 OUTPUTS MODULE - Gestione Output e Artefatti

Organizza tutti gli output di Aether:
- File generati
- Reports e statistiche  
- Database backups
- Artefatti di codice
"""

from pathlib import Path
from datetime import datetime
import json

# Directory output
OUTPUTS_DIR = Path(__file__).parent
OUTPUTS_DIR.mkdir(exist_ok=True)

# Sottodirectory specializzate
GENERATED_CODE_DIR = OUTPUTS_DIR / "generated_code"
REPORTS_DIR = OUTPUTS_DIR / "reports"
BACKUPS_DIR = OUTPUTS_DIR / "backups"
ARTIFACTS_DIR = OUTPUTS_DIR / "artifacts"

# Crea tutte le directory
for directory in [GENERATED_CODE_DIR, REPORTS_DIR, BACKUPS_DIR, ARTIFACTS_DIR]:
    directory.mkdir(exist_ok=True)

def save_output(output_type: str, data: dict, filename: str = None):
    """Salva un output in modo strutturato"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_type}_{timestamp}.json"
    
    output_dirs = {
        'code': GENERATED_CODE_DIR,
        'report': REPORTS_DIR,
        'backup': BACKUPS_DIR,
        'artifact': ARTIFACTS_DIR
    }
    
    target_dir = output_dirs.get(output_type, OUTPUTS_DIR)
    filepath = target_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filepath

__all__ = [
    'OUTPUTS_DIR', 'GENERATED_CODE_DIR', 'REPORTS_DIR', 
    'BACKUPS_DIR', 'ARTIFACTS_DIR', 'save_output'
] 