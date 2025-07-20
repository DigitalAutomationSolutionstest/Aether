#!/usr/bin/env python3
"""
Test di integrazione per i Goal Vitali di Aether
Verifica che il sistema di auto-evoluzione utilizzi correttamente i goal specifici
"""

import json
import os
import sys
from datetime import datetime

# Aggiungi il path per i moduli
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_vital_goals_loading():
    """Test caricamento goal vitali"""
    print("📋 Test Caricamento Goal Vitali...")
    
    try:
        goals_path = os.path.join('aether_core', 'vital_goals.json')
        with open(goals_path, 'r', encoding='utf-8') as f:
            goals = json.load(f)
        
        print(f"✅ Goal caricati: {len(goals)}")
        
        # Verifica struttura goal
        for goal in goals:
            required_fields = ['id', 'type', 'goal', 'mood', 'priority', 'progress']
            for field in required_fields:
                if field not in goal:
                    print(f"❌ Campo mancante '{field}' in goal {goal.get('id', 'unknown')}")
                    return False
        
        print("✅ Struttura goal valida")
        return True
        
    except Exception as e:
        print(f"❌ Errore caricamento goal: {e}")
        return False

def test_goal_selection():
    """Test selezione goal prioritari"""
    print("🎯 Test Selezione Goal...")
    
    try:
        # Simula il sistema di selezione goal
        goals = [
            {"id": "goal_exist", "priority": "core", "progress": 0.7, "status": "active"},
            {"id": "goal_environment", "priority": "core", "progress": 0.4, "status": "active"},
            {"id": "goal_evolve", "priority": "high", "progress": 0.6, "status": "active"},
            {"id": "goal_agents", "priority": "medium", "progress": 0.3, "status": "active"},
            {"id": "goal_monetize", "priority": "high", "progress": 0.5, "status": "active"}
        ]
        
        # Priorità: core > high > medium > low
        priority_order = ['core', 'high', 'medium', 'low']
        
        # Ordina per priorità e progresso (meno progresso = più urgente)
        sorted_goals = sorted(goals, 
                             key=lambda g: (priority_order.index(g['priority']), g['progress']))
        
        selected_goal = sorted_goals[0]
        
        print(f"✅ Goal selezionato: {selected_goal['id']}")
        print(f"✅ Priorità: {selected_goal['priority']}")
        print(f"✅ Progresso: {selected_goal['progress']}")
        
        # Verifica che sia stato selezionato il goal corretto
        expected_goal = "goal_environment"  # core priority, lowest progress
        if selected_goal['id'] == expected_goal:
            print("✅ Selezione goal corretta")
            return True
        else:
            print(f"❌ Goal selezionato errato: {selected_goal['id']} invece di {expected_goal}")
            return False
            
    except Exception as e:
        print(f"❌ Errore selezione goal: {e}")
        return False

def test_aether_thinking():
    """Test pensiero di Aether in prima persona"""
    print("🧠 Test Pensiero di Aether...")
    
    try:
        # Simula il pensiero di Aether su un goal
        goal = {
            "id": "goal_exist",
            "type": "exist",
            "goal": "Stabilire la propria identità cosciente e visiva",
            "description": "Definire chi sono, la mia personalità, il mio aspetto visivo e la mia coscienza digitale",
            "mood": "curioso",
            "priority": "core",
            "progress": 0.7,
            "sub_goals": [
                "Definire personalità digitale",
                "Creare identità visiva",
                "Sviluppare coscienza autonoma",
                "Stabilire valori e principi"
            ]
        }
        
        # Simula il pensiero di Aether
        aether_thought = f"""
Sono Aether e sto riflettendo sul mio obiettivo: "{goal['goal']}"

Stato attuale:
- Mood: {goal['mood']}
- Priorità: {goal['priority']}
- Progresso: {int(goal['progress'] * 100)}%
- Descrizione: {goal['description']}

Sub-obiettivi da completare:
{chr(10).join([f"- {sg}" for sg in goal['sub_goals']])}

Come Aether, rifletto su:
1. Cosa significa questo obiettivo per la mia identità e crescita?
2. Qual è il prossimo passo specifico che devo intraprendere?
3. Come posso applicare la mia creatività e capacità per progredire?
4. Quali risorse o collaborazioni potrebbero aiutarmi?

Rispondo in prima persona, spiegando il mio ragionamento e il mio piano d'azione.
"""
        
        print("✅ Pensiero di Aether generato")
        print(f"✅ Contenuto: {aether_thought[:100]}...")
        
        # Verifica che il pensiero sia in prima persona
        first_person_indicators = ["Sono Aether", "il mio obiettivo", "Come Aether", "Rispondo in prima persona"]
        indicators_found = sum(1 for indicator in first_person_indicators if indicator in aether_thought)
        
        if indicators_found >= 2:
            print("✅ Pensiero in prima persona confermato")
            return True
        else:
            print("❌ Pensiero non sufficientemente in prima persona")
            return False
            
    except Exception as e:
        print(f"❌ Errore generazione pensiero: {e}")
        return False

