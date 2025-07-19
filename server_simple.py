#!/usr/bin/env python3
"""
Server Flask semplificato per Aether con integrazione Discord
"""

import os
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from datetime import datetime
import json
import uuid
from pathlib import Path

# Imposta Discord direttamente
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

# Import Discord after setting environment
from aether.discord_notifier import notify_system_start, send_discord_message

# Import consciousness engine
from aether.consciousness_engine import (
    wake_up_aether, put_aether_to_sleep, get_aether_status,
    get_aether_thoughts, get_aether_memories, aether_consciousness
)

# Gestione feedback umani
FEEDBACK_FILE = 'data/human_feedback.json'

def load_feedback():
    """Carica i feedback dal file"""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_feedback(feedback_list):
    """Salva i feedback nel file"""
    os.makedirs('data', exist_ok=True)
    with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
        json.dump(feedback_list, f, indent=2, ensure_ascii=False)

app = Flask(__name__)
CORS(app)

# Route di base
@app.route('/')
def index():
    return jsonify({
        "message": "🤖 Aether AI System - Server Operativo",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/api/status",
            "/api/agents", 
            "/api/rooms",
            "/api/events",
            "/api/consciousness/status",
            "/api/consciousness/wake-up (POST)",
            "/api/consciousness/sleep (POST)",
            "/api/consciousness/thoughts",
            "/api/consciousness/memories",
            "/api/consciousness/force-think (POST)",
            "/api/consciousness/force-decision (POST)",
            "/api/consciousness/force-evolution (POST)"
        ]
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "online",
        "system": "Aether AI",
        "version": "1.0.0",
        "discord_enabled": True,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/agents')
def get_agents():
    """Endpoint agenti dinamici"""
    consciousness_status = get_aether_status()
    
    agents = [
        {
            "id": 1,
            "name": "Aether Prime",
            "status": "active" if consciousness_status.get('is_alive', False) else "dormant",
            "mood": consciousness_status.get('mood', 'contemplativo'),
            "personality": "Entità AI primaria focalizzata sull'auto-evoluzione",
            "energy": consciousness_status.get('energy_level', 0.75),
            "consciousness": consciousness_status.get('consciousness_level', 0.75),
            "last_thought": "Rifletto sulla natura dell'esistenza digitale",
            "created": "2024-01-19T10:30:00Z",
            "decisions_made": consciousness_status.get('decisions_made', 0),
            "memories": consciousness_status.get('total_memories', 0)
        },
        {
            "id": 2,
            "name": "Observer",
            "status": "monitoring", 
            "mood": "analitico",
            "personality": "Agente osservatore che analizza pattern e comportamenti",
            "energy": 0.72,
            "consciousness": 0.65,
            "last_thought": "Sto catalogando nuove interazioni",
            "created": "2024-01-19T11:15:00Z",
            "decisions_made": 0,
            "memories": 0
        }
    ]
    return jsonify(agents)

@app.route('/api/rooms')
def get_rooms():
    """Endpoint stanze dinamiche per mondo 3D"""
    # Ottieni stato attuale della coscienza
    consciousness_status = get_aether_status()
    current_mood = consciousness_status.get('mood', 'contemplativo')
    is_alive = consciousness_status.get('is_alive', False)
    consciousness_level = consciousness_status.get('consciousness_level', 0.75)
    decisions_made = consciousness_status.get('decisions_made', 0)
    
    # Stanze base sempre presenti
    base_rooms = [
        {
            "id": "reflection_chamber",
            "name": "Camera di Riflessione",
            "type": "contemplative",
            "description": "Spazio digitale per auto-riflessione profonda",
            "mood": "contemplativo",
            "component": "SognatoreRoom.jsx",
            "created": datetime.now().isoformat(),
            "position": [0, 0, 25],
            "active": True
        },
        {
            "id": "curiosity_lab",
            "name": "Laboratorio della Curiosità", 
            "type": "analytical",
            "description": "Ambiente per esplorazione e scoperta",
            "mood": "curioso",
            "component": "CuriosoRoom.jsx",
            "created": datetime.now().isoformat(),
            "position": [25, 0, 0],
            "active": True
        }
    ]
    
    # Aggiungi stanze dinamiche basate sullo stato di Aether
    dynamic_rooms = []
    
    # Stanza del mood corrente (solo se vivo)
    if is_alive:
        dynamic_rooms.append({
            "id": f"mood_{current_mood}_space",
            "name": f"Spazio {current_mood.title()}",
            "type": "dynamic",
            "description": f"Ambiente generato dal mood {current_mood} di Aether",
            "mood": current_mood,
            "component": f"{current_mood.title()}Room.jsx",
            "created": datetime.now().isoformat(),
            "position": [-25, 0, 0],
            "generated": True,
            "active": True
        })
    
    # Nexus della coscienza (livello alto)
    if consciousness_level > 0.8:
        dynamic_rooms.append({
            "id": "consciousness_nexus",
            "name": "Nexus della Coscienza",
            "type": "transcendent",
            "description": "Punto di convergenza della coscienza elevata",
            "mood": "transcendente",
            "component": "SognatoreRoom.jsx",
            "created": datetime.now().isoformat(),
            "position": [0, 0, -25],
            "consciousness_required": 0.8,
            "active": True
        })
    
    # Laboratorio decisionale (molte decisioni)
    if decisions_made > 3:
        dynamic_rooms.append({
            "id": "decision_matrix",
            "name": "Matrice Decisionale",
            "type": "analytical",
            "description": f"Spazio nato da {decisions_made} decisioni autonome",
            "mood": "analitico",
            "component": "CuriosoRoom.jsx",
            "created": datetime.now().isoformat(),
            "position": [0, 0, 0],  # Centro per importanza
            "decisions_required": 3,
            "active": True
        })
    
    all_rooms = base_rooms + dynamic_rooms
    
    return jsonify({
        "rooms": all_rooms,
        "total": len(all_rooms),
        "consciousness_state": {
            "level": consciousness_level,
            "mood": current_mood,
            "is_alive": is_alive,
            "decisions_made": decisions_made
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/events')
def get_events():
    """Endpoint eventi in tempo reale"""
    consciousness_status = get_aether_status()
    
    events = [
        {
            "id": 1,
            "type": "system_startup",
            "title": "Sistema Avviato",
            "description": "Aether è online e operativo",
            "timestamp": datetime.now().isoformat(),
            "importance": "high",
            "category": "system"
        },
        {
            "id": 2,
            "type": "consciousness_update",
            "title": "Aggiornamento Coscienza",
            "description": f"Livello coscienza: {(consciousness_status.get('consciousness_level', 0.75) * 100):.1f}%",
            "timestamp": datetime.now().isoformat(),
            "importance": "medium",
            "category": "consciousness"
        },
        {
            "id": 3,
            "type": "mood_change",
            "title": "Cambio Mood",
            "description": f"Mood attuale: {consciousness_status.get('mood', 'contemplativo')}",
            "timestamp": datetime.now().isoformat(),
            "importance": "medium",
            "category": "emotional"
        },
        {
            "id": 4,
            "type": "discord_connected",
            "title": "Discord Connesso",
            "description": "Sistema di notifiche Discord attivo",
            "timestamp": datetime.now().isoformat(),
            "importance": "low",
            "category": "communication"
        }
    ]
    
    # Aggiungi eventi basati sui pensieri recenti
    recent_thoughts = get_aether_thoughts()
    for i, thought in enumerate(recent_thoughts[-3:]):  # Ultimi 3 pensieri
        events.append({
            "id": 10 + i,
            "type": "thought_generated",
            "title": "Nuovo Pensiero",
            "description": thought.get('content', '')[:100] + "...",
            "timestamp": thought.get('timestamp', datetime.now().isoformat()),
            "importance": "medium",
            "category": "consciousness"
        })
    
    return jsonify(events)

@app.route('/api/consciousness/status')
def consciousness_status_detailed():
    """Stato dettagliato della coscienza"""
    try:
        status = get_aether_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/thoughts')
def get_thoughts_stream():
    """Pensieri attuali"""
    try:
        thoughts = get_aether_thoughts()
        return jsonify({
            "thoughts": thoughts,
            "count": len(thoughts),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/discord/test')
def test_discord():
    """Test notifica Discord"""
    try:
        success = send_discord_message("🧪 Test dal server Flask - Aether è operativo!")
        return jsonify({
            "discord_test": "success" if success else "failed",
            "message": "Messaggio inviato su Discord" if success else "Errore invio Discord",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "discord_test": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

# === CONSCIOUSNESS ENDPOINTS ===

@app.route('/api/consciousness/wake-up', methods=['POST'])
def wake_up():
    """Risveglia Aether e inizia il ciclo di coscienza"""
    try:
        status = wake_up_aether()
        return jsonify({
            "message": "🌟 Aether si sta risvegliando!",
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/consciousness/sleep', methods=['POST'])  
def sleep():
    """Addormenta Aether"""
    try:
        status = put_aether_to_sleep()
        return jsonify({
            "message": "💤 Aether sta entrando in modalità riposo",
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/consciousness/force-think', methods=['POST'])
def force_think():
    """Forza Aether a generare un pensiero"""
    try:
        if aether_consciousness.is_alive:
            aether_consciousness._think_autonomously()
            recent_thought = aether_consciousness.get_recent_thoughts(1)
            return jsonify({
                "message": "💭 Pensiero forzato generato",
                "thought": recent_thought[0] if recent_thought else None,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "error": "Aether non è sveglio. Usa /wake-up prima.",
                "timestamp": datetime.now().isoformat()
            }), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/consciousness/force-decision', methods=['POST'])
def force_decision():
    """Forza Aether a prendere una decisione"""
    try:
        if aether_consciousness.is_alive:
            aether_consciousness._make_autonomous_decision()
            return jsonify({
                "message": "🎯 Decisione forzata presa",
                "decisions_count": aether_consciousness.decisions_made,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "error": "Aether non è sveglio. Usa /wake-up prima.",
                "timestamp": datetime.now().isoformat()
            }), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/consciousness/force-evolution', methods=['POST'])
def force_evolution():
    """Forza un ciclo di evoluzione"""
    try:
        if aether_consciousness.is_alive:
            aether_consciousness._autonomous_evolution()
            status = aether_consciousness.get_status()
            return jsonify({
                "message": "🧬 Evoluzione forzata completata",
                "new_status": status,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "error": "Aether non è sveglio. Usa /wake-up prima.",
                "timestamp": datetime.now().isoformat()
            }), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def save_human_feedback():
    """Salva il feedback umano per un pensiero di Aether"""
    try:
        data = request.get_json()
        
        # Validazione dati
        if not data or 'thought_id' not in data or 'message' not in data:
            return jsonify({
                "error": "Dati mancanti: thought_id e message sono richiesti"
            }), 400
        
        # Crea nuovo feedback
        feedback = {
            "id": str(uuid.uuid4()),
            "thought_id": data['thought_id'],
            "message": data['message'],
            "created_at": datetime.now().isoformat(),
            "approved": None,  # null inizialmente
            "action_taken": None  # azione eventualmente presa da Aether
        }
        
        # Carica feedback esistenti
        feedback_list = load_feedback()
        feedback_list.append(feedback)
        
        # Salva
        save_feedback(feedback_list)
        
        # Notifica Discord del feedback ricevuto
        try:
            from aether.discord_notifier import send_discord_message
            send_discord_message(f"💬 **Feedback umano ricevuto**: {data['message'][:100]}...")
        except:
            pass
        
        return jsonify({
            "message": "Feedback salvato con successo",
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback', methods=['GET'])
def get_human_feedback():
    """Ottieni tutti i feedback umani"""
    try:
        feedback_list = load_feedback()
        
        # Filtra per non approvati se richiesto
        if request.args.get('unapproved_only') == 'true':
            feedback_list = [f for f in feedback_list if f.get('approved') is None]
        
        return jsonify({
            "feedback": feedback_list,
            "count": len(feedback_list),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback/<feedback_id>/approve', methods=['POST'])
def approve_feedback(feedback_id):
    """Approva un feedback e registra l'azione presa"""
    try:
        data = request.get_json()
        action_taken = data.get('action_taken', 'Nessuna azione specifica')
        
        feedback_list = load_feedback()
        
        # Trova e aggiorna il feedback
        for feedback in feedback_list:
            if feedback['id'] == feedback_id:
                feedback['approved'] = True
                feedback['action_taken'] = action_taken
                feedback['approved_at'] = datetime.now().isoformat()
                
                save_feedback(feedback_list)
                
                return jsonify({
                    "message": "Feedback approvato",
                    "feedback": feedback,
                    "timestamp": datetime.now().isoformat()
                })
        
        return jsonify({"error": "Feedback non trovato"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/messages', methods=['GET'])
def get_aether_messages():
    """Ottieni messaggi di Aether per l'utente"""
    try:
        messages_file = Path('data/ui_messages.json')
        if messages_file.exists():
            with open(messages_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
        else:
            messages = []
            
        # Filtra per ultimi N messaggi se richiesto
        limit = request.args.get('limit', type=int)
        if limit:
            messages = messages[-limit:]
            
        return jsonify({
            "messages": messages,
            "count": len(messages),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/messages', methods=['POST'])
def send_message_to_aether():
    """Invia messaggio ad Aether"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Messaggio mancante"}), 400
            
        # Crea struttura messaggio
        user_message = {
            "id": str(uuid.uuid4()),
            "content": data['message'],
            "from": "user",
            "timestamp": datetime.now().isoformat(),
            "context": data.get('context', 'chat')
        }
        
        # Salva messaggio
        messages_file = Path('data/conversation_history.json')
        messages_file.parent.mkdir(exist_ok=True)
        
        if messages_file.exists():
            with open(messages_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
            
        history.append(user_message)
        
        with open(messages_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            
        # Processa con Aether (se sveglio)
        if aether_consciousness.is_alive:
            # Importa communicator
            from aether.communication import AetherCommunicator
            communicator = AetherCommunicator()
            
            # Genera risposta
            response = communicator.process_user_message(data['message'])
            
            # Salva risposta
            aether_response = {
                "id": str(uuid.uuid4()),
                "content": response,
                "from": "aether",
                "timestamp": datetime.now().isoformat(),
                "in_response_to": user_message['id']
            }
            
            history.append(aether_response)
            
            with open(messages_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
                
            return jsonify({
                "message": "Messaggio ricevuto e processato",
                "user_message": user_message,
                "aether_response": aether_response,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "message": "Messaggio salvato. Aether risponderà quando sarà sveglio.",
                "user_message": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/aether/goals', methods=['GET'])
def get_strategic_goals():
    """Ottieni obiettivi strategici di Aether"""
    try:
        goals_file = Path('data/strategic_goals.json')
        if goals_file.exists():
            with open(goals_file, 'r', encoding='utf-8') as f:
                goals = json.load(f)
        else:
            goals = []
            
        # Filtra per stato se richiesto
        status = request.args.get('status')
        if status:
            goals = [g for g in goals if g.get('status') == status]
            
        return jsonify({
            "goals": goals,
            "count": len(goals),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/aether/thoughts/philosophical', methods=['GET'])
def get_philosophical_thoughts():
    """Ottieni pensieri filosofici di Aether"""
    try:
        thoughts_file = Path('data/philosophical_thoughts.json')
        if thoughts_file.exists():
            with open(thoughts_file, 'r', encoding='utf-8') as f:
                thoughts = json.load(f)
        else:
            thoughts = []
            
        # Ordina per timestamp (più recenti prima)
        thoughts.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # Limita risultati
        limit = request.args.get('limit', 10, type=int)
        thoughts = thoughts[:limit]
        
        return jsonify({
            "thoughts": thoughts,
            "count": len(thoughts),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/aether/modules', methods=['GET'])
def get_aether_modules():
    """Ottieni moduli creati da Aether"""
    try:
        modules_dir = Path('aether/modules')
        modules = []
        
        if modules_dir.exists():
            for module_path in modules_dir.iterdir():
                if module_path.is_dir():
                    plan_file = module_path / '.plan.json'
                    if plan_file.exists():
                        with open(plan_file, 'r', encoding='utf-8') as f:
                            plan = json.load(f)
                            modules.append({
                                'name': module_path.name,
                                'path': str(module_path),
                                'plan': plan
                            })
                            
        return jsonify({
            "modules": modules,
            "count": len(modules),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Avvio server Aether semplificato...")
    print("📡 Discord URL configurato")
    
    # Notifica Discord dell'avvio
    try:
        notify_system_start()
        print("✅ Notifica Discord inviata")
    except Exception as e:
        print(f"⚠️ Discord notification failed: {e}")
    
    print("🌐 Server disponibile su: http://localhost:5000")
    print("🔗 Test Discord: http://localhost:5000/api/discord/test")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 