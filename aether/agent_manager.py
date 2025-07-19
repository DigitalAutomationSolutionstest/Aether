# aether/agent_manager.py

import os
import importlib.util
import sys
from typing import Dict, List, Any
from datetime import datetime

class AgentManager:
    """
    🤖 Gestore degli agenti di Aether
    Coordina tutti gli agenti creati automaticamente
    """
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.agents_path = "aether/agents"
        self.active_agents = {}
        self.agent_interactions = {}
        
        # Ensure agents directory exists
        os.makedirs(self.agents_path, exist_ok=True)
        
        # Load existing agents
        self.load_all_agents()
        
        print(f"🤖 Agent Manager initialized with {len(self.active_agents)} agents")
    
    def load_all_agents(self):
        """Load all agent files from the agents directory"""
        if not os.path.exists(self.agents_path):
            return
        
        for filename in os.listdir(self.agents_path):
            if filename.endswith('.py') and not filename.startswith('__'):
                agent_name = filename[:-3]  # Remove .py extension
                self.load_agent(agent_name)
    
    def load_agent(self, agent_name: str) -> bool:
        """Load a specific agent by name"""
        try:
            agent_file = f"{self.agents_path}/{agent_name}.py"
            
            if not os.path.exists(agent_file):
                print(f"⚠️ Agent file not found: {agent_file}")
                return False
            
            # Import the agent module
            spec = importlib.util.spec_from_file_location(agent_name, agent_file)
            if spec is None or spec.loader is None:
                print(f"❌ Cannot load spec for agent {agent_name}")
                return False
                
            agent_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(agent_module)
            
            # Get the agent instance
            if hasattr(agent_module, 'get_agent'):
                agent_instance = agent_module.get_agent()
                agent_instance.memory = self.memory  # Inject memory manager
                
                self.active_agents[agent_name] = agent_instance
                self.agent_interactions[agent_name] = 0
                
                print(f"✅ Agent loaded: {agent_name}")
                return True
            else:
                print(f"❌ Agent {agent_name} missing get_agent() function")
                return False
                
        except Exception as e:
            print(f"❌ Error loading agent {agent_name}: {e}")
            return False
    
    def get_all_agents(self) -> Dict[str, Any]:
        """Get all active agents"""
        return self.active_agents
    
    def get_agent(self, agent_name: str):
        """Get specific agent by name"""
        return self.active_agents.get(agent_name)
    
    def agent_think_all(self) -> List[Dict[str, Any]]:
        """Make all agents think and return their thoughts"""
        thoughts = []
        
        for agent_name, agent in self.active_agents.items():
            try:
                thought = agent.think()
                thoughts.append(thought)
                self.agent_interactions[agent_name] += 1
                
                print(f"💭 {agent_name}: {thought.get('content', '')[:50]}...")
                
            except Exception as e:
                print(f"❌ Error with agent {agent_name}: {e}")
        
        return thoughts
    
    def agent_interact_with_aether(self, aether_thought: Dict[str, Any]) -> List[str]:
        """Make all agents interact with Aether's thought"""
        responses = []
        
        for agent_name, agent in self.active_agents.items():
            try:
                if hasattr(agent, 'interact_with_aether'):
                    response = agent.interact_with_aether(aether_thought)
                    responses.append(f"{agent_name}: {response}")
                    
                    # Save interaction to memory
                    self.memory.save_thought({
                        "type": "agent_interaction",
                        "content": response,
                        "context": {
                            "agent_name": agent_name,
                            "responding_to": aether_thought.get('content', '')[:100],
                            "timestamp": datetime.now().isoformat()
                        }
                    })
                    
                    print(f"🤖💬 {agent_name}: {response[:50]}...")
                    
            except Exception as e:
                print(f"❌ Error with agent interaction {agent_name}: {e}")
        
        return responses
    
    def get_agents_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {
            "total_agents": len(self.active_agents),
            "agent_list": list(self.active_agents.keys()),
            "interactions": self.agent_interactions.copy(),
            "agents_detail": {}
        }
        
        for agent_name, agent in self.active_agents.items():
            try:
                if hasattr(agent, 'get_status'):
                    status["agents_detail"][agent_name] = agent.get_status()
                else:
                    status["agents_detail"][agent_name] = {
                        "name": agent_name,
                        "active": True,
                        "interactions": self.agent_interactions.get(agent_name, 0)
                    }
            except Exception as e:
                status["agents_detail"][agent_name] = {"error": str(e)}
        
        return status
    
    def reload_agents(self):
        """Reload all agents (useful after auto-evolution creates new ones)"""
        print("🔄 Reloading all agents...")
        self.active_agents.clear()
        self.agent_interactions.clear()
        self.load_all_agents()
        print(f"✅ Reloaded {len(self.active_agents)} agents")

# Global instance
agent_manager_instance = None

def get_agent_manager(memory_manager=None):
    """Get or create the global agent manager instance"""
    global agent_manager_instance
    if agent_manager_instance is None and memory_manager:
        agent_manager_instance = AgentManager(memory_manager)
    return agent_manager_instance 