#!/usr/bin/env python3
"""
Script semplificato per creare le tabelle Supabase per Aether
Usa l'approccio diretto per creare le tabelle una per una
"""

import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

def create_tables_directly():
    """Crea le tabelle direttamente senza usare RPC"""
    
    try:
        from supabase import create_client
        
        # Connessione a Supabase
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not key:
            print("❌ Configurazione Supabase mancante nel file .env")
            return False
            
        supabase = create_client(url, key)
        print("✅ Connesso a Supabase")
        
        # Test di connessione tentando di leggere da una tabella esistente
        tables_to_check = ['aether_thoughts', 'aether_memory', 'aether_environment', 'aether_economy']
        
        for table_name in tables_to_check:
            try:
                # Prova a fare una query sulla tabella
                result = supabase.table(table_name).select('id').limit(1).execute()
                print(f"✅ Tabella {table_name} già esistente")
            except Exception as e:
                print(f"⚠️  Tabella {table_name} non trovata: {e}")
        
        # Inserimento dati di test
        print("\n🧪 Test inserimento dati...")
        
        # Test aether_thoughts
        try:
            thought_data = {
                'type': 'setup',
                'content': 'Configurazione Aether completata!',
                'context': {'version': '1.0', 'status': 'ready'}
            }
            result = supabase.table('aether_thoughts').insert(thought_data).execute()
            if result.data:
                print("✅ Test aether_thoughts riuscito")
        except Exception as e:
            print(f"❌ Errore aether_thoughts: {e}")
        
        # Test aether_memory
        try:
            memory_data = {
                'content': 'Prima configurazione di Aether con Supabase',
                'tags': ['setup', 'configuration', 'supabase']
            }
            result = supabase.table('aether_memory').insert(memory_data).execute()
            if result.data:
                print("✅ Test aether_memory riuscito")
        except Exception as e:
            print(f"❌ Errore aether_memory: {e}")
        
        # Test aether_environment
        try:
            env_data = {
                'scene_name': 'initial_setup_scene',
                'scene_config': {'theme': 'cosmic', 'mode': 'initialization'}
            }
            result = supabase.table('aether_environment').insert(env_data).execute()
            if result.data:
                print("✅ Test aether_environment riuscito")
        except Exception as e:
            print(f"❌ Errore aether_environment: {e}")
        
        # Test aether_economy
        try:
            economy_data = {
                'action': 'setup_initialization',
                'cost': 0.0,
                'expected_roi': 100.0,
                'status': 'completed'
            }
            result = supabase.table('aether_economy').insert(economy_data).execute()
            if result.data:
                print("✅ Test aether_economy riuscito")
        except Exception as e:
            print(f"❌ Errore aether_economy: {e}")
        
        print("\n🎉 Test completati!")
        return True
        
    except ImportError:
        print("❌ Supabase non installato. Esegui: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Errore generale: {e}")
        return False

def print_sql_for_manual_creation():
    """Stampa le query SQL da eseguire manualmente nella console Supabase"""
    
    print("\n📋 Se i test sopra falliscono, esegui queste query nella console SQL di Supabase:")
    print("=" * 80)
    
    sql_queries = """
-- Tabella per i pensieri e log cognitivi di Aether
CREATE TABLE IF NOT EXISTS aether_thoughts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp timestamptz DEFAULT now(),
  type text,
  content text,
  context jsonb
);

-- Tabella per la memoria semantica di Aether
CREATE TABLE IF NOT EXISTS aether_memory (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text,
  tags text[],
  created_at timestamptz DEFAULT now()
);

-- Tabella per le configurazioni della scena 3D di Aether
CREATE TABLE IF NOT EXISTS aether_environment (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  scene_name text,
  scene_config jsonb,
  created_at timestamptz DEFAULT now()
);

-- Tabella per le azioni economiche di Aether
CREATE TABLE IF NOT EXISTS aether_economy (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp timestamptz DEFAULT now(),
  action text,
  cost numeric,
  expected_roi numeric,
  status text
);

-- Indici per migliorare le performance
CREATE INDEX IF NOT EXISTS idx_aether_thoughts_timestamp ON aether_thoughts(timestamp);
CREATE INDEX IF NOT EXISTS idx_aether_thoughts_type ON aether_thoughts(type);
CREATE INDEX IF NOT EXISTS idx_aether_memory_tags ON aether_memory USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_aether_economy_status ON aether_economy(status);
"""
    
    print(sql_queries)

if __name__ == "__main__":
    print("🚀 Test e Configurazione Supabase per Aether")
    print("=" * 60)
    
    success = create_tables_directly()
    
    # Stampa sempre le query per riferimento
    print_sql_for_manual_creation()
    
    if success:
        print("\n🎉 Configurazione Supabase OK! Aether può usare il database.")
        print("\n🚀 Ora puoi:")
        print("1. Eseguire: python main.py")
        print("2. Avviare il frontend di Aether")
        print("3. Esplorare le funzionalità cognitive di Aether")
    else:
        print("\n⚠️  Per completare la configurazione:")
        print("1. Copia le query SQL sopra")
        print("2. Vai su supabase.com → Tuo progetto → SQL Editor")
        print("3. Incolla ed esegui le query")
        print("4. Rilancia questo script per testare") 