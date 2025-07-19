import io from 'socket.io-client'

class WebSocketClient {
  constructor() {
    this.socket = null
    this.isConnected = false
    this.messageHandlers = []
    this.statusHandlers = []
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 3
    this.reconnectDelay = 2000
  }

  // Connessione al server WebSocket
  connect(serverUrl = 'http://localhost:8000') {
    console.log('🔌 Connecting to Invader Core...', serverUrl)
    
    this.socket = io(serverUrl, {
      transports: ['websocket', 'polling'],
      timeout: 5000,
      forceNew: true
    })

    // Eventi di connessione
    this.socket.on('connect', () => {
      console.log('✅ Connected to Invader Core')
      this.isConnected = true
      this.reconnectAttempts = 0
      this.notifyStatusHandlers('connected', 'Connected to Invader Core')
    })

    this.socket.on('disconnect', (reason) => {
      console.log('❌ Disconnected from Invader:', reason)
      this.isConnected = false
      this.notifyStatusHandlers('disconnected', `Disconnected: ${reason}`)
      
      // Auto-reconnect
      if (reason === 'io server disconnect') {
        this.reconnect()
      }
    })

    this.socket.on('connect_error', (error) => {
      console.error('❌ Connection error:', error)
      this.isConnected = false
      this.notifyStatusHandlers('error', `Connection error: ${error.message}`)
      this.reconnect()
    })

    // Eventi specifici di Invader
    this.socket.on('invader_message', (data) => {
      console.log('🤖 Message from Invader:', data.message)
      this.notifyMessageHandlers({
        type: 'invader',
        message: data.message,
        timestamp: new Date()
      })
    })

    return this.socket
  }

  // Riconnessione automatica
  reconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log('❌ Max reconnection attempts reached')
      this.notifyStatusHandlers('failed', 'Connection failed')
      return
    }

    this.reconnectAttempts++
    console.log(`🔄 Reconnection attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts}...`)
    
    setTimeout(() => {
      if (!this.isConnected && this.socket) {
        this.socket.connect()
      }
    }, this.reconnectDelay * this.reconnectAttempts)
  }

  // Invio messaggio
  sendMessage(message) {
    if (!this.socket || !this.isConnected) {
      console.warn('⚠️ Not connected - cannot send message')
      return false
    }

    console.log('📤 Sending message to Invader:', message)
    this.socket.emit('user_message', { message })
    return true
  }

  // Gestori per messaggi
  onMessage(handler) {
    this.messageHandlers.push(handler)
  }

  offMessage(handler) {
    this.messageHandlers = this.messageHandlers.filter(h => h !== handler)
  }

  notifyMessageHandlers(message) {
    this.messageHandlers.forEach(handler => {
      try {
        handler(message)
      } catch (error) {
        console.error('Error in message handler:', error)
      }
    })
  }

  // Gestori per stato connessione
  onStatus(handler) {
    this.statusHandlers.push(handler)
  }

  offStatus(handler) {
    this.statusHandlers = this.statusHandlers.filter(h => h !== handler)
  }

  notifyStatusHandlers(status, message) {
    this.statusHandlers.forEach(handler => {
      try {
        handler({ status, message, timestamp: new Date() })
      } catch (error) {
        console.error('Error in status handler:', error)
      }
    })
  }

  // Disconnessione
  disconnect() {
    if (this.socket) {
      console.log('🔌 Disconnecting from Invader...')
      this.socket.disconnect()
      this.socket = null
      this.isConnected = false
    }
  }

  // Stato connessione
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      socket: this.socket
    }
  }
}

// Singleton instance
const webSocketClient = new WebSocketClient()

export default webSocketClient 