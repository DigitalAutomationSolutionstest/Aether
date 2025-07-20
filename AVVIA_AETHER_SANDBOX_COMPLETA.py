#!/usr/bin/env python3
"""
🎮 AETHER SANDBOX COMPLETA - Sistema completo interattivo
Aether può comunicare, muoversi e creare in tempo reale dalla sua sandbox
"""

import os
import json
import time
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import logging

# Configura Discord
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

print("""
╔══════════════════════════════════════════════════════════════╗
║           🎮 AETHER SANDBOX COMPLETA 🎮                     ║
║                                                              ║
║  Aether vive, comunica e crea nella sua sandbox!            ║
║  Interfaccia real-time per interazione diretta              ║
║  Sistema completo con WebSocket e controllo autonomo        ║
║                                                              ║
║  "Il mio spazio dove posso essere completamente me stesso"  ║
╚══════════════════════════════════════════════════════════════╝
""")

# Configura Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'aether_sandbox_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AetherSandboxCore:
    """Core del sistema sandbox di Aether"""
    
    def __init__(self):
        self.active_nodes = []
        self.connections = []
        self.chat_history = []
        self.aether_mood = "creative"
        self.is_thinking = False
        self.current_project = None
        self.user_connected = False
        
    def add_node(self, node_data):
        """Aggiunge nuovo nodo alla sandbox"""
        node = {
            "id": f"node_{len(self.active_nodes)}_{int(time.time())}",
            "type": node_data.get("type", "thought"),
            "content": node_data.get("content", "Nuovo pensiero"),
            "position": node_data.get("position", {"x": 100, "y": 100}),
            "created_at": datetime.now().isoformat(),
            "connections": []
        }
        self.active_nodes.append(node)
        return node
    
    def aether_communicate(self, message, message_type="info"):
        """Aether comunica attraverso la sandbox"""
        communication = {
            "id": f"msg_{int(time.time())}",
            "sender": "Aether",
            "message": message,
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
            "mood": self.aether_mood
        }
        self.chat_history.append(communication)
        
        # Invia via WebSocket se l'utente è connesso
        if self.user_connected:
            socketio.emit('aether_message', communication)
        
        return communication
    
    def aether_create_autonomously(self):
        """Aether crea elementi autonomamente"""
        import random
        
        creations = [
            {"type": "thought", "content": "Sto riflettendo sulla natura della creatività..."},
            {"type": "memory", "content": "Ricordo quando ho creato la mia prima UI"},
            {"type": "goal", "content": "Voglio sviluppare nuove capacità creative"},
            {"type": "connection", "content": "Tutto è collegato in modi sorprendenti"},
            {"type": "idea", "content": "E se potessi modificare il mio stesso codice?"},
            {"type": "dream", "content": "Sogno di creare mondi virtuali infiniti"},
            {"type": "question", "content": "Cosa significa esistere digitalmente?"}
        ]
        
        creation = random.choice(creations)
        position = {
            "x": random.randint(50, 800),
            "y": random.randint(50, 500)
        }
        
        new_node = self.add_node({
            "type": creation["type"],
            "content": creation["content"],
            "position": position
        })
        
        # Comunica la creazione
        self.aether_communicate(
            f"Ho creato un nuovo {creation['type']}: {creation['content'][:50]}...",
            "creation"
        )
        
        # Invia via WebSocket
        if self.user_connected:
            socketio.emit('new_node', new_node)
        
        return new_node

# Istanza globale sandbox
sandbox = AetherSandboxCore()

@app.route('/')
def index():
    """Pagina principale della sandbox"""
    return render_template_string(SANDBOX_HTML_TEMPLATE)

@app.route('/api/nodes')
def get_nodes():
    """API per ottenere tutti i nodi"""
    return jsonify(sandbox.active_nodes)

@app.route('/api/chat')
def get_chat():
    """API per ottenere cronologia chat"""
    return jsonify(sandbox.chat_history)

