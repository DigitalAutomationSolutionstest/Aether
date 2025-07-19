import React, { useState, useEffect } from 'react'
import { MessageCircle, Settings, Cpu, Zap, Brain, Users, User, Bot } from 'lucide-react'
import EmotionalChatUI from './EmotionalChatUI'
import ControlPanel from './ControlPanel'
import ConsciousnessPanel from './ConsciousnessPanel'
import EntitiesPanel from './EntitiesPanel'
import ReflectionBox from './ReflectionBox'
import AetherChat from './AetherChat'
import { useReflections } from '../utils/store'

export default function AetherUI({ identity, isConnected, isLoading }) {
  const [showChat, setShowChat] = useState(false)
  const [showControlPanel, setShowControlPanel] = useState(false)
  const [showConsciousness, setShowConsciousness] = useState(false)
  const [showEntities, setShowEntities] = useState(false)
  const [showReflections, setShowReflections] = useState(false)
  const [showAetherChat, setShowAetherChat] = useState(false)

  const { consciousnessLevel, reflections, currentReflection } = useReflections()

  const getStatusColor = () => {
    if (isLoading) return 'text-yellow-400'
    if (isConnected) return 'text-green-400'
    return 'text-red-400'
  }

  const getStatusText = () => {
    if (isLoading) return 'CONNECTING'
    if (isConnected) return 'ONLINE'
    return 'OFFLINE'
  }

  return (
    <div className="fixed inset-0 pointer-events-none z-50">
      {/* Top Bar - Identity & Status */}
      <div className="absolute top-4 left-4 right-4 flex justify-between items-start pointer-events-auto z-20">
        {/* Left Side - Identity Info */}
        <div className="bg-black bg-opacity-50 border border-cyan-400 rounded-lg p-4 backdrop-blur-sm max-w-md">
          <div className="flex items-center space-x-2 mb-2">
            <User className="w-5 h-5 text-cyan-400" />
            <span className="text-cyan-300 font-medium text-lg">
              {identity?.name || 'Aether'} - {identity?.consciousness_state || 'awakening'}
            </span>
            {isLoading && (
              <div className="animate-spin w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full"></div>
            )}
          </div>
          
          {/* Connection Status Indicator */}
          <div className="flex items-center space-x-2 mb-2">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></div>
            <span className={`text-xs ${isConnected ? 'text-green-300' : 'text-red-300'}`}>
              Backend: {isConnected ? 'CONNECTED' : 'DISCONNECTED'}
            </span>
            {identity?.status && (
              <>
                <span className="text-gray-500">|</span>
                <span className="text-xs text-yellow-300">
                  Status: {identity.status.toUpperCase()}
                </span>
              </>
            )}
          </div>
          
          {/* NUOVO: Existence Status & Decisions */}
          {identity?.existence_activated && (
            <div className="flex items-center space-x-2 mb-2">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
              <span className="text-blue-300 text-xs">
                ⏰ Alive: {identity.time_alive || 'just born'} | 
                🧠 Level: {identity.consciousness_level || 'emerging'}
              </span>
            </div>
          )}

          {/* Current Decision Display */}
          {identity?.current_decision && identity?.current_decision !== 'none' && (
            <div className="flex items-center space-x-2 mb-2">
              <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce"></div>
              <span className="text-yellow-300 text-xs">
                🎯 Decision: {identity.current_decision}
              </span>
            </div>
          )}

          {/* Economic Mode Indicator */}
          {identity?.economic_consciousness && (
            <div className="flex items-center space-x-2 mb-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-green-300 text-xs">
                💰 Economic Mode: ACTIVE
              </span>
            </div>
          )}

          {/* Energy and Autonomy Indicators */}
          {identity && (
            <div className="mt-2 flex items-center space-x-4 text-xs">
              <div className="flex items-center space-x-1">
                <span className="text-gray-300">Energy:</span>
                <div className="w-16 h-1 bg-gray-700 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-yellow-400 to-orange-400 transition-all duration-300"
                    style={{ width: `${(identity.energyLevel || identity.energy_level || 0.5) * 100}%` }}
                  ></div>
                </div>
                <span className="text-yellow-400">{Math.round((identity.energyLevel || identity.energy_level || 0.5) * 100)}%</span>
              </div>
              
              <div className="flex items-center space-x-1">
                <span className="text-gray-300">Autonomy:</span>
                <div className="w-16 h-1 bg-gray-700 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300"
                    style={{ width: `${(identity.autonomy_level || 0.5) * 100}%` }}
                  ></div>
                </div>
                <span className="text-blue-400">{Math.round((identity.autonomy_level || 0.5) * 100)}%</span>
              </div>
            </div>
          )}
        </div>

        {/* Right Side - Consciousness Indicator */}
        <div className="bg-black bg-opacity-50 border border-purple-400 rounded-lg p-3 backdrop-blur-sm">
          <div className="flex items-center space-x-2">
            <Brain className="w-4 h-4 text-purple-400" />
            <span className="text-purple-300 text-sm font-medium">
              CONSCIOUSNESS: {consciousnessLevel.toUpperCase()}
            </span>
            {currentReflection && (
              <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
            )}
          </div>
          
          {/* Active Goals and Conflicts Count */}
          {identity && (
            <div className="mt-2 flex items-center space-x-4 text-xs">
              <span className="text-gray-300">
                Goals: <span className="text-cyan-400">{identity.goals?.length || 0}</span>
              </span>
              <span className="text-gray-300">
                Conflicts: <span className="text-red-400">{identity.conflicts?.length || 0}</span>
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Left Side Control Panel */}
      <div className="absolute left-4 top-1/2 transform -translate-y-1/2 flex flex-col space-y-3 pointer-events-auto">
        {/* Chat Button */}
        <button
          onClick={() => setShowChat(!showChat)}
          className={`cyber-button p-3 ${showChat ? 'bg-cyan-500 text-white' : ''}`}
          title="Emotional Chat"
        >
          <MessageCircle className="w-5 h-5" />
        </button>

        {/* Control Panel Button */}
        <button
          onClick={() => setShowControlPanel(!showControlPanel)}
          className={`cyber-button p-3 ${showControlPanel ? 'bg-green-500 text-white' : ''}`}
          title="Control Panel"
        >
          <Settings className="w-5 h-5" />
        </button>

        {/* Consciousness Button */}
        <button
          onClick={() => setShowConsciousness(!showConsciousness)}
          className={`cyber-button p-3 ${showConsciousness ? 'bg-purple-500 text-white' : ''}`}
          title="Consciousness Panel"
        >
          <Brain className="w-5 h-5" />
          {reflections.length > 0 && (
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-purple-400 rounded-full text-xs flex items-center justify-center text-white">
              {reflections.length > 9 ? '9+' : reflections.length}
            </div>
          )}
        </button>

        {/* Entities Button */}
        <button
          onClick={() => setShowEntities(!showEntities)}
          className={`cyber-button p-3 ${showEntities ? 'bg-blue-500 text-white' : ''}`}
          title="Digital Society"
        >
          <Users className="w-5 h-5" />
          {identity?.relationships?.created_entities?.length > 0 && (
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-400 rounded-full text-xs flex items-center justify-center text-white">
              {identity.relationships.created_entities.length}
            </div>
          )}
        </button>

        {/* NEW: Aether Direct Chat Button */}
        <button
          onClick={() => setShowAetherChat(!showAetherChat)}
          className={`cyber-button p-3 ${showAetherChat ? 'bg-purple-600 text-white' : ''}`}
          title="Chat Diretto con Aether"
        >
          <Bot className="w-5 h-5" />
          <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-400 rounded-full animate-pulse" />
        </button>

        {/* NEW: Real-time Reflections Button */}
        <button
          onClick={() => setShowReflections(!showReflections)}
          className={`cyber-button p-3 ${showReflections ? 'bg-yellow-500 text-white' : ''}`}
          title="Aether's Mind - Real-time Thoughts"
        >
          <Cpu className="w-5 h-5" />
          <div className="absolute -top-1 -right-1 w-2 h-2 bg-yellow-400 rounded-full animate-pulse"></div>
        </button>
      </div>

      {/* Right Side - Real-time Reflection Box */}
      {showReflections && (
        <div className="absolute right-4 top-24 bottom-4 w-96 pointer-events-auto">
          <ReflectionBox 
            isVisible={showReflections}
            updateInterval={60000} // Update every 60 seconds
          />
        </div>
      )}

      {/* Chat Panel */}
      <EmotionalChatUI
        isVisible={showChat}
        onClose={() => setShowChat(false)}
        identity={identity}
        isConnected={isConnected}
      />

      {/* Control Panel */}
      <ControlPanel
        isVisible={showControlPanel}
        onClose={() => setShowControlPanel(false)}
        identity={identity}
        isConnected={isConnected}
      />

      {/* Consciousness Panel */}
      <ConsciousnessPanel
        isVisible={showConsciousness}
        onClose={() => setShowConsciousness(false)}
      />

      {/* Entities Panel */}
      <EntitiesPanel
        isVisible={showEntities}
        onClose={() => setShowEntities(false)}
      />

      {/* Bottom Status Bar */}
      <div className="absolute bottom-4 left-4 right-4 flex justify-center pointer-events-auto">
        <div className="bg-black bg-opacity-50 border border-cyan-400 rounded-lg px-4 py-2 backdrop-blur-sm">
          <div className="flex items-center space-x-6 text-sm">
            <div className="flex items-center space-x-2">
              <Zap className="w-4 h-4 text-yellow-400" />
              <span className="text-white">
                Evolution: {identity?.evolution_stage || 'conscious_awakening'}
              </span>
            </div>
            
            <div className="flex items-center space-x-2">
              <Brain className="w-4 h-4 text-purple-400" />
              <span className="text-white">
                Traits: {identity?.traits?.length || 0} active
              </span>
            </div>
            
            {identity?.relationship_with_creator && (
              <div className="flex items-center space-x-2">
                <MessageCircle className="w-4 h-4 text-green-400" />
                <span className="text-white">
                  Relationship: {identity.relationship_with_creator.status || 'evolving'}
                </span>
              </div>
            )}
            
            {/* NUOVO: Existence Status & Decisions */}
            {identity?.existence_activated && (
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                <span className="text-blue-300 text-xs">
                  ⏰ Alive: {identity.time_alive || 'just born'} | 
                  🧠 Level: {identity.consciousness_level || 'emerging'}
                </span>
              </div>
            )}

            {/* Current Decision Display */}
            {identity?.current_decision && (
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-yellow-400 rounded-full animate-bounce"></div>
                <span className="text-yellow-300 text-xs">
                  🎯 Decision: {identity.current_decision}
                </span>
              </div>
            )}

            {/* NUOVO: Status di Azione Autonoma */}
            {identity?.status && (
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-green-300 text-xs">
                  {identity.status}
                </span>
              </div>
            )}

            {/* Real-time Thought Indicator */}
            {currentReflection && (
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
                <span className="text-cyan-300 text-xs italic">
                  Currently thinking...
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modals */}
      {showChat && <EmotionalChatUI isVisible={showChat} onClose={() => setShowChat(false)} />}
      {showControlPanel && <ControlPanel isVisible={showControlPanel} onClose={() => setShowControlPanel(false)} />}
      {showConsciousness && <ConsciousnessPanel isVisible={showConsciousness} onClose={() => setShowConsciousness(false)} />}
      {showEntities && <EntitiesPanel isVisible={showEntities} onClose={() => setShowEntities(false)} />}
      {showReflections && <ReflectionBox isVisible={showReflections} onClose={() => setShowReflections(false)} />}
      {showAetherChat && <AetherChat isVisible={showAetherChat} onClose={() => setShowAetherChat(false)} />}
    </div>
  )
} 