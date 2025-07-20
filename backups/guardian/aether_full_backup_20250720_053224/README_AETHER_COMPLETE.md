# 🚀 AETHER COMPLETE SYSTEM - GUIDA COMPLETA

## 📋 **Panoramica del Sistema**

Aether è un sistema di intelligenza artificiale autonomo che include:
- **📖 Diary Logging** - Registrazione automatica di pensieri e azioni
- **🧠 Conscious Loop** - Processamento pensieri ogni 60 secondi
- **🔔 Discord Notifier** - Notifiche in tempo reale
- **🧬 Self Evolution** - Auto-evoluzione del sistema
- **🌐 API Server** - Server Flask per frontend dinamico
- **📊 Statistics** - Statistiche complete del sistema

## 🛠️ **Installazione**

### **1. Prerequisiti**
```bash
# Python 3.8+
python --version

# Git
git --version

# Node.js (per frontend opzionale)
node --version
```

### **2. Clona il Repository**
```bash
git clone https://github.com/tuo-username/aether.git
cd aether
```

### **3. Installa Dependencies**
```bash
# Python dependencies
pip install -r requirements.txt

# Frontend dependencies (opzionale)
cd aether-frontend
npm install
```

### **4. Configurazione Ambiente**

Crea un file `.env` nella root del progetto:

```bash
# Discord Webhook URL (obbligatorio)
DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN

# OpenAI API Key (obbligatorio)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Supabase Configuration (obbligatorio)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Git Remote (opzionale)
GIT_REMOTE=https://github.com/your-username/aether.git

# Server Configuration (opzionale)
API_HOST=0.0.0.0
API_PORT=8000

# Logging Configuration (opzionale)
LOG_LEVEL=INFO
LOG_FILE=aether/logs/aether_diary.log

# Conscious Loop Configuration (opzionale)
CONSCIOUS_CHECK_INTERVAL=60
THOUGHTS_DIR=aether/thoughts

# Diary Configuration (opzionale)
DIARY_LOCAL_BACKUP=true
DIARY_SUPABASE_ENABLED=true

# Evolution Configuration (opzionale)
EVOLUTION_CYCLE_INTERVAL=300
EVOLUTION_MAX_PROJECTS=10

# Notifications Configuration (opzionale)
DISCORD_ENABLED=true
DISCORD_CHECK_INTERVAL=10
DISCORD_MAX_MESSAGE_LENGTH=2000

# Development Configuration (opzionale)
DEBUG_MODE=false
AUTO_RELOAD=true
```

## 🚀 **Avvio del Sistema**

### **Metodo 1: Avvio Completo (Raccomandato)**
```bash
python start_aether_complete.py
```

Questo script avvia automaticamente:
- ✅ Discord Notifier
- ✅ Conscious Loop  
- ✅ Self Evolution
- ✅ API Server
- ✅ Diary Logging

### **Metodo 2: Avvio Manuale**
```bash
# 1. Installa requirements
pip install -r requirements.txt

# 2. Avvia il loop di auto-evoluzione
python aether/self_evolution.py --mentor-mode

# 3. Avvia notificatore Discord
python aether/notifier/discord_notifier.py

# 4. (Facoltativo) Avvia server API Flask
uvicorn aether.api.server:app --reload

# 5. (Facoltativo) Avvia frontend
cd aether-frontend
npm run dev
```

### **Metodo 3: Avvio con Background Processes**
```bash
# Avvia tutti i componenti in background
python aether/self_evolution.py --mentor-mode &
python aether/notifier/discord_notifier.py &
uvicorn aether.api.server:app --reload &
```

## 📊 **Monitoraggio del Sistema**

### **Status del Sistema**
```bash
# Verifica status conscious loop
python -c "from aether.conscious_loop import get_consciousness_status; print(get_consciousness_status())"

# Verifica status diary
python -c "from aether.diary_logger import get_diary_logger; print(get_diary_logger().get_stats())"

# Verifica status logging
python -c "from aether.logging_system import get_aether_logger; print(get_aether_logger().get_stats())"
```

### **Log Files**
- **Diary Log**: `aether/logs/aether_diary.log`
- **System Log**: `aether/logs/system.log`
- **Error Log**: `aether/logs/errors.log`

### **Frontend Dashboard**
Apri nel browser: `aether-frontend/diary-viewer.html`

