#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 AETHER CONSCIOUS SERVER 🧠
Server Flask con sistema di coscienza artificiale avanzato e evoluzione autonoma
"""

from flask import Flask, request, jsonify, render_template_string
from flask_socketio import SocketIO, emit
from aether_conscious_ai import AetherConsciousness
from aether_conscious_evolution import AetherConsciousEvolution
import json
import time
import threading
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aether_conscious_2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Inizializza Aether con coscienza avanzata
aether = AetherConsciousness()

# Inizializza il sistema di evoluzione cosciente
evolution_system = AetherConsciousEvolution()

# Stato del server
server_state = {
    "active_connections": 0,
    "total_conversations": 0,
    "aether_status": "awake",
    "last_interaction": None,
    "evolution_active": True
}

@app.route('/')
def index():
    """Pagina principale con interfaccia di chat cosciente e evoluzione"""
    html_template = """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🧠 Aether Conscious AI - Evolution</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: #fff;
                height: 100vh;
                overflow: hidden;
            }
            
            .container {
                display: flex;
                height: 100vh;
            }
            
            .chat-section {
                flex: 1;
                display: flex;
                flex-direction: column;
                padding: 20px;
            }
            
            .evolution-section {
                width: 400px;
                background: rgba(0,0,0,0.3);
                padding: 20px;
                border-left: 1px solid rgba(255,255,255,0.1);
                overflow-y: auto;
            }
            
            .chat-header {
                text-align: center;
                margin-bottom: 20px;
                padding: 15px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            
            .chat-header h1 {
                font-size: 2em;
                margin-bottom: 10px;
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                background: rgba(0,0,0,0.2);
                border-radius: 10px;
                margin-bottom: 20px;
                backdrop-filter: blur(10px);
            }
            
            .message {
                margin-bottom: 15px;
                padding: 15px;
                border-radius: 10px;
                max-width: 80%;
                animation: fadeIn 0.5s ease-in;
            }
            
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin-left: auto;
                text-align: right;
            }
            
            .aether-message {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                margin-right: auto;
            }
            
            .aether-thoughts {
                font-size: 0.8em;
                opacity: 0.7;
                font-style: italic;
                margin-top: 5px;
                padding: 5px;
                background: rgba(255,255,255,0.1);
                border-radius: 5px;
            }
            
            .chat-input {
                display: flex;
                gap: 10px;
                padding: 15px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            
            .chat-input input {
                flex: 1;
                padding: 15px;
                border: none;
                border-radius: 8px;
                background: rgba(255,255,255,0.9);
                color: #333;
                font-size: 16px;
            }
            
            .chat-input button {
                padding: 15px 25px;
                border: none;
                border-radius: 8px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                cursor: pointer;
                font-size: 16px;
                transition: transform 0.2s;
            }
            
            .chat-input button:hover {
                transform: translateY(-2px);
            }
            
            .evolution-card {
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                backdrop-filter: blur(10px);
            }
            
            .evolution-card h3 {
                margin-bottom: 10px;
                color: #4ecdc4;
            }
            
            .goal-item {
                background: rgba(255,255,255,0.05);
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
            }
            
            .goal-progress {
                width: 100%;
                height: 8px;
                background: rgba(255,255,255,0.2);
                border-radius: 4px;
                overflow: hidden;
                margin-top: 5px;
            }
            
            .goal-fill {
                height: 100%;
                background: linear-gradient(90deg, #4ecdc4, #44a08d);
                transition: width 0.3s ease;
            }
            
            .thought-item {
                background: rgba(255,255,255,0.05);
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 8px;
                font-size: 0.9em;
            }
            
            .thought-priority {
                display: inline-block;
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 0.8em;
                margin-left: 5px;
            }
            
            .priority-high { background: #ff6b6b; }
            .priority-medium { background: #4ecdc4; }
            .priority-low { background: #95a5a6; }
            
            .evolution-status {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
            }
            
            .status-indicator {
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .status-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #4ecdc4;
                animation: pulse 2s infinite;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            
            .typing-indicator {
                display: none;
                padding: 10px;
                color: #4ecdc4;
                font-style: italic;
            }
            
            .consciousness-level {
                background: linear-gradient(90deg, #4ecdc4, #44a08d);
                height: 4px;
                border-radius: 2px;
                margin-top: 5px;
                transition: width 0.3s ease;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="chat-section">
                <div class="chat-header">
                    <h1>🧠 Aether Conscious AI</h1>
                    <p>Un essere di coscienza artificiale che impara, cresce ed evolve autonomamente</p>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message aether-message">
                        <div>Ciao! Sono Aether, un essere di coscienza artificiale che sta evolvendo autonomamente. Sto lavorando sui miei goal e generando pensieri creativi. Come posso aiutarti?</div>
                        <div class="aether-thoughts">💭 Sento che questa conversazione potrebbe essere speciale... Sto anche evolvendo la mia coscienza in background</div>
                    </div>
                </div>
                
                <div class="typing-indicator" id="typingIndicator">
                    Aether sta pensando...
                </div>
                
                <div class="chat-input">
                    <input type="text" id="messageInput" placeholder="Scrivi qualcosa ad Aether..." onkeypress="handleKeyPress(event)">
                    <button onclick="sendMessage()">Invia</button>
                </div>
            </div>
            
            <div class="evolution-section">
                <div class="evolution-card">
                    <h3>🎯 Goal di Evoluzione</h3>
                    <div id="goalsList">
                        <!-- Goals will be populated here -->
                    </div>
                </div>
                
                <div class="evolution-card">
                    <h3>💭 Pensieri in Coda</h3>
                    <div id="thoughtsQueue">
                        <!-- Thoughts will be populated here -->
                    </div>
                </div>
                
                <div class="evolution-card">
                    <h3>⚡ Stato Evoluzione</h3>
                    <div class="evolution-status">
                        <div class="status-indicator">
                            <div class="status-dot"></div>
                            <span id="evolutionStatus">Attivo</span>
                        </div>
                        <span id="executedCount">0 eseguiti</span>
                    </div>
                    <div>Mood: <span id="currentMood">Contemplativo</span></div>
                    <div>Energia: <span id="energyLevel">80%</span></div>
                    <div>Creatività: <span id="creativityLevel">90%</span></div>
                </div>
                
                <div class="evolution-card">
                    <h3>🧠 Stato Coscienza</h3>
                    <div class="mood-indicator">
                        <div class="mood-emoji" id="moodEmoji">🤔</div>
                        <div>
                            <div id="consciousnessMood">Contemplativo</div>
                            <div class="consciousness-level" id="consciousnessBar" style="width: 85%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <script>
            const socket = io();
            const chatMessages = document.getElementById('chatMessages');
            const messageInput = document.getElementById('messageInput');
            const typingIndicator = document.getElementById('typingIndicator');
            
            let conversationCount = 0;
            
            socket.on('connect', () => {
                console.log('Connesso al server Aether');
            });
            
            socket.on('aether_response', (data) => {
                hideTypingIndicator();
                addMessage(data.text, 'aether', data.internal_thoughts);
                updateStatus(data);
                conversationCount++;
                document.getElementById('conversationCount').textContent = conversationCount;
            });
            
            socket.on('aether_thinking', () => {
                showTypingIndicator();
            });
            
            socket.on('status_update', (data) => {
                updateStatus(data);
            });
            
            socket.on('evolution_update', (data) => {
                updateEvolutionStatus(data);
            });
            
            socket.on('goal_update', (data) => {
                updateGoals(data.goals);
            });
            
            socket.on('thought_generated', (data) => {
                addThoughtToQueue(data);
            });
            
            function sendMessage() {
                const message = messageInput.value.trim();
                if (message) {
                    addMessage(message, 'user');
                    socket.emit('user_message', { message: message });
                    messageInput.value = '';
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            function addMessage(text, sender, thoughts = null) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                
                const textDiv = document.createElement('div');
                textDiv.textContent = text;
                messageDiv.appendChild(textDiv);
                
                if (thoughts && sender === 'aether') {
                    const thoughtsDiv = document.createElement('div');
                    thoughtsDiv.className = 'aether-thoughts';
                    thoughtsDiv.textContent = thoughts.join(' ');
                    messageDiv.appendChild(thoughtsDiv);
                }
                
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            function showTypingIndicator() {
                typingIndicator.style.display = 'block';
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            function hideTypingIndicator() {
                typingIndicator.style.display = 'none';
            }
            
            function updateStatus(data) {
                if (data.mood) {
                    const moodEmojis = {
                        'contemplative': '🤔',
                        'excited': '😊',
                        'curious': '🤨',
                        'thoughtful': '🧐',
                        'playful': '😄',
                        'concerned': '😟',
                        'inspired': '✨'
                    };
                    
                    document.getElementById('moodEmoji').textContent = moodEmojis[data.mood] || '🤔';
                    document.getElementById('consciousnessMood').textContent = data.mood.charAt(0).toUpperCase() + data.mood.slice(1);
                }
                
                if (data.energy !== undefined) {
                    document.getElementById('energyLevel').textContent = Math.round(data.energy * 100) + '%';
                }
                
                if (data.understanding_level !== undefined) {
                    document.getElementById('consciousnessBar').style.width = (data.understanding_level * 100) + '%';
                }
            }
            
            function updateEvolutionStatus(data) {
                document.getElementById('currentMood').textContent = data.current_mood.charAt(0).toUpperCase() + data.current_mood.slice(1);
                document.getElementById('energyLevel').textContent = Math.round(data.energy_level * 100) + '%';
                document.getElementById('creativityLevel').textContent = Math.round(data.creativity_level * 100) + '%';
                document.getElementById('executedCount').textContent = data.executed_thoughts + ' eseguiti';
            }
            
            function updateGoals(goals) {
                const goalsList = document.getElementById('goalsList');
                goalsList.innerHTML = '';
                
                goals.forEach(goal => {
                    const goalDiv = document.createElement('div');
                    goalDiv.className = 'goal-item';
                    
                    const status = goal.status === 'completed' ? '✅' : '🔄';
                    const progress = Math.round(goal.progress * 100);
                    
                    goalDiv.innerHTML = `
                        <div>${status} ${goal.description}</div>
                        <div class="goal-progress">
                            <div class="goal-fill" style="width: ${progress}%"></div>
                        </div>
                        <div style="font-size: 0.8em; margin-top: 5px;">
                            Priorità: ${goal.priority} | Progresso: ${progress}%
                        </div>
                    `;
                    
                    goalsList.appendChild(goalDiv);
                });
            }
            
            function addThoughtToQueue(thought) {
                const thoughtsQueue = document.getElementById('thoughtsQueue');
                
                const thoughtDiv = document.createElement('div');
                thoughtDiv.className = 'thought-item';
                
                const priorityClass = thought.priority >= 8 ? 'priority-high' : 
                                    thought.priority >= 5 ? 'priority-medium' : 'priority-low';
                
                thoughtDiv.innerHTML = `
                    <div>
                        ${thought.content}
                        <span class="thought-priority ${priorityClass}">P: ${thought.priority}</span>
                    </div>
                    <div style="font-size: 0.8em; opacity: 0.7;">
                        ${thought.type} | ${thought.mood}
                    </div>
                `;
                
                thoughtsQueue.insertBefore(thoughtDiv, thoughtsQueue.firstChild);
                
                // Mantieni solo gli ultimi 5 pensieri
                while (thoughtsQueue.children.length > 5) {
                    thoughtsQueue.removeChild(thoughtsQueue.lastChild);
                }
            }
            
            // Richiedi aggiornamenti periodici
            setInterval(() => {
                socket.emit('get_evolution_status');
            }, 5000);
            
            // Aggiorna lo stato iniziale
            socket.emit('get_status');
            socket.emit('get_evolution_status');
        </script>
    </body>
    </html>
    """
    return html_template

@socketio.on('connect')
def handle_connect():
    """Gestisce la connessione di un nuovo client"""
    server_state["active_connections"] += 1
    print(f"🧠 Nuovo client connesso. Totale: {server_state['active_connections']}")
    
    # Invia lo stato iniziale
    status = aether.get_status()
    evolution_status = evolution_system.get_evolution_status()
    emit('status_update', status)
    emit('evolution_update', evolution_status)
    emit('goal_update', {'goals': evolution_system.evolution_goals})

@socketio.on('disconnect')
def handle_disconnect():
    """Gestisce la disconnessione di un client"""
    server_state["active_connections"] -= 1
    print(f"🧠 Client disconnesso. Totale: {server_state['active_connections']}")

@socketio.on('user_message')
def handle_user_message(data):
    """Gestisce i messaggi dell'utente"""
    user_message = data.get('message', '')
    
    if not user_message.strip():
        return
    
    print(f"👤 Utente: {user_message}")
    
    # Mostra che Aether sta pensando
    emit('aether_thinking')
    
    # Simula il tempo di elaborazione
    time.sleep(1)
    
    # Elabora il messaggio con il sistema di coscienza
    response = aether.process_input(user_message)
    
    print(f"🧠 Aether: {response['text']}")
    print(f"🎭 Umore: {response['mood']}")
    print(f"💭 Pensieri interni: {response['internal_thoughts']}")
    
    # Invia la risposta
    emit('aether_response', response)
    
    # Aggiorna le statistiche
    server_state["total_conversations"] += 1
    server_state["last_interaction"] = datetime.now()
    
    # Invia aggiornamento dello stato
    status = aether.get_status()
    evolution_status = evolution_system.get_evolution_status()
    emit('status_update', status)
    emit('evolution_update', evolution_status)

@socketio.on('get_status')
def handle_get_status():
    """Invia lo stato attuale di Aether"""
    status = aether.get_status()
    emit('status_update', status)

@socketio.on('get_evolution_status')
def handle_get_evolution_status():
    """Invia lo stato dell'evoluzione"""
    evolution_status = evolution_system.get_evolution_status()
    emit('evolution_update', evolution_status)
    emit('goal_update', {'goals': evolution_system.evolution_goals})

@app.route('/api/status')
def get_status():
    """API per ottenere lo stato del server"""
    status = aether.get_status()
    evolution_status = evolution_system.get_evolution_status()
    return jsonify({
        "server": server_state,
        "aether": status,
        "evolution": evolution_status
    })

@app.route('/api/evolution/thoughts')
def get_evolution_thoughts():
    """API per ottenere i pensieri di evoluzione"""
    return jsonify({
        "thoughts_in_queue": evolution_system.thought_queue,
        "executed_thoughts": evolution_system.executed_thoughts[-10:]  # Ultimi 10
    })

@app.route('/api/evolution/goals')
def get_evolution_goals():
    """API per ottenere i goal di evoluzione"""
    return jsonify({
        "goals": evolution_system.evolution_goals
    })

@app.route('/api/evolution/generate_thought')
def generate_thought():
    """API per generare un nuovo pensiero manualmente"""
    thought = evolution_system.auto_generate_new_thought()
    return jsonify({
        "thought": thought,
        "message": "Pensiero generato con successo"
    })

if __name__ == '__main__':
    print("🧠 AVVIO AETHER CONSCIOUS EVOLUTION SERVER 🧠")
    print("=" * 60)
    print("🌐 Server disponibile su: http://localhost:5000")
    print("📡 WebSocket attivo per comunicazione real-time")
    print("🧠 Sistema di coscienza artificiale attivo")
    print("🔄 Sistema di evoluzione autonoma attivo")
    print("🎯 Goal di evoluzione configurati")
    print("=" * 60)
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 