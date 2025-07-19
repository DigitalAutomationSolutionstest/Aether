from openai import OpenAI
from config import settings

# Inizializza il client OpenAI con OpenRouter
client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def ask_brain(prompt, history=None):
    messages = history or []
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=settings.MODEL,
        messages=messages,
    )
    return response.choices[0].message.content 