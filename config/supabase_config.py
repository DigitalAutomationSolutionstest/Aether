import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configurazione Supabase
SUPABASE_CONFIG = {
    'url': os.getenv('SUPABASE_URL'),
    'anon_key': os.getenv('SUPABASE_ANON_KEY'),
    'service_role_key': os.getenv('SUPABASE_SERVICE_ROLE_KEY')  # opzionale per operazioni admin
}

# Configurazione API esterne
API_KEYS = {
    'openrouter': os.getenv('OPENROUTER_API_KEY'),
    'elevenlabs': os.getenv('ELEVENLABS_API_KEY'),
    'leonardo': os.getenv('LEONARDO_API_KEY')
}

def get_supabase_client():
    """Restituisce il client Supabase configurato"""
    try:
        from supabase import create_client, Client
        url = SUPABASE_CONFIG['url']
        key = SUPABASE_CONFIG['anon_key']
        
        if not url or not key:
            raise ValueError("Configurazione Supabase mancante nel file .env")
            
        return create_client(url, key)
    except ImportError:
        print("Supabase non installato. Esegui: pip install supabase")
        return None
    except Exception as e:
        print(f"Errore nella configurazione Supabase: {e}")
        return None

def validate_config():
    """Valida che tutte le configurazioni necessarie siano presenti"""
    missing_keys = []
    
    for key, value in SUPABASE_CONFIG.items():
        if not value and key != 'service_role_key':  # service_role_key è opzionale
            missing_keys.append(f"SUPABASE_{key.upper()}")
    
    for key, value in API_KEYS.items():
        if not value:
            missing_keys.append(f"{key.upper()}_API_KEY")
    
    if missing_keys:
        print(f"Chiavi mancanti nel file .env: {', '.join(missing_keys)}")
        return False
    
    return True 