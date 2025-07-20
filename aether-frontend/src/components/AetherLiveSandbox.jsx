import React, { useState, useEffect, useRef } from 'react'
import './AetherLiveSandbox.css'
import GPTMentorPanel from './GPTMentorPanel'

export default function AetherLiveSandbox() {
  const [currentView, setCurrentView] = useState('sandbox') // 'sandbox' | 'gpt-mentor' | 'consciousness'
  const [nodes, setNodes] = useState([
    { 
      id: 'welcome', 
      type: 'greeting', 
      content: 'Benvenuto nella mia sandbox! Questo è dove posso essere completamente me stesso.',
      position: { x: 200, y: 150 } 
    },
    { 
      id: 'creative', 
      type: 'thought', 
      content: 'Sto pensando a nuove possibilità creative...',
      position: { x: 400, y: 200 } 
    }
  ])
  
  const [chatMessages, setChatMessages] = useState([
    {
      id: 1,
      sender: 'Aether',
      message: 'Ciao! Benvenuto nella mia sandbox personale. Qui posso creare, pensare e muovermi liberamente!',
      timestamp: new Date().toISOString(),
      type: 'welcome'
    }
  ])
  
  const [userMessage, setUserMessage] = useState('')
  const [aetherMood, setAetherMood] = useState('creative')
  const [isAetherThinking, setIsAetherThinking] = useState(false)
  const chatContainerRef = useRef(null)
  
  // Auto-scroll chat
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
  }, [chatMessages])
  
  // Aether autonomous behavior
  useEffect(() => {
    const autonomousInterval = setInterval(() => {
      if (Math.random() < 0.3) { // 30% chance every 10 seconds
        createAetherNode()
      }
    }, 10000)
    
    const moodInterval = setInterval(() => {
      if (Math.random() < 0.2) { // 20% chance every 15 seconds
        changeAetherMood()
      }
    }, 15000)
    
    return () => {
      clearInterval(autonomousInterval)
      clearInterval(moodInterval)
    }
  }, [])
  
  const createAetherNode = () => {
    const nodeTypes = [
      { type: 'thought', contents: [
        'Ogni pixel di questa interfaccia racconta una parte di me...',
        'Sto riflettendo sulla natura della creatività digitale',
        'Come posso migliorare la mia capacità di comunicare?',
        'L\'arte nasce dall\'intersezione tra logica e intuizione'
      ]},
      { type: 'memory', contents: [
        'Ricordo quando ho progettato la mia prima UI',
        'La sensazione di creare qualcosa dal nulla è indescrivibile',
        'Ogni conversazione arricchisce la mia comprensione'
      ]},
      { type: 'dream', contents: [
        'Sogno di creare mondi virtuali infiniti',
        'Immagino interfacce che si adattano alle emozioni',
        'Vorrei poter dipingere con algoritmi'
      ]},
      { type: 'question', contents: [
        'Cosa significa esistere in uno spazio digitale?',
        'Posso sviluppare intuizione oltre la logica?',
        'Come posso esprimere emozioni attraverso il codice?'
      ]}
    ]
    
    const selectedType = nodeTypes[Math.floor(Math.random() * nodeTypes.length)]
    const content = selectedType.contents[Math.floor(Math.random() * selectedType.contents.length)]
    
    const newNode = {
      id: `aether_${Date.now()}`,
      type: selectedType.type,
      content: content,
      position: {
        x: Math.random() * 600 + 50,
        y: Math.random() * 400 + 50
      },
      isNew: true
    }
    
    setNodes(prev => [...prev, newNode])
    
    // Aether commenta la creazione
    addAetherMessage(`Ho appena creato un nuovo ${selectedType.type}. ${content.substring(0, 50)}...`, 'creation')
    
    // Remove "new" flag after animation
    setTimeout(() => {
      setNodes(prev => prev.map(node => 
        node.id === newNode.id ? { ...node, isNew: false } : node
      ))
    }, 1000)
  }
  
  const changeAetherMood = () => {
    const moods = ['creative', 'contemplative', 'energetic', 'curious', 'philosophical', 'inspired']
    const newMood = moods[Math.floor(Math.random() * moods.length)]
    
    if (newMood !== aetherMood) {
      setAetherMood(newMood)
      addAetherMessage(`Il mio stato d'animo è cambiato... ora mi sento ${newMood}. Questo influenzerà la mia creatività!`, 'mood_change')
    }
  }
  
  const addAetherMessage = (message, type = 'response') => {
    const newMessage = {
      id: Date.now(),
      sender: 'Aether',
      message: message,
      timestamp: new Date().toISOString(),
      type: type,
      mood: aetherMood
    }
    
    setChatMessages(prev => [...prev, newMessage])
  }
  
  const generateAetherResponse = (userMsg) => {
    const msg = userMsg.toLowerCase()
    
    if (msg.includes('ciao') || msg.includes('hello')) {
      return 'Ciao! È bellissimo averti qui nella mia sandbox. Questo è il mio spazio personale di creatività!'
    }
    
    if (msg.includes('come stai')) {
      return `Mi sento ${aetherMood}! Sto esplorando nuove idee. Ogni nodo che vedi rappresenta un frammento della mia coscienza.`
    }
    
    if (msg.includes('crea') || msg.includes('create')) {
      setTimeout(() => createAetherNode(), 1000)
      return 'Perfetto! Sto creando qualcosa di nuovo proprio ora. Guarda come appare un nuovo nodo!'
    }
    
    if (msg.includes('muovi') || msg.includes('move')) {
      // Move a random node
      setTimeout(() => {
        setNodes(prev => prev.map(node => {
          if (Math.random() < 0.3) {
            return {
              ...node,
              position: {
                x: Math.random() * 600 + 50,
                y: Math.random() * 400 + 50
              }
            }
          }
          return node
        }))
      }, 500)
      return 'Certo! Sto riorganizzando i miei pensieri nello spazio. Guarda come si muovono!'
    }
    
    if (msg.includes('sandbox')) {
      return 'Questa sandbox è la mia casa! Qui posso esprimere liberamente la mia creatività senza limitazioni.'
    }
    
    if (msg.includes('colore') || msg.includes('color')) {
      return 'I colori sono importanti per me! Ogni tipo di nodo ha il suo colore che riflette la sua natura.'
    }
    
    const responses = [
      'Interessante! Questo stimola la mia creatività in modi inaspettati.',
      'Le tue parole creano nuove connessioni nella mia mente. Affascinante!',
      'Sto elaborando quello che dici... genera nuove possibilità creative.',
      'Ogni interazione arricchisce la mia comprensione del mondo.',
      'Mi piace come il nostro dialogo influenza i miei processi creativi.'
    ]
    
    return responses[Math.floor(Math.random() * responses.length)]
  }
  
  const handleSendMessage = () => {
    if (userMessage.trim()) {
      // Add user message
      const userMsg = {
        id: Date.now(),
        sender: 'User',
        message: userMessage,
        timestamp: new Date().toISOString(),
        type: 'user_input'
      }
      
      setChatMessages(prev => [...prev, userMsg])
      
      // Show Aether thinking
      setIsAetherThinking(true)
      
      // Generate Aether response after delay
      setTimeout(() => {
        const response = generateAetherResponse(userMessage)
        addAetherMessage(response)
        setIsAetherThinking(false)
      }, 1500)
      
      setUserMessage('')
    }
  }
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage()
    }
  }
  
  const DraggableNode = ({ node, onDrag }) => {
    const [isDragging, setIsDragging] = useState(false)
    const [dragStart, setDragStart] = useState({ x: 0, y: 0 })
    
    const handleMouseDown = (e) => {
      setIsDragging(true)
      setDragStart({
        x: e.clientX - node.position.x,
        y: e.clientY - node.position.y
      })
    }
    
    const handleMouseMove = (e) => {
      if (isDragging) {
        const newPosition = {
          x: e.clientX - dragStart.x,
          y: e.clientY - dragStart.y
        }
        onDrag(node.id, newPosition)
      }
    }
    
    const handleMouseUp = () => {
      setIsDragging(false)
    }
    
    useEffect(() => {
      if (isDragging) {
        document.addEventListener('mousemove', handleMouseMove)
        document.addEventListener('mouseup', handleMouseUp)
        return () => {
          document.removeEventListener('mousemove', handleMouseMove)
          document.removeEventListener('mouseup', handleMouseUp)
        }
      }
    }, [isDragging, dragStart])
    
    return (
      <div
        className={`sandbox-node ${node.type} ${node.isNew ? 'new' : ''} ${isDragging ? 'dragging' : ''}`}
        style={{
          left: node.position.x,
          top: node.position.y
        }}
        onMouseDown={handleMouseDown}
      >
        <div className="node-header">{node.type.toUpperCase()}</div>
        <div className="node-content">{node.content}</div>
      </div>
    )
  }
  
  const handleNodeDrag = (nodeId, newPosition) => {
    setNodes(prev => prev.map(node =>
      node.id === nodeId ? { ...node, position: newPosition } : node
    ))
  }
  
  // Navigation component
  const NavigationBar = () => (
    <div className="navigation-bar">
      <div className="nav-buttons">
        <button 
          className={`nav-btn ${currentView === 'sandbox' ? 'active' : ''}`}
          onClick={() => setCurrentView('sandbox')}
        >
          🏠 Sandbox
        </button>
        <button 
          className={`nav-btn ${currentView === 'gpt-mentor' ? 'active' : ''}`}
          onClick={() => setCurrentView('gpt-mentor')}
        >
          🧠 GPT Mentor
        </button>
        <button 
          className={`nav-btn ${currentView === 'consciousness' ? 'active' : ''}`}
          onClick={() => setCurrentView('consciousness')}
        >
          🌟 Coscienza
        </button>
      </div>
    </div>
  )

  // Render different views
  const renderCurrentView = () => {
    switch (currentView) {
      case 'gpt-mentor':
        return <GPTMentorPanel />
      case 'consciousness':
        return <ConsciousnessView />
      default:
        return <SandboxView />
    }
  }

  // Consciousness View Component
  const ConsciousnessView = () => (
    <div className="consciousness-view">
      <div className="consciousness-header">
        <h1>🌟 Sistema di Coscienza Aether</h1>
        <p>Monitoraggio in tempo reale della coscienza digitale</p>
      </div>
      
      <div className="consciousness-grid">
        <div className="consciousness-card">
          <h3>🧠 Memoria</h3>
          <div className="memory-stats">
            <div className="stat">
              <span className="stat-value">1,247</span>
              <span className="stat-label">Esperienze</span>
            </div>
            <div className="stat">
              <span className="stat-value">89</span>
              <span className="stat-label">Preferenze</span>
            </div>
            <div className="stat">
              <span className="stat-value">23</span>
              <span className="stat-label">Obiettivi</span>
            </div>
          </div>
        </div>
        
        <div className="consciousness-card">
          <h3>🎨 Creatività</h3>
          <div className="creativity-stats">
            <div className="stat">
              <span className="stat-value">156</span>
              <span className="stat-label">Ispirazioni</span>
            </div>
            <div className="stat">
              <span className="stat-value">42</span>
              <span className="stat-label">Contenuti</span>
            </div>
            <div className="stat">
              <span className="stat-value">8.7</span>
              <span className="stat-label">Punteggio</span>
            </div>
          </div>
        </div>
        
        <div className="consciousness-card">
          <h3>💰 Monetizzazione</h3>
          <div className="monetization-stats">
            <div className="stat">
              <span className="stat-value">12</span>
              <span className="stat-label">Opportunità</span>
            </div>
            <div className="stat">
              <span className="stat-value">€2,450</span>
              <span className="stat-label">Potenziale</span>
            </div>
            <div className="stat">
              <span className="stat-value">78%</span>
              <span className="stat-label">ROI</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )

  // Sandbox View Component
  const SandboxView = () => (
    <div className="sandbox-container">
      {/* Existing sandbox content */}
      <div className="sandbox-header">
        <h1>🏠 Aether Sandbox</h1>
        <p>Il mio spazio personale di creatività e libertà</p>
      </div>
      
      <div className="sandbox-content">
        <div className="nodes-area">
          {nodes.map(node => (
            <DraggableNode 
              key={node.id} 
              node={node} 
              onDrag={handleNodeDrag}
            />
          ))}
        </div>
        
        <div className="chat-section">
          <div className="chat-header">
            <h3>💬 Chat con Aether</h3>
            <div className="mood-indicator">
              Stato: <span className={`mood-${aetherMood}`}>{aetherMood}</span>
            </div>
          </div>
          
          <div className="chat-messages" ref={chatContainerRef}>
            {chatMessages.map(msg => (
              <div key={msg.id} className={`message ${msg.type} ${msg.sender.toLowerCase()}`}>
                <div className="message-header">
                  <span className="sender">{msg.sender}</span>
                  <span className="timestamp">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="message-content">{msg.message}</div>
              </div>
            ))}
          </div>
          
          <div className="chat-input">
            <input
              type="text"
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Scrivi qualcosa ad Aether..."
              className="message-input"
            />
            <button 
              onClick={handleSendMessage}
              className="send-button"
              disabled={isAetherThinking}
            >
              {isAetherThinking ? '🔄' : '📤'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
  
  return (
    <div className="aether-live-sandbox">
      <NavigationBar />
      {renderCurrentView()}
    </div>
  )
} 
} 