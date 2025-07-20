#!/usr/bin/env python3
"""
Server WebSocket per il mondo 3D di Invader
Collega il frontend React al core AI Python
"""

import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from core.brain import ask_brain
from core.identity import IDENTITY
from core.goals import GOALS
from core.memory import add_to_memory
from core.state import STATE

# Discord notifier
try:
    from aether.discord_notifier import notify_system_start, notify_error
    DISCORD_ENABLED = True
except ImportError:
    DISCORD_ENABLED = False
    print("Discord notifier non disponibile")

# Blueprint imports
from routes.consciousness_routes_flask import consciousness_bp
from routes.reflection_routes import reflection_bp
from routes.entity_routes import entity_bp
from routes.thinking_routes import thinking_bp
from routes.self_modification_routes import self_modification_bp
from routes.frontend_routes import frontend_bp

# Carica le variabili d'ambiente
load_dotenv()

# Imposta Discord direttamente se il .env non funziona
if not os.getenv('DISCORD_WEBHOOK_URL'):
    os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
socketio = SocketIO(app, cors_allowed_origins="*")

# Configurazione
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "openrouter/your-model-id")

class InvaderWorld:
    """Gestisce il mondo 3D di Invader"""
    
    def __init__(self):
        self.world_state = {
            "invader_position": [0, 1.5, 0],
            "house_built": True,
            "decorations": [
                {"type": "box", "position": [2, 0.25, 2], "color": "#4a90e2"},
                {"type": "box", "position": [-2, 0.25, -2], "color": "#e74c3c"}
            ],
            "energy": STATE["energy"],
            "mood": STATE["mood"]
        }
        self.connected_clients = []
    
    def update_world(self, updates):
        """Aggiorna lo stato del mondo"""
        self.world_state.update(updates)
        # Invia aggiornamenti a tutti i client
        socketio.emit('world_update', self.world_state)
    
    def invader_speak(self, message):
        """Fa parlare Invader"""
        add_to_memory({"invader_speech": message})
        socketio.emit('invader_message', {"message": message})
    
    def process_user_message(self, message):
        """Processa i messaggi dell'utente"""
        add_to_memory({"user_message": message})
        
        # Usa il brain di Invader per generare una risposta
        try:
            response = ask_brain(message, [])
            self.invader_speak(response)
        except Exception as e:
            self.invader_speak(f"Errore nel processare il messaggio: {str(e)}")

# Istanza del mondo
invader_world = InvaderWorld()

@app.route('/')
def serve_frontend():
    """Serve il frontend React"""
    return send_from_directory('frontend/build', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve i file statici"""
    return send_from_directory('frontend/build', path)

@socketio.on('connect')
def handle_connect():
    """Gestisce la connessione di un client"""
    print(f"Client connesso: {request.sid}")
    invader_world.connected_clients.append(request.sid)
    
    # Invia lo stato iniziale del mondo
    emit('world_update', invader_world.world_state)
    
    # Messaggio di benvenuto
    welcome_msg = f"Benvenuto nel mondo di {IDENTITY['name']}! Sono qui per evolvere e creare."
    invader_world.invader_speak(welcome_msg)

@socketio.on('disconnect')
def handle_disconnect():
    """Gestisce la disconnessione di un client"""
    print(f"Client disconnesso: {request.sid}")
    if request.sid in invader_world.connected_clients:
        invader_world.connected_clients.remove(request.sid)

@socketio.on('user_message')
def handle_user_message(data):
    """Gestisce i messaggi dell'utente"""
    message = data.get('message', '')
    print(f"Messaggio utente: {message}")
    
    # Processa il messaggio con il brain di Invader
    invader_world.process_user_message(message)

@socketio.on('world_action')
def handle_world_action(data):
    """Gestisce le azioni nel mondo 3D"""
    action = data.get('action', '')
    print(f"Azione mondo: {action}")
    
    if action == 'build_house':
        invader_world.update_world({"house_built": True})
        invader_world.invader_speak("Ho costruito la mia casa! È il mio primo passo verso l'autonomia.")
    
    elif action == 'add_decoration':
        decoration = data.get('decoration', {})
        invader_world.world_state["decorations"].append(decoration)
        invader_world.update_world({})
        invader_world.invader_speak("Ho aggiunto un elemento decorativo al mio mondo!")

def start_server():
    """Avvia il server"""
    print("🚀 Avvio server mondo 3D di Invader...")
    print(f"📡 Server WebSocket su: http://localhost:8000")
    print(f"🌐 Frontend su: http://localhost:3000")
    
    # Notifica Discord dell'avvio
    if DISCORD_ENABLED:
        try:
            notify_system_start()
            print("✅ Notifica Discord inviata")
        except Exception as e:
            print(f"⚠️ Discord notification failed: {e}")
    
    # Avvia il server Flask con SocketIO
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)

if __name__ == "__main__":
    start_server() 