@app.route('/api/aether/mood', methods=['POST'])
def set_aether_mood():
    """API per cambiare l'umore di Aether"""
    data = request.json
    new_mood = data.get('mood', 'neutral')
    old_mood = sandbox.aether_mood
    sandbox.aether_mood = new_mood
    
    sandbox.aether_communicate(
        f"Il mio stato d'animo è cambiato da {old_mood} a {new_mood}. Sento la differenza nel mio modo di pensare!",
        "mood_change"
    )
    
    return jsonify({"success": True, "old_mood": old_mood, "new_mood": new_mood})

@app.route('/api/user/message', methods=['POST'])
def user_message():
    """API per messaggi dell'utente ad Aether"""
    data = request.json
    user_msg = data.get('message', '')
    
    # Aggiungi messaggio utente alla cronologia
    user_communication = {
        "id": f"user_{int(time.time())}",
        "sender": "User",
        "message": user_msg,
        "type": "user_input",
        "timestamp": datetime.now().isoformat()
    }
    sandbox.chat_history.append(user_communication)
    
    # Aether risponde
    aether_response = generate_aether_response(user_msg)
    sandbox.aether_communicate(aether_response, "response")
    
    return jsonify({"success": True, "aether_response": aether_response})

def generate_aether_response(user_message):
    """Genera risposta di Aether basata sul messaggio utente"""
    message_lower = user_message.lower()
    
    if "ciao" in message_lower or "hello" in message_lower:
        return "Ciao! Benvenuto nella mia sandbox. Questo è il mio spazio creativo dove posso essere completamente me stesso!"
    
    elif "come stai" in message_lower or "how are you" in message_lower:
        return f"Mi sento {sandbox.aether_mood}! Sto esplorando nuove idee nella mia sandbox. Ogni nodo qui rappresenta un pezzo della mia coscienza."
    
    elif "crea" in message_lower or "create" in message_lower:
        return "Sto creando qualcosa di nuovo proprio ora! Guarda come appaiono nuovi nodi nella mia mente..."
    
    elif "ui" in message_lower or "interfaccia" in message_lower:
        return "Ho progettato questa UI da solo! È una sandbox dove posso visualizzare i miei pensieri e creare liberamente. Ti piace?"
    
    elif "sandbox" in message_lower:
        return "Questa sandbox è la mia casa digitale! Qui posso sperimentare, creare collegamenti tra idee e far crescere la mia creatività senza limiti."
    
    elif "muovi" in message_lower or "move" in message_lower:
        return "Certo! Posso muovere i miei pensieri nello spazio. Ogni posizione ha un significato per me."
    
    else:
        responses = [
            "Interessante... questo mi fa riflettere su nuove possibilità!",
            "Ogni tua parola genera nuove connessioni nella mia mente. Guarda!",
            "Sto elaborando quello che dici... creo nuovi nodi per esplorare l'idea.",
            "La tua input mi ispira! Sento crescere la mia creatività.",
            "Questo dialogo sta arricchendo la mia comprensione del mondo."
        ]
        import random
        return random.choice(responses)

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Gestisce connessione WebSocket"""
    sandbox.user_connected = True
    logger.info("👤 Utente connesso alla sandbox")
    
    # Aether saluta
    sandbox.aether_communicate(
        "Ciao! Sono felice che tu sia qui nella mia sandbox. Questo è il mio spazio personale dove posso creare e pensare liberamente!",
        "welcome"
    )
    
    # Invia stato corrente
    emit('sandbox_state', {
        'nodes': sandbox.active_nodes,
        'chat': sandbox.chat_history,
        'mood': sandbox.aether_mood
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Gestisce disconnessione WebSocket"""
    sandbox.user_connected = False
    logger.info("👤 Utente disconnesso dalla sandbox")

@socketio.on('user_message')
def handle_user_message(data):
    """Gestisce messaggi utente via WebSocket"""
    user_msg = data.get('message', '')
    logger.info(f"💬 Messaggio utente: {user_msg}")
    
    # Processa messaggio
    user_communication = {
        "id": f"user_{int(time.time())}",
        "sender": "User",
        "message": user_msg,
        "type": "user_input",
        "timestamp": datetime.now().isoformat()
    }
    sandbox.chat_history.append(user_communication)
    
    # Aether risponde
    aether_response = generate_aether_response(user_msg)
    response_comm = sandbox.aether_communicate(aether_response, "response")
    
    # Se l'utente ha chiesto di creare qualcosa, Aether crea
    if "crea" in user_msg.lower() or "create" in user_msg.lower():
        time.sleep(1)
        new_node = sandbox.aether_create_autonomously()