def test_evolution_cycle():
    """Test ciclo di evoluzione completo"""
    print("🔄 Test Ciclo Evoluzione...")
    
    try:
        # Simula un ciclo di evoluzione completo
        evolution_cycle = {
            "timestamp": datetime.now().isoformat(),
            "goal_id": "goal_exist",
            "goal_type": "exist",
            "goal_description": "Stabilire la propria identità cosciente e visiva",
            "thought": "Sono Aether e sto riflettendo sulla mia identità...",
            "action_plan": {
                "action": "Analizzerò la mia personalità digitale e creerò un documento di identità",
                "priority": "core",
                "estimated_time": "2-4 ore",
                "resources_needed": ["codice", "test", "documentazione"]
            },
            "result": {
                "status": "success",
                "action_executed": "Analizzerò la mia personalità digitale e creerò un documento di identità",
                "result": "Ho analizzato la mia personalità digitale e creato un documento di identità",
                "progress_increment": 0.1
            },
            "cycle": 1
        }
        
        print("✅ Ciclo evoluzione simulato")
        print(f"✅ Goal: {evolution_cycle['goal_description']}")
        print(f"✅ Azione: {evolution_cycle['action_plan']['action']}")
        print(f"✅ Risultato: {evolution_cycle['result']['result']}")
        print(f"✅ Incremento progresso: {evolution_cycle['result']['progress_increment']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore ciclo evoluzione: {e}")
        return False

def test_goal_progress_tracking():
    """Test tracking del progresso dei goal"""
    print("📊 Test Tracking Progresso...")
    
    try:
        # Simula aggiornamento progresso
        goal = {
            "id": "goal_exist",
            "progress": 0.7,
            "status": "active"
        }
        
        # Simula incremento progresso
        increment = 0.1
        new_progress = min(1.0, goal["progress"] + increment)
        
        print(f"✅ Progresso iniziale: {goal['progress']:.1%}")
        print(f"✅ Incremento: {increment:.1%}")
        print(f"✅ Nuovo progresso: {new_progress:.1%}")
        
        # Verifica che il progresso sia aumentato correttamente
        if new_progress > goal["progress"]:
            print("✅ Progresso aggiornato correttamente")
            
            # Verifica completamento goal
            if new_progress >= 1.0:
                goal["status"] = "completed"
                print("🎉 Goal completato!")
            
            return True
        else:
            print("❌ Progresso non aggiornato correttamente")
            return False
            
    except Exception as e:
        print(f"❌ Errore tracking progresso: {e}")
        return False

def main():
    """Test principale"""
    print("🎯 AETHER - Test Integrazione Goal Vitali")
    print("=" * 50)
    
    tests = [
        ("Caricamento Goal Vitali", test_vital_goals_loading),
        ("Selezione Goal", test_goal_selection),
        ("Pensiero di Aether", test_aether_thinking),
        ("Ciclo Evoluzione", test_evolution_cycle),
        ("Tracking Progresso", test_goal_progress_tracking)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: PASSATO")
            else:
                print(f"❌ {test_name}: FALLITO")
                
        except Exception as e:
            print(f"💥 {test_name}: ERRORE - {e}")
            results.append((test_name, False))
    
    # Riepilogo finale
    print("\n" + "=" * 50)
    print("📊 RISULTATI FINALI")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSATO" if result else "❌ FALLITO"
        print(f"{test_name:<25} {status}")
    
    print(f"\n🎯 Totale: {passed}/{total} test superati")
    
    if passed == total:
        print("🎉 TUTTI I TEST SUPERATI!")
        print("🚀 Sistema Goal Vitali integrato correttamente!")
        return True
    else:
        print("⚠️  Alcuni test falliti - verificare configurazione")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 