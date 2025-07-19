#!/usr/bin/env python3
"""
Simple HTTP server per servire l'app React di Aether
"""
import http.server
import socketserver
import os
import sys
import mimetypes

PORT = 3001

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Imposta le estensioni MIME corrette per React
        mimetypes.init()
        mimetypes.add_type('application/javascript', '.js')
        mimetypes.add_type('application/javascript', '.jsx')
        mimetypes.add_type('application/javascript', '.mjs')
        mimetypes.add_type('text/css', '.css')
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        # Aggiungi headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def guess_type(self, path):
        """Sovrascrivi per gestire correttamente i file JSX"""
        path_str = str(path)
        mimetype = super().guess_type(path)
        if path_str.endswith('.jsx'):
            return ('application/javascript', None)
        elif path_str.endswith('.js'):
            return ('application/javascript', None)
        elif path_str.endswith('.mjs'):
            return ('application/javascript', None)
        return mimetype

def start_server():
    # Cambia alla directory corrente (frontend)
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    Handler = MyHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🌟 Aether React Frontend Server")
            print(f"📍 Serving from: {web_dir}")
            print(f"🚀 Server running at: http://localhost:{PORT}")
            print(f"🔗 Backend expected at: http://localhost:8000")
            print(f"⚡ Press Ctrl+C to stop")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48 or e.errno == 10048:  # Port already in use
            print(f"❌ Port {PORT} already in use!")
            print("🔧 Try killing the process or use a different port")
        else:
            raise

if __name__ == "__main__":
    start_server() 