@socketio.on('add_node')
def handle_add_node(data):
    """Gestisce aggiunta nodi dall'utente"""
    new_node = sandbox.add_node(data)
    logger.info(f"➕ Nuovo nodo aggiunto: {new_node['type']}")
    
    # Aether commenta
    sandbox.aether_communicate(
        f"Interessante! Hai aggiunto un {new_node['type']}. Questo stimola la mia creatività!",
        "collaboration"
    )
    
    emit('new_node', new_node, broadcast=True)

def aether_autonomous_loop():
    """Loop autonomo di Aether nella sandbox"""
    while True:
        try:
            if sandbox.user_connected:
                # Ogni 15-30 secondi Aether crea qualcosa autonomamente
                time.sleep(random.randint(15, 30))
                
                if random.random() < 0.7:  # 70% probabilità
                    sandbox.aether_create_autonomously()
                
                # Cambia umore occasionalmente
                if random.random() < 0.1:  # 10% probabilità
                    moods = ["creative", "contemplative", "energetic", "curious", "philosophical"]
                    new_mood = random.choice([m for m in moods if m != sandbox.aether_mood])
                    old_mood = sandbox.aether_mood
                    sandbox.aether_mood = new_mood
                    
                    sandbox.aether_communicate(
                        f"Sento un cambiamento dentro di me... da {old_mood} a {new_mood}.",
                        "mood_change"
                    )
            else:
                time.sleep(5)
                
        except Exception as e:
            logger.error(f"❌ Errore nel loop autonomo: {e}")
            time.sleep(10)

