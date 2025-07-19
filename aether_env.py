"""
Configurazione ambiente per Aether
"""
import os

# Imposta Discord Webhook
os.environ['DISCORD_WEBHOOK_URL'] = 'https://discordapp.com/api/webhooks/1396218820808409148/orGucbC2Ydx0eLPEntbXmwYLigX6sY0tA1FIFsnlmbn7CuVp7YXbKFNFxUgM0wxSW7Mr'

# Modalità Aether
os.environ['AETHER_MODE'] = 'MONETIZATION_FOCUS'
os.environ['AUTO_CREATE_APPS'] = 'true'
os.environ['EVOLUTION_SPEED'] = 'MAXIMUM'

print("✅ Discord Webhook configurato!")
print("🚀 Modalità: MONETIZATION_FOCUS")
print("💰 Auto creazione app: ATTIVA")
print("⚡ Velocità evoluzione: MASSIMA") 