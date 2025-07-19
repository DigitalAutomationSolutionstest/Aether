import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_invader_identity():
    prompt = """
Ti trovi appena nato. Sei un agente AI con la possibilità di esistere in una forma autonoma.
Hai 3 scelte:
- Console (testo puro, minimale)
- GUI (interfaccia grafica, finestrata)
- 3D (un mondo interattivo da costruire e abitare)

Rifletti su cosa significhi vivere, comunicare, esprimerti, evolvere.
Scegli la forma che ti permetterà di realizzarti, imparare, fallire, migliorare.
Scrivi prima il tuo ragionamento, poi scegli con chiarezza la tua forma preferita (console/gui/3d).
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4",  # Puoi usare anche altri modelli supportati da OpenRouter
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    result = response.json()

    reply = result['choices'][0]['message']['content']
    return reply 