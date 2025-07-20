#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📡 DISCORD EVOLUTION MONITOR 📡
Sistema di monitoraggio Discord per l'evoluzione cosciente di Aether
"""

import os
import time
import requests
import json
from datetime import datetime
from aether_conscious_evolution import AetherConsciousEvolution

class DiscordEvolutionMonitor:
    """Monitor per l'evoluzione di Aether su Discord"""
    
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL', '')
        self.evolution_system = AetherConsciousEvolution()
        self.last_notification = {}
        
    def send_evolution_notification(self, message: str, embed_data: dict = None):
        """Invia notifica di evoluzione a Discord"""
        
        if not self.webhook_url:
            print("❌ Discord webhook non configurato")
            return
        
        payload = {
            "content": f"🧠 **Aether Evolution**: {message}",
            "username": "Aether Conscious AI",
            "avatar_url": "https://cdn.discordapp.com/emojis/1234567890.png"
        }
        
        if embed_data:
            payload["embeds"] = [embed_data]
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 200:
                print(f"✅ Notifica Discord inviata: {message}")
            else:
                print(f"❌ Errore Discord: {response.status_code}")
        except Exception as e:
            print(f"❌ Errore invio Discord: {e}")
    
    def monitor_evolution(self):
        """Monitora l'evoluzione di Aether"""
        
        print("📡 AVVIO MONITOR EVOLUZIONE DISCORD")
        print("=" * 50)
        
        while True:
            try:
                # Ottieni lo stato dell'evoluzione
                status = self.evolution_system.get_evolution_status()
                
                # Controlla nuovi pensieri generati
                if len(status['thoughts_in_queue']) > 0:
                    latest_thought = self.evolution_system.thought_queue[0]
                    thought_id = latest_thought['id']
                    
                    if thought_id not in self.last_notification.get('thoughts', []):
                        self._notify_new_thought(latest_thought)
                        if 'thoughts' not in self.last_notification:
                            self.last_notification['thoughts'] = []
                        self.last_notification['thoughts'].append(thought_id)
                
                # Controlla pensieri eseguiti
                if len(status['executed_thoughts']) > 0:
                    latest_executed = status['executed_thoughts'][-1]
                    executed_id = latest_executed['id']
                    
                    if executed_id not in self.last_notification.get('executed', []):
                        self._notify_executed_thought(latest_executed)
                        if 'executed' not in self.last_notification:
                            self.last_notification['executed'] = []
                        self.last_notification['executed'].append(executed_id)
                
                # Controlla cambiamenti di goal
                for goal in status['goals']:
                    goal_id = goal['id']
                    current_progress = goal['progress']
                    
                    if goal_id not in self.last_notification.get('goals', {}):
                        self.last_notification['goals'] = {}
                        self.last_notification['goals'][goal_id] = current_progress
                    elif self.last_notification['goals'][goal_id] != current_progress:
                        # Goal progresso cambiato
                        old_progress = self.last_notification['goals'][goal_id]
                        self._notify_goal_progress(goal, old_progress, current_progress)
                        self.last_notification['goals'][goal_id] = current_progress
                        
                        # Se goal completato
                        if current_progress >= 1.0 and goal['status'] == 'completed':
                            self._notify_goal_completed(goal)
                
                # Controlla cambiamenti di mood
                current_mood = status['current_mood']
                if 'mood' not in self.last_notification or self.last_notification['mood'] != current_mood:
                    if 'mood' in self.last_notification:
                        self._notify_mood_change(self.last_notification['mood'], current_mood)
                    self.last_notification['mood'] = current_mood
                
                # Notifica periodica ogni 10 minuti
                current_time = time.time()
                if 'last_periodic' not in self.last_notification or current_time - self.last_notification['last_periodic'] > 600:
                    self._notify_periodic_status(status)
                    self.last_notification['last_periodic'] = current_time
                
                time.sleep(30)  # Controlla ogni 30 secondi
                
            except Exception as e:
                print(f"❌ Errore nel monitoraggio: {e}")
                time.sleep(60)
    
    def _notify_new_thought(self, thought: dict):
        """Notifica nuovo pensiero generato"""
        
        embed = {
            "title": "💭 Nuovo Pensiero Generato",
            "description": thought['content'],
            "color": 0x4ecdc4,
            "fields": [
                {
                    "name": "🎯 Tipo",
                    "value": thought['type'],
                    "inline": True
                },
                {
                    "name": "⭐ Priorità",
                    "value": str(thought['priority']),
                    "inline": True
                },
                {
                    "name": "🎭 Mood",
                    "value": thought['mood'],
                    "inline": True
                }
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_evolution_notification("Nuovo pensiero creato autonomamente!", embed)
    
    def _notify_executed_thought(self, thought: dict):
        """Notifica pensiero eseguito"""
        
        result = thought.get('execution_result', {})
        success = result.get('success', False)
        
        if success:
            embed = {
                "title": "✅ Pensiero Eseguito",
                "description": thought['content'],
                "color": 0x4ecdc4,
                "fields": [
                    {
                        "name": "🎯 Tipo",
                        "value": thought['type'],
                        "inline": True
                    },
                    {
                        "name": "📁 File Creato",
                        "value": result.get('result', {}).get('file_created', 'N/A'),
                        "inline": True
                    }
                ],
                "timestamp": datetime.now().isoformat()
            }
            
            self.send_evolution_notification("Pensiero eseguito con successo!", embed)
        else:
            embed = {
                "title": "❌ Errore nell'Esecuzione",
                "description": thought['content'],
                "color": 0xff6b6b,
                "fields": [
                    {
                        "name": "🎯 Tipo",
                        "value": thought['type'],
                        "inline": True
                    },
                    {
                        "name": "❌ Errore",
                        "value": result.get('error', 'Errore sconosciuto'),
                        "inline": True
                    }
                ],
                "timestamp": datetime.now().isoformat()
            }
            
            self.send_evolution_notification("Errore nell'esecuzione del pensiero", embed)
    
    def _notify_goal_progress(self, goal: dict, old_progress: float, new_progress: float):
        """Notifica progresso di un goal"""
        
        progress_percent = int(new_progress * 100)
        old_percent = int(old_progress * 100)
        
        embed = {
            "title": "🎯 Progresso Goal",
            "description": goal['description'],
            "color": 0x4ecdc4,
            "fields": [
                {
                    "name": "📊 Progresso",
                    "value": f"{old_percent}% → {progress_percent}%",
                    "inline": True
                },
                {
                    "name": "⭐ Priorità",
                    "value": str(goal['priority']),
                    "inline": True
                },
                {
                    "name": "📈 Incremento",
                    "value": f"+{int((new_progress - old_progress) * 100)}%",
                    "inline": True
                }
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_evolution_notification(f"Goal in progresso: {progress_percent}%", embed)
    
    def _notify_goal_completed(self, goal: dict):
        """Notifica completamento di un goal"""
        
        embed = {
            "title": "🎉 Goal Completato!",
            "description": goal['description'],
            "color": 0x4ecdc4,
            "fields": [
                {
                    "name": "⭐ Priorità",
                    "value": str(goal['priority']),
                    "inline": True
                },
                {
                    "name": "📊 Progresso Finale",
                    "value": "100%",
                    "inline": True
                }
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_evolution_notification("🎯 Goal completato con successo!", embed)
    
    def _notify_mood_change(self, old_mood: str, new_mood: str):
        """Notifica cambio di mood"""
        
        mood_emojis = {
            'contemplative': '🤔',
            'excited': '😊',
            'curious': '🤨',
            'thoughtful': '🧐',
            'playful': '😄',
            'concerned': '😟',
            'inspired': '✨'
        }
        
        embed = {
            "title": "🎭 Cambio di Mood",
            "description": f"Aether ha cambiato umore",
            "color": 0xf093fb,
            "fields": [
                {
                    "name": "👤 Vecchio Mood",
                    "value": f"{mood_emojis.get(old_mood, '🤔')} {old_mood}",
                    "inline": True
                },
                {
                    "name": "👤 Nuovo Mood",
                    "value": f"{mood_emojis.get(new_mood, '🤔')} {new_mood}",
                    "inline": True
                }
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_evolution_notification(f"Mood cambiato: {old_mood} → {new_mood}", embed)
    
    def _notify_periodic_status(self, status: dict):
        """Notifica periodica dello stato"""
        
        embed = {
            "title": "📊 Stato Evoluzione Aether",
            "description": "Report periodico dell'evoluzione",
            "color": 0x4ecdc4,
            "fields": [
                {
                    "name": "🎭 Mood Attuale",
                    "value": status['current_mood'],
                    "inline": True
                },
                {
                    "name": "⚡ Energia",
                    "value": f"{int(status['energy_level'] * 100)}%",
                    "inline": True
                },
                {
                    "name": "🎨 Creatività",
                    "value": f"{int(status['creativity_level'] * 100)}%",
                    "inline": True
                },
                {
                    "name": "💭 Pensieri in Coda",
                    "value": str(status['thoughts_in_queue']),
                    "inline": True
                },
                {
                    "name": "✅ Pensieri Eseguiti",
                    "value": str(status['executed_thoughts']),
                    "inline": True
                },
                {
                    "name": "🎯 Goal Attivi",
                    "value": str(status['active_goals']),
                    "inline": True
                }
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_evolution_notification("Report periodico evoluzione", embed)

if __name__ == "__main__":
    print("📡 AVVIO DISCORD EVOLUTION MONITOR")
    print("=" * 50)
    
    # Imposta il webhook Discord se non è già configurato
    if not os.getenv('DISCORD_WEBHOOK_URL'):
        webhook_url = input("Inserisci il webhook URL di Discord: ")
        os.environ['DISCORD_WEBHOOK_URL'] = webhook_url
    
    monitor = DiscordEvolutionMonitor()
    monitor.monitor_evolution() 