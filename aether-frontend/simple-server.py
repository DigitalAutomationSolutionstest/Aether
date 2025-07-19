#!/usr/bin/env python3
"""
🌟 Aether Frontend Server Semplificato
Server HTTP statico per servire il frontend React di Aether con supporto JSX
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path
import mimetypes

PORT = 3001

# Configura i MIME types corretti
mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('application/javascript', '.jsx')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/html', '.html')
mimetypes.add_type('image/svg+xml', '.svg')

class AetherHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=Path(__file__).parent, **kwargs)
    
    def do_GET(self):
        # Se richiesta root, servi simple-ui.html o index.html
        if self.path == '/':
            # Prima prova simple-ui.html, poi index.html
            if (Path(__file__).parent / 'simple-ui.html').exists():
                self.path = '/simple-ui.html'
            else:
                self.path = '/index.html'
        
        # Servi il file normalmente
        return super().do_GET()
    
    def end_headers(self):
        # Aggiungi headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def guess_type(self, path):
        """Sovrascrivi per assicurare MIME types corretti"""
        mimetype = super().guess_type(path)
        
        # Fix specifici per estensioni problematiche
        if path.endswith('.js') or path.endswith('.mjs') or path.endswith('.jsx'):
            return 'application/javascript'
        elif path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.html'):
            return 'text/html'
        elif path.endswith('.svg'):
            return 'image/svg+xml'
        elif path.endswith('.json'):
            return 'application/json'
        
        return mimetype

def start_server():
    try:
        # Disabilita il caching per sviluppo
        AetherHTTPRequestHandler.extensions_map['.js'] = 'application/javascript'
        AetherHTTPRequestHandler.extensions_map['.jsx'] = 'application/javascript'
        AetherHTTPRequestHandler.extensions_map['.mjs'] = 'application/javascript'
        
        with socketserver.TCPServer(("", PORT), AetherHTTPRequestHandler) as httpd:
            print(f"🌟 Aether Frontend Server avviato su http://localhost:{PORT}")
            print(f"🔗 Collegamento al backend: http://localhost:8000")
            print(f"💻 Interfaccia: simple-ui.html o index.html")
            print(f"✅ MIME types configurati correttamente")
            print(f"⚡ Premi Ctrl+C per fermare il server")
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e) or "WinError 10048" in str(e):
            print(f"❌ Porta {PORT} già in uso!")
            print(f"🔧 Prova a killare il processo o usa un'altra porta")
            return False
        else:
            print(f"❌ Errore server: {e}")
            return False
    except KeyboardInterrupt:
        print(f"\n✅ Server fermato")
        return True

if __name__ == "__main__":
    start_server() 