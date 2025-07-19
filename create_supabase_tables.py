#!/usr/bin/env python3
"""
Script per creare automaticamente le tabelle Supabase per Aether
Esegue le query SQL direttamente tramite il client Supabase
"""

import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

def create_all_tables():
    """Crea tutte le tabelle necessarie per Aether in Supabase"""
    
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
        
        # Query SQL per creare le tabelle
        tables = {
            'aether_thoughts': """
                CREATE TABLE IF NOT EXISTS aether_thoughts (
                    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
                    timestamp timestamptz DEFAULT now(),
                    type text,
                    content text,
                    context jsonb
                );
            """,
            
            'aether_memory': """
                CREATE TABLE IF NOT EXISTS aether_memory (
                    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
                    content text,
                    tags text[],
                    created_at timestamptz DEFAULT now()
                );
            """,
            
            'aether_environment': """
                CREATE TABLE IF NOT EXISTS aether_environment (
                    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
                    scene_name text,
                    scene_config jsonb,
                    created_at timestamptz DEFAULT now()
                );
            """,
            
            'aether_economy': """
                CREATE TABLE IF NOT EXISTS aether_economy (
                    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
                    timestamp timestamptz DEFAULT now(),
                    action text,
                    cost numeric,
                    expected_roi numeric,
                    status text
                );
            """
        }
        
        # Indici per le performance
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_aether_thoughts_timestamp ON aether_thoughts(timestamp);",
            "CREATE INDEX IF NOT EXISTS idx_aether_thoughts_type ON aether_thoughts(type);",
            "CREATE INDEX IF NOT EXISTS idx_aether_memory_tags ON aether_memory USING GIN(tags);",
            "CREATE INDEX IF NOT EXISTS idx_aether_economy_status ON aether_economy(status);"
        ]
        
        print("🔧 Creazione tabelle Supabase...")
        
        # Crea le tabelle usando query dirette
        for table_name, sql in tables.items():
            try:
                # Prova a usare la funzione SQL diretta se disponibile
                result = supabase.rpc('execute_sql', {'query': sql}).execute()
                print(f"✅ Tabella {table_name} creata")
            except Exception as e:
                # Se non funziona, mostra la query da eseguire manualmente
                print(f"⚠️  Tabella {table_name} - eseguire manualmente:")
                print(f"   {sql.strip()}")
        
        print("\n🔧 Creazione indici...")
        for index_sql in indices:
            try:
                result = supabase.rpc('execute_sql', {'query': index_sql}).execute()
                print(f"✅ Indice creato")
            except Exception as e:
                print(f"⚠️  Indice - eseguire manualmente: {index_sql.strip()}")
        
        # Test inserimento dati
        print("\n🧪 Test inserimento dati...")
        test_data()
        
        print("\n🎉 Configurazione Supabase completata!")
        return True
        
    except ImportError:
        print("❌ Supabase non installato. Esegui: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Errore: {e}")
        print("\n📋 Esegui manualmente queste query nella console SQL di Supabase:")
        print_manual_queries()
        return False

def test_data():
    """Testa l'inserimento di dati nelle tabelle"""
    try:
        from supabase import create_client
        
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        supabase = create_client(url, key)
        
        # Test inserimento pensiero
        thought_data = {
            'type': 'initialization',
            'content': 'Aether è stato configurato con successo!',
            'context': {'setup': True, 'version': '1.0'}
        }
        
        result = supabase.table('aether_thoughts').insert(thought_data).execute()
        if result.data:
            print("✅ Test inserimento aether_thoughts riuscito")
            
            # Test lettura
            read_result = supabase.table('aether_thoughts').select('*').limit(1).execute()
            if read_result.data:
                print("✅ Test lettura aether_thoughts riuscito")
                print(f"   Dato inserito: {read_result.data[0]['content']}")
        
        # Test inserimento memoria
        memory_data = {
            'content': 'Prima memoria di Aether dopo la configurazione',
            'tags': ['setup', 'initialization', 'supabase']
        }
        
        result = supabase.table('aether_memory').insert(memory_data).execute()
        if result.data:
            print("✅ Test inserimento aether_memory riuscito")
        
        # Test inserimento ambiente
        env_data = {
            'scene_name': 'initial_setup',
            'scene_config': {'background': 'cosmic', 'mood': 'awakening'}
        }
        
        result = supabase.table('aether_environment').insert(env_data).execute()
        if result.data:
            print("✅ Test inserimento aether_environment riuscito")
        
        # Test inserimento economia
        economy_data = {
            'action': 'initial_setup',
            'cost': 0.0,
            'expected_roi': 100.0,
            'status': 'completed'
        }
        
        result = supabase.table('aether_economy').insert(economy_data).execute()
        if result.data:
            print("✅ Test inserimento aether_economy riuscito")
            
    except Exception as e:
        print(f"⚠️  Errore nei test: {e}")

def print_manual_queries():
    """Stampa le query da eseguire manualmente"""
    queries = """
-- Tabella per i pensieri e log cognitivi
CREATE TABLE IF NOT EXISTS aether_thoughts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp timestamptz DEFAULT now(),
  type text,
  content text,
  context jsonb
);

-- Tabella per la memoria semantica
CREATE TABLE IF NOT EXISTS aether_memory (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
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
  status text
);

-- Indici per migliorare le performance
CREATE INDEX IF NOT EXISTS idx_aether_thoughts_timestamp ON aether_thoughts(timestamp);
CREATE INDEX IF NOT EXISTS idx_aether_thoughts_type ON aether_thoughts(type);
CREATE INDEX IF NOT EXISTS idx_aether_memory_tags ON aether_memory USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_aether_economy_status ON aether_economy(status);
"""
    
    print(queries)

if __name__ == "__main__":
    print("🚀 Creazione automatica tabelle Supabase per Aether")
    print("=" * 60)
    
    if create_all_tables():
        print("\n🎉 Setup Supabase completato! Aether è pronto per l'uso.")
        print("\n🚀 Prossimi passi:")
        print("1. Esegui: python main.py")
        print("2. Apri il frontend per vedere Aether in azione")
    else:
        print("\n❌ Setup non completato automaticamente.")
        print("Copia e incolla le query SQL sopra nella console Supabase.") 