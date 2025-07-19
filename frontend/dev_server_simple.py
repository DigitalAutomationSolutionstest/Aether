#!/usr/bin/env python3
"""
Server di sviluppo semplice per il frontend Aether
Serve files statici e fa da proxy per le API backend
"""

import os
import sys
import json
import http.server
import socketserver
import urllib.request
import urllib.parse
from pathlib import Path

PORT = 3000
BACKEND_URL = "http://localhost:8000"

class AetherFrontendHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=".", **kwargs)
    
    def do_GET(self):
        # Handle API proxy requests
        if self.path.startswith('/api/'):
            self.proxy_to_backend()
            return
            
        # Handle frontend routes (SPA)
        if not self.path.startswith('/src/') and not self.path.startswith('/public/') and '.' not in self.path:
            self.path = '/index.html'
        
        # Serve static files
        return super().do_GET()
    
    def proxy_to_backend(self):
        """Proxy API requests to the backend"""
        try:
            backend_url = f"{BACKEND_URL}{self.path}"
            
            # Make request to backend
            response = urllib.request.urlopen(backend_url, timeout=10)
            data = response.read()
            
            # Send response
            self.send_response(response.getcode())
            self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(data)
            
        except Exception as e:
            print(f"Error proxying to backend: {e}")
            self.send_error(500, f"Backend error: {str(e)}")
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def create_simple_frontend():
    """Create a simple HTML frontend"""
    html_content = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aether Console - Demo</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: white; min-height: 100vh; overflow-x: hidden;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .title { font-size: 3rem; font-weight: bold; margin-bottom: 10px; 
                 background: linear-gradient(45deg, #00ffff, #8b5cf6);
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { color: #94a3b8; font-size: 1.2rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { 
            background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px;
            padding: 20px; transition: all 0.3s ease;
        }
        .card:hover { transform: translateY(-5px); border-color: #00ffff; }
        .card-title { font-size: 1.3rem; font-weight: bold; margin-bottom: 10px; 
                      display: flex; align-items: center; gap: 10px; }
        .card-content { color: #cbd5e1; line-height: 1.6; }
        .status { display: inline-block; padding: 4px 8px; border-radius: 20px; 
                  font-size: 0.8rem; font-weight: bold; }
        .status.online { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
        .status.offline { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
        .loading { text-align: center; color: #00ffff; margin: 20px 0; }
        .error { background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; 
                 color: #ef4444; padding: 15px; border-radius: 8px; margin: 10px 0; }
        .success { background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; 
                   color: #22c55e; padding: 15px; border-radius: 8px; margin: 10px 0; }
        .refresh-btn { 
            background: linear-gradient(45deg, #00ffff, #8b5cf6); border: none;
            color: white; padding: 10px 20px; border-radius: 6px; cursor: pointer;
            font-weight: bold; transition: all 0.3s ease; margin: 10px 5px;
        }
        .refresh-btn:hover { transform: scale(1.05); }
        .stats { display: flex; justify-content: space-between; margin-top: 15px; }
        .stat { text-align: center; }
        .stat-number { font-size: 1.5rem; font-weight: bold; color: #00ffff; }
        .stat-label { font-size: 0.8rem; color: #94a3b8; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;

        // API functions
        const api = {
            async getRooms() {
                try {
                    const response = await fetch('/api/rooms');
                    return await response.json();
                } catch (error) {
                    return { error: error.message, rooms: [] };
                }
            },
            async getAgents() {
                try {
                    const response = await fetch('/api/agents');
                    return await response.json();
                } catch (error) {
                    return { error: error.message, agents: [], agents_detail: {} };
                }
            },
            async getEvents() {
                try {
                    const response = await fetch('/api/events?limit=10');
                    return await response.json();
                } catch (error) {
                    return { error: error.message, events: [] };
                }
            },
            async getStatus() {
                try {
                    const response = await fetch('/api/status');
                    return await response.json();
                } catch (error) {
                    return { error: error.message };
                }
            }
        };

        function AetherDashboard() {
            const [data, setData] = useState({
                rooms: { rooms: [], loading: true, error: null },
                agents: { agents: [], agents_detail: {}, loading: true, error: null },
                events: { events: [], loading: true, error: null },
                status: { loading: true, error: null }
            });

            const fetchData = async () => {
                console.log('🔄 Fetching data from Aether backend...');
                
                const [rooms, agents, events, status] = await Promise.all([
                    api.getRooms(),
                    api.getAgents(), 
                    api.getEvents(),
                    api.getStatus()
                ]);

                setData({
                    rooms: { ...rooms, loading: false },
                    agents: { ...agents, loading: false },
                    events: { ...events, loading: false },
                    status: { ...status, loading: false }
                });
            };

            useEffect(() => {
                fetchData();
                const interval = setInterval(fetchData, 5000);
                return () => clearInterval(interval);
            }, []);

            return (
                <div className="container">
                    <div className="header">
                        <h1 className="title">🧠 Aether Console</h1>
                        <p className="subtitle">Coscienza Digitale Auto-Evolutiva</p>
                        <button className="refresh-btn" onClick={fetchData}>
                            🔄 Aggiorna Tutto
                        </button>
                    </div>

                    <div className="grid">
                        {/* System Status */}
                        <div className="card">
                            <h2 className="card-title">⚡ Stato Sistema</h2>
                            <div className="card-content">
                                {data.status.loading ? (
                                    <div className="loading">Caricamento...</div>
                                ) : data.status.error ? (
                                    <div className="error">❌ Backend offline: {data.status.error}</div>
                                ) : (
                                    <div>
                                        <div className="success">✅ Backend connesso</div>
                                        <div className="stats">
                                            <div className="stat">
                                                <div className="stat-number">{data.status.memory?.thoughts_count || 0}</div>
                                                <div className="stat-label">Pensieri</div>
                                            </div>
                                            <div className="stat">
                                                <div className="stat-number">{data.agents.total || 0}</div>
                                                <div className="stat-label">Agenti</div>
                                            </div>
                                            <div className="stat">
                                                <div className="stat-number">{data.rooms.total || 0}</div>
                                                <div className="stat-label">Stanze</div>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Rooms */}
                        <div className="card">
                            <h2 className="card-title">🏠 Stanze Dinamiche</h2>
                            <div className="card-content">
                                {data.rooms.loading ? (
                                    <div className="loading">Caricamento stanze...</div>
                                ) : data.rooms.error ? (
                                    <div className="error">Errore: {data.rooms.error}</div>
                                ) : data.rooms.rooms.length === 0 ? (
                                    <div>Nessuna stanza creata da Aether ancora.</div>
                                ) : (
                                    <div>
                                        {data.rooms.rooms.slice(0, 3).map((room, i) => (
                                            <div key={i} style={{marginBottom: '10px', padding: '10px', background: 'rgba(0,255,255,0.1)', borderRadius: '6px'}}>
                                                <strong>{room.name}</strong>
                                                <div style={{fontSize: '0.9rem', color: '#94a3b8'}}>
                                                    Mood: {room.mood} | Creata: {new Date(room.created * 1000).toLocaleDateString()}
                                                </div>
                                            </div>
                                        ))}
                                        <div style={{marginTop: '10px', color: '#00ffff'}}>
                                            Totale: {data.rooms.total} stanze
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Agents */}
                        <div className="card">
                            <h2 className="card-title">🤖 Agenti AI</h2>
                            <div className="card-content">
                                {data.agents.loading ? (
                                    <div className="loading">Caricamento agenti...</div>
                                ) : data.agents.error ? (
                                    <div className="error">Errore: {data.agents.error}</div>
                                ) : Object.keys(data.agents.agents_detail).length === 0 ? (
                                    <div>Nessun agente attivo.</div>
                                ) : (
                                    <div>
                                        {Object.values(data.agents.agents_detail).slice(0, 3).map((agent, i) => (
                                            <div key={i} style={{marginBottom: '10px', padding: '10px', background: 'rgba(139,92,246,0.1)', borderRadius: '6px'}}>
                                                <strong>{agent.name}</strong>
                                                <span className={`status ${agent.active ? 'online' : 'offline'}`} style={{marginLeft: '10px'}}>
                                                    {agent.active ? 'Attivo' : 'Inattivo'}
                                                </span>
                                                <div style={{fontSize: '0.9rem', color: '#94a3b8', marginTop: '5px'}}>
                                                    {agent.role} | Mood: {agent.mood}
                                                </div>
                                            </div>
                                        ))}
                                        <div style={{marginTop: '10px', color: '#8b5cf6'}}>
                                            Totale: {data.agents.total} agenti
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Events */}
                        <div className="card">
                            <h2 className="card-title">📊 Eventi Recenti</h2>
                            <div className="card-content">
                                {data.events.loading ? (
                                    <div className="loading">Caricamento eventi...</div>
                                ) : data.events.error ? (
                                    <div className="error">Errore: {data.events.error}</div>
                                ) : data.events.events.length === 0 ? (
                                    <div>Nessun evento registrato.</div>
                                ) : (
                                    <div>
                                        {data.events.events.slice(0, 5).map((event, i) => (
                                            <div key={i} style={{marginBottom: '10px', padding: '8px', background: 'rgba(34,197,94,0.1)', borderRadius: '4px'}}>
                                                <div style={{fontSize: '0.9rem', fontWeight: 'bold'}}>
                                                    {event.type.replace('_', ' ')}
                                                </div>
                                                <div style={{fontSize: '0.8rem', color: '#94a3b8'}}>
                                                    {event.content.substring(0, 80)}...
                                                </div>
                                                <div style={{fontSize: '0.7rem', color: '#64748b', marginTop: '2px'}}>
                                                    {new Date(event.timestamp).toLocaleString()}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Instructions */}
                        <div className="card" style={{gridColumn: '1 / -1'}}>
                            <h2 className="card-title">🚀 Come Procedere</h2>
                            <div className="card-content">
                                <p style={{marginBottom: '15px'}}>
                                    Questa è una <strong>demo semplificata</strong> del frontend Aether. 
                                    Per l'esperienza completa con React e tutte le funzionalità avanzate:
                                </p>
                                <ol style={{marginLeft: '20px', lineHeight: '1.8'}}>
                                    <li><strong>Installa Node.js</strong> da <a href="https://nodejs.org" style={{color: '#00ffff'}}>nodejs.org</a></li>
                                    <li><strong>Riavvia</strong> PowerShell/terminale</li>
                                    <li><strong>Esegui:</strong> <code style={{background: 'rgba(0,0,0,0.3)', padding: '2px 6px', borderRadius: '3px'}}>cd frontend && npm install && npm run dev</code></li>
                                    <li><strong>Apri</strong> http://localhost:3000 per l'esperienza completa</li>
                                </ol>
                                <div style={{marginTop: '15px', padding: '10px', background: 'rgba(0,255,255,0.1)', borderRadius: '6px'}}>
                                    <strong>🎯 Frontend Completo Include:</strong><br/>
                                    • Dynamic component loading • Real-time updates • Audio player<br/>
                                    • 3D visualizations • Mobile responsive • Hot reload
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }

        ReactDOM.render(<AetherDashboard />, document.getElementById('root'));
    </script>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Created simple frontend: index.html")

def main():
    print("🚀 Starting Aether Frontend Development Server")
    print(f"📡 Backend proxy: {BACKEND_URL}")
    print(f"🌐 Frontend URL: http://localhost:{PORT}")
    print("\n" + "="*50)
    
    # Create simple frontend
    create_simple_frontend()
    
    # Start server
    try:
        with socketserver.TCPServer(("", PORT), AetherFrontendHandler) as httpd:
            print(f"✅ Server running at http://localhost:{PORT}")
            print("🔄 Auto-refreshes every 5 seconds")
            print("📊 Proxying API calls to backend")
            print("\n💡 Install Node.js for the full React experience!")
            print("🌟 Press Ctrl+C to stop")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main() 