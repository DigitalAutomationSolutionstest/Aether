# 🚀 Configurazione Aether + Supabase

Questa guida ti aiuta a configurare Aether per utilizzare Supabase come database e sistema di autenticazione.

## 📋 Prerequisiti

1. **Account Supabase**: Crea un progetto su [supabase.com](https://supabase.com)
2. **Python 3.8+**: Assicurati di avere Python installato
3. **Git**: Per il controllo versione

## 🔧 Configurazione Iniziale

### 1. File .env

Crea un file `.env` nella root del progetto con le seguenti variabili:

```bash
SUPABASE_URL=https://zsgiscyujdsoagjwuhoy.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpzZ2lzY3l1amRzb2Fnand1aG95Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI5NDUxMTUsImV4cCI6MjA2ODUyMTExNX0.icyLG9RPcpCUcQ4sQ58cx5Np9aJJLSrHB6AVt45HFik
OPENROUTER_API_KEY=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
ELEVENLABS_API_KEY=sk_fe4bdc0f7bc33f6dc8b388df9de81c744de9cf0693409faf
LEONARDO_API_KEY=506e8e3b-431a-4768-8613-13b9fb130f68
```

### 2. Installazione Dipendenze

```bash
pip install -r requirements.txt
```

### 3. Configurazione Database

Esegui lo script di configurazione:

```bash
python setup_supabase.py
```

Questo script:
- ✅ Testa la connessione a Supabase
- ✅ Crea le tabelle necessarie
- ✅ Verifica che tutto funzioni correttamente

## 🗄️ Struttura Database

### Tabelle Create

1. **aether_thoughts**: Pensieri e log cognitivi
   - `id`: UUID primario
   - `timestamp`: Timestamp automatico
   - `type`: Tipo di pensiero ("thought", "decision", "action")
   - `content`: Contenuto del pensiero
   - `context`: Contesto JSON

2. **aether_memory**: Memoria semantica
   - `id`: UUID primario
   - `embedding`: Vettore per similarity search (opzionale)
   - `content`: Contenuto della memoria
   - `tags`: Array di tag
   - `created_at`: Timestamp di creazione

3. **aether_environment**: Configurazione scene 3D
   - `id`: UUID primario
   - `scene_name`: Nome della scena
   - `scene_config`: Configurazione JSON della scena
   - `created_at`: Timestamp di creazione

4. **aether_economy**: Log decisioni economiche
   - `id`: UUID primario
   - `timestamp`: Timestamp automatico
   - `action`: Azione economica
   - `cost`: Costo dell'azione
   - `expected_roi`: ROI atteso
   - `status`: Stato ("executed", "failed", "planned")

## 🔗 Integrazione con Aether

### Utilizzo nel Codice

```python
from config.supabase_config import get_supabase_client, validate_config

# Valida la configurazione
if validate_config():
    # Ottieni il client Supabase
    supabase = get_supabase_client()
    
    # Esempio: salva un pensiero
    thought_data = {
        'type': 'thought',
        'content': 'Aether sta pensando...',
        'context': {'mood': 'curious', 'energy': 0.8}
    }
    
    result = supabase.table('aether_thoughts').insert(thought_data).execute()
```

## 🚀 Comandi Git

```bash
# Inizializza Git (se non già fatto)
git init

# Aggiungi il remote
git remote add origin https://github.com/DigitalAutomationSolutionstest/Aether.git

# Imposta il branch principale
git branch -M main

# Aggiungi tutti i file
git add .

# Primo commit
git commit -m "Setup iniziale Aether + Supabase"

# Push al repository
git push -u origin main
```

## 🔍 Test della Configurazione

Esegui questi test per verificare che tutto funzioni:

```bash
# Test connessione Supabase
python -c "from config.supabase_config import test_supabase_connection; test_supabase_connection()"

# Test completo setup
python setup_supabase.py
```

## 🛠️ Risoluzione Problemi

### Errore "Supabase non installato"
```bash
pip install supabase==2.3.4
```

### Errore "Configurazione mancante"
- Verifica che il file `.env` esista nella root
- Controlla che tutte le chiavi API siano presenti

### Errore di connessione
- Verifica che l'URL e la chiave anonima siano corretti
- Controlla che il progetto Supabase sia attivo

## 📚 Prossimi Passi

1. **Integrazione Frontend**: Configura il frontend per utilizzare Supabase
2. **Autenticazione**: Implementa sistema di login/logout
3. **Real-time**: Abilita le funzionalità real-time per aggiornamenti live
4. **Storage**: Configura lo storage per file e media

---

🎉 **Congratulazioni!** Aether è ora configurato con Supabase e pronto per l'uso! 