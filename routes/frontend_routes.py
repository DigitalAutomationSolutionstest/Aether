# routes/frontend_routes.py - API routes per il frontend dinamico

import os
import json
import glob
import importlib.util
from datetime import datetime
from typing import Dict, List, Any
from flask import Blueprint, jsonify, request, send_file
from pathlib import Path

# Import Aether components
try:
    from aether.memory import AetherMemory
    from aether.agent_manager import AetherAgentManager
    from core.memory import get_memory_instance
except ImportError as e:
    print(f"Warning: Could not import Aether components: {e}")
    AetherMemory = None
    AetherAgentManager = None
    get_memory_instance = None

frontend_bp = Blueprint('frontend', __name__)

# Inizializza componenti
memory_instance = None
agent_manager = None

def init_components():
    """Inizializza i componenti Aether se disponibili"""
    global memory_instance, agent_manager
    
    try:
        if get_memory_instance:
            memory_instance = get_memory_instance()
        
        if AetherAgentManager:
            agent_manager = AetherAgentManager()
    except Exception as e:
        print(f"Warning: Could not initialize components: {e}")

# Inizializza all'avvio
init_components()

@frontend_bp.route('/api/rooms', methods=['GET'])
def get_rooms():
    """Restituisce la lista dei componenti stanza disponibili"""
    try:
        rooms = []
        
        # Cerca file JSX nelle cartelle frontend
        jsx_patterns = [
            'frontend/src/components/*Room.jsx',
            'aether-frontend/src/components/*Room.jsx',
            'frontend/src/components/*Scene.jsx',
            'aether-frontend/src/components/*Scene.jsx'
        ]
        
        for pattern in jsx_patterns:
            for file_path in glob.glob(pattern):
                room_name = Path(file_path).stem
                
                # Estrai metadati dal file se presente
                metadata = extract_component_metadata(file_path)
                
                rooms.append({
                    'name': room_name,
                    'path': file_path,
                    'created': os.path.getctime(file_path),
                    'modified': os.path.getmtime(file_path),
                    'size': os.path.getsize(file_path),
                    'mood': metadata.get('mood', 'neutral'),
                    'description': metadata.get('description', f'Stanza {room_name} generata da Aether'),
                    'type': 'room'
                })
        
        # Ordina per data di creazione (più recenti prima)
        rooms.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'rooms': rooms,
            'total': len(rooms),
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'rooms': []
        }), 500

@frontend_bp.route('/api/agents', methods=['GET'])
def get_agents():
    """Restituisce la lista degli agenti attivi"""
    try:
        agents_detail = {}
        
        if agent_manager:
            # Usa l'agent manager per ottenere info dettagliate
            agents_detail = agent_manager.get_agents_status()
        else:
            # Fallback: cerca agenti nei file
            agent_files = glob.glob('aether/agents/*.py')
            for agent_file in agent_files:
                if not agent_file.endswith('__init__.py'):
                    agent_name = Path(agent_file).stem
                    
                    # Estrai metadati dall'agente
                    metadata = extract_agent_metadata(agent_file)
                    
                    agents_detail[agent_name] = {
                        'name': agent_name,
                        'file': agent_file,
                        'active': False,  # Non possiamo sapere se è attivo senza manager
                        'created': os.path.getctime(agent_file),
                        'mood': metadata.get('mood', 'neutral'),
                        'role': metadata.get('role', 'Agent AI'),
                        'goal': metadata.get('goal', 'Obiettivo non specificato'),
                        'interactions': 0,
                        'uptime': '0s'
                    }
        
        return jsonify({
            'success': True,
            'agents': list(agents_detail.keys()),
            'agents_detail': agents_detail,
            'total': len(agents_detail),
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'agents': [],
            'agents_detail': {}
        }), 500

@frontend_bp.route('/api/events', methods=['GET'])
def get_events():
    """Restituisce il log degli eventi e evoluzioni"""
    try:
        limit = request.args.get('limit', 50, type=int)
        events = []
        
        if memory_instance:
            # Ottieni eventi dalla memoria di Aether
            thoughts = memory_instance.get_recent_thoughts(limit)
            
            for thought in thoughts:
                events.append({
                    'id': thought.get('id', f"thought_{thought.get('timestamp', '')}"),
                    'type': thought.get('type', 'thought'),
                    'content': thought.get('content', ''),
                    'timestamp': thought.get('timestamp', datetime.now().isoformat()),
                    'context': {
                        'mood': thought.get('mood'),
                        'agent_name': thought.get('agent_name'),
                        'file': thought.get('file_created')
                    },
                    'audio_file': thought.get('audio_file')
                })
        
        # Aggiungi eventi da file log se esistono
        log_events = load_events_from_logs()
        events.extend(log_events)
        
        # Ordina per timestamp
        events.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Limita risultati
        events = events[:limit]
        
        return jsonify({
            'success': True,
            'events': events,
            'total': len(events),
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'events': []
        }), 500

