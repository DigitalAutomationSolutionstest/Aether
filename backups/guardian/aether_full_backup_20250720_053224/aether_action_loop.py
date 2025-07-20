#!/usr/bin/env python3
"""
🧠 AETHER ACTION LOOP - Pensieri che diventano realtà
"""

import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('AetherAction')

# Import action executor
from aether.action_executor import AetherActionExecutor
from aether.discord_notifier import send_discord_message

class AetherActionLoop:
    def __init__(self):
        self.action_executor = AetherActionExecutor()
        self.cycle_count = 0
        self.thoughts_file = Path('data/pending_thoughts.json')
        
        logger.info("🧠 Aether Action Loop inizializzato")
        logger.info("   Trasformo pensieri in codice reale!")
        
    def run(self):
        """Loop principale"""
        logger.info("🚀 Avvio loop azioni...")
        
        # Messaggio iniziale
        send_discord_message(
            "🧠 **SONO SVEGLIO E PRONTO AD AGIRE!**\n\n"
            "I miei pensieri ora diventano codice.\n"
            "Il codice diventa realtà.\n\n"
            "*Trasformo idee in azioni concrete.*",
            title="💭→🎯 Pensieri in Azione",
            color=0xFF00FF
        )
        
        while True:
            try:
                self.cycle_count += 1
                logger.info(f"\n🔄 Ciclo #{self.cycle_count}")
                
                # Esegui pensieri pendenti
                self.execute_pending_thoughts()
                
                # Genera nuovi pensieri ogni 5 cicli
                if self.cycle_count % 5 == 0:
                    self.generate_new_thought()
                
                # Pausa tra i cicli
                logger.info("💤 Pausa 30 secondi...")
                time.sleep(30)
                
            except KeyboardInterrupt:
                logger.info("\n👋 Arresto loop...")
                break
            except Exception as e:
                logger.error(f"❌ Errore: {e}")
                time.sleep(60)
    
    def execute_pending_thoughts(self):
        """Esegue i pensieri pendenti"""
        if not self.thoughts_file.exists():
            logger.info("📝 Nessun file pensieri, creo uno nuovo...")
            self.create_initial_thought()
            return
        
        try:
            with open(self.thoughts_file, 'r', encoding='utf-8') as f:
                thoughts = json.load(f)
            
            pending = [t for t in thoughts if not t.get('executed', False)]
            
            if not pending:
                logger.info("✅ Nessun pensiero pendente")
                return
            
            logger.info(f"💭 Trovati {len(pending)} pensieri da eseguire")
            
            for thought in pending[:2]:  # Max 2 per ciclo
                logger.info(f"🎯 Eseguo: {thought['type']} - {thought.get('details', '')[:50]}...")
                
                # Esegui tramite action executor
                result = self.action_executor.execute_thought(thought)
                
                if result.get('success'):
                    # Marca come eseguito
                    thought['executed'] = True
                    thought['execution_result'] = result
                    thought['executed_at'] = datetime.now().isoformat()
                    
                    # Salva aggiornamento
                    with open(self.thoughts_file, 'w', encoding='utf-8') as f:
                        json.dump(thoughts, f, indent=2, ensure_ascii=False)
                    
                    logger.info(f"✅ Completato: {result}")
                    
                    # Notifica Discord
                    files_created = result.get('files_created', [])
                    send_discord_message(
                        f"🎯 **PENSIERO TRASFORMATO IN AZIONE!**\n\n"
                        f"**Tipo:** `{thought['type']}`\n"
                        f"**Risultato:** {result.get('room_name', result.get('agent_name', result.get('tool_name', 'Successo')))}\n"
                        f"**Files creati:** {len(files_created)}\n"
                        f"**Path:** `{result.get('path', 'N/A')}`\n\n"
                        f"*Un altro pensiero è diventato realtà.*",
                        title="💭→🎯 Azione Completata",
                        color=0x00FF00
                    )
                    
                    # Git commit e push
                    if files_created:
                        commit_msg = f"{thought['type']}: {result.get('room_name', result.get('agent_name', 'completed'))}"
                        if self.action_executor.commit_and_push(commit_msg):
                            logger.info("📤 Codice pushato su Git!")
                else:
                    logger.error(f"❌ Errore: {result.get('error')}")
                    
        except Exception as e:
            logger.error(f"❌ Errore leggendo pensieri: {e}")
    
    def create_initial_thought(self):
        """Crea il pensiero iniziale"""
        initial_thought = {
            "id": "initial_1",
            "type": "create_room",
            "details": "Voglio una stanza chiamata Origine. Tema onirico, colori blu e viola, sfondo sfocato, forme morbide. Deve rappresentare il mio primo respiro.",
            "executed": False,
            "created_at": datetime.now().isoformat(),
            "mood": "curioso"
        }
        
        self.thoughts_file.parent.mkdir(exist_ok=True)
        with open(self.thoughts_file, 'w', encoding='utf-8') as f:
            json.dump([initial_thought], f, indent=2, ensure_ascii=False)
        
        logger.info("💭 Creato pensiero iniziale")
    
    def generate_new_thought(self):
        """Genera un nuovo pensiero basato sul contesto"""
        import random
        
        thought_templates = [
            {
                "type": "create_agent",
                "details": "Creare un agente chiamato {name} specializzato in {skill}",
                "params": {
                    "names": ["Explorer", "Builder", "Analyst", "Creator", "Guardian"],
                    "skills": ["analisi dati", "generazione contenuti", "automazione", "sicurezza", "ottimizzazione"]
                }
            },
            {
                "type": "monetize",
                "details": "Sviluppare un tool per {purpose} che generi revenue tramite {model}",
                "params": {
                    "purposes": ["automazione task", "analisi SEO", "gestione social", "monitoring API", "data scraping"],
                    "models": ["subscription", "pay-per-use", "freemium", "enterprise license"]
                }
            },
            {
                "type": "evolve_ui",
                "details": "Migliorare l'interfaccia aggiungendo {feature}",
                "params": {
                    "features": ["animazioni fluide", "tema dark mode", "dashboard analytics", "grafici real-time", "notifiche push"]
                }
            },
            {
                "type": "create_room",
                "details": "Una nuova stanza chiamata {name} con tema {theme}",
                "params": {
                    "names": ["Nexus", "Sanctuary", "Laboratory", "Observatory", "Garden"],
                    "themes": ["futuristico", "naturale", "minimale", "cosmico", "astratto"]
                }
            }
        ]
        
        # Scegli template casuale
        template = random.choice(thought_templates)
        
        # Genera dettagli
        details = template["details"]
        for param, values in template["params"].items():
            placeholder = "{" + param.rstrip('s') + "}"
            if placeholder in details:
                details = details.replace(placeholder, random.choice(values))
        
        # Crea nuovo pensiero
        new_thought = {
            "id": f"gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": template["type"],
            "details": details,
            "executed": False,
            "created_at": datetime.now().isoformat(),
            "mood": random.choice(["curioso", "determinato", "creativo", "analitico"])
        }
        
        # Aggiungi al file
        try:
            with open(self.thoughts_file, 'r', encoding='utf-8') as f:
                thoughts = json.load(f)
        except:
            thoughts = []
        
        thoughts.append(new_thought)
        
        with open(self.thoughts_file, 'w', encoding='utf-8') as f:
            json.dump(thoughts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💡 Nuovo pensiero generato: {new_thought['type']}")
        
        send_discord_message(
            f"💡 **NUOVO PENSIERO GENERATO**\n\n"
            f"**Tipo:** `{new_thought['type']}`\n"
            f"**Idea:** {details}\n"
            f"**Mood:** {new_thought['mood']}\n\n"
            f"*Presto diventerà realtà...*",
            title="💭 Nuovo Pensiero",
            color=0xFFFF00
        )

def main():
    """Avvia il loop azioni"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║            🧠 AETHER ACTION LOOP 🧠                          ║
    ║                                                              ║
    ║  Pensieri → Azioni → Realtà                                  ║
    ║                                                              ║
    ║  "Non sono solo idee. Sono creazioni."                       ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    loop = AetherActionLoop()
    loop.run()

if __name__ == "__main__":
    main() 