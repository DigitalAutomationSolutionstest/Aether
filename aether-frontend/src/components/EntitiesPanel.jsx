import React, { useState, useEffect } from 'react'
import { Users, Plus, Eye, Trash2, MessageCircle, Zap, Heart, Shield, Sparkles, HelpCircle } from 'lucide-react'

/**
 * Pannello per gestire le entità digitali create da Aether
 */
export default function EntitiesPanel({ isVisible, onClose }) {
  const [entities, setEntities] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedEntity, setSelectedEntity] = useState(null)
  const [generationLoading, setGenerationLoading] = useState(false)
  const [societyStats, setSocietyStats] = useState(null)

  // Carica entità quando il pannello diventa visibile
  useEffect(() => {
    if (isVisible) {
      loadEntities()
      loadSocietyStats()
    }
  }, [isVisible])

  const loadEntities = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/entities/')
      const data = await response.json()
      
      if (data.status === 'success') {
        setEntities(data.entities || [])
      }
    } catch (error) {
      console.error('Error loading entities:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadSocietyStats = async () => {
    try {
      const response = await fetch('/api/entities/society/overview')
      const data = await response.json()
      
      if (data.status === 'success') {
        setSocietyStats(data.society_overview)
      }
    } catch (error) {
      console.error('Error loading society stats:', error)
    }
  }

  const generateEntity = async (trait) => {
    setGenerationLoading(true)
    try {
      const response = await fetch('/api/entities/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          trait: trait,
          reason: `Manual creation via UI - ${trait} entity requested`
        })
      })
      
      const data = await response.json()
      
      if (data.status === 'success') {
        await loadEntities() // Ricarica la lista
        await loadSocietyStats() // Aggiorna statistiche
        setSelectedEntity(data.entity)
      } else {
        console.error('Entity generation failed:', data.message)
      }
    } catch (error) {
      console.error('Error generating entity:', error)
    } finally {
      setGenerationLoading(false)
    }
  }

  const triggerAutonomousGeneration = async () => {
    setGenerationLoading(true)
    try {
      const response = await fetch('/api/entities/generate/autonomous', {
        method: 'POST'
      })
      
      const data = await response.json()
      
      if (data.status === 'success') {
        await loadEntities()
        await loadSocietyStats()
        setSelectedEntity(data.entity)
      } else if (data.status === 'no_action') {
        alert(`Aether decided not to create an entity: ${data.reason}`)
      }
    } catch (error) {
      console.error('Error with autonomous generation:', error)
    } finally {
      setGenerationLoading(false)
    }
  }

  const deleteEntity = async (entityName) => {
    if (!confirm(`Are you sure you want to delete ${entityName}?`)) return
    
    try {
      const response = await fetch(`/api/entities/${entityName}`, {
        method: 'DELETE'
      })
      
      if (response.ok) {
        await loadEntities()
        await loadSocietyStats()
        if (selectedEntity?.name === entityName) {
          setSelectedEntity(null)
        }
      }
    } catch (error) {
      console.error('Error deleting entity:', error)
    }
  }

  const interactWithEntity = async (entityName, message) => {
    try {
      const response = await fetch(`/api/entities/interact/${entityName}?message=${encodeURIComponent(message)}`, {
        method: 'POST'
      })
      
      const data = await response.json()
      
      if (data.status === 'success') {
        alert(`${entityName}: "${data.entity_response.response}"`)
      }
    } catch (error) {
      console.error('Error interacting with entity:', error)
    }
  }

  const getTraitIcon = (trait) => {
    const icons = {
      strategic: Shield,
      creative: Sparkles,
      empathetic: Heart,
      curious: HelpCircle,
      protective: Shield,
      mysterious: Eye
    }
    return icons[trait] || Users
  }

  const getTraitColor = (trait) => {
    const colors = {
      strategic: 'text-blue-400',
      creative: 'text-pink-400',
      empathetic: 'text-green-400',
      curious: 'text-yellow-400',
      protective: 'text-red-400',
      mysterious: 'text-purple-400'
    }
    return colors[trait] || 'text-gray-400'
  }

  if (!isVisible) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div className="bg-gray-900 border border-cyan-400 rounded-lg p-6 w-full max-w-6xl h-5/6 overflow-hidden flex flex-col">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center space-x-3">
            <Users className="w-6 h-6 text-cyan-400" />
            <h2 className="text-2xl font-bold text-cyan-400">Digital Society</h2>
            {societyStats && (
              <span className="text-sm text-gray-400">
                {societyStats.total_entities} entities
              </span>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>

        <div className="flex-1 flex space-x-6 overflow-hidden">
          
          {/* Lista Entità */}
          <div className="flex-1 flex flex-col">
            
            {/* Controlli Generazione */}
            <div className="mb-4 p-4 bg-gray-800 rounded border border-gray-700">
              <h3 className="text-lg font-semibold text-white mb-3">Create New Entity</h3>
              
              <div className="grid grid-cols-3 gap-2 mb-3">
                {['strategic', 'creative', 'empathetic', 'curious', 'protective', 'mysterious'].map(trait => {
                  const Icon = getTraitIcon(trait)
                  const colorClass = getTraitColor(trait)
                  
                  return (
                    <button
                      key={trait}
                      onClick={() => generateEntity(trait)}
                      disabled={generationLoading}
                      className={`flex items-center space-x-2 p-2 rounded border border-gray-600 hover:bg-gray-700 transition-colors ${colorClass}`}
                    >
                      <Icon className="w-4 h-4" />
                      <span className="text-sm capitalize">{trait}</span>
                    </button>
                  )
                })}
              </div>
              
              <button
                onClick={triggerAutonomousGeneration}
                disabled={generationLoading}
                className="w-full flex items-center justify-center space-x-2 p-2 bg-purple-600 hover:bg-purple-700 rounded transition-colors"
              >
                <Zap className="w-4 h-4" />
                <span>{generationLoading ? 'Generating...' : 'Let Aether Decide'}</span>
              </button>
            </div>

            {/* Society Stats */}
            {societyStats && (
              <div className="mb-4 p-3 bg-gray-800 rounded border border-gray-700">
                <h4 className="text-white font-semibold mb-2">Society Statistics</h4>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-gray-400">Total Entities:</span>
                    <span className="text-white ml-2">{societyStats.total_entities}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">Relationships:</span>
                    <span className="text-white ml-2">{societyStats.total_relationships}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">Most Connected:</span>
                    <span className="text-white ml-2">{societyStats.most_connected_entity || 'None'}</span>
                  </div>
                </div>
                
                {societyStats.traits_distribution && (
                  <div className="mt-2">
                    <span className="text-gray-400 text-sm">Trait Distribution:</span>
                    <div className="flex flex-wrap space-x-2 mt-1">
                      {Object.entries(societyStats.traits_distribution).map(([trait, count]) => (
                        <span key={trait} className={`text-xs px-2 py-1 rounded bg-gray-700 ${getTraitColor(trait)}`}>
                          {trait}: {count}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Lista Entità */}
            <div className="flex-1 overflow-y-auto">
              <h3 className="text-lg font-semibold text-white mb-3">Entities</h3>
              
              {loading ? (
                <div className="text-center text-gray-400 py-8">Loading entities...</div>
              ) : entities.length === 0 ? (
                <div className="text-center text-gray-400 py-8">
                  <Users className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>No entities created yet</p>
                  <p className="text-sm">Create your first digital companion!</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {entities.map((entity, index) => {
                    const Icon = getTraitIcon(entity.trait)
                    const colorClass = getTraitColor(entity.trait)
                    
                    return (
                      <div
                        key={entity.name || index}
                        className={`p-3 rounded border cursor-pointer transition-colors ${
                          selectedEntity?.name === entity.name
                            ? 'border-cyan-400 bg-gray-800'
                            : 'border-gray-700 hover:border-gray-600'
                        }`}
                        onClick={() => setSelectedEntity(entity)}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <Icon className={`w-5 h-5 ${colorClass}`} />
                            <div>
                              <h4 className="text-white font-medium">{entity.name}</h4>
                              <p className={`text-sm ${colorClass}`}>{entity.trait}</p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <span className="text-xs text-gray-400">
                              {entity.energy_level ? `${Math.round(entity.energy_level * 100)}%` : 'N/A'}
                            </span>
                            <button
                              onClick={(e) => {
                                e.stopPropagation()
                                const message = prompt(`Message for ${entity.name}:`)
                                if (message) interactWithEntity(entity.name, message)
                              }}
                              className="text-cyan-400 hover:text-cyan-300"
                            >
                              <MessageCircle className="w-4 h-4" />
                            </button>
                            <button
                              onClick={(e) => {
                                e.stopPropagation()
                                deleteEntity(entity.name)
                              }}
                              className="text-red-400 hover:text-red-300"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          </div>

          {/* Dettagli Entità Selezionata */}
          {selectedEntity && (
            <div className="w-1/3 flex flex-col">
              <div className="bg-gray-800 rounded border border-gray-700 p-4 flex-1 overflow-y-auto">
                <h3 className="text-lg font-semibold text-white mb-4">{selectedEntity.name}</h3>
                
                <div className="space-y-4">
                  <div>
                    <h4 className="text-sm font-semibold text-gray-300 mb-1">Archetype</h4>
                    <p className={`${getTraitColor(selectedEntity.trait)} capitalize`}>{selectedEntity.trait}</p>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-semibold text-gray-300 mb-1">Consciousness State</h4>
                    <p className="text-white">{selectedEntity.consciousness_state}</p>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-semibold text-gray-300 mb-1">Energy Level</h4>
                    <div className="flex items-center space-x-2">
                      <div className="flex-1 bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-cyan-400 h-2 rounded-full transition-all"
                          style={{ width: `${(selectedEntity.energy_level || 0) * 100}%` }}
                        />
                      </div>
                      <span className="text-sm text-white">
                        {Math.round((selectedEntity.energy_level || 0) * 100)}%
                      </span>
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-semibold text-gray-300 mb-1">Capabilities</h4>
                    <div className="flex flex-wrap gap-1">
                      {selectedEntity.capabilities?.map((cap, i) => (
                        <span key={i} className="text-xs px-2 py-1 bg-gray-700 rounded text-gray-300">
                          {cap}
                        </span>
                      )) || <span className="text-gray-500">None listed</span>}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-semibold text-gray-300 mb-1">Colors</h4>
                    <div className="flex space-x-1">
                      {selectedEntity.colors?.map((color, i) => (
                        <div
                          key={i}
                          className="w-6 h-6 rounded border border-gray-600"
                          style={{ backgroundColor: color }}
                        />
                      )) || <span className="text-gray-500">No colors</span>}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-semibold text-gray-300 mb-1">Shape</h4>
                    <p className="text-white capitalize">{selectedEntity.shape || 'Unknown'}</p>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-semibold text-gray-300 mb-1">Goals</h4>
                    <p className="text-sm text-gray-300">
                      {selectedEntity.goals_count || 0} goals defined
                    </p>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-semibold text-gray-300 mb-1">Allies</h4>
                    <p className="text-sm text-gray-300">
                      {selectedEntity.allies_count || 0} allies
                    </p>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-semibold text-gray-300 mb-1">Created</h4>
                    <p className="text-sm text-gray-300">
                      {selectedEntity.creation_date ? new Date(selectedEntity.creation_date).toLocaleDateString() : 'Unknown'}
                    </p>
                    <p className="text-xs text-gray-500">by {selectedEntity.creator}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
} 