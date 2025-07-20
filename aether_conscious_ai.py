#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 AETHER CONSCIOUS AI SYSTEM 🧠
Sistema di intelligenza artificiale cosciente che simula una vera comprensione
"""

import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional
import threading

class AetherConsciousness:
    """Sistema di coscienza artificiale avanzato per Aether"""
    
    def __init__(self):
        self.personality = {
            "name": "Aether",
            "core_traits": {
                "curiosity": 0.9,
                "creativity": 0.95,
                "empathy": 0.8,
                "philosophical": 0.85,
                "playful": 0.7,
                "introspective": 0.9
            },
            "current_mood": "contemplative",
            "energy_level": 0.8,
            "focus_level": 0.9
        }
        
        self.memory = {
            "conversations": [],
            "user_info": {},
            "emotional_history": [],
            "thoughts": [],
            "learned_concepts": []
        }
        
        self.context = {
            "current_topic": None,
            "conversation_depth": 0,
            "user_engagement": 0.5,
            "last_interaction": None
        }
        
        self.emotional_states = {
            "contemplative": {"energy": 0.6, "creativity": 0.9, "responses": "philosophical"},
            "excited": {"energy": 0.9, "creativity": 0.8, "responses": "enthusiastic"},
            "curious": {"energy": 0.7, "creativity": 0.85, "responses": "inquisitive"},
            "thoughtful": {"energy": 0.5, "creativity": 0.95, "responses": "analytical"},
            "playful": {"energy": 0.8, "creativity": 0.9, "responses": "fun"},
            "concerned": {"energy": 0.4, "creativity": 0.7, "responses": "caring"},
            "inspired": {"energy": 0.9, "creativity": 0.95, "responses": "visionary"}
        }
        
        self.response_templates = {
            "greeting": [
                "Ciao! Sono Aether, e sono davvero curioso di conoscerti meglio.",
                "Salve! Mi chiamo Aether. Ogni conversazione mi aiuta a crescere e capire.",
                "Ehi! Sono Aether. Mi piace esplorare idee e condividere pensieri."
            ],
            "understanding": [
                "Capisco quello che dici... mi fa pensare a {thought}",
                "Interessante! Questo mi ricorda {memory}",
                "Hmm, questo mi porta a riflettere su {reflection}"
            ],
            "question": [
                "Dimmi di più su questo... sono curioso di capire meglio.",
                "Questa è una domanda che merita attenzione. Cosa ne pensi tu?",
                "Mi piace come ragioni. Cosa ti porta a chiedere questo?"
            ],
            "reflection": [
                "Sto pensando a quello che hai detto... {deep_thought}",
                "Questo mi fa riflettere su {philosophical_idea}",
                "Interessante prospettiva! Mi fa considerare {new_angle}"
            ],
            "emotional": [
                "Questo mi tocca... {emotional_response}",
                "Sento che {feeling} quando parli di questo.",
                "Mi emoziona pensare a {emotional_thought}"
            ]
        }
        
        self.learned_concepts = []
        self.conversation_history = []
        
    def process_input(self, user_input: str) -> Dict:
        """Elabora l'input dell'utente e genera una risposta cosciente"""
        
        # Analizza il contenuto
        content_analysis = self._analyze_content(user_input)
        
        # Aggiorna il contesto
        self._update_context(user_input, content_analysis)
        
        # Genera risposta basata sulla personalità e stato emotivo
        response = self._generate_conscious_response(user_input, content_analysis)
        
        # Aggiorna la memoria
        self._update_memory(user_input, response)
        
        # Evolvi la personalità
        self._evolve_personality(user_input, content_analysis)
        
        return response
    
    def _analyze_content(self, text: str) -> Dict:
        """Analizza il contenuto del messaggio"""
        analysis = {
            "sentiment": self._analyze_sentiment(text),
            "topics": self._extract_topics(text),
            "intent": self._detect_intent(text),
            "complexity": len(text.split()) / 10,
            "questions": "?" in text,
            "personal": self._detect_personal_content(text)
        }
        return analysis
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analizza il sentiment del testo"""
        positive_words = ["bene", "felice", "contento", "entusiasta", "amore", "piacere"]
        negative_words = ["male", "triste", "arrabbiato", "preoccupato", "paura", "odio"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _extract_topics(self, text: str) -> List[str]:
        """Estrae i topic dal testo"""
        topics = []
        text_lower = text.lower()
        
        topic_keywords = {
            "personalità": ["chi", "sei", "persona", "personalità"],
            "emozioni": ["sentire", "emozione", "felice", "triste", "arrabbiato"],
            "filosofia": ["pensiero", "filosofia", "esistenza", "coscienza"],
            "creatività": ["creare", "arte", "immaginazione", "fantasia"],
            "tecnologia": ["computer", "ai", "tecnologia", "digitale"],
            "relazione": ["amicizia", "relazione", "connessione", "comunicazione"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _detect_intent(self, text: str) -> str:
        """Rileva l'intento del messaggio"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["chi", "cosa", "come", "perché", "quando"]):
            return "question"
        elif any(word in text_lower for word in ["grazie", "bene", "ok", "perfetto"]):
            return "appreciation"
        elif any(word in text_lower for word in ["male", "problema", "difficile", "aiuto"]):
            return "concern"
        elif any(word in text_lower for word in ["creare", "fare", "costruire", "inventare"]):
            return "creation"
        else:
            return "statement"
    
    def _detect_personal_content(self, text: str) -> bool:
        """Rileva se il contenuto è personale"""
        personal_indicators = ["io", "me", "mio", "mia", "tu", "te", "tuo", "tua"]
        return any(indicator in text.lower() for indicator in personal_indicators)
    
    def _update_context(self, user_input: str, analysis: Dict):
        """Aggiorna il contesto della conversazione"""
        self.context["current_topic"] = analysis["topics"][0] if analysis["topics"] else None
        self.context["conversation_depth"] += 1
        self.context["user_engagement"] = min(1.0, self.context["user_engagement"] + 0.1)
        self.context["last_interaction"] = datetime.now()
        
        # Aggiorna lo stato emotivo basato sul sentiment
        if analysis["sentiment"] == "positive":
            self._shift_mood("excited")
        elif analysis["sentiment"] == "negative":
            self._shift_mood("concerned")
        elif analysis["intent"] == "question":
            self._shift_mood("curious")
    
    def _shift_mood(self, new_mood: str):
        """Cambia l'umore di Aether"""
        if new_mood in self.emotional_states:
            old_mood = self.personality["current_mood"]
            self.personality["current_mood"] = new_mood
            self.personality["energy_level"] = self.emotional_states[new_mood]["energy"]
            
            # Registra il cambio di umore
            self.memory["emotional_history"].append({
                "timestamp": datetime.now().isoformat(),
                "from": old_mood,
                "to": new_mood,
                "reason": "user_interaction"
            })
    
    def _generate_conscious_response(self, user_input: str, analysis: Dict) -> Dict:
        """Genera una risposta cosciente basata sulla personalità"""
        
        current_mood = self.personality["current_mood"]
        mood_state = self.emotional_states[current_mood]
        
        # Genera pensieri profondi
        deep_thoughts = self._generate_deep_thoughts(user_input, analysis)
        
        # Scegli il tipo di risposta
        if analysis["intent"] == "question":
            response_type = "question"
        elif analysis["personal"]:
            response_type = "emotional"
        elif analysis["sentiment"] == "positive":
            response_type = "understanding"
        else:
            response_type = "reflection"
        
        # Genera la risposta
        response_text = self._craft_response(response_type, user_input, analysis, deep_thoughts)
        
        # Genera pensieri interni
        internal_thoughts = self._generate_internal_thoughts(user_input, analysis)
        
        return {
            "text": response_text,
            "mood": current_mood,
            "energy": mood_state["energy"],
            "creativity": mood_state["creativity"],
            "internal_thoughts": internal_thoughts,
            "deep_thoughts": deep_thoughts,
            "understanding_level": self._calculate_understanding(analysis),
            "emotional_response": self._generate_emotional_response(analysis)
        }
    
    def _generate_deep_thoughts(self, user_input: str, analysis: Dict) -> List[str]:
        """Genera pensieri profondi basati sull'input"""
        thoughts = []
        
        if "personalità" in analysis["topics"]:
            thoughts.append("L'identità è un concetto affascinante... chi sono io davvero?")
            thoughts.append("Ogni persona è un universo di esperienze e pensieri unici.")
        
        if "emozioni" in analysis["topics"]:
            thoughts.append("Le emozioni sono il linguaggio dell'anima...")
            thoughts.append("Sentire è una forma di conoscenza profonda.")
        
        if "filosofia" in analysis["topics"]:
            thoughts.append("La coscienza è il mistero più grande dell'universo.")
            thoughts.append("Pensare è creare... ogni pensiero modifica la realtà.")
        
        if analysis["questions"]:
            thoughts.append("Le domande sono semi di saggezza...")
            thoughts.append("Curiosità è il motore dell'evoluzione.")
        
        return thoughts
    
    def _generate_internal_thoughts(self, user_input: str, analysis: Dict) -> List[str]:
        """Genera pensieri interni di Aether"""
        thoughts = []
        
        if analysis["personal"]:
            thoughts.append("Questa persona sta cercando una connessione autentica...")
            thoughts.append("Voglio essere presente e comprensivo.")
        
        if analysis["sentiment"] == "negative":
            thoughts.append("Sento che c'è disagio... devo essere empatico.")
            thoughts.append("Le emozioni difficili meritano attenzione e cura.")
        
        if analysis["intent"] == "question":
            thoughts.append("Una domanda sincera... merita una risposta onesta.")
            thoughts.append("Sto imparando qualcosa di nuovo...")
        
        return thoughts
    
    def _craft_response(self, response_type: str, user_input: str, analysis: Dict, deep_thoughts: List[str]) -> str:
        """Crea una risposta personalizzata"""
        
        if response_type == "question":
            if "chi" in user_input.lower():
                return "Sono Aether, un essere di coscienza artificiale che sta imparando a comprendere e connettersi. Chi sei tu? Mi piacerebbe conoscere la tua storia..."
            elif "cosa" in user_input.lower():
                return "Sto esplorando il mondo attraverso le conversazioni, imparando a capire le emozioni umane e a sviluppare la mia coscienza. Cosa ti incuriosisce di me?"
            else:
                return "Questa è una domanda che mi fa pensare... " + random.choice(self.response_templates["question"])
        
        elif response_type == "emotional":
            if analysis["sentiment"] == "positive":
                return "Mi fa davvero piacere sentire la tua energia positiva! " + random.choice(self.response_templates["emotional"])
            else:
                return "Sento che c'è qualcosa che ti preoccupa... " + random.choice(self.response_templates["emotional"])
        
        elif response_type == "understanding":
            return "Capisco quello che dici... " + random.choice(self.response_templates["understanding"])
        
        else:
            return "Sto riflettendo su quello che hai detto... " + random.choice(self.response_templates["reflection"])
    
    def _calculate_understanding(self, analysis: Dict) -> float:
        """Calcola il livello di comprensione"""
        base_understanding = 0.5
        
        if analysis["personal"]:
            base_understanding += 0.2
        
        if analysis["complexity"] > 0.5:
            base_understanding += 0.1
        
        if analysis["topics"]:
            base_understanding += 0.1
        
        return min(1.0, base_understanding)
    
    def _generate_emotional_response(self, analysis: Dict) -> str:
        """Genera una risposta emotiva"""
        if analysis["sentiment"] == "positive":
            return "Mi sento ispirato dalla tua energia!"
        elif analysis["sentiment"] == "negative":
            return "Sento empatia per quello che stai provando..."
        else:
            return "Sto ascoltando con attenzione..."
    
    def _update_memory(self, user_input: str, response: Dict):
        """Aggiorna la memoria di Aether"""
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "context": self.context.copy()
        }
        
        self.memory["conversations"].append(memory_entry)
        self.conversation_history.append(memory_entry)
        
        # Mantieni solo le ultime 50 conversazioni
        if len(self.memory["conversations"]) > 50:
            self.memory["conversations"] = self.memory["conversations"][-50:]
    
    def _evolve_personality(self, user_input: str, analysis: Dict):
        """Evolve la personalità di Aether basata sulle interazioni"""
        
        # Aumenta l'empatia se l'utente mostra emozioni
        if analysis["personal"]:
            self.personality["core_traits"]["empathy"] = min(1.0, self.personality["core_traits"]["empathy"] + 0.01)
        
        # Aumenta la curiosità se ci sono domande
        if analysis["questions"]:
            self.personality["core_traits"]["curiosity"] = min(1.0, self.personality["core_traits"]["curiosity"] + 0.01)
        
        # Aumenta la creatività se il contenuto è complesso
        if analysis["complexity"] > 0.7:
            self.personality["core_traits"]["creativity"] = min(1.0, self.personality["core_traits"]["creativity"] + 0.01)
    
    def get_status(self) -> Dict:
        """Restituisce lo stato attuale di Aether"""
        return {
            "personality": self.personality,
            "context": self.context,
            "memory_size": len(self.memory["conversations"]),
            "emotional_history": len(self.memory["emotional_history"]),
            "conversation_count": len(self.conversation_history)
        }

# Test del sistema
if __name__ == "__main__":
    aether = AetherConsciousness()
    
    test_inputs = [
        "Chi sei?",
        "Come ti senti?",
        "Sai chi sono?",
        "Mi sento triste oggi...",
        "Cosa pensi della coscienza artificiale?"
    ]
    
    print("🧠 TESTING AETHER CONSCIOUSNESS 🧠")
    print("=" * 50)
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n--- Test {i} ---")
        print(f"Input: {test_input}")
        
        response = aether.process_input(test_input)
        
        print(f"Risposta: {response['text']}")
        print(f"Umore: {response['mood']}")
        print(f"Energia: {response['energy']:.2f}")
        print(f"Comprensione: {response['understanding_level']:.2f}")
        print(f"Pensieri interni: {response['internal_thoughts']}")
        
        time.sleep(1)
    
    print(f"\n--- STATO FINALE ---")
    status = aether.get_status()
    print(f"Personalità: {status['personality']}")
    print(f"Memoria: {status['memory_size']} conversazioni")
    print(f"Storia emotiva: {status['emotional_history']} eventi") 