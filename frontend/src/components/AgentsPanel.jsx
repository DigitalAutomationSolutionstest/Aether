// src/components/AgentsPanel.jsx - Pannello agenti di Aether

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { aetherAPI } from '../services/api';
import { Bot, Activity, MessageCircle, Clock, Brain, Zap } from 'lucide-react';

const AgentCard = ({ agent, onClick, isActive }) => {
  const getMoodIcon = (mood) => {
    const icons = {
      creativo: '🎨',
      analitico: '📊', 
      curioso: '🔍',
      sognatore: '☁️',
      ambizioso: '🚀'
    };
    return icons[mood] || '🤖';
  };

  const getMoodColor = (mood) => {
    const colors = {
      creativo: 'from-pink-500 to-orange-500',
      analitico: 'from-blue-500 to-green-500',
      curioso: 'from-blue-500 to-purple-500',
      sognatore: 'from-purple-500 to-pink-500',
      ambizioso: 'from-yellow-500 to-red-500'
    };
    return colors[mood] || 'from-gray-500 to-gray-600';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      whileHover={{ scale: 1.02 }}
      className={`
        relative bg-gray-900 bg-opacity-50 backdrop-blur-sm border border-gray-700 
        rounded-lg p-4 cursor-pointer transition-all duration-300 group
        ${isActive ? 'ring-2 ring-cyan-400 border-cyan-400' : 'hover:border-gray-500'}
      `}
      onClick={() => onClick(agent)}
    >
      {/* Agent avatar and status */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className={`
            relative w-12 h-12 bg-gradient-to-br ${getMoodColor(agent.mood)} 
            rounded-full flex items-center justify-center text-2xl
          `}>
            {getMoodIcon(agent.mood)}
            
            {/* Status indicator */}
            <div className="absolute -bottom-1 -right-1">
              <div className={`
                w-4 h-4 rounded-full border-2 border-gray-900 
                ${agent.active ? 'bg-green-400 animate-pulse' : 'bg-gray-500'}
              `} />
            </div>
          </div>
          
          <div>
            <h3 className="text-white font-semibold text-sm">
              {agent.name || 'Unknown Agent'}
            </h3>
            <p className="text-gray-400 text-xs">
              {agent.role || 'Agent Role'}
            </p>
          </div>
        </div>

        <div className="text-right">
          <div className="flex items-center gap-1 text-xs text-gray-500 mb-1">
            <Activity className="w-3 h-3" />
            <span>{agent.interactions || 0}</span>
          </div>
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <Clock className="w-3 h-3" />
            <span>{agent.uptime || '0s'}</span>
          </div>
        </div>
      </div>

      {/* Agent goal/description */}
      <p className="text-gray-300 text-xs mb-3 line-clamp-2">
        {agent.goal || 'Nessun obiettivo specificato'}
      </p>

      {/* Quick stats */}
      <div className="flex items-center justify-between text-xs">
        <span className={`
          px-2 py-1 rounded-full 
          ${agent.mood === 'creativo' ? 'bg-pink-900 text-pink-300' : ''}
          ${agent.mood === 'analitico' ? 'bg-blue-900 text-blue-300' : ''}
          ${agent.mood === 'curioso' ? 'bg-purple-900 text-purple-300' : ''}
          ${agent.mood === 'sognatore' ? 'bg-indigo-900 text-indigo-300' : ''}
          ${agent.mood === 'ambizioso' ? 'bg-yellow-900 text-yellow-300' : ''}
          ${!agent.mood || !['creativo', 'analitico', 'curioso', 'sognatore', 'ambizioso'].includes(agent.mood) ? 'bg-gray-900 text-gray-300' : ''}
        `}>
          {agent.mood || 'neutral'}
        </span>
        
        <div className="flex items-center gap-2 text-gray-500">
          <Brain className="w-3 h-3" />
          <span>AI Agent</span>
        </div>
      </div>

      {/* Hover effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity rounded-lg" />
    </motion.div>
  );
};

const AgentDetail = ({ agent, onClose }) => {
  const [thoughts, setThoughts] = useState([]);
  const [interactions, setInteractions] = useState([]);

  useEffect(() => {
    // Simulate fetching agent-specific data
    // In real implementation, you'd fetch from API
    setThoughts([
      { content: "Sto analizzando nuovi pattern...", timestamp: Date.now() - 30000 },
      { content: "Ho trovato una connessione interessante", timestamp: Date.now() - 60000 }
    ]);
    
    setInteractions([
      { type: "response", content: "Questo mi ispira una nuova idea!", timestamp: Date.now() - 45000 },
      { type: "thought", content: "Potrei creare qualcosa di nuovo", timestamp: Date.now() - 90000 }
    ]);
  }, [agent]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 bg-black bg-opacity-90 backdrop-blur-sm"
      onClick={onClose}
    >
      <div className="absolute inset-4 bg-gray-900 rounded-lg overflow-hidden">
        <div className="relative h-full flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-700">
            <div className="flex items-center gap-4">
              <div className={`
                w-16 h-16 bg-gradient-to-br from-${agent.mood === 'creativo' ? 'pink' : agent.mood === 'analitico' ? 'blue' : 'purple'}-500 
                to-${agent.mood === 'creativo' ? 'orange' : agent.mood === 'analitico' ? 'green' : 'pink'}-500 
                rounded-full flex items-center justify-center text-3xl
              `}>
                {agent.mood === 'creativo' && '🎨'}
                {agent.mood === 'analitico' && '📊'}
                {agent.mood === 'curioso' && '🔍'}
                {agent.mood === 'sognatore' && '☁️'}
                {agent.mood === 'ambizioso' && '🚀'}
                {!['creativo', 'analitico', 'curioso', 'sognatore', 'ambizioso'].includes(agent.mood) && '🤖'}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">{agent.name}</h2>
                <p className="text-gray-400">{agent.role}</p>
                <p className="text-sm text-gray-500 mt-1">{agent.goal}</p>
              </div>
            </div>
            
            <button
              onClick={onClose}
              className="bg-black bg-opacity-50 hover:bg-opacity-70 rounded-full p-2 text-white transition-colors"
            >
              ✕
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 p-6 overflow-auto">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Stats */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-white mb-4">Statistiche</h3>
                
                <div className="bg-gray-800 rounded-lg p-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-cyan-400">{agent.interactions || 0}</div>
                      <div className="text-xs text-gray-400">Interazioni</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-400">{agent.uptime || '0s'}</div>
                      <div className="text-xs text-gray-400">Uptime</div>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-800 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-white mb-2">Stato</h4>
                  <div className="flex items-center gap-2">
                    <div className={`w-3 h-3 rounded-full ${agent.active ? 'bg-green-400' : 'bg-red-400'}`} />
                    <span className="text-sm text-gray-300">
                      {agent.active ? 'Attivo' : 'Inattivo'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-white mb-4">Attività Recente</h3>
                
                <div className="bg-gray-800 rounded-lg p-4 max-h-64 overflow-y-auto">
                  <div className="space-y-3">
                    {[...thoughts, ...interactions]
                      .sort((a, b) => b.timestamp - a.timestamp)
                      .slice(0, 10)
                      .map((item, index) => (
                        <div key={index} className="border-l-2 border-cyan-500 pl-3">
                          <p className="text-sm text-gray-300">{item.content}</p>
                          <p className="text-xs text-gray-500 mt-1">
                            {new Date(item.timestamp).toLocaleTimeString()}
                          </p>
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

const AgentsPanel = () => {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAgent, setSelectedAgent] = useState(null);

  const fetchAgents = async () => {
    try {
      setLoading(true);
      const data = await aetherAPI.getAgents();
      
      if (data.error) {
        setError(data.error);
        return;
      }

      // Transform agents data
      const agentsArray = data.agents_detail ? Object.values(data.agents_detail) : [];
      setAgents(agentsArray);
      setError(null);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
    
    // Auto-refresh every 10 seconds
    const interval = setInterval(fetchAgents, 10000);
    
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <Bot className="w-8 h-8 animate-pulse text-cyan-400 mx-auto mb-2" />
          <p className="text-gray-400">Caricamento agenti...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-4 text-red-400">
        <h3 className="font-bold mb-2">⚠️ Errore Caricamento Agenti</h3>
        <p className="text-sm">{error}</p>
        <button
          onClick={fetchAgents}
          className="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-white text-sm transition-colors"
        >
          Riprova
        </button>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Bot className="w-6 h-6" />
            Agenti di Aether ({agents.length})
          </h2>
          <button
            onClick={fetchAgents}
            className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm text-white transition-colors"
          >
            Aggiorna
          </button>
        </div>

        {agents.length === 0 ? (
          <div className="text-center py-12">
            <Bot className="w-12 h-12 text-gray-600 mx-auto mb-4" />
            <h3 className="text-gray-400 text-lg mb-2">Nessun Agente Attivo</h3>
            <p className="text-gray-500 text-sm">
              Aether non ha ancora creato agenti. Attendere l'auto-evoluzione...
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <AnimatePresence>
              {agents.map((agent, index) => (
                <AgentCard
                  key={agent.name || index}
                  agent={agent}
                  onClick={setSelectedAgent}
                  isActive={selectedAgent?.name === agent.name}
                />
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>

      {/* Agent detail modal */}
      <AnimatePresence>
        {selectedAgent && (
          <AgentDetail
            agent={selectedAgent}
            onClose={() => setSelectedAgent(null)}
          />
        )}
      </AnimatePresence>
    </>
  );
};

export default AgentsPanel; 