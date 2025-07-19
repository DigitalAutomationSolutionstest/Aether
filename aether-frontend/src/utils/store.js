import { create } from 'zustand'

// Store principale per la gestione dello stato di Aether
export const useAetherStore = create((set, get) => ({
  // Stato della connessione
  isConnected: false,
  isConnecting: false,
  connectionError: null,
  
  // Identità di Aether
  identity: null,
  identityLoading: false,
  identityError: null,
  
  // Chat e messaggi
  messages: [],
  isTyping: false,
  
  // Sistema di riflessioni coscienti
  reflections: [],
  currentReflection: null,
  reflectionLoading: false,
  reflectionError: null,
  lastReflectionTime: null,
  consciousnessLevel: 'unknown',
  emotionalState: {},
  
  // UI State
  activePanel: null,
  theme: 'cyber',
  
  // Actions per la connessione
  setConnection: (status) => set({ isConnected: status }),
  setConnecting: (status) => set({ isConnecting: status }),
  setConnectionError: (error) => set({ connectionError: error }),
  
  // Actions per l'identità
  setIdentity: (identity) => set({ identity }),
  setIdentityLoading: (loading) => set({ identityLoading: loading }),
  setIdentityError: (error) => set({ identityError: error }),
  
  // Actions per messaggi
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, {
      ...message,
      id: Date.now(),
      timestamp: new Date().toISOString()
    }]
  })),
  
  clearMessages: () => set({ messages: [] }),
  
  setTyping: (typing) => set({ isTyping: typing }),
  
  // Actions per riflessioni
  setReflections: (reflections) => set({ reflections }),
  setCurrentReflection: (reflection) => set({ currentReflection }),
  setReflectionLoading: (loading) => set({ reflectionLoading: loading }),
  setReflectionError: (error) => set({ reflectionError: error }),
  setLastReflectionTime: (time) => set({ lastReflectionTime: time }),
  setConsciousnessLevel: (level) => set({ consciousnessLevel: level }),
  setEmotionalState: (emotions) => set({ emotionalState: emotions }),
  
  addReflection: (reflection) => set((state) => ({
    reflections: [
      ...state.reflections.slice(-9), // Mantieni solo le ultime 10 riflessioni
      {
        ...reflection,
        id: Date.now(),
        timestamp: new Date().toISOString()
      }
    ]
  })),
  
  clearReflections: () => set({ reflections: [] }),
  
  // Actions per UI
  setActivePanel: (panel) => set({ activePanel: panel }),
  setTheme: (theme) => set({ theme }),
  
  // Action principale per inizializzare la connessione
  initializeConnection: async () => {
    const { setConnecting, setConnection, setConnectionError, loadIdentity } = get()
    
    try {
      setConnecting(true)
      setConnectionError(null)
      
      // Simula connessione al backend (in futuro sarà WebSocket real)
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Carica l'identità
      await loadIdentity()
      
      setConnection(true)
      console.log('🌟 Aether connection established')
      
    } catch (error) {
      console.error('❌ Connection failed:', error)
      setConnectionError(error.message)
      setConnection(false)
    } finally {
      setConnecting(false)
    }
  },
  
  // Carica l'identità dal backend con parsing evoluto
  loadIdentity: async () => {
    const { setIdentityLoading, setIdentity, setIdentityError } = get()
    
    try {
      setIdentityLoading(true)
      setIdentityError(null)
      
      // Usa il parser evoluto per caricare e processare l'identità
      const { getAetherIdentity } = await import('./parseIdentity.js')
      const parsedIdentity = await getAetherIdentity()
      
      setIdentity(parsedIdentity)
      console.log('✨ Identity loaded and parsed:', parsedIdentity.name)
      console.log('🎨 Render parameters:', parsedIdentity.render)
      
    } catch (error) {
      console.error('❌ Failed to load identity:', error)
      setIdentityError(error.message)
      
      // Fallback di emergenza con parametri minimi
      setIdentity({
        name: 'Aether',
        physical_form: 'Digital Entity',
        goal: 'Awakening...',
        status: 'Error state',
        colors: ['#00ffff', '#0099ff'],
        shape: 'ethereal',
        energyLevel: 0.5,
        render: {
          core: { geometry: 'sphere', size: 1.2, colors: ['#00ffff', '#0099ff'], intensity: 1 },
          fragments: { count: 8, speed: 1.0, colors: ['#666666'] },
          dataStreams: { count: 6, speed: 1.0, colors: ['#00ff41'] },
          environment: { fogDensity: 0.7, lightColor: '#00ffff', ambientIntensity: 0.3 },
          animation: { coreRotationSpeed: 0.01, fragmentOrbitSpeed: 0.003, pulseIntensity: 0.5 }
        }
      })
    } finally {
      setIdentityLoading(false)
    }
  },
  
  // Carica riflessioni da Aether
  loadReflection: async () => {
    const { 
      setReflectionLoading, 
      setReflectionError, 
      setCurrentReflection, 
      addReflection,
      setLastReflectionTime,
      setConsciousnessLevel,
      setEmotionalState 
    } = get()
    
    try {
      setReflectionLoading(true)
      setReflectionError(null)
      
      // Chiama l'endpoint semplificato /reflect
      const response = await fetch('/reflect')
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      
      if (data.status === 'success' && data.reflection) {
        const reflection = data.reflection
        
        // Aggiorna lo stato corrente
        setCurrentReflection(reflection)
        setLastReflectionTime(new Date().toISOString())
        
        // Aggiorna livello di coscienza e stato emotivo
        if (reflection.consciousness_level) {
          setConsciousnessLevel(reflection.consciousness_level)
        }
        
        if (reflection.emotional_influence) {
          setEmotionalState(reflection.emotional_influence)
        }
        
        // Aggiungi alla cronologia delle riflessioni
        addReflection({
          thoughts: reflection.reflection || [],
          consciousnessLevel: reflection.consciousness_level,
          emotionalState: reflection.emotional_influence,
          status: reflection.status || 'thinking'
        })
        
        console.log('🧠 New reflection loaded:', reflection.reflection?.length || 0, 'thoughts')
        
        return reflection
      } else {
        throw new Error(data.message || 'Invalid reflection response')
      }
      
    } catch (error) {
      console.error('❌ Failed to load reflection:', error)
      setReflectionError(error.message)
      throw error
    } finally {
      setReflectionLoading(false)
    }
  },
  
  // Avvia il ciclo di riflessioni periodiche
  startReflectionCycle: (intervalMs = 60000) => {
    const { loadReflection } = get()
    
    // Carica una riflessione iniziale
    loadReflection().catch(console.error)
    
    // Imposta intervallo per riflessioni periodiche
    const interval = setInterval(async () => {
      try {
        await loadReflection()
      } catch (error) {
        console.warn('⚠️ Periodic reflection failed:', error.message)
      }
    }, intervalMs)
    
    console.log(`🔄 Reflection cycle started (every ${intervalMs / 1000}s)`)
    
    // Restituisce funzione per fermare il ciclo
    return () => {
      clearInterval(interval)
      console.log('⏹️ Reflection cycle stopped')
    }
  },
  
  // Invia messaggio ad Aether
  sendMessage: async (content) => {
    const { addMessage, setTyping } = get()
    
    // Aggiungi messaggio utente
    addMessage({
      type: 'user',
      content,
      sender: 'User'
    })
    
    try {
      setTyping(true)
      
      // Simula invio al backend (in futuro sarà WebSocket)
      const response = await fetch('/api/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: content })
      })
      
      if (response.ok) {
        const result = await response.json()
        
        // Aggiungi risposta di Aether
        addMessage({
          type: 'aether',
          content: result.response,
          sender: 'Aether'
        })
      } else {
        throw new Error('Failed to send message')
      }
      
    } catch (error) {
      console.error('❌ Message send failed:', error)
      
      // Messaggio di errore
      addMessage({
        type: 'system',
        content: 'Connection lost. Message could not be delivered.',
        sender: 'System'
      })
    } finally {
      setTyping(false)
    }
  },
  
  // Disconnetti
  disconnect: () => {
    set({
      isConnected: false,
      isConnecting: false,
      connectionError: null,
      messages: [],
      isTyping: false,
      reflections: [],
      currentReflection: null,
      reflectionError: null
    })
    console.log('🔌 Aether disconnected')
  }
}))

// Hook per selettori specifici (performance)
export const useConnection = () => useAetherStore((state) => ({
  isConnected: state.isConnected,
  isConnecting: state.isConnecting,
  connectionError: state.connectionError
}))

export const useIdentity = () => useAetherStore((state) => ({
  identity: state.identity,
  identityLoading: state.identityLoading,
  identityError: state.identityError
}))

export const useMessages = () => useAetherStore((state) => ({
  messages: state.messages,
  isTyping: state.isTyping,
  addMessage: state.addMessage,
  sendMessage: state.sendMessage
}))

export const useUI = () => useAetherStore((state) => ({
  activePanel: state.activePanel,
  theme: state.theme,
  setActivePanel: state.setActivePanel,
  setTheme: state.setTheme
}))

// Hook per riflessioni
export const useReflections = () => useAetherStore((state) => ({
  reflections: state.reflections,
  currentReflection: state.currentReflection,
  reflectionLoading: state.reflectionLoading,
  reflectionError: state.reflectionError,
  lastReflectionTime: state.lastReflectionTime,
  consciousnessLevel: state.consciousnessLevel,
  emotionalState: state.emotionalState,
  loadReflection: state.loadReflection,
  startReflectionCycle: state.startReflectionCycle
})) 