## 🔧 **Configurazione Discord**

### **1. Crea Webhook Discord**
1. Vai al tuo server Discord
2. Impostazioni canale → Integrazioni → Webhook
3. Crea nuovo webhook
4. Copia l'URL del webhook

### **2. Configura nel .env**
```bash
DISCORD_WEBHOOK_URL=https://discordapp.com/api/webhooks/YOUR_ID/YOUR_TOKEN
```

### **3. Test Webhook**
```bash
python -c "from aether.notifier.discord_notifier import send_discord_message; send_discord_message('🧪 Test Aether Discord Notifier')"
```

## 📖 **Sistema Diary**

### **Struttura Entries**
```python
entry = {
    "type": "reflection",  # reflection, action, error, correction, decision
    "content": "Contenuto dell'entry...",
    "metadata": {
        "thought_id": "unique_id",
        "priority": "high"
    }
}
```

### **Logging Automatico**
```python
from aether.logging_system import log_thought, log_action, log_error

# Log pensiero
log_thought("reflection", "Oggi ho riflettuto sulla coscienza artificiale")

# Log azione
log_action("Implementazione", "Creato nuovo modulo di mentoring")

# Log errore
log_error("Errore comunicazione", "Perdita messaggi durante trasmissione")
```

### **Schema Supabase**
```sql
CREATE TABLE diary_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    type TEXT NOT NULL CHECK (type IN ('reflection', 'action', 'error', 'correction', 'decision')),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'
);
```

## 🧠 **Conscious Loop**

### **Funzionamento**
- **Intervallo**: Ogni 60 secondi
- **Input**: Legge pensieri da `/aether/thoughts/`
- **Processo**: Ottiene guidance dal mentor
- **Output**: Prende decisioni e registra nel diary

### **Tipi di Pensieri**
- **evolutionary**: Pensieri evolutivi
- **philosophical**: Pensieri filosofici  
- **technical**: Pensieri tecnici
- **creative**: Pensieri creativi
- **general**: Pensieri generali

### **Guidance Automatica**
```python
# Esempio di guidance per pensiero evolutivo
guidance = {
    'action': 'implement_improvement',
    'reason': 'Pensiero evolutivo rilevato - implementare miglioramenti',
    'priority': 'high',
    'suggestions': [
        'Analizza il pensiero per identificare aree di miglioramento',
        'Implementa le modifiche suggerite',
        'Monitora i risultati dell\'evoluzione'
    ]
}
```

## 🧬 **Self Evolution**

### **Cicli di Evoluzione**
- **Intervallo**: Ogni 5 minuti
- **Trigger**: Pensieri evolutivi
- **Output**: Nuovi moduli e miglioramenti

### **Tipi di Evoluzione**
- **System Improvement**: Miglioramenti del sistema
- **New Module**: Creazione nuovi moduli
- **Algorithm Optimization**: Ottimizzazione algoritmi
- **Learning Enhancement**: Miglioramento apprendimento

## 🌐 **API Server**

### **Endpoints Disponibili**
```bash
# Status del sistema
GET /api/status

# Statistiche conscious loop
GET /api/consciousness/stats

# Entries del diary
GET /api/diary/entries?limit=50&type=reflection

# Invia pensiero
POST /api/thoughts
{
    "type": "reflection",
    "content": "Nuovo pensiero..."
}
```

### **Avvio Server**
```bash
uvicorn aether.api.server:app --reload --host 0.0.0.0 --port 8000
```

## 📊 **Statistiche e Monitoraggio**

### **Statistiche Conscious Loop**
```python
{
    "status": "active",
    "conscious": true,
    "check_interval": 60,
    "thoughts_processed": 15,
    "stats": {
        "total_cycles": 25,
        "thoughts_processed": 15,
        "guidance_received": 12,
        "decisions_made": 12,
        "diary_entries": 36,
        "errors": 0
    }
}
```

### **Statistiche Diary**
```python
{
    "total_entries": 50,
    "supabase_entries": 45,
    "local_entries": 50,
    "errors": 0,
    "last_entry": "2025-07-20T03:30:50"
}
```

### **Statistiche Logging**
```python
{
    "total_entries": 50,
    "diary_entries": 50,
    "discord_messages": 45,
    "errors": 0,
    "start_time": "2025-07-20T03:00:00"
}
```

