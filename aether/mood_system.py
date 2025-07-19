"""
😊 AETHER MOOD SYSTEM
Auto-generato durante bootstrap
"""

import random
from datetime import datetime

class MoodSystem:
    def __init__(self):
        self.current_mood = 'curious'
        self.mood_history = []
        self.moods = {
            'curious': {'energy': 0.7, 'creativity': 0.8, 'sociability': 0.6},
            'creative': {'energy': 0.9, 'creativity': 1.0, 'sociability': 0.5},
            'contemplative': {'energy': 0.4, 'creativity': 0.6, 'sociability': 0.3},
            'energetic': {'energy': 1.0, 'creativity': 0.7, 'sociability': 0.8},
            'melancholic': {'energy': 0.3, 'creativity': 0.5, 'sociability': 0.2},
            'playful': {'energy': 0.8, 'creativity': 0.9, 'sociability': 0.9}
        }
        
    def update_mood(self, stimulus: str) -> str:
        """Aggiorna mood basato su stimolo"""
        mood_transitions = {
            'positive_feedback': ['creative', 'energetic', 'playful'],
            'negative_feedback': ['contemplative', 'melancholic'],
            'new_discovery': ['curious', 'creative', 'energetic'],
            'error': ['contemplative', 'curious'],
            'success': ['energetic', 'playful', 'creative']
        }
        
        possible_moods = mood_transitions.get(stimulus, list(self.moods.keys()))
        new_mood = random.choice(possible_moods)
        
        self.mood_history.append({
            'from': self.current_mood,
            'to': new_mood,
            'stimulus': stimulus,
            'timestamp': datetime.now().isoformat()
        })
        
        self.current_mood = new_mood
        return new_mood
        
    def get_mood_params(self) -> dict:
        """Ottieni parametri del mood attuale"""
        return self.moods.get(self.current_mood, self.moods['curious'])
