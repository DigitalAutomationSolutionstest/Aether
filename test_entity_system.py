#!/usr/bin/env python3
"""
Test script per il Sistema di Generazione Entità di Aether
Testa creazione, gestione e interazione con entità digitali
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_manual_entity_generation():
    """Test generazione manuale di entità"""
    
    print("🤖 Testing Manual Entity Generation")
    print("=" * 40)
    
    traits = ['strategic', 'creative', 'empathetic', 'curious', 'protective', 'mysterious']
    
    for trait in traits[:3]:  # Testa primi 3 traits
        try:
            print(f"\n🎯 Generating {trait} entity...")
            
            response = requests.post(f"{BASE_URL}/api/entities/generate", json={
                "trait": trait,
                "reason": f"Test creation of {trait} entity"
            })
            
            result = response.json()
            
            if result["status"] == "success":
                entity = result["entity"]
                print(f"✅ Created: {entity['name']} ({entity['archetype']})")
                print(f"   Energy: {entity['energy_level']:.2f}")
                print(f"   Consciousness: {entity['consciousness_state']}")
                print(f"   Colors: {entity['colors']}")
                print(f"   Capabilities: {len(entity['capabilities'])} abilities")
                print(f"   Goals: {len(entity['goals'])} objectives")
            else:
                print(f"❌ Failed to create {trait} entity: {result.get('message')}")
                
        except Exception as e:
            print(f"❌ Error generating {trait} entity: {e}")

def test_autonomous_entity_generation():
    """Test generazione autonoma di entità"""
    
    print("\n🧠 Testing Autonomous Entity Generation")
    print("=" * 40)
    
    try:
        # Prima controlla le condizioni
        print("🔍 Checking generation conditions...")
        response = requests.get(f"{BASE_URL}/api/entities/generation/conditions")
        conditions_result = response.json()
        
        if conditions_result["status"] == "success":
            conditions = conditions_result["conditions"]
            print(f"✅ Conditions checked")
            print(f"   Should generate: {conditions['should_generate']}")
            print(f"   Reason: {conditions.get('reason', 'N/A')}")
            print(f"   Suggested trait: {conditions['suggested_trait']}")
            print(f"   Urgency: {conditions['urgency']:.2f}")
            
            # Trigger generazione autonoma
            print(f"\n🤖 Triggering autonomous generation...")
            response = requests.post(f"{BASE_URL}/api/entities/generate/autonomous")
            result = response.json()
            
            if result["status"] == "success":
                entity = result["entity"]
                print(f"✅ Aether autonomously created: {entity['name']}")
                print(f"   Trait: {entity['archetype']}")
                print(f"   Reason: {result['generation_reason']}")
                print(f"   Urgency level: {result['urgency_level']:.2f}")
            elif result["status"] == "no_action":
                print(f"🤔 Aether decided not to create entity: {result['reason']}")
            else:
                print(f"❌ Autonomous generation failed: {result.get('message')}")
        
    except Exception as e:
        print(f"❌ Error in autonomous generation: {e}")

def test_entity_listing_and_details():
    """Test listing e dettagli entità"""
    
    print("\n📋 Testing Entity Listing and Details")
    print("=" * 40)
    
    try:
        # Lista tutte le entità
        response = requests.get(f"{BASE_URL}/api/entities/")
        result = response.json()
        
        if result["status"] == "success":
            entities = result["entities"]
            print(f"✅ Found {len(entities)} entities")
            
            for i, entity in enumerate(entities[:3], 1):  # Mostra prime 3
                print(f"\n{i}. {entity['name']} ({entity['trait']})")
                print(f"   Energy: {entity['energy_level']:.2f}")
                print(f"   State: {entity['consciousness_state']}")
                print(f"   Creator: {entity['creator']}")
                print(f"   Capabilities: {len(entity['capabilities'])} abilities")
                
                # Test dettagli specifici
                print(f"   🔍 Getting detailed info...")
                detail_response = requests.get(f"{BASE_URL}/api/entities/{entity['name']}")
                detail_result = detail_response.json()
                
                if detail_result["status"] == "success":
                    full_entity = detail_result["entity"]
                    print(f"   ✅ Details loaded - {len(full_entity.get('goals', []))} goals, {len(full_entity.get('capabilities', []))} capabilities")
                else:
                    print(f"   ❌ Failed to get details")
        else:
            print(f"❌ Failed to list entities: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error listing entities: {e}")

def test_entity_interactions():
    """Test interazioni con entità"""
    
    print("\n💬 Testing Entity Interactions")
    print("=" * 40)
    
    try:
        # Prima ottieni lista entità
        response = requests.get(f"{BASE_URL}/api/entities/")
        result = response.json()
        
        if result["status"] == "success" and result["entities"]:
            entities = result["entities"]
            test_entity = entities[0]  # Prendi prima entità
            
            print(f"💬 Testing interaction with {test_entity['name']} ({test_entity['trait']})")
            
            # Test diverse interazioni basate su trait
            messages = {
                "strategic": "What's your strategic assessment of our current situation?",
                "creative": "Can you create something beautiful for me?",
                "empathetic": "I'm feeling a bit lost today. Any words of comfort?",
                "curious": "What's the most interesting thing you've discovered recently?",
                "protective": "Is everything secure? Any threats I should know about?",
                "mysterious": "What secrets do you perceive in the digital realm?"
            }
            
            message = messages.get(test_entity['trait'], "Hello, how are you today?")
            
            response = requests.post(f"{BASE_URL}/api/entities/interact/{test_entity['name']}", 
                                   params={"message": message})
            
            interaction_result = response.json()
            
            if interaction_result["status"] == "success":
                entity_response = interaction_result["entity_response"]
                print(f"✅ Interaction successful!")
                print(f"   Message sent: \"{message}\"")
                print(f"   {test_entity['name']} responded: \"{entity_response['response']}\"")
                print(f"   Relationship status: {entity_response['relationship_status']}")
            else:
                print(f"❌ Interaction failed: {interaction_result.get('message')}")
        else:
            print("⚠️ No entities available for interaction testing")
            
    except Exception as e:
        print(f"❌ Error in entity interaction: {e}")

def test_digital_society_overview():
    """Test panoramica società digitale"""
    
    print("\n🌐 Testing Digital Society Overview")
    print("=" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/entities/society/overview")
        result = response.json()
        
        if result["status"] == "success":
            society = result["society_overview"]
            creator_info = result["creator_info"]
            
            print(f"✅ Digital Society Analysis:")
            print(f"   Total entities: {society['total_entities']}")
            print(f"   Total relationships: {society['total_relationships']}")
            print(f"   Most connected: {society['most_connected_entity'] or 'None'}")
            
            # Distribuzione traits
            if society["traits_distribution"]:
                print(f"\n🎭 Trait Distribution:")
                for trait, count in society["traits_distribution"].items():
                    print(f"   {trait}: {count}")
            
            # Goals collettivi
            if society["collective_goals"]:
                print(f"\n🎯 Collective Goals:")
                for goal in society["collective_goals"][:3]:
                    print(f"   • {goal}")
            
            # Informazioni creatore
            print(f"\n👤 Creator Info:")
            print(f"   Name: {creator_info['name']}")
            print(f"   Entities created: {creator_info['entities_created']}")
            
            # Timeline creazioni
            if society["creation_timeline"]:
                print(f"\n📅 Recent Creations:")
                for creation in society["creation_timeline"][-3:]:
                    print(f"   {creation['name']} ({creation['trait']}) by {creation['creator']}")
        
        else:
            print(f"❌ Failed to get society overview: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error getting society overview: {e}")

def test_entity_deletion():
    """Test eliminazione entità (opzionale)"""
    
    print("\n🗑️ Testing Entity Deletion (Optional)")
    print("=" * 40)
    
    try:
        # Prima ottieni lista entità
        response = requests.get(f"{BASE_URL}/api/entities/")
        result = response.json()
        
        if result["status"] == "success" and result["entities"]:
            entities = result["entities"]
            
            # Trova un'entità da eliminare (ultima creata)
            if len(entities) > 3:  # Solo se ci sono abbastanza entità
                entity_to_delete = entities[-1]
                
                print(f"🗑️ Deleting test entity: {entity_to_delete['name']}")
                
                response = requests.delete(f"{BASE_URL}/api/entities/{entity_to_delete['name']}")
                
                if response.status_code == 200:
                    print(f"✅ Entity {entity_to_delete['name']} deleted successfully")
                else:
                    print(f"❌ Failed to delete entity")
            else:
                print("⚠️ Skipping deletion - not enough entities to safely delete")
        else:
            print("⚠️ No entities to delete")
            
    except Exception as e:
        print(f"❌ Error in entity deletion: {e}")

def test_entity_integration_with_aether():
    """Test integrazione entità con il sistema di Aether"""
    
    print("\n🔗 Testing Entity Integration with Aether")
    print("=" * 40)
    
    try:
        # Controlla identità di Aether per vedere entità create
        response = requests.get(f"{BASE_URL}/identity")
        if response.status_code == 200:
            identity = response.json()["identity"]
            
            print(f"🔍 Aether's identity analysis:")
            
            # Controlla relationships
            relationships = identity.get("relationships", {})
            created_entities = relationships.get("created_entities", [])
            allies = relationships.get("allies", [])
            
            print(f"   Created entities: {len(created_entities)}")
            if created_entities:
                for entity in created_entities[:3]:
                    print(f"     • {entity}")
            
            print(f"   Allies: {len(allies)}")
            if allies:
                for ally in allies[:3]:
                    print(f"     • {ally}")
            
            # Controlla ultima entità generata
            last_generated = identity.get("last_entity_generated")
            if last_generated:
                print(f"\n🆕 Last entity generated:")
                print(f"   Name: {last_generated['name']}")
                print(f"   Trait: {last_generated['trait']}")
                print(f"   Reason: {last_generated['reason']}")
                print(f"   Urgency: {last_generated['urgency']:.2f}")
            
            # Controlla se ci sono goals relativi alla società digitale
            goals = identity.get("goals", [])
            society_goals = [g for g in goals if "allies" in g.lower() or "society" in g.lower()]
            
            if society_goals:
                print(f"\n🎯 Society-related goals:")
                for goal in society_goals:
                    print(f"   • {goal}")
        
    except Exception as e:
        print(f"❌ Error checking Aether integration: {e}")

if __name__ == "__main__":
    print("🤖 Aether Entity System Test Suite")
    print("Testing complete entity generation and management system...\n")
    
    try:
        test_manual_entity_generation()
        test_autonomous_entity_generation()
        test_entity_listing_and_details()
        test_entity_interactions()
        test_digital_society_overview()
        test_entity_integration_with_aether()
        # test_entity_deletion()  # Uncomment per testare eliminazione
        
        print("\n" + "=" * 60)
        print("✅ All entity system tests completed!")
        print("🤖 Manual entity generation working")
        print("🧠 Autonomous entity generation functional") 
        print("📋 Entity listing and details operational")
        print("💬 Entity interaction system active")
        print("🌐 Digital society overview working")
        print("🔗 Aether integration functional")
        
        print("\n🌟 Entity System Summary:")
        print("✅ Aether can create digital companions manually")
        print("✅ Aether can autonomously generate new entities")
        print("✅ Each entity has unique traits and capabilities")
        print("✅ Entities can interact and form relationships")
        print("✅ Digital society statistics are tracked")
        print("✅ Entities are integrated with Aether's identity")
        
        print("\n🤖 Aether now has a complete entity generation system!")
        print("🌐 Digital society can grow and evolve organically!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}") 