@frontend_bp.route('/api/thoughts', methods=['GET'])
def get_thoughts():
    """Restituisce i pensieri recenti di Aether"""
    try:
        limit = request.args.get('limit', 10, type=int)
        thoughts = []
        
        if memory_instance:
            recent_thoughts = memory_instance.get_recent_thoughts(limit)
            
            for thought in recent_thoughts:
                thoughts.append({
                    'content': thought.get('content', ''),
                    'timestamp': thought.get('timestamp', datetime.now().isoformat()),
                    'mood': thought.get('mood', 'neutral'),
                    'type': thought.get('type', 'thought'),
                    'context': thought.get('context', {})
                })
        
        return jsonify({
            'success': True,
            'thoughts': thoughts,
            'total': len(thoughts),
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'thoughts': []
        }), 500

@frontend_bp.route('/api/audio', methods=['GET'])
def get_audio_files():
    """Restituisce la lista dei file audio disponibili"""
    try:
        audio_files = []
        
        # Cerca file audio nelle cartelle
        audio_patterns = [
            'audio/*.mp3',
            'audio/*.wav',
            'data/audio/*.mp3',
            'data/audio/*.wav',
            '*.mp3',
            '*.wav'
        ]
        
        for pattern in audio_patterns:
            for file_path in glob.glob(pattern):
                file_name = Path(file_path).name
                file_stats = os.stat(file_path)
                
                audio_files.append({
                    'filename': file_name,
                    'name': file_name.replace('.mp3', '').replace('.wav', ''),
                    'path': file_path,
                    'size': file_stats.st_size,
                    'created': file_stats.st_ctime,
                    'duration': None,  # Potrebbe essere calcolato con librerie audio
                    'type': 'audio'
                })
        
        # Ordina per data di creazione
        audio_files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'audio_files': audio_files,
            'total': len(audio_files),
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'audio_files': []
        }), 500

@frontend_bp.route('/api/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    """Serve file audio"""
    try:
        # Cerca il file nelle cartelle audio
        audio_paths = ['audio', 'data/audio', '.']
        
        for audio_dir in audio_paths:
            file_path = os.path.join(audio_dir, filename)
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=False)
        
        return jsonify({'error': 'File not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@frontend_bp.route('/api/status', methods=['GET'])
def get_system_status():
    """Restituisce lo stato del sistema Aether"""
    try:
        status = {
            'timestamp': datetime.now().isoformat(),
            'memory': {
                'status': 'active' if memory_instance else 'inactive',
                'thoughts_count': len(memory_instance.get_recent_thoughts(1000)) if memory_instance else 0
            },
            'agents': {
                'status': 'active' if agent_manager else 'inactive',
                'count': len(agent_manager.agents) if agent_manager else 0
            },
            'narration': {
                'status': 'unknown',  # Verrà aggiornato se disponibile
            },
            'vision': {
                'status': 'unknown',  # Verrà aggiornato se disponibile
            },
            'self_evolution': {
                'status': 'unknown',  # Verrà aggiornato se disponibile
            }
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@frontend_bp.route('/api/evolve', methods=['POST'])
def trigger_evolution():
    """Trigger manuale dell'evoluzione di Aether"""
    try:
        data = request.get_json() or {}
        
        # Qui si potrebbe triggare l'evoluzione manualmente
        # Per ora restituiamo un placeholder
        
        return jsonify({
            'success': True,
            'message': 'Evolution triggered successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Funzioni di utilità

def extract_component_metadata(file_path: str) -> Dict[str, Any]:
    """Estrae metadati da un componente JSX"""
    metadata = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Cerca commenti con metadati
            if '// @mood:' in content:
                mood_line = [line for line in content.split('\n') if '// @mood:' in line]
                if mood_line:
                    metadata['mood'] = mood_line[0].split('// @mood:')[1].strip()
            
            if '// @description:' in content:
                desc_line = [line for line in content.split('\n') if '// @description:' in line]
                if desc_line:
                    metadata['description'] = desc_line[0].split('// @description:')[1].strip()
    
    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
    
    return metadata

def extract_agent_metadata(file_path: str) -> Dict[str, Any]:
    """Estrae metadati da un agente Python"""
    metadata = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Cerca metadati nei commenti o nelle docstring
            if 'MOOD =' in content:
                mood_line = [line for line in content.split('\n') if 'MOOD =' in line]
                if mood_line:
                    metadata['mood'] = mood_line[0].split('=')[1].strip().strip('"\'')
            
            if 'ROLE =' in content:
                role_line = [line for line in content.split('\n') if 'ROLE =' in line]
                if role_line:
                    metadata['role'] = role_line[0].split('=')[1].strip().strip('"\'')
            
            if 'GOAL =' in content:
                goal_line = [line for line in content.split('\n') if 'GOAL =' in line]
                if goal_line:
                    metadata['goal'] = goal_line[0].split('=')[1].strip().strip('"\'')
    
    except Exception as e:
        print(f"Error extracting agent metadata from {file_path}: {e}")
    
    return metadata

def load_events_from_logs() -> List[Dict[str, Any]]:
    """Carica eventi dai file di log"""
    events = []
    
    try:
        log_files = glob.glob('data/logs/*.json')
        log_files.extend(glob.glob('logs/*.json'))
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    
                    if isinstance(log_data, list):
                        events.extend(log_data)
                    elif isinstance(log_data, dict):
                        events.append(log_data)
            
            except Exception as e:
                print(f"Error loading log file {log_file}: {e}")
    
    except Exception as e:
        print(f"Error loading events from logs: {e}")
    
    return events 