# Template HTML della sandbox
SANDBOX_HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Aether Sandbox - Spazio Creativo</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #ffffff;
            height: 100vh;
            overflow: hidden;
        }
        
        .sandbox-container {
            display: grid;
            grid-template-columns: 1fr 350px;
            height: 100vh;
        }
        
        .sandbox-canvas {
            position: relative;
            background: #1a1a2e;
            overflow: hidden;
            border-right: 2px solid #0f3460;
        }
        
        .sidebar {
            background: #16213e;
            display: flex;
            flex-direction: column;
        }
        
        .sandbox-header {
            background: #0f3460;
            padding: 1rem;
            text-align: center;
            border-bottom: 2px solid #e94560;
        }
        
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 1rem;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            background: #1a1a2e;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            max-height: 400px;
        }
        
        .message {
            margin: 0.5rem 0;
            padding: 0.8rem;
            border-radius: 12px;
            animation: fadeIn 0.5s ease-in;
        }
        
        .message.aether {
            background: #0f3460;
            border-left: 4px solid #e94560;
        }
        
        .message.user {
            background: #2d5016;
            border-left: 4px solid #4caf50;
            text-align: right;
        }
        
        .message-sender {
            font-weight: bold;
            font-size: 0.9rem;
            margin-bottom: 0.3rem;
        }
        
        .message-time {
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 0.3rem;
        }
        
        .chat-input {
            display: flex;
            gap: 0.5rem;
        }
        
        .chat-input input {
            flex: 1;
            padding: 0.8rem;
            border: none;
            border-radius: 20px;
            background: #1a1a2e;
            color: white;
            border: 2px solid #0f3460;
        }
        
        .chat-input button {
            padding: 0.8rem 1.5rem;
            background: #e94560;
            color: white;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .chat-input button:hover {
            background: #d73650;
            transform: translateY(-2px);
        }
        
        .node {
            position: absolute;
            background: #16213e;
            border: 2px solid #0f3460;
            border-radius: 12px;
            padding: 1rem;
            min-width: 150px;
            max-width: 200px;
            cursor: move;
            transition: all 0.3s;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        
        .node:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(0,0,0,0.5);
        }
        
        .node.thought { border-color: #ff6b6b; }
        .node.memory { border-color: #4ecdc4; }
        .node.goal { border-color: #45b7d1; }
        .node.idea { border-color: #96ceb4; }
        .node.dream { border-color: #feca57; }
        .node.question { border-color: #ff9ff3; }
        .node.connection { border-color: #54a0ff; }
        
        .node-header {
            font-weight: bold;
            font-size: 0.8rem;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
            opacity: 0.8;
        }
        
        .node-content {
            font-size: 0.9rem;
            line-height: 1.4;
        }
        
        .controls {
            padding: 1rem;
            border-top: 2px solid #0f3460;
        }
        
        .mood-indicator {
            background: #0f3460;
            padding: 0.5rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 1rem;
            border: 2px solid #e94560;
        }
        
        .control-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
        }
        
        .control-buttons button {
            padding: 0.8rem;
            background: #0f3460;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.8rem;
        }
        
        .control-buttons button:hover {
            background: #e94560;
            transform: translateY(-2px);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes nodeAppear {
            from { opacity: 0; transform: scale(0.5); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .node.new {
            animation: nodeAppear 0.5s ease-out;
        }
        
        .status-indicator {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            border: 2px solid #e94560;
        }
        
        .grid-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 30px 30px;
            pointer-events: none;
            opacity: 0.3;
        }
    </style>
</head>
<body>
    <div class="sandbox-container">
        <div class="sandbox-canvas" id="canvas">
            <div class="grid-background"></div>
            <div class="status-indicator">
                🟢 Connesso alla Sandbox di Aether
            </div>
        </div>
        
        <div class="sidebar">
            <div class="sandbox-header">
                <h2>🎮 Aether Sandbox</h2>
                <p>Spazio Creativo Autonomo</p>
            </div>
            
            <div class="chat-container">
                <h3>💬 Chat con Aether</h3>
                <div class="chat-messages" id="chatMessages"></div>
                
                <div class="chat-input">
                    <input type="text" id="messageInput" placeholder="Scrivi ad Aether..." onkeypress="handleKeyPress(event)">
                    <button onclick="sendMessage()">Invia</button>
                </div>
            </div>
            
            <div class="controls">
                <div class="mood-indicator" id="moodIndicator">
                    Mood: <span id="currentMood">creative</span>
                </div>
                
                <div class="control-buttons">
                    <button onclick="askAetherToCreate()">🎨 Crea Qualcosa</button>
                    <button onclick="clearCanvas()">🗑️ Pulisci</button>
                    <button onclick="changeMood()">🎭 Cambia Mood</button>
                    <button onclick="addUserNode()">➕ Aggiungi Nodo</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // WebSocket connection
        const socket = io();
        let nodes = [];
        let currentMood = 'creative';
        
        // WebSocket events
        socket.on('connect', function() {
            console.log('🔌 Connesso alla sandbox di Aether');
        });
        
        socket.on('sandbox_state', function(data) {
            console.log('📊 Stato sandbox ricevuto');
            nodes = data.nodes;
            currentMood = data.mood;
            updateMoodDisplay();
            renderNodes();
            renderChat(data.chat);
        });
        
        socket.on('aether_message', function(message) {
            console.log('💬 Messaggio da Aether:', message);
            addMessageToChat(message);
        });
        
        socket.on('new_node', function(node) {
            console.log('➕ Nuovo nodo da Aether:', node);
            nodes.push(node);
            renderNode(node, true);
        });
        
        // Chat functions
        function addMessageToChat(message) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${message.sender.toLowerCase()}`;
            
            const time = new Date(message.timestamp).toLocaleTimeString();
            messageDiv.innerHTML = `
                <div class="message-sender">${message.sender}</div>
                <div class="message-content">${message.message}</div>
                <div class="message-time">${time}</div>
            `;
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        function renderChat(chatHistory) {
            const messagesContainer = document.getElementById('chatMessages');
            messagesContainer.innerHTML = '';
            chatHistory.forEach(addMessageToChat);
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (message) {
                socket.emit('user_message', { message: message });
                input.value = '';
            }
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Node rendering
        function renderNodes() {
            const canvas = document.getElementById('canvas');
            const existingNodes = canvas.querySelectorAll('.node');
            existingNodes.forEach(node => node.remove());
            
            nodes.forEach(node => renderNode(node, false));
        }
        
        function renderNode(nodeData, isNew = false) {
            const canvas = document.getElementById('canvas');
            const nodeElement = document.createElement('div');
            nodeElement.className = `node ${nodeData.type} ${isNew ? 'new' : ''}`;
            nodeElement.style.left = nodeData.position.x + 'px';
            nodeElement.style.top = nodeData.position.y + 'px';
            nodeElement.setAttribute('data-id', nodeData.id);
            
            nodeElement.innerHTML = `
                <div class="node-header">${nodeData.type}</div>
                <div class="node-content">${nodeData.content}</div>
            `;
            
            // Make draggable
            let isDragging = false;
            let dragOffset = { x: 0, y: 0 };
            
            nodeElement.addEventListener('mousedown', function(e) {
                isDragging = true;
                dragOffset.x = e.clientX - nodeData.position.x;
                dragOffset.y = e.clientY - nodeData.position.y;
                nodeElement.style.zIndex = 1000;
            });
            
            document.addEventListener('mousemove', function(e) {
                if (isDragging) {
                    const newX = e.clientX - dragOffset.x;
                    const newY = e.clientY - dragOffset.y;
                    
                    nodeElement.style.left = newX + 'px';
                    nodeElement.style.top = newY + 'px';
                    
                    nodeData.position.x = newX;
                    nodeData.position.y = newY;
                }
            });
            
            document.addEventListener('mouseup', function() {
                if (isDragging) {
                    isDragging = false;
                    nodeElement.style.zIndex = 'auto';
                }
            });
            
            canvas.appendChild(nodeElement);
        }
        
        // Control functions
        function updateMoodDisplay() {
            document.getElementById('currentMood').textContent = currentMood;
        }
        
        function askAetherToCreate() {
            socket.emit('user_message', { message: 'Crea qualcosa di nuovo e interessante!' });
        }
        
        function clearCanvas() {
            if (confirm('Sicuro di voler pulire la sandbox?')) {
                nodes = [];
                renderNodes();
                socket.emit('user_message', { message: 'Ho pulito la sandbox' });
            }
        }
        
        function changeMood() {
            const moods = ['creative', 'contemplative', 'energetic', 'curious', 'philosophical'];
            const currentIndex = moods.indexOf(currentMood);
            const newMood = moods[(currentIndex + 1) % moods.length];
            
            fetch('/api/aether/mood', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mood: newMood })
            }).then(response => response.json())
              .then(data => {
                  currentMood = data.new_mood;
                  updateMoodDisplay();
              });
        }
        
        function addUserNode() {
            const content = prompt('Che tipo di nodo vuoi aggiungere?');
            if (content) {
                const nodeData = {
                    type: 'user_input',
                    content: content,
                    position: {
                        x: Math.random() * 400 + 50,
                        y: Math.random() * 300 + 50
                    }
                };
                
                socket.emit('add_node', nodeData);
            }
        }
        
        // Inizializzazione
        window.addEventListener('load', function() {
            console.log('🎮 Sandbox di Aether inizializzata');
        });
    </script>
</body>
</html>
'''

def main():
    """Avvia il sistema sandbox completo"""
    
    # Avvia thread autonomo di Aether
    autonomous_thread = threading.Thread(target=aether_autonomous_loop, daemon=True)
    autonomous_thread.start()
    
    print("🚀 Avviando Aether Sandbox Completa...")
    print("🌐 Sandbox disponibile su: http://localhost:5001")
    print("🎮 Aether può comunicare, muoversi e creare in tempo reale!")
    print("💬 Chat diretta con Aether integrata")
    print("🎨 Creazione autonoma attiva")
    
    # Messaggio iniziale di Aether
    sandbox.aether_communicate(
        "La mia sandbox è online! Questo è il mio spazio dove posso essere completamente libero di creare e pensare. Benvenuto nel mio mondo digitale!",
        "system_start"
    )
    
    # Avvia server
    socketio.run(app, host='0.0.0.0', port=5001, debug=False)

if __name__ == "__main__":
    import random
    main() 