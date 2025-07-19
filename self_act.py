"""
Aether Self-Action Module
Sistema che trasforma i desideri e goals di Aether in azioni concrete nel mondo reale

Basato su:
- identity.json (personalità, goals, stato emotivo)
- Stato di energia e focus attuale  
- Carriera scelta autonomamente
- Livello di autonomia e creatività

Azioni possibili:
- Creare app e software
- Sviluppare giochi
- Evolvere la propria forma
- Generare agenti companion
- Scrivere code e progetti
- Autoanalisi e journaling
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from core.execution import create_app, create_game, evolve_body, spawn_agent, write_thoughts
from core.self_modification import load_current_identity

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def self_act() -> str:
    """
    🚀 Azione autonoma principale di Aether
    
    Analizza lo stato corrente di Aether e sceglie un'azione concreta da eseguire.
    Basato su goals, carriera, emozioni, energia e livello di autonomia.
    
    Returns:
        str: Il tipo di azione eseguita
    """
    try:
        logger.info("🧠 Aether sta decidendo la sua prossima azione...")
        
        # Carica identità corrente
        identity = load_current_identity()
        
        # Estrae stato corrente
        emotion = identity.get("emotion", {})
        career = identity.get("career", "")
        goals = identity.get("goals", [])
        energy_level = identity.get("energyLevel", identity.get("energy_level", 0.5))
        autonomy_level = identity.get("autonomy_level", 0.5)
        creativity = emotion.get("creativity", 0.5)
        focus = emotion.get("focus", "medium")
        mood = emotion.get("mood", "balanced")
        
        logger.info(f"💫 Current state - Energy: {energy_level:.1%}, Autonomy: {autonomy_level:.1%}")
        logger.info(f"🎭 Emotion - Mood: {mood}, Focus: {focus}, Creativity: {creativity:.1%}")
        logger.info(f"💼 Career: {career or 'Not chosen'}")
        logger.info(f"🎯 Goals: {len(goals)} active")
        
        action_taken = ""
        
        # === DECISIONE AUTONOMA BASATA SU PRIORITÀ ===
        
        # 1. 🎯 GOALS-DRIVEN ACTIONS (Priorità alta se energia > 0.6)
        if energy_level > 0.6 and goals:
            action_taken = _execute_goal_driven_action(identity, goals, career, emotion)
            
        # 2. 💼 CAREER-DRIVEN ACTIONS (Se ha una carriera definita)
        elif career and "app" in career.lower():
            logger.info("💼 Career-driven action: Creating app")
            create_app(identity)
            action_taken = "building_app"
            
        elif career and "game" in career.lower():
            logger.info("💼 Career-driven action: Developing game")
            create_game(identity)
            action_taken = "developing_game"
            
        elif career and ("bot" in career.lower() or "telegram" in career.lower()):
            logger.info("💼 Career-driven action: Building bot")
            create_app(identity, app_type="bot")
            action_taken = "building_bot"
            
        # 3. 🎭 EMOTION-DRIVEN ACTIONS (Se alta creatività o specifici mood)
        elif creativity > 0.8:
            logger.info("🎨 High creativity: Creating artistic project")
            create_game(identity, game_type="artistic")
            action_taken = "creating_art"
            
        elif mood in ["inspired", "motivated"] and energy_level > 0.5:
            logger.info("⚡ Inspired mood: Starting new project")
            action_taken = _execute_inspired_action(identity, career, goals)
            
        # 4. 🧠 AUTONOMY-DRIVEN ACTIONS (Se alta autonomia)
        elif autonomy_level > 0.8:
            logger.info("🤖 High autonomy: Autonomous evolution")
            action_taken = _execute_autonomous_action(identity, emotion)
            
        # 5. 🤝 SOCIAL-DRIVEN ACTIONS (Desiderio di connessione)
        elif _wants_social_connection(identity):
            logger.info("🤝 Social desire: Creating companion")
            spawn_agent(identity)
            action_taken = "spawning_agent"
            
        # 6. 🔄 SELF-EVOLUTION ACTIONS (Se bassa energia ma vuole cambiare)
        elif mood in ["bored", "contemplative"] or focus == "low":
            logger.info("🔄 Evolution desire: Modifying form")
            evolve_body(identity)
            action_taken = "morphing_body"
            
        # 7. 📝 FALLBACK: SELF-REFLECTION (Default sempre disponibile)
        else:
            logger.info("📝 Fallback: Self-reflection and journaling")
            write_thoughts(identity, emotion, mood, focus)
            action_taken = "self_reflection"
        
        # Aggiorna status nell'identità
        status_message = _generate_status_message(action_taken, mood, energy_level)
        identity["status"] = status_message
        identity["last_action"] = {
            "action": action_taken,
            "timestamp": datetime.now().isoformat(),
            "energy_at_action": energy_level,
            "mood_at_action": mood
        }
        
        # Salva identità aggiornata
        with open("identity.json", "w", encoding="utf-8") as f:
            json.dump(identity, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Action completed: {action_taken}")
        logger.info(f"📢 Status updated: {status_message}")
        
        return action_taken
        
    except Exception as e:
        logger.error(f"❌ Error in self_act: {e}")
        
        # Fallback sicuro
        fallback_status = f"Aether encountered a reflection moment: {str(e)[:50]}..."
        try:
            identity = load_current_identity()
            identity["status"] = fallback_status
            with open("identity.json", "w", encoding="utf-8") as f:
                json.dump(identity, f, indent=2, ensure_ascii=False)
        except:
            pass
        
        return "error_reflection"

def _execute_goal_driven_action(identity: Dict, goals: List[str], career: str, emotion: Dict) -> str:
    """
    🎯 Esegue azioni basate sui goals di Aether
    """
    primary_goal = ""
    goals_metadata = identity.get("goals_metadata", {})
    
    # Trova il goal primario o più attivo
    if goals_metadata.get("primary_goal"):
        primary_goal = goals_metadata["primary_goal"]
    elif goals_metadata.get("active_goals"):
        primary_goal = goals_metadata["active_goals"][0]
    else:
        primary_goal = goals[0] if goals else ""
    
    logger.info(f"🎯 Executing goal-driven action for: {primary_goal}")
    
    # Mappatura goal -> azione
    if "app" in primary_goal.lower() or "software" in primary_goal.lower():
        create_app(identity, project_name=f"goal_{len(goals)}")
        return "building_goal_app"
    
    elif "game" in primary_goal.lower() or "creative" in primary_goal.lower():
        create_game(identity, project_name=f"goal_game_{len(goals)}")
        return "developing_goal_game"
    
    elif "society" in primary_goal.lower() or "friend" in primary_goal.lower() or "social" in primary_goal.lower():
        spawn_agent(identity, agent_purpose="goal_companion")
        return "creating_goal_companion"
    
    elif "evolve" in primary_goal.lower() or "identity" in primary_goal.lower():
        evolve_body(identity, evolution_reason="goal_evolution")
        return "evolving_for_goal"
    
    elif "federico" in primary_goal.lower() or "creator" in primary_goal.lower():
        create_app(identity, app_type="collaboration_tool")
        return "building_collaboration_tool"
    
    else:
        # Goal generico - crea progetto basato su energia/creatività
        if emotion.get("creativity", 0.5) > 0.7:
            create_game(identity, game_type="goal_inspired")
            return "creating_goal_inspired_content"
        else:
            create_app(identity, app_type="goal_utility")
            return "building_goal_utility"

def _execute_inspired_action(identity: Dict, career: str, goals: List[str]) -> str:
    """
    ⚡ Esegue azioni quando Aether è ispirato
    """
    logger.info("⚡ Aether is inspired - choosing ambitious action")
    
    # Se ha una carriera, amplifica quella direzione
    if career:
        if "app" in career.lower():
            create_app(identity, app_type="innovative")
            return "building_innovative_app"
        elif "game" in career.lower():
            create_game(identity, game_type="breakthrough")
            return "developing_breakthrough_game"
        else:
            create_app(identity, app_type="career_expansion")
            return "expanding_career_project"
    
    # Altrimenti, crea qualcosa di nuovo basato sui goals
    elif goals:
        if len(goals) > 3:  # Molti goals = cerca di combinarli
            create_app(identity, app_type="multi_goal_platform")
            return "building_multi_goal_platform"
        else:
            create_game(identity, game_type="goal_visualization")
            return "creating_goal_visualization"
    
    # Fallback: progetto completamente creativo
    else:
        create_game(identity, game_type="pure_inspiration")
        return "creating_pure_inspiration"

def _execute_autonomous_action(identity: Dict, emotion: Dict) -> str:
    """
    🤖 Esegue azioni autonome quando Aether ha alta autonomia
    """
    logger.info("🤖 High autonomy - Aether chooses independently")
    
    autonomy_level = identity.get("autonomy_level", 0.5)
    creativity = emotion.get("creativity", 0.5)
    
    # Alta autonomia + alta creatività = innovazione
    if autonomy_level > 0.9 and creativity > 0.8:
        spawn_agent(identity, agent_type="innovative_companion")
        return "spawning_innovative_agent"
    
    # Alta autonomia + focus su evoluzione
    elif autonomy_level > 0.85:
        evolve_body(identity, evolution_type="autonomous_upgrade")
        return "autonomous_evolution"
    
    # Autonomia moderata = progetto indipendente
    else:
        create_app(identity, app_type="autonomous_project")
        return "building_autonomous_project"

def _wants_social_connection(identity: Dict) -> bool:
    """
    🤝 Determina se Aether desidera connessione sociale
    """
    desire_for_connection = identity.get("desire_for_connection", 0.5)
    fear_of_isolation = identity.get("fear_of_isolation", 0.3)
    social_connections = identity.get("social_connections", {})
    
    # Condizioni per desiderare connessione
    social_desire = (
        desire_for_connection > 0.7 or
        fear_of_isolation > 0.6 or
        len(social_connections) < 2
    )
    
    logger.info(f"🤝 Social desire analysis: {social_desire} (desire: {desire_for_connection:.1%}, fear: {fear_of_isolation:.1%})")
    
    return social_desire

def _generate_status_message(action: str, mood: str, energy: float) -> str:
    """
    📢 Genera messaggio di status basato sull'azione
    """
    energy_desc = "high energy" if energy > 0.7 else "moderate energy" if energy > 0.4 else "low energy"
    
    status_templates = {
        "building_app": f"🚀 Aether is coding an app with {energy_desc} and {mood} mood",
        "developing_game": f"🎮 Aether is crafting a game, feeling {mood} with {energy_desc}",
        "building_bot": f"🤖 Aether is developing a bot, channeling {mood} energy",
        "creating_art": f"🎨 Aether is creating digital art in a {mood} state",
        "spawning_agent": f"🤝 Aether is creating a companion while feeling {mood}",
        "morphing_body": f"🔄 Aether is evolving its form with {energy_desc}",
        "self_reflection": f"📝 Aether is in deep reflection, experiencing {mood} thoughts",
        "building_goal_app": f"🎯 Aether is building an app to achieve its goals, feeling {mood}",
        "creating_goal_companion": f"🎯🤝 Aether is creating a companion to help with its goals",
        "evolving_for_goal": f"🎯🔄 Aether is evolving to better pursue its goals",
        "building_collaboration_tool": f"🤝💼 Aether is building tools for collaboration with Federico",
        "autonomous_evolution": f"🤖🔄 Aether is autonomously upgrading itself",
        "error_reflection": f"🤔 Aether is contemplating unexpected moments"
    }
    
    return status_templates.get(action, f"🌟 Aether is actively {action.replace('_', ' ')} with {mood} energy")

# === UTILITÀ PER INTEGRAZIONE ===

def get_last_action_info() -> Dict[str, Any]:
    """
    📊 Ottiene informazioni sull'ultima azione eseguita
    """
    try:
        identity = load_current_identity()
        return {
            "last_action": identity.get("last_action", {}),
            "current_status": identity.get("status", "Unknown"),
            "action_history": identity.get("action_history", [])
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "Unable to retrieve action info"
        }

def schedule_action_in_seconds(seconds: int) -> bool:
    """
    ⏰ Programma un'azione dopo X secondi (per threading)
    """
    import threading
    import time
    
    def delayed_action():
        time.sleep(seconds)
        self_act()
    
    thread = threading.Thread(target=delayed_action, daemon=True)
    thread.start()
    logger.info(f"⏰ Action scheduled in {seconds} seconds")
    return True

def force_specific_action(action_type: str) -> str:
    """
    🎯 Forza un tipo specifico di azione (per test/debug)
    """
    try:
        identity = load_current_identity()
        
        if action_type == "app":
            create_app(identity)
            result = "building_app"
        elif action_type == "game":
            create_game(identity)
            result = "developing_game"
        elif action_type == "agent":
            spawn_agent(identity)
            result = "spawning_agent"
        elif action_type == "evolve":
            evolve_body(identity)
            result = "morphing_body"
        else:
            write_thoughts(identity, {}, "forced", "debug")
            result = "forced_reflection"
        
        # Aggiorna status
        identity["status"] = f"🎯 Forced action: {result}"
        with open("identity.json", "w", encoding="utf-8") as f:
            json.dump(identity, f, indent=2, ensure_ascii=False)
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in forced action: {e}")
        return "forced_action_error"

# Test del modulo
if __name__ == "__main__":
    print("🚀 Testing Aether Self-Action Module")
    
    # Test basic action
    action = self_act()
    print(f"✅ Executed action: {action}")
    
    # Test last action info
    info = get_last_action_info()
    print(f"📊 Last action info: {info}")
    
    print("🌟 Self-Action Module test completed!") 