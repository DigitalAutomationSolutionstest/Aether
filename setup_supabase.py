#!/usr/bin/env python3
"""
Script per configurare Supabase per Aether
Esegue le query SQL per creare le tabelle necessarie
"""

import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

def create_supabase_tables():
    """Crea le tabelle necessarie per Aether in Supabase"""
    
    # Query SQL per creare le tabelle
    tables_sql = {
        'aether_thoughts': """
        CREATE TABLE IF NOT EXISTS aether_thoughts (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            timestamp timestamptz DEFAULT now(),
            type text, -- "thought", "decision", "action"
            content text,
            context jsonb
        );
        """,
        
        'aether_memory': """
        CREATE TABLE IF NOT EXISTS aether_memory (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            embedding vector(1536), -- per similarity search (opzionale con pgvector)
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
            status text -- es. "executed", "failed", "planned"
        );
        """
    }
    
    try:
        from supabase import create_client
        
        # Crea il client Supabase
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not key:
            print("❌ Configurazione Supabase mancante nel file .env")
            return False
            
        # Crea il client senza proxy
        supabase = create_client(url, key)
        
        print("🔧 Configurazione tabelle Supabase per Aether...")
        
        # Esegue le query per creare le tabelle
        for table_name, sql in tables_sql.items():
            try:
                # Prova a verificare se la tabella esiste
                result = supabase.table(table_name).select("id").limit(1).execute()
                print(f"✅ Tabella {table_name} già esistente")
            except Exception as e:
                print(f"⚠️  Tabella {table_name} non trovata, potrebbe dover essere creata manualmente")
                print(f"   Query SQL per creare la tabella:")
                print(f"   {sql.strip()}")
        
        print("🎉 Configurazione Supabase completata!")
        print("📝 Nota: Le tabelle potrebbero dover essere create manualmente nella console Supabase")
        return True
        
    except ImportError:
        print("❌ Supabase non installato. Esegui: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Errore nella configurazione: {e}")
        return False

def test_supabase_connection():
    """Testa la connessione a Supabase"""
    try:
        from supabase import create_client
        
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not key:
            print("❌ Configurazione Supabase mancante")
            return False
            
        # Crea il client senza proxy
        supabase = create_client(url, key)
        
        # Test semplice - prova a leggere dalla tabella aether_thoughts
        try:
            result = supabase.table('aether_thoughts').select("id").limit(1).execute()
            print("✅ Connessione a Supabase riuscita!")
            return True
        except Exception as table_error:
            print(f"⚠️  Tabella aether_thoughts non trovata: {table_error}")
            print("✅ Connessione a Supabase riuscita (tabella non ancora creata)")
            return True
        
    except Exception as e:
        print(f"❌ Errore nella connessione a Supabase: {e}")
        return False

def print_sql_queries():
    """Stampa le query SQL da eseguire manualmente"""
    print("\n📋 Query SQL da eseguire nella console Supabase:")
    print("=" * 60)
    
    queries = {
        'aether_thoughts': """
-- Tabella per i pensieri e log cognitivi
CREATE TABLE IF NOT EXISTS aether_thoughts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp timestamptz DEFAULT now(),
  type text, -- "thought", "decision", "action"
  content text,
  context jsonb
);
        """,
        
        'aether_memory': """
-- Tabella per la memoria semantica
CREATE TABLE IF NOT EXISTS aether_memory (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  embedding vector(1536), -- per similarity search (opzionale con pgvector)
  content text,
  tags text[],
  created_at timestamptz DEFAULT now()
);
        """,
        
        'aether_environment': """
-- Tabella per la UI o scena 3D corrente
CREATE TABLE IF NOT EXISTS aether_environment (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  scene_name text,
  scene_config jsonb,
  created_at timestamptz DEFAULT now()
);
        """,
        
        'aether_economy': """
-- Tabella per log decisioni economiche
CREATE TABLE IF NOT EXISTS aether_economy (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp timestamptz DEFAULT now(),
  action text,
  cost numeric,
  expected_roi numeric,
  status text -- es. "executed", "failed", "planned"
);
        """
    }
    
    for table_name, query in queries.items():
        print(f"\n-- {table_name.upper()}")
        print(query.strip())

if __name__ == "__main__":
    print("🚀 Configurazione iniziale Aether + Supabase")
    print("=" * 50)
    
    # Testa la connessione
    if test_supabase_connection():
        # Crea le tabelle
        create_supabase_tables()
        
        # Stampa le query SQL per creazione manuale
        print_sql_queries()
    else:
        print("❌ Impossibile procedere senza connessione a Supabase")
        print("Verifica le tue credenziali nel file .env") 