import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_ANON_KEY"]
sb = create_client(SUPABASE_URL, SUPABASE_KEY)

def test_supabase():
    print("🧪 Test connessione Supabase...")
    
    # Test connessione base
    try:
        result = sb.table("aether_thoughts").select("*").limit(1).execute()
        print("✅ Supabase connesso. Thoughts table OK:", len(result.data), "records")
    except Exception as e:
        print("❌ Errore connessione Supabase:", e)
        return
    
    # Test tutte le tabelle
    tables = ["aether_thoughts", "aether_memory", "aether_environment", "aether_economy"]
    
    for table in tables:
        try:
            result = sb.table(table).select("*").limit(1).execute()
            print(f"✅ Tabella {table}: {len(result.data)} records")
        except Exception as e:
            print(f"❌ Errore tabella {table}: {e}")

def test_insert():
    print("\n🧪 Test inserimento dati...")
    try:
        # Test insert in aether_thoughts
        test_data = {
            "type": "connection_test",
            "content": f"Test connessione da script - {os.environ.get('COMPUTERNAME', 'unknown')}",
            "context": {"test": True, "source": "test_script"}
        }
        
        result = sb.table("aether_thoughts").insert(test_data).execute()
        print("✅ Insert test completato:", result.data[0]["id"])
        
    except Exception as e:
        print("❌ Errore insert test:", e)

if __name__ == "__main__":
    test_supabase()
    test_insert() 