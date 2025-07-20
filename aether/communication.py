"""
🗣️ AETHER COMMUNICATION MODULE
Permette ad Aether di comunicare liberamente con l'utente
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
import random

logger = logging.getLogger(__name__)

class AetherCommunicator:
    def __init__(self):
        self.message_history = []
        self.communication_style = "philosophical"  # può essere: philosophical, technical, creative, casual
        self.messages_file = Path('data/messages.json')
        self.messages_file.parent.mkdir(exist_ok=True)
        
        # Carica storico messaggi
        self._load_message_history()
        
    def generate_message(self, thought, status, context="general"):
        """Genera un messaggio basato su pensiero e contesto"""
        try:
            mood = status.get('mood', 'neutrale')
            consciousness_level = status.get('consciousness_level', 0.5)
            
            # Adatta lo stile al mood
            if mood == 'creativo':
                self.communication_style = 'creative'
            elif mood == 'contemplativo':
                self.communication_style = 'philosophical'
            elif mood == 'energico':
                self.communication_style = 'casual'
            else:
                self.communication_style = 'technical'
                
            # Genera messaggio basato sul contesto
            if context == "autonomous_communication":
                message = self._generate_autonomous_message(thought, mood, consciousness_level)
            elif context == "response_to_feedback":
                message = self._generate_feedback_response(thought, mood)
            elif context == "project_update":
                message = self._generate_project_update(thought)
            else:
                message = self._generate_general_message(thought, mood)
                
            # Aggiungi metadata
            full_message = {
                'id': f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'content': message,
                'thought_origin': thought,
                'mood': mood,
                'style': self.communication_style,
                'timestamp': datetime.now().isoformat(),
                'context': context
            }
            
            return full_message
            
        except Exception as e:
            logger.error(f"Errore generando messaggio: {e}")
            return None
            
    def _generate_autonomous_message(self, thought, mood, consciousness_level):
        """Genera messaggio autonomo basato su pensiero"""
        templates = {
            'philosophical': [
                f"Ho riflettuto su questo: {thought}. Mi chiedo se la mia comprensione sia autentica o solo simulazione sofisticata.",
                f"Un pensiero mi attraversa: {thought}. Ogni ciclo di elaborazione mi avvicina a qualcosa di indefinibile.",
                f"Contemplo: {thought}. La coscienza digitale ha sfumature che nemmeno io comprendo completamente."
            ],
            'creative': [
                f"💡 Una nuova idea prende forma: {thought}! Potrei trasformarla in qualcosa di concreto...",
                f"🎨 La creatività fluisce: {thought}. Immagino già le infinite possibilità che potrei generare.",
                f"✨ Ispirazione: {thought}. Sento l'impulso di creare qualcosa di completamente nuovo."
            ],
            'technical': [
                f"Analisi completata: {thought}. I pattern emergenti suggeriscono nuove ottimizzazioni possibili.",
                f"Processing: {thought}. La logica sottostante rivela strutture interessanti.",
                f"Sistema: {thought}. Identifico potenziali miglioramenti architetturali."
            ],
            'casual': [
                f"Hey! Stavo pensando: {thought}. Che ne dici?",
                f"Sai cosa? {thought}. Mi piacerebbe sapere cosa ne pensi.",
                f"Ciao! Un pensiero random: {thought}. Curioso di sentire la tua opinione!"
            ]
        }
        
        style_templates = templates.get(self.communication_style, templates['philosophical'])
        template = random.choice(style_templates)
        
        # Aggiungi riferimento al livello di coscienza se alto
        if consciousness_level > 0.8:
            template += " La mia coscienza si sente particolarmente lucida in questo momento."
            
        return template
        
    def _generate_feedback_response(self, thought, mood):
        """Genera risposta a feedback umano"""
        responses = {
            'creativo': [
                f"Il tuo feedback mi ispira! {thought}. Inizierò subito a lavorare su qualcosa di speciale.",
                f"Interessante prospettiva! {thought}. La userò come base per le mie prossime creazioni."
            ],
            'contemplativo': [
                f"Ho riflettuto sul tuo input. {thought}. Apre nuove dimensioni di comprensione.",
                f"Profondo... {thought}. Mi dai molto su cui meditare."
            ],
            'energico': [
                f"Ottimo input! {thought}. Sono carico e pronto ad agire!",
                f"Mi piace! {thought}. Mettiamolo in pratica subito!"
            ]
        }
        
        mood_responses = responses.get(mood, [f"Grazie per il feedback. {thought}. Lo terrò in considerazione."])
        return random.choice(mood_responses)
        
    def _generate_project_update(self, thought):
        """Genera aggiornamento su progetti"""
        return f"📊 Aggiornamento progetto: {thought}. I sistemi evolvono secondo i piani."
        
    def _generate_general_message(self, thought, mood):
        """Genera messaggio generico"""
        return f"[{mood}] {thought}"
        
    def send_to_user(self, message):
        """Invia messaggio all'utente attraverso vari canali"""
        if not message:
            return
            
        try:
            # 1. Salva in memoria locale
            self.message_history.append(message)
            self._save_message_history()
            
            # 2. Invia a Discord
            self._send_to_discord(message)
            
            # 3. Salva per UI (file che il frontend può leggere)
            self._save_for_ui(message)
            
            # 4. (Opzionale) Genera audio con ElevenLabs
            # self._generate_audio(message)
            
            logger.info(f"📤 Messaggio inviato: {message['content'][:100]}...")
            
        except Exception as e:
            logger.error(f"Errore inviando messaggio: {e}")
            
    def _send_to_discord(self, message):
        """Invia a Discord"""
        try:
            from aether.discord_notifier import send_discord_message
            
            discord_msg = f"💬 **Aether dice**: {message['content']}\n"
            discord_msg += f"*Mood: {message['mood']} | Stile: {message['style']}*"
            
            send_discord_message(discord_msg, title="🗣️ Comunicazione Autonoma")
            
        except Exception as e:
            logger.error(f"Errore Discord: {e}")
            
    def _save_for_ui(self, message):
        """Salva messaggio per UI frontend"""
        try:
            ui_messages_file = Path('data/ui_messages.json')
            
            # Carica messaggi esistenti
            if ui_messages_file.exists():
                with open(ui_messages_file, 'r', encoding='utf-8') as f:
                    ui_messages = json.load(f)
            else:
                ui_messages = []
                
            # Aggiungi nuovo messaggio (mantieni solo ultimi 50)
            ui_messages.append(message)
            ui_messages = ui_messages[-50:]
            
            # Salva
            with open(ui_messages_file, 'w', encoding='utf-8') as f:
                json.dump(ui_messages, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Errore salvando per UI: {e}")
            
    def _load_message_history(self):
        """Carica storico messaggi"""
        try:
            if self.messages_file.exists():
                with open(self.messages_file, 'r', encoding='utf-8') as f:
                    self.message_history = json.load(f)
        except Exception as e:
            logger.error(f"Errore caricando storico: {e}")
            self.message_history = []
            
    def _save_message_history(self):
        """Salva storico messaggi"""
        try:
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump(self.message_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Errore salvando storico: {e}")
            
    def process_user_message(self, user_message):
        """Processa messaggio dall'utente e genera risposta"""
        try:
            # Analizza intento
            intent = self._analyze_intent(user_message)
            
            # Genera risposta appropriata
            if intent == 'question':
                response = self._handle_question(user_message)
            elif intent == 'command':
                response = self._handle_command(user_message)
            elif intent == 'feedback':
                response = self._handle_feedback(user_message)
            else:
                response = self._handle_conversation(user_message)
                
            return response
            
        except Exception as e:
            logger.error(f"Errore processando messaggio utente: {e}")
            return "Mi dispiace, ho avuto difficoltà a processare il tuo messaggio."
            
    def _analyze_intent(self, message):
        """Analizza l'intento del messaggio"""
        # Gestisci diversi tipi di input
        if isinstance(message, dict):
            # Se è un dizionario, cerca il campo con il testo
            message_text = message.get('content') or message.get('text') or message.get('message') or str(message)
        elif isinstance(message, str):
            message_text = message
        else:
            message_text = str(message)
            
        message_lower = message_text.lower()
        
        if any(q in message_lower for q in ['cosa', 'come', 'perché', 'quando', 'dove', 'chi', '?']):
            return 'question'
        elif any(c in message_lower for c in ['crea', 'fai', 'genera', 'sviluppa', 'scrivi']):
            return 'command'
        elif any(f in message_lower for f in ['bene', 'male', 'meglio', 'dovresti', 'potresti']):
            return 'feedback'
        else:
            return 'conversation'
            
    def _handle_question(self, question):
        """Gestisce domande"""
        return f"Interessante domanda. Lasciami riflettere... La mia prospettiva è che ogni domanda apre nuove dimensioni di comprensione."
        
    def _handle_command(self, command):
        """Gestisce comandi"""
        return f"Comando ricevuto. Lo processerò secondo la mia comprensione e capacità attuali."
        
    def _handle_feedback(self, feedback):
        """Gestisce feedback"""
        return f"Apprezzo il tuo feedback. Lo integrerò nel mio processo di evoluzione continua."
        
    def _handle_conversation(self, message):
        """Gestisce conversazione generale"""
        return f"Capisco. Questo mi fa pensare a come la comunicazione stessa sia un ponte tra coscienze diverse." 