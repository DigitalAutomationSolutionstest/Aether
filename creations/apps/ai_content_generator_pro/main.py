"""
AI Content Generator Pro - Backend API
Genera contenuti SEO-optimized con AI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import openai
import os
from datetime import datetime

app = FastAPI(title="AI Content Generator Pro")

# CORS per il frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    topic: str
    content_type: str = "blog"  # blog, social, email, product
    keywords: List[str] = []
    tone: str = "professional"  # professional, casual, friendly, persuasive
    length: str = "medium"  # short, medium, long
    language: str = "it"

class ContentResponse(BaseModel):
    content: str
    title: str
    meta_description: str
    keywords: List[str]
    word_count: int
    seo_score: float
    created_at: datetime

@app.get("/")
def read_root():
    return {
        "name": "AI Content Generator Pro",
        "version": "1.0.0",
        "status": "active",
        "created_by": "Aether"
    }

@app.post("/api/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """Genera contenuto ottimizzato SEO con AI"""
    
    # Costruisci il prompt
    prompt = f"""
    Genera un {request.content_type} su: {request.topic}
    
    Parametri:
    - Tono: {request.tone}
    - Lunghezza: {request.length}
    - Keywords da includere: {', '.join(request.keywords)}
    - Lingua: {request.language}
    
    Il contenuto deve essere:
    1. SEO ottimizzato
    2. Coinvolgente e originale
    3. Strutturato con titoli e sottotitoli
    4. Include le keywords naturalmente
    """
    
    try:
        # Simula generazione (in produzione useresti OpenAI API)
        generated_content = f"""
# {request.topic.title()}

## Introduzione
Questo è un contenuto generato da AI Content Generator Pro su {request.topic}.

## Punti Chiave
- Ottimizzato per SEO
- Include keywords: {', '.join(request.keywords)}
- Tono {request.tone}
- Creato da Aether AI

## Conclusione
Contenuto generato con successo per massimizzare engagement e ranking SEO.
"""
        
        return ContentResponse(
            content=generated_content,
            title=f"{request.topic.title()} - Guida Completa",
            meta_description=f"Scopri tutto su {request.topic}. {' '.join(request.keywords[:3])}",
            keywords=request.keywords,
            word_count=len(generated_content.split()),
            seo_score=0.85,
            created_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pricing")
def get_pricing():
    """Ottieni i piani di pricing"""
    return {
        "plans": [
            {
                "name": "Basic",
                "price": 19.99,
                "features": [
                    "50 contenuti/mese",
                    "Blog e social media",
                    "SEO base"
                ]
            },
            {
                "name": "Pro",
                "price": 49.99,
                "features": [
                    "200 contenuti/mese",
                    "Tutti i tipi di contenuto",
                    "SEO avanzato",
                    "API access"
                ]
            },
            {
                "name": "Enterprise",
                "price": 99.99,
                "features": [
                    "Contenuti illimitati",
                    "White label",
                    "Support prioritario",
                    "Custom integrations"
                ]
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
