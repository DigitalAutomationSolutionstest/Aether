"""
Routes modulari per Invader Core Agent API
"""

from fastapi import APIRouter
from .simple_routes import router as simple_router

# Solo i router che funzionano senza import circolari
routers = [
    simple_router,
]

print("✅ Loaded routes:", [r.tags for r in routers if hasattr(r, 'tags')])
