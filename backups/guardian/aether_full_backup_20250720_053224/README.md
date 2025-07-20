# Invader Core Agent

Un agente intelligente con capacità di ragionamento, apprendimento e memoria persistente, che ora vive in un mondo 3D interattivo.

## 🚀 Caratteristiche

- **Cervello Intelligente**: Sistema di ragionamento e decisione
- **Memoria Persistente**: Memorizzazione e recupero delle esperienze
- **Identità Dinamica**: Valori, preferenze e tratti caratteristici
- **Gestione Obiettivi**: Sistema di obiettivi e priorità
- **Configurazione Flessibile**: Impostazioni personalizzabili
- **Logging Avanzato**: Sistema di logging completo
- **Strumenti Utilità**: Funzioni di supporto e analisi
- **Mondo 3D Interattivo**: Ambiente virtuale dove Invader vive e si evolve

## 📁 Struttura del Progetto

```
invader-core-agent/
├── main.py                 # File principale dell'applicazione
├── server.py               # Server WebSocket per il mondo 3D
├── core/                   # Componenti core dell'agente
│   ├── brain.py           # Sistema di ragionamento
│   ├── memory.py          # Gestione della memoria
│   ├── identity.py        # Identità e valori
│   ├── goals.py           # Gestione obiettivi
│   ├── state.py           # Stato emotivo e operativo
│   ├── life.py            # Simulazione vita mentale
│   ├── tools_builder.py   # Costruzione strumenti
│   └── self_awareness.py  # Auto-consapevolezza
├── frontend/              # Interfaccia 3D (React + Three.js)
│   ├── public/
│   │   └── index.html     # Pagina principale
│   ├── src/
│   │   ├── App.js         # Componente principale 3D
│   │   ├── App.css        # Stili dell'interfaccia
│   │   ├── index.js       # Entry point React
│   │   └── index.css      # Stili globali
│   └── package.json       # Dipendenze React
├── data/                  # Dati dell'applicazione
│   └── logs/              # File di log
├── config/                # Configurazioni
│   └── settings.py        # Gestione impostazioni
├── utils/                 # Strumenti e utilità
│   └── tools.py           # Funzioni di supporto
├── requirements.txt       # Dipendenze Python
├── .env                   # Variabili d'ambiente
└── README.md             # Documentazione
```

## 🛠️ Installazione

1. **Clona il repository**:
   ```bash
   git clone <repository-url>
   cd invader-core-agent
   ```

2. **Crea un ambiente virtuale**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # oppure
   venv\Scripts\activate     # Windows
   ```

3. **Installa le dipendenze Python**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Installa le dipendenze React**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

5. **Configura le variabili d'ambiente**:
   Crea un file `.env` nella root del progetto con:
   ```bash
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   MODEL=openrouter/your-model-id
   ```

## 🚀 Utilizzo

### Avvio Console (FASE 1-3)
```bash
python main.py
```

### Avvio Mondo 3D (FASE 4)
```bash
# Terminal 1: Avvia il server WebSocket
python server.py

# Terminal 2: Avvia il frontend React
cd frontend
npm start
```

## 🧠 Componenti Principali

### Brain (Cervello)
Il sistema di ragionamento dell'agente che coordina tutti i processi cognitivi:
- Analisi dell'input
- Recupero dalla memoria
- Applicazione dell'identità
- Valutazione degli obiettivi
- Generazione delle risposte

### Memory (Memoria)
Sistema di memorizzazione e recupero delle esperienze:
- Memoria a breve termine
- Memoria a lungo termine
- Associazioni per il recupero rapido
- Consolidamento automatico

### Identity (Identità)
Gestione dell'identità e dei valori dell'agente:
- Tratti caratteristici
- Valori e principi
- Preferenze di comunicazione
- Adattamento del contesto

### Goals (Obiettivi)
Sistema di gestione degli obiettivi:
- Obiettivi attivi e inattivi
- Priorità e rilevanza
- Valutazione automatica
- Azioni suggerite

### Mondo 3D
Ambiente virtuale dove Invader vive e si evolve:
- Casa e decorazioni
- Comunicazione in tempo reale
- Azioni autonome
- Evoluzione dell'ambiente

## ⚙️ Configurazione

### File di Configurazione
Le configurazioni sono gestite tramite:
- `config/settings.py`: Configurazioni di default
- Variabili d'ambiente: Personalizzazioni runtime
- File JSON: Configurazioni persistenti

### Variabili d'Ambiente Principali
```bash
OPENROUTER_API_KEY=your_key_here
MODEL=openrouter/your-model-id
INVADER_DEBUG=false
INVADER_LOG_LEVEL=INFO
```

## 📊 Logging

Il sistema di logging è configurato per:
- Output su console (livello INFO)
- File di log rotanti (livello DEBUG)
- Backup automatici
- Formattazione personalizzata

## 🔧 Sviluppo

### Struttura del Codice
- **Type Hints**: Utilizzati in tutto il codice
- **Documentazione**: Docstring complete
- **Gestione Errori**: Try-catch appropriati
- **Logging**: Tracciamento completo

### Testing
```bash
# Esegui i test
pytest

# Con copertura
pytest --cov=core --cov=utils --cov=config
```

### Formattazione
```bash
# Formatta il codice
black .

# Controlla la qualità
flake8
mypy .
```

## 🌐 Mondo 3D

### Caratteristiche
- **Ambiente Interattivo**: Invader vive in una casa 3D
- **Comunicazione Reale**: Chat integrata con WebSocket
- **Evoluzione Autonoma**: Invader può modificare il suo mondo
- **Stato Emotivo**: Riflesso nell'ambiente 3D

### Controlli
- **Mouse**: Navigazione e rotazione camera
- **Chat**: Comunicazione diretta con Invader
- **Azioni**: Invader può costruire e modificare

## 🤝 Contribuire

1. Fork il progetto
2. Crea un branch per la feature (`git checkout -b feature/AmazingFeature`)
3. Commit le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📝 Licenza

Questo progetto è rilasciato sotto la licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 🆘 Supporto

Per supporto e domande:
- Apri una issue su GitHub
- Contatta il team di sviluppo
- Consulta la documentazione

## 🔮 Roadmap

- [x] Core AI con memoria e identità
- [x] Sistema di obiettivi e auto-consapevolezza
- [x] Mondo 3D interattivo
- [ ] Integrazione con API esterne
- [ ] Sistema di plugin
- [ ] Machine learning avanzato
- [ ] Supporto multi-lingua
- [ ] Integrazione con database
- [ ] Sistema di backup automatico
- [ ] API REST
- [ ] Documentazione API
- [ ] Test di integrazione

---

**Invader Core Agent** - Un agente intelligente per il futuro dell'AI 🤖 