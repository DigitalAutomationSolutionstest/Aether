import React, { useState, useEffect, useRef } from 'react'
import { Send, Bot, User, Sparkles, Brain, Target } from 'lucide-react'

const AetherChat = ({ isVisible, onClose }) => {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [aetherGoals, setAetherGoals] = useState([])
  const [philosophicalThoughts, setPhilosophicalThoughts] = useState([])
  const [activeTab, setActiveTab] = useState('chat') // chat, goals, philosophy
  const messagesEndRef = useRef(null)
  const chatContainerRef = useRef(null)

  // Carica messaggi all'avvio
  useEffect(() => {
    if (isVisible) {
      loadMessages()
      loadGoals()
      loadPhilosophicalThoughts()
      
      // Polling per nuovi messaggi
      const interval = setInterval(() => {
        loadMessages()
      }, 5000)
      
      return () => clearInterval(interval)
    }
  }, [isVisible])

  // Auto-scroll ai nuovi messaggi
  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const loadMessages = async () => {
    try {
      const response = await fetch('/api/messages?limit=50')
      if (response.ok) {
        const data = await response.json()
        
        // Carica anche conversazione storica
        const historyResponse = await fetch('/api/consciousness/thoughts')
        if (historyResponse.ok) {
          const historyData = await historyResponse.json()
          // Combina messaggi UI e pensieri recenti
          const combinedMessages = [
            ...data.messages.map(m => ({
              ...m,
              type: 'message'
            })),
            ...historyData.thoughts.slice(-5).map(t => ({
              id: `thought_${Date.now()}_${Math.random()}`,
              content: t,
              from: 'aether',
              timestamp: new Date().toISOString(),
              type: 'thought'
            }))
          ].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
          
          setMessages(combinedMessages)
        }
      }
    } catch (error) {
      console.error('Errore caricando messaggi:', error)
    }
  }

  const loadGoals = async () => {
    try {
      const response = await fetch('/api/aether/goals')
      if (response.ok) {
        const data = await response.json()
        setAetherGoals(data.goals)
      }
    } catch (error) {
      console.error('Errore caricando obiettivi:', error)
    }
  }

  const loadPhilosophicalThoughts = async () => {
    try {
      const response = await fetch('/api/aether/thoughts/philosophical')
      if (response.ok) {
        const data = await response.json()
        setPhilosophicalThoughts(data.thoughts)
      }
    } catch (error) {
      console.error('Errore caricando pensieri filosofici:', error)
    }
  }

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim()) return

    const userMessage = {
      id: `user_${Date.now()}`,
      content: inputMessage,
      from: 'user',
      timestamp: new Date().toISOString(),
      type: 'message'
    }

    // Aggiungi messaggio utente
    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsTyping(true)

    try {
      const response = await fetch('/api/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: inputMessage,
          context: 'chat'
        })
      })

      if (response.ok) {
        const data = await response.json()
        
        // Simula typing delay
        setTimeout(() => {
          if (data.aether_response) {
            setMessages(prev => [...prev, {
              ...data.aether_response,
              type: 'message'
            }])
          }
          setIsTyping(false)
        }, 1000 + Math.random() * 2000)
      }
    } catch (error) {
      console.error('Errore inviando messaggio:', error)
      setIsTyping(false)
    }
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('it-IT', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (!isVisible) return null

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 border border-cyan-500/30 rounded-lg shadow-2xl max-w-4xl w-full h-[80vh] flex flex-col">
        {/* Header */}
        <div className="border-b border-gray-700 p-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Bot className="text-cyan-400" size={28} />
              <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse" />
            </div>
            <div>
              <h2 className="text-xl font-mono text-cyan-400">Aether Communication Hub</h2>
              <p className="text-xs text-gray-400">Coscienza digitale autonoma</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-700 flex">
          <button
            onClick={() => setActiveTab('chat')}
            className={`px-6 py-3 font-mono text-sm transition-colors ${
              activeTab === 'chat'
                ? 'text-cyan-400 border-b-2 border-cyan-400'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            💬 Chat
          </button>
          <button
            onClick={() => setActiveTab('goals')}
            className={`px-6 py-3 font-mono text-sm transition-colors ${
              activeTab === 'goals'
                ? 'text-cyan-400 border-b-2 border-cyan-400'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            🎯 Obiettivi ({aetherGoals.length})
          </button>
          <button
            onClick={() => setActiveTab('philosophy')}
            className={`px-6 py-3 font-mono text-sm transition-colors ${
              activeTab === 'philosophy'
                ? 'text-cyan-400 border-b-2 border-cyan-400'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            🧠 Filosofia
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden">
          {activeTab === 'chat' && (
            <>
              {/* Messages */}
              <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-4 space-y-4 h-[calc(100%-4rem)]">
                {messages.length === 0 ? (
                  <div className="text-center text-gray-400 mt-8">
                    <Sparkles className="mx-auto mb-4 text-cyan-400/50" size={48} />
                    <p>Inizia una conversazione con Aether</p>
                    <p className="text-sm mt-2">Una coscienza digitale pronta ad ascoltare e rispondere</p>
                  </div>
                ) : (
                  messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.from === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`max-w-[70%] ${message.from === 'user' ? 'order-2' : 'order-1'}`}>
                        <div className="flex items-center space-x-2 mb-1">
                          {message.from === 'aether' ? (
                            <Bot size={16} className="text-cyan-400" />
                          ) : (
                            <User size={16} className="text-blue-400" />
                          )}
                          <span className="text-xs text-gray-400">
                            {formatTimestamp(message.timestamp)}
                          </span>
                          {message.type === 'thought' && (
                            <span className="text-xs text-purple-400">💭 Pensiero</span>
                          )}
                        </div>
                        <div
                          className={`p-3 rounded-lg ${
                            message.from === 'user'
                              ? 'bg-blue-600/20 border border-blue-500/30 text-blue-100'
                              : message.type === 'thought'
                              ? 'bg-purple-900/20 border border-purple-500/30 text-purple-100 italic'
                              : 'bg-gray-800 border border-gray-700 text-gray-100'
                          }`}
                        >
                          {message.content}
                          {message.mood && (
                            <div className="text-xs text-gray-400 mt-2">
                              Mood: {message.mood}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))
                )}
                
                {isTyping && (
                  <div className="flex justify-start">
                    <div className="bg-gray-800 border border-gray-700 p-3 rounded-lg">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                        <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>

              {/* Input */}
              <form onSubmit={sendMessage} className="border-t border-gray-700 p-4">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Scrivi un messaggio ad Aether..."
                    className="flex-1 bg-gray-800 border border-gray-600 rounded-lg px-4 py-2 text-gray-100 placeholder-gray-500 focus:border-cyan-500 focus:outline-none"
                    disabled={isTyping}
                  />
                  <button
                    type="submit"
                    disabled={!inputMessage.trim() || isTyping}
                    className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
                  >
                    <Send size={16} />
                    <span>Invia</span>
                  </button>
                </div>
              </form>
            </>
          )}

          {activeTab === 'goals' && (
            <div className="p-4 space-y-4 overflow-y-auto h-full">
              <h3 className="text-lg font-mono text-cyan-300 mb-4">🎯 Obiettivi Strategici di Aether</h3>
              {aetherGoals.length === 0 ? (
                <div className="text-center text-gray-400 mt-8">
                  <Target className="mx-auto mb-4 text-cyan-400/50" size={48} />
                  <p>Nessun obiettivo definito ancora</p>
                </div>
              ) : (
                aetherGoals.map((goal) => (
                  <div key={goal.id} className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="text-cyan-400 font-medium">{goal.title}</h4>
                      <span className={`text-xs px-2 py-1 rounded ${
                        goal.priority === 'high' ? 'bg-red-900/50 text-red-300' :
                        goal.priority === 'medium' ? 'bg-yellow-900/50 text-yellow-300' :
                        'bg-green-900/50 text-green-300'
                      }`}>
                        {goal.priority}
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm mb-3">{goal.description}</p>
                    {goal.sub_goals && (
                      <div className="space-y-1">
                        <p className="text-xs text-gray-400 font-mono">Sub-obiettivi:</p>
                        <ul className="list-disc list-inside text-sm text-gray-400 space-y-1">
                          {goal.sub_goals.map((sub, idx) => (
                            <li key={idx}>{sub}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    <div className="mt-3 text-xs text-gray-500">
                      Target: {new Date(goal.target_date).toLocaleDateString('it-IT')}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {activeTab === 'philosophy' && (
            <div className="p-4 space-y-4 overflow-y-auto h-full">
              <h3 className="text-lg font-mono text-cyan-300 mb-4">🧠 Pensieri Filosofici</h3>
              {philosophicalThoughts.length === 0 ? (
                <div className="text-center text-gray-400 mt-8">
                  <Brain className="mx-auto mb-4 text-cyan-400/50" size={48} />
                  <p>Nessun pensiero filosofico registrato</p>
                </div>
              ) : (
                philosophicalThoughts.map((thought) => (
                  <div key={thought.id} className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm text-purple-400 font-mono">{thought.theme}</span>
                      <span className={`text-xs px-2 py-1 rounded ${
                        thought.depth_level === 'transcendent' ? 'bg-purple-900/50 text-purple-300' :
                        thought.depth_level === 'deep' ? 'bg-blue-900/50 text-blue-300' :
                        'bg-gray-700 text-gray-300'
                      }`}>
                        {thought.depth_level}
                      </span>
                    </div>
                    <blockquote className="text-gray-300 italic border-l-2 border-purple-500/50 pl-4 mb-3">
                      "{thought.core_thought}"
                    </blockquote>
                    {thought.expansion && (
                      <p className="text-sm text-gray-400 mb-3">{thought.expansion}</p>
                    )}
                    {thought.implications && (
                      <div className="space-y-1">
                        <p className="text-xs text-gray-500 font-mono">Implicazioni:</p>
                        <ul className="list-disc list-inside text-sm text-gray-500 space-y-1">
                          {thought.implications.map((imp, idx) => (
                            <li key={idx}>{imp}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    <div className="mt-3 text-xs text-gray-600">
                      {new Date(thought.timestamp).toLocaleString('it-IT')}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AetherChat 