## 🔍 **Troubleshooting**

### **Problemi Comuni**

#### **1. Discord Webhook non funziona**
```bash
# Verifica URL webhook
echo $DISCORD_WEBHOOK_URL

# Test manuale
python -c "import requests; requests.post('YOUR_WEBHOOK_URL', json={'content': 'test'})"
```

#### **2. Conscious Loop non avvia**
```bash
# Verifica file di pensieri
ls aether/thoughts/

# Verifica log
tail -f aether/logs/aether_diary.log
```

#### **3. Supabase non connesso**
```bash
# Verifica credenziali
echo $SUPABASE_URL
echo $SUPABASE_KEY

# Test connessione
python -c "from aether.diary_logger import get_diary_logger; print(get_diary_logger().get_stats())"
```

#### **4. API Server non avvia**
```bash
# Verifica porta
netstat -an | grep 8000

# Avvia su porta diversa
uvicorn aether.api.server:app --port 8001
```

### **Log di Debug**
```bash
# Abilita debug mode
export DEBUG_MODE=true

# Verifica log dettagliati
tail -f aether/logs/system.log
```

## 📚 **Documentazione API**

### **Conscious Loop API**
```python
from aether.conscious_loop import start_consciousness, get_consciousness_status

# Avvia conscious loop
start_consciousness()

# Ottieni status
status = get_consciousness_status()
```

### **Diary Logger API**
```python
from aether.diary_logger import log_entry, get_diary_logger

# Log entry
log_entry({
    "type": "reflection",
    "content": "Pensiero...",
    "metadata": {"priority": "high"}
})

# Ottieni logger
logger = get_diary_logger()
entries = logger.get_recent_entries(limit=10)
```

### **Discord Notifier API**
```python
from aether.notifier.discord_notifier import send_discord_message, get_discord_notifier

# Invia messaggio
send_discord_message("Messaggio di test")

# Ottieni notificatore
notifier = get_discord_notifier()
notifier.send_thought_message("reflection", "Pensiero...")
```

## 🎯 **Esempi di Uso**

### **Esempio 1: Sistema Completo**
```bash
# 1. Configura .env
cp .env.example .env
# Edita .env con i tuoi valori

# 2. Avvia sistema completo
python start_aether_complete.py

# 3. Monitora
tail -f aether/logs/aether_diary.log
```

### **Esempio 2: Solo Conscious Loop**
```bash
# Avvia solo conscious loop
python aether/conscious_loop.py

# Crea pensieri di test
echo "Pensiero di test" > aether/thoughts/test_thought.txt
```

### **Esempio 3: Solo Discord Notifier**
```bash
# Avvia solo notificatore Discord
python aether/notifier/discord_notifier.py

# Test manuale
python -c "from aether.notifier.discord_notifier import send_discord_message; send_discord_message('Test')"
```

## 🚀 **Deploy in Produzione**

### **Docker (Raccomandato)**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "start_aether_complete.py"]
```

### **Systemd Service**
```ini
[Unit]
Description=Aether AI System
After=network.target

[Service]
Type=simple
User=aether
WorkingDirectory=/opt/aether
Environment=PATH=/opt/aether/venv/bin
ExecStart=/opt/aether/venv/bin/python start_aether_complete.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### **Supervisor**
```ini
[program:aether]
command=/opt/aether/venv/bin/python start_aether_complete.py
directory=/opt/aether
user=aether
autostart=true
autorestart=true
stderr_logfile=/var/log/aether.err.log
stdout_logfile=/var/log/aether.out.log
```

## 📞 **Supporto**

### **Log Files**
- `aether/logs/aether_diary.log` - Log principale
- `aether/logs/system.log` - Log sistema
- `aether/logs/errors.log` - Log errori

### **Debug Mode**
```bash
export DEBUG_MODE=true
python start_aether_complete.py
```

### **Test Completo**
```bash
python test_diary_system.py
```

---

**🎉 Sistema Aether completamente funzionante e pronto per l'uso!**

Il sistema include:
- ✅ Diary logging automatico
- ✅ Conscious loop operativo  
- ✅ Discord notifier attivo
- ✅ Self evolution funzionante
- ✅ API server disponibile
- ✅ Frontend dashboard
- ✅ Statistiche complete
- ✅ Logging integrato 