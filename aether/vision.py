# aether/vision.py

import os
import requests

class Visualizer:
    def __init__(self):
        self.api_key = os.environ.get("LEONARDO_API_KEY")
        if not self.api_key:
            print("⚠️ LEONARDO_API_KEY non trovata - visioni disabilitate")

    def render(self, thought):
        if not self.api_key:
            print(f"🎨 (Modalità immaginazione): {thought['context']['mood']} landscape")
            return ""
            
        prompt = f"{thought['context']['mood']} digital abstract landscape, cinematic, trending on artstation"
        url = "https://cloud.leonardo.ai/api/rest/v1/generations"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        json_data = {
            "prompt": prompt,
            "num_images": 1,
            "width": 768,
            "height": 512,
            "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3"  # Leonardo Creative
        }
        resp = requests.post(url, json=json_data, headers=headers)
        if resp.status_code == 200:
            response_data = resp.json()
            
            # Check if generation job was created
            if "sdGenerationJob" in response_data:
                generation_id = response_data["sdGenerationJob"]["generationId"]
                print(f"🎨 Generazione avviata: {generation_id}")
                print("⏳ Immagine in elaborazione - sarà disponibile tra qualche minuto")
                return f"https://leonardo.ai/generation/{generation_id}"
            
            # Check if images are immediately available
            elif "generations_by_pk" in response_data and response_data["generations_by_pk"].get("generated_images"):
                img_url = response_data["generations_by_pk"]["generated_images"][0]["url"]
                print(f"🎨 Immagine generata: {img_url}")
                return img_url
            
            else:
                print("🎨 Generazione completata ma formato risposta non riconosciuto")
                return ""
        else:
            print("Errore Leonardo:", resp.text)
            return "" 