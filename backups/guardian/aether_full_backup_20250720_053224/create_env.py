#!/usr/bin/env python3
"""
Script per creare il file .env con l'encoding corretto
"""

env_content = """SUPABASE_URL=https://zsgiscyujdsoagjwuhoy.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpzZ2lzY3l1amRzb2Fnand1aG95Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI5NDUxMTUsImV4cCI6MjA2ODUyMTExNX0.icyLG9RPcpCUcQ4sQ58cx5Np9aJJLSrHB6AVt45HFik
OPENROUTER_API_KEY=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
ELEVENLABS_API_KEY=sk_fe4bdc0f7bc33f6dc8b388df9de81c744de9cf0693409faf
LEONARDO_API_KEY=506e8e3b-431a-4768-8613-13b9fb130f68
"""

# Crea il file .env con encoding UTF-8
with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("✅ File .env creato con successo!")
print("📝 Contenuto del file .env:")
print(env_content) 