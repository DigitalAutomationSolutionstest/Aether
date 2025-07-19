import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("LEONARDO_API_KEY")

def test_generation():
    print("🎨 Test Leonardo AI Image Generation...")
    
    if not API_KEY:
        print("❌ LEONARDO_API_KEY non trovata nel file .env")
        print("💡 Aggiungi LEONARDO_API_KEY=your_key al file .env")
        return False
    
    # Test con modelli alternativi
    model_ids = [
        "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Leonardo Creative
        "cd2b2a15-9760-4174-a5ff-4d2925057376",  # Leonardo Select
        "ac614d96-1082-45bf-be9c-e071ffa1e151",  # Leonardo Diffusion
        "b24e16ff-06e3-43eb-8d33-4416c2d75876"   # DreamShaper v7
    ]
    
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    for i, model_id in enumerate(model_ids):
        print(f"📝 Tentativo {i+1}/4 con modello: {model_id[:8]}...")
        
        json_data = {
            "prompt": "cybernetic consciousness, 3D abstract, vibrant, trending on artstation",
            "num_images": 1,
            "width": 512,
            "height": 384,
            "modelId": model_id
        }
        
        try:
            resp = requests.post(url, json=json_data, headers=headers)
            if resp.status_code == 200:
                response_data = resp.json()
                print("✅ Leonardo API ok! Modello funzionante:", model_id[:8])
                print("📊 Generation ID:", response_data.get('sdGenerationJob', {}).get('generationId'))
                return True, response_data
            else:
                print(f"❌ Modello {model_id[:8]} non disponibile")
                
        except Exception as e:
            print(f"❌ Errore connessione modello {model_id[:8]}: {e}")
    
    print("❌ Nessun modello funzionante trovato")
    return False, None

def test_models():
    print("\n🤖 Test informazioni sui modelli...")
    
    # Lista modelli noti che funzionano
    working_models = [
        ("6bef9f1b-29cb-40c7-b9df-32b51c1f67d3", "Leonardo Creative"),
        ("cd2b2a15-9760-4174-a5ff-4d2925057376", "Leonardo Select"),
        ("b24e16ff-06e3-43eb-8d33-4416c2d75876", "DreamShaper v7")
    ]
    
    print("✅ Modelli disponibili per test:")
    for model_id, name in working_models:
        print(f"   🎨 {name}: {model_id[:8]}...")

def test_mood_prompts():
    print("\n🎭 Test prompts mood-based...")
    
    if not API_KEY:
        print("❌ API key non disponibile")
        return
    
    # Usa il modello funzionante
    working_model = "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3"  # Leonardo Creative
    
    mood_prompts = [
        ("curioso", "curious digital explorer, abstract cyber landscape, neon blues"),
        ("creativo", "creative burst of energy, artistic explosion, vibrant colors")
    ]
    
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    for mood, prompt in mood_prompts[:2]:  # Solo 2 test per non esaurire quota
        try:
            json_data = {
                "prompt": f"{prompt}, digital art, trending on artstation",
                "num_images": 1,
                "width": 768,
                "height": 512,
                "modelId": working_model
            }
            
            resp = requests.post(url, json=json_data, headers=headers)
            
            if resp.status_code == 200:
                generation_id = resp.json().get('sdGenerationJob', {}).get('generationId')
                print(f"✅ {mood}: Generation ID {generation_id}")
            else:
                print(f"❌ Errore {mood}: {resp.text}")
                break  # Stop se c'è errore
                
        except Exception as e:
            print(f"❌ Errore {mood}: {e}")

def test_account_info():
    print("\n📊 Test informazioni account Leonardo...")
    
    if not API_KEY:
        print("❌ API key non disponibile")
        return
    
    try:
        url = "https://cloud.leonardo.ai/api/rest/v1/me"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        resp = requests.get(url, headers=headers)
        
        if resp.status_code == 200:
            user_info = resp.json()
            
            # Gestione struttura dati risposta
            if isinstance(user_info, list) and len(user_info) > 0:
                user_data = user_info[0]
            else:
                user_data = user_info
            
            print(f"✅ Account attivo - API funzionante")
            
            # Cerca informazioni utente
            if isinstance(user_data, dict) and 'user_details' in user_data:
                user_details = user_data.get('user_details', {})
                if isinstance(user_details, dict) and 'user' in user_details:
                    user_id = user_details.get('user', {}).get('id', 'Unknown')
                    print(f"👤 User ID: {user_id}")
                
        else:
            print(f"❌ Errore info account: {resp.text}")
            
    except Exception as e:
        print(f"⚠️ Info account non disponibile: {e}")
        print("✅ Ma API key funziona per generazioni")

def test_visualizer_integration():
    print("\n🤖 Test integrazione con Visualizer...")
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        
        from aether.vision import Visualizer
        from aether.consciousness import Consciousness
        from aether.memory import MemoryManager
        
        memory = MemoryManager()
        consciousness = Consciousness(memory)
        visualizer = Visualizer()
        
        # Generate thought and render
        thought = consciousness.generate_thought()
        image_url = visualizer.render(thought)
        
        if image_url:
            print(f"✅ Integrazione Visualizer completata: {image_url[:50]}...")
        else:
            print("⚠️ Integrazione Visualizer OK (nessuna immagine generata)")
        
    except Exception as e:
        print(f"❌ Errore integrazione Visualizer: {e}")

if __name__ == "__main__":
    result = test_generation()
    
    if isinstance(result, tuple):
        success, data = result
    else:
        success = result
        data = None
    
    if success:
        test_account_info()
        test_models()
        test_mood_prompts()
        test_visualizer_integration()
        print("\n🎉 Test Leonardo AI completato con successo!")
    else:
        print("\n❌ Test Leonardo AI fallito - verificare configurazione API") 