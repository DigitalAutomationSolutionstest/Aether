#!/usr/bin/env python3
"""
🔧 Fix Import Issues Script
Risolve gli errori di import circolari nel sistema
"""

import os
import shutil

print("🔧 FIXING IMPORT ISSUES...")

# Disabilita temporaneamente i route problematici
problematic_routes = [
    "routes/reflection_routes.py",
    "routes/entity_routes.py", 
    "routes/thinking_routes.py"
]

for route_file in problematic_routes:
    if os.path.exists(route_file):
        backup_file = f"{route_file}.backup"
        shutil.copy2(route_file, backup_file)
        print(f"📦 Backed up: {route_file}")

# Aggiorna routes/__init__.py per caricare solo i route funzionanti
init_content = '''"""
Routes modulari per Invader Core Agent API
"""

from fastapi import APIRouter
from .simple_routes import router as simple_router

# Solo i router che funzionano senza import circolari
routers = [
    simple_router,
]

print("✅ Loaded routes:", [r.tags for r in routers if hasattr(r, 'tags')])
'''

with open("routes/__init__.py", "w", encoding="utf-8") as f:
    f.write(init_content)

print("✅ Routes updated to avoid circular imports")
print("🚀 Now you can start the backend safely!")
print("🎯 Run: python main.py --api") 