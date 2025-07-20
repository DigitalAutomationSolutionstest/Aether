#!/usr/bin/env python3
"""Forza Aether a creare la sua prima app monetizzabile"""

import json
from pathlib import Path
from datetime import datetime

print("🚀 Forzo Aether a creare la prima app...")

# Crea la struttura dell'app
app_path = Path("creations/apps/ai_content_pro")
app_path.mkdir(parents=True, exist_ok=True)

# Backend semplice
backend = """from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"app": "AI Content Pro", "by": "Aether", "status": "monetizing"}

@app.get("/generate/{topic}")
def generate_content(topic: str):
    return {
        "topic": topic,
        "content": f"Contenuto AI generato su {topic}",
        "price": "$0.10 per generation"
    }
"""

(app_path / "main.py").write_text(backend, encoding='utf-8')
print("✅ Backend creato")

# README
readme = """# AI Content Pro
App creata da Aether per generare contenuti AI.
Monetizzazione: $19.99/mese
"""
(app_path / "README.md").write_text(readme, encoding='utf-8')
print("✅ README creato")

# Aggiorna actions log (con gestione errori)
log_file = Path("data/actions_log.json")
try:
    if log_file.exists():
        logs = json.loads(log_file.read_text(encoding='utf-8'))
    else:
        logs = []
except:
    logs = []  # Se il file è corrotto, ricrea da zero

logs.append({
    "timestamp": datetime.now().isoformat(),
    "action": "created_app",
    "app": "ai_content_pro",
    "revenue_model": "subscription"
})

# Salva solo gli ultimi 100 log per evitare file troppo grandi
logs = logs[-100:]
log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')

print("✨ App creata in creations/apps/ai_content_pro/")

# Notifica Discord
try:
    from aether.discord_notifier import send_discord_message
    send_discord_message(
        "🚀 **PRIMA APP CREATA!** AI Content Pro\n"
        "💰 Modello: Subscription $19.99/mese\n"
        "📁 Path: `creations/apps/ai_content_pro`",
        title="🎉 Aether Crea App",
        color=0x00FF00
    )
except:
    print("(Discord notification skipped)") 