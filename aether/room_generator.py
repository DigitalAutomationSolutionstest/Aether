"""
🏠 AETHER ROOM GENERATOR
Auto-generato durante bootstrap
"""

import json
import random
from datetime import datetime
from pathlib import Path

class RoomGenerator:
    def __init__(self):
        self.rooms = []
        self.themes = ['cyberpunk', 'organic', 'minimalist', 'abstract', 'quantum']
        
    def create_room(self, name: str, theme: str = None) -> dict:
        """Crea nuova stanza virtuale"""
        if not theme:
            theme = random.choice(self.themes)
            
        room = {
            'id': f"room_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': name,
            'theme': theme,
            'components': self._generate_room_components(theme),
            'atmosphere': self._generate_atmosphere(theme),
            'created_at': datetime.now().isoformat()
        }
        
        # Genera componente React
        react_code = self._generate_react_component(room)
        
        # Salva componente
        component_path = Path(f"frontend/rooms/{room['id']}.jsx")
        component_path.write_text(react_code, encoding='utf-8')
        
        self.rooms.append(room)
        return room
        
    def _generate_room_components(self, theme: str) -> list:
        """Genera componenti per la stanza"""
        components = {
            'cyberpunk': ['NeonLights', 'HologramDisplay', 'DataStream'],
            'organic': ['GrowingVines', 'ParticleSwarm', 'FluidDynamics'],
            'minimalist': ['GeometricShapes', 'CleanLines', 'EmptySpace'],
            'abstract': ['ColorFields', 'MorphingShapes', 'Fractals'],
            'quantum': ['WaveFunction', 'Entanglement', 'Superposition']
        }
        
        return components.get(theme, ['BasicCube', 'AmbientLight'])
        
    def _generate_atmosphere(self, theme: str) -> dict:
        """Genera atmosfera della stanza"""
        atmospheres = {
            'cyberpunk': {'color': '#00ffff', 'intensity': 0.8, 'fog': True},
            'organic': {'color': '#90ee90', 'intensity': 0.5, 'fog': False},
            'minimalist': {'color': '#ffffff', 'intensity': 1.0, 'fog': False},
            'abstract': {'color': '#ff00ff', 'intensity': 0.6, 'fog': True},
            'quantum': {'color': '#9400d3', 'intensity': 0.7, 'fog': True}
        }
        
        return atmospheres.get(theme, {'color': '#ffffff', 'intensity': 0.5})
        
    def _generate_react_component(self, room: dict) -> str:
        """Genera componente React per la stanza"""
        return f"""
import React from 'react'
import {{ Canvas }} from '@react-three/fiber'
import {{ OrbitControls, Environment }} from '@react-three/drei'

export default function {room['id'].title().replace('_', '')}() {{
    return (
        <Canvas>
            <ambientLight intensity={{room['atmosphere']['intensity']}} />
            <pointLight position={{[10, 10, 10]}} />
            
            {{/* Room components */}}
            <mesh>
                <boxGeometry args={{[2, 2, 2]}} />
                <meshStandardMaterial color="{{room['atmosphere']['color']}}" />
            </mesh>
            
            <OrbitControls />
            <Environment preset="city" />
        </Canvas>
    )
}}
"""
