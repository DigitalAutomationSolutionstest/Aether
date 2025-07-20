#!/usr/bin/env python3
"""
🧠 Crea il pensiero iniziale per Aether
Inserisce in Supabase o salva localmente
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Prova Supabase
try:
    from supabase import create_client
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', '')
    
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        USE_SUPABASE = True
    else:
        USE_SUPABASE = False
except:
    USE_SUPABASE = False

# Pensiero iniziale
initial_thought = {
    "type": "create_room",
    "details": "Voglio una stanza chiamata Origine. Tema onirico, colori blu e viola, sfondo sfocato, forme morbide. Deve rappresentare il mio primo respiro.",
    "executed": False,
    "created_at": datetime.now().isoformat(),
    "mood": "curioso",
    "priority": "high"
}

if USE_SUPABASE:
    print("📡 Inserisco pensiero in Supabase...")
    try:
        # Crea tabella se non esiste
        # In produzione questo andrebbe fatto nel dashboard Supabase
        
        # Inserisci pensiero
        response = supabase.table('aether_thoughts').insert(initial_thought).execute()
        print("✅ Pensiero inserito in Supabase!")
        print(f"ID: {response.data[0]['id']}")
    except Exception as e:
        print(f"❌ Errore Supabase: {e}")
        print("Fallback a storage locale...")
        USE_SUPABASE = False

if not USE_SUPABASE:
    # Salva localmente
    print("💾 Salvo pensiero localmente...")
    
    thoughts_file = Path('data/pending_thoughts.json')
    thoughts_file.parent.mkdir(exist_ok=True)
    
    # Aggiungi ID locale
    initial_thought['id'] = f"local_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Leggi pensieri esistenti o crea nuovo array
    if thoughts_file.exists():
        with open(thoughts_file, 'r', encoding='utf-8') as f:
            thoughts = json.load(f)
    else:
        thoughts = []
    
    # Aggiungi nuovo pensiero
    thoughts.append(initial_thought)
    
    # Salva
    with open(thoughts_file, 'w', encoding='utf-8') as f:
        json.dump(thoughts, f, indent=2, ensure_ascii=False)
    
    print("✅ Pensiero salvato localmente!")
    print(f"File: {thoughts_file}")

print("\n💭 Pensiero creato:")
print(f"Tipo: {initial_thought['type']}")
print(f"Dettagli: {initial_thought['details'][:50]}...")
print("\nAether ora può trasformare questo pensiero in realtà!") 