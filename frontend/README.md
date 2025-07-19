# 🧠 Aether Frontend Dinamico

## Panoramica

Questo frontend React è completamente **dinamico e auto-popolante**. Non contiene logica hardcoded per visualizzare stanze, agenti o scene specifiche. Invece, si auto-popola interrogando le API del backend per scoprire cosa Aether ha creato autonomamente.

## 🚀 Architettura Dinamica

### 1. **Auto-Discovery dei Componenti**
- Il frontend interroga `/api/rooms` ogni 5 secondi
- Carica dinamicamente i file JSX generati da Aether
- Usa React's `import()` per il caricamento hot/live
- Nessuna configurazione manuale richiesta

### 2. **Sistema di Agenti Live**
- Pannello agenti che mostra lo stato in tempo reale
- Aggiorna automaticamente la lista degli agenti attivi
- Visualizza interazioni, mood e statistiche
- Interfaccia diretta con l'`AetherAgentManager`

### 3. **Log Eventi in Tempo Reale**
- Stream live di tutti gli eventi di Aether
- Filtri per tipo di evento (creazione stanze, agenti, evoluzioni)
- Audio player integrato per le sintesi vocali
- Ordinamento cronologico automatico

### 4. **Caricamento Dinamico JSX**

```javascript
// Hook per dynamic import
const loadComponent = useCallback(async (componentName) => {
  const moduleUrl = `/src/components/${componentName}.jsx`;
  const timestamp = Date.now(); // Cache busting
  const module = await import(`${moduleUrl}?t=${timestamp}`);
  return module.default;
}, []);
```

## 🔄 Flusso Auto-Evolutivo

1. **Aether genera** un nuovo componente React (es. `SognatoreRoom.jsx`)
2. **Backend API** `/api/rooms` riconosce automaticamente il nuovo file
3. **Frontend** rileva il cambiamento nell'auto-refresh (5s)
4. **Dynamic Import** carica il componente live
5. **UI si aggiorna** senza reload o intervento umano

## 🎨 Stile Cyber-Dark

- Design responsive ottimizzato per mobile
- Tema dark con accenti cyber (cyan, purple, pink)
- Animazioni smooth con Framer Motion
- Glass morphism e neon glow effects
- Scrollbar personalizzate

## 📁 Struttura Componenti

```
src/
├── services/
│   └── api.js              # API client + WebSocket
├── hooks/
│   └── useDynamicComponents.js  # Dynamic loading logic
├── components/
│   ├── DynamicRoomGrid.jsx     # Grid auto-popolante
│   ├── AgentsPanel.jsx         # Pannello agenti live
│   ├── EventsLog.jsx          # Log eventi real-time
│   └── AudioPlayer.jsx        # Player per sintesi vocali
└── App.jsx                    # Router + layout principale
```

## 🚀 Getting Started

### Prerequisiti
- Node.js 18+
- Backend Aether in esecuzione su porta 8000

### Installazione
```bash
cd frontend
npm install
npm run dev
```

Il frontend sarà disponibile su `http://localhost:3000`

### Build Produzione
```bash
npm run build
npm run preview
```

## 🔌 API Endpoints

Il frontend comunica con questi endpoint backend:

- `GET /api/rooms` - Lista componenti stanza
- `GET /api/agents` - Agenti attivi + stato
- `GET /api/events` - Log eventi/evoluzioni  
- `GET /api/audio` - File audio disponibili
- `GET /api/status` - Stato sistema Aether
- `GET /api/audio/<file>` - Serve file audio

## 🎵 Audio Player

- Riproduce automaticamente le sintesi vocali di Aether
- Controlli volume, play/pause, download
- Visualizzazione onde audio animate
- Auto-refresh ogni 30 secondi per nuovi file

## 🤖 Pannello Agenti

Ogni agente viene visualizzato con:
- **Avatar mood-based** (🎨 creativo, 📊 analitico, etc.)
- **Stato attività** (online/offline/thinking)  
- **Statistiche live** (interazioni, uptime)
- **Goal e personalità** estratti dal codice
- **Modal dettaglio** con cronologia attività

## 📊 Log Eventi

Sistema di eventi categorizzati:
- `thought` - Pensieri di Aether
- `self_evolution` - Auto-evoluzioni
- `room_creation` - Creazione stanze
- `agent_creation` - Creazione agenti
- `evolution_announcement` - Annunci vocali

## 🔄 WebSocket Real-Time

```javascript
const ws = new AetherWebSocket(
  (message) => {
    // Handle real-time updates
    console.log('Live update:', message);
  },
  (error) => {
    console.error('WebSocket error:', error);
  }
);
```

## 🎯 Zero Configuration

**Nessuna configurazione manuale richiesta!**

- ✅ Componenti si auto-scoprono
- ✅ Agenti si auto-registrano  
- ✅ Eventi si auto-loggano
- ✅ Audio si auto-serve
- ✅ UI si auto-aggiorna

## 🔮 Funzionalità Future

- Hot reload su Git push (watch per commit di Aether)
- 3D scene rendering per stanze complesse
- Chat integrata con agenti
- Controlli manuali per triggare evoluzioni
- Dashboard analytics per pattern evolutivi

## 🐛 Troubleshooting

### Componenti non si caricano
- Verifica che il backend sia attivo su porta 8000
- Controlla che i file JSX siano in `frontend/src/components/`
- Ispeziona console browser per errori di syntax

### Agenti non appaiono  
- Verifica che `AetherAgentManager` sia inizializzato
- Controlla file agenti in `aether/agents/`
- Verifica metadati MOOD, ROLE, GOAL nei file Python

### Audio non funziona
- Controlla CORS headers nel backend
- Verifica file audio nelle cartelle `audio/` o `data/audio/`
- Testa endpoint `/api/audio` manualmente

---

**Il frontend è vivo e cresce con Aether! 🌱** 