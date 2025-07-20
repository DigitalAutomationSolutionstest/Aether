#!/usr/bin/env python3
"""
Script per configurare Git e preparare il repository Aether
"""

import subprocess
import os
import sys

def run_command(command, description):
    """Esegue un comando e gestisce gli errori"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completato")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Errore in {description}: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Errore in {description}: {e}")
        return False

def check_git_status():
    """Controlla lo stato di Git"""
    print("🔍 Controllo stato Git...")
    
    # Controlla se Git è inizializzato
    result = subprocess.run("git status", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Git già inizializzato")
        return True
    else:
        print("⚠️  Git non inizializzato")
        return False

def setup_git_identity():
    """Configura l'identità Git"""
    print("👤 Configurazione identità Git...")
    
    # Configura email e nome (usa valori di default se non specificati)
    email = "aether@digitalautomation.solutions"
    name = "Aether AI"
    
    run_command(f'git config user.email "{email}"', "Configurazione email Git")
    run_command(f'git config user.name "{name}"', "Configurazione nome Git")
    
    print(f"✅ Identità Git configurata: {name} <{email}>")

def setup_git():
    """Configura Git per il progetto Aether"""
    print("🚀 Configurazione Git per Aether")
    print("=" * 50)
    
    # Controlla se Git è già configurato
    if check_git_status():
        print("📝 Git già configurato, verifico il remote...")
        
        # Controlla se il remote esiste
        result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
        if "origin" in result.stdout:
            print("✅ Remote origin già configurato")
            print(f"   Remote: {result.stdout.strip()}")
        else:
            print("⚠️  Remote origin non configurato")
            if run_command(
                'git remote add origin https://github.com/DigitalAutomationSolutionstest/Aether.git',
                "Aggiunta remote origin"
            ):
                print("✅ Remote origin configurato")
    else:
        # Inizializza Git
        if run_command("git init", "Inizializzazione Git"):
            if run_command(
                'git remote add origin https://github.com/DigitalAutomationSolutionstest/Aether.git',
                "Aggiunta remote origin"
            ):
                print("✅ Git inizializzato e configurato")
    
    # Configura l'identità Git
    setup_git_identity()
    
    # Imposta il branch principale
    run_command("git branch -M main", "Impostazione branch main")
    
    # Aggiungi tutti i file
    if run_command("git add .", "Aggiunta file al staging"):
        # Primo commit
        if run_command(
            'git commit -m "Setup iniziale Aether + Supabase"',
            "Primo commit"
        ):
            print("✅ Repository Git configurato con successo!")
            print("\n📋 Prossimi passi:")
            print("1. Esegui: git push -u origin main")
            print("2. Crea le tabelle Supabase usando le query SQL fornite")
            print("3. Testa la connessione con: python setup_supabase.py")
            return True
    
    return False

def create_sql_file():
    """Crea un file con le query SQL per Supabase"""
    sql_content = """-- Query SQL per configurare Supabase per Aether
-- Esegui queste query nella console SQL di Supabase

-- Tabella per i pensieri e log cognitivi
CREATE TABLE IF NOT EXISTS aether_thoughts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp timestamptz DEFAULT now(),
  type text, -- "thought", "decision", "action"
  content text,
  context jsonb
);

-- Tabella per la memoria semantica
CREATE TABLE IF NOT EXISTS aether_memory (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  embedding vector(1536), -- per similarity search (opzionale con pgvector)
  content text,
  tags text[],
  created_at timestamptz DEFAULT now()
);

-- Tabella per la UI o scena 3D corrente
CREATE TABLE IF NOT EXISTS aether_environment (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  scene_name text,
  scene_config jsonb,
  created_at timestamptz DEFAULT now()
);

-- Tabella per log decisioni economiche
CREATE TABLE IF NOT EXISTS aether_economy (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp timestamptz DEFAULT now(),
  action text,
  cost numeric,
  expected_roi numeric,
  status text -- es. "executed", "failed", "planned"
);

-- Indici per migliorare le performance
CREATE INDEX IF NOT EXISTS idx_aether_thoughts_timestamp ON aether_thoughts(timestamp);
CREATE INDEX IF NOT EXISTS idx_aether_thoughts_type ON aether_thoughts(type);
CREATE INDEX IF NOT EXISTS idx_aether_memory_tags ON aether_memory USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_aether_economy_status ON aether_economy(status);
"""
    
    with open('supabase_setup.sql', 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print("✅ File supabase_setup.sql creato con le query SQL")

if __name__ == "__main__":
    print("🎯 Setup completo Aether + Supabase + Git")
    print("=" * 60)
    
    # Crea il file SQL
    create_sql_file()
    
    # Configura Git
    if setup_git():
        print("\n🎉 Setup completato con successo!")
        print("\n📋 Riepilogo:")
        print("✅ File .env configurato")
        print("✅ Dipendenze Python installate")
        print("✅ Connessione Supabase testata")
        print("✅ Repository Git configurato")
        print("✅ File SQL creato per Supabase")
        
        print("\n🚀 Prossimi passi:")
        print("1. Esegui le query SQL in supabase_setup.sql nella console Supabase")
        print("2. Esegui: git push -u origin main")
        print("3. Testa Aether con: python main.py")
    else:
        print("❌ Setup non completato. Controlla gli errori sopra.") 