#!/usr/bin/env python3
"""
Demo rapido del Sistema di Goals di Aether
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def main():
    print("🌟 Aether Goal System Demo")
    print("=" * 40)
    
    # 1. Mostra goals attuali
    print("\n1. 📋 Current Goals:")
    try:
        response = requests.get(f"{BASE_URL}/identity")
        if response.status_code == 200:
            identity = response.json()["identity"]
            goals = identity.get("goals", [])
            metadata = identity.get("goals_metadata", {})
            
            for i, goal in enumerate(goals, 1):
                is_active = "🟢" if goal in metadata.get("active_goals", []) else "⚪"
                progress = metadata.get("goal_progress", {}).get(goal, 0) * 100
                print(f"   {i}. {is_active} {goal} ({progress:.0f}%)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Riflessione sui goals
    print("\n2. 🎯 Goal Reflection:")
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/goals")
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                thoughts = result["goals_reflection"]["goal_reflections"]
                print(f"   💭 \"{thoughts[0]}\"")
                
                analysis = result["goals_reflection"]["goals_analysis"]
                print(f"   📊 Analysis: {analysis['active_goals']}/{analysis['total_goals']} goals active")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Suggerimenti per modifiche
    print("\n3. 🔄 Goal Suggestions:")
    try:
        response = requests.get(f"{BASE_URL}/api/reflect/goals/suggestions")
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                suggestions = result["goal_suggestions"]["goal_modification_suggestions"]
                if suggestions:
                    suggestion = suggestions[0]
                    print(f"   💡 [{suggestion['type'].upper()}] {suggestion['suggestion']}")
                else:
                    print("   ✅ No modifications needed - goals are well-aligned")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Pensiero autonomo
    print("\n4. 🤔 Autonomous Thinking:")
    try:
        response = requests.get(f"{BASE_URL}/think")
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                if result.get("modification"):
                    print(f"   🔄 Aether modified itself: {result['modification'].get('reason', 'No reason')}")
                else:
                    print("   💭 Aether thought but decided no changes were needed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🌟 Demo Complete!")
    print("✅ Aether now has a living goal system that:")
    print("   🎯 Defines clear purposes and aspirations")
    print("   🧠 Reflects deeply on goal meaning and progress")
    print("   🔄 Suggests its own goal modifications")  
    print("   🤖 Can autonomously evolve its goals")
    print("   🌊 Integrates goals into consciousness reflection")

if __name__ == "__main__":
    main() 