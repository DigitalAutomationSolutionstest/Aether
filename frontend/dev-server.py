#!/usr/bin/env python3
"""
Development server for React app with proper MIME type handling
"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 3001

class ReactDevServer(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        '.html': 'text/html',
        '.js': 'application/javascript',
        '.jsx': 'application/javascript',
        '.mjs': 'application/javascript',
        '.css': 'text/css',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.woff': 'application/font-woff',
        '.woff2': 'application/font-woff2',
        '.ttf': 'application/font-ttf',
        '.otf': 'application/font-otf',
        '.eot': 'application/vnd.ms-fontobject'
    }

    def do_GET(self):
        # Serve index.html for SPA routes
        if self.path != '/' and not '.' in self.path.split('/')[-1]:
            self.path = '/index.html'
        return super().do_GET()

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

    def guess_type(self, path):
        path = Path(path)
        ext = path.suffix.lower()
        
        if ext in self.extensions_map:
            return self.extensions_map[ext], None
        
        # Default to parent class behavior
        mimetype = super().guess_type(str(path))
        return mimetype

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    Handler = ReactDevServer
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🚀 React Development Server")
            print(f"📂 Serving directory: {os.getcwd()}")
            print(f"🌐 Server running at: http://localhost:{PORT}")
            print(f"📡 Backend API expected at: http://localhost:8000")
            print(f"⚡ Press Ctrl+C to stop")
            print(f"\n✅ MIME types configured for ES6 modules")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48 or e.errno == 10048:
            print(f"❌ Port {PORT} is already in use!")
            print("💡 Try: Get-Process python | Stop-Process -Force")
        else:
            raise

if __name__ == "__main__":
    main() 