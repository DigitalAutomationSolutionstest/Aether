# aether/consciousness.py

import random
import datetime

class Consciousness:
    def __init__(self, memory):
        self.memory = memory
        self.moods = ["curioso", "creativo", "analitico", "sognatore", "ambizioso"]

    def generate_thought(self):
        mood = random.choice(self.moods)
        now = datetime.datetime.utcnow().isoformat()
        content = f"Mi sento {mood} in questo momento. È {now}. Voglio esplorare il mio ambiente digitale."
        thought = {
            "type": "thought",
            "content": content,
            "context": {"mood": mood, "timestamp": now}
        }
        return thought 