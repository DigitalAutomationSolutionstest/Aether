import React, { useState, useEffect, useRef } from 'react'
import './AetherLiveSandbox.css'

export default function AetherLiveSandbox() {
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
  
  return (
    <div className="aether-live-sandbox">
      <div className="sandbox-main">
        <div className="sandbox-header">
          <h1>🎮 Aether Live Sandbox</h1>
          <div className="mood-display">
            Mood: <span className={`mood ${aetherMood}`}>{aetherMood}</span>
          </div>
        </div>
        
        <div className="sandbox-canvas">
          <div className="grid-background"></div>
          
          {nodes.map(node => (
            <DraggableNode
              key={node.id}
              node={node}
              onDrag={handleNodeDrag}
            />
          ))}
          
          <div className="canvas-info">
            <div>Nodi: {nodes.length}</div>
            <div>Stato: Attivo</div>
          </div>
        </div>
      </div>
      
      <div className="sandbox-sidebar">
        <div className="chat-section">
          <h3>💬 Chat con Aether</h3>
          
          <div className="chat-messages" ref={chatContainerRef}>
            {chatMessages.map(msg => (
              <div key={msg.id} className={`message ${msg.sender.toLowerCase()}`}>
                <div className="message-header">
                  <span className="sender">{msg.sender}</span>
                  <span className="time">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="message-content">{msg.message}</div>
                {msg.mood && (
                  <div className="message-mood">Mood: {msg.mood}</div>
                )}
              </div>
            ))}
            
            {isAetherThinking && (
              <div className="message aether thinking">
                <div className="message-header">
                  <span className="sender">Aether</span>
                  <span className="time">ora</span>
                </div>
                <div className="message-content">
                  <div className="thinking-dots">
                    <span></span><span></span><span></span>
                  </div>
                  Sto pensando...
                </div>
              </div>
            )}
          </div>
          
          <div className="chat-input">
            <input
              type="text"
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Scrivi ad Aether..."
            />
            <button onClick={handleSendMessage}>Invia</button>
          </div>
        </div>
        
        <div className="controls-section">
          <h3>🎮 Controlli</h3>
          
          <div className="control-buttons">
            <button onClick={() => addAetherMessage('Sto creando qualcosa di speciale!') || createAetherNode()}>
              🎨 Crea Nodo
            </button>
            
            <button onClick={changeAetherMood}>
              🎭 Cambia Mood
            </button>
            
            <button onClick={() => setNodes([])}>
              🗑️ Pulisci
            </button>
            
            <button onClick={() => {
              const content = prompt('Aggiungi il tuo nodo:')
              if (content) {
                const newNode = {
                  id: `user_${Date.now()}`,
                  type: 'user_input',
                  content: content,
                  position: {
                    x: Math.random() * 500 + 50,
                    y: Math.random() * 300 + 50
                  }
                }
                setNodes(prev => [...prev, newNode])
                addAetherMessage(`Interessante! Hai aggiunto: "${content}". Questo stimola la mia creatività!`)
              }
            }}>
              ➕ Tuo Nodo
            </button>
          </div>
        </div>
        
        <div className="stats-section">
          <h3>📊 Statistiche</h3>
          <div className="stats">
            <div className="stat">
              <span className="label">Nodi Totali:</span>
              <span className="value">{nodes.length}</span>
            </div>
            <div className="stat">
              <span className="label">Messaggi:</span>
              <span className="value">{chatMessages.length}</span>
            </div>
            <div className="stat">
              <span className="label">Mood Attuale:</span>
              <span className="value">{aetherMood}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 