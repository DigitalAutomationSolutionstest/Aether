# aether/narration.py

import os
import requests

class Narrator:
    def __init__(self):
        self.api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not self.api_key:
            print("⚠️ ELEVENLABS_API_KEY non trovata - narrazione disabilitata")

    def speak(self, text):
        if not self.api_key:
            print(f"🗣️ (Modalità silenzio): {text}")
            return
            
        url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"
        headers = {"xi-api-key": self.api_key}
        data = {"text": text, "voice_settings": {"stability": 0.3, "similarity_boost": 0.75}}
        resp = requests.post(url, json=data, headers=headers)
        if resp.status_code == 200:
            filename = f"data/voice_output/{hash(text)}.mp3"
            with open(filename, "wb") as f:
                f.write(resp.content)
            print(f"🗣️ Ho parlato! Audio salvato in {filename}")
        else:
            print("Errore ElevenLabs:", resp.text) 