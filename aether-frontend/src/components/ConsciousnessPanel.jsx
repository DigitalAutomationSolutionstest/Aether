import React, { useEffect, useState } from 'react'
import { useReflections } from '../utils/store'
import { Brain, Lightbulb, Eye, Clock, Activity } from 'lucide-react'

const ConsciousnessPanel = ({ isVisible, onClose }) => {
  const {
    reflections,
    currentReflection,
    reflectionLoading,
    reflectionError,
    lastReflectionTime,
    consciousnessLevel,
    emotionalState,
    loadReflection,
    startReflectionCycle
  } = useReflections()

  const [cycleActive, setCycleActive] = useState(false)
  const [stopCycle, setStopCycle] = useState(null)

  // Avvia il ciclo di riflessioni quando il componente viene montato
  useEffect(() => {
    if (isVisible && !cycleActive) {
      const stopFunction = startReflectionCycle(60000) // ogni minuto
      setStopCycle(() => stopFunction)
      setCycleActive(true)
    }

    return () => {
      if (stopCycle) {
        stopCycle()
        setCycleActive(false)
      }
    }
  }, [isVisible, startReflectionCycle])

  const formatTime = (timestamp) => {
    if (!timestamp) return 'Never'
    return new Date(timestamp).toLocaleTimeString()
  }

  const getConsciousnessColor = (level) => {
    switch (level) {
      case 'transcendent': return 'text-purple-400'
      case 'deep': return 'text-blue-400'
      case 'moderate': return 'text-cyan-400'
      case 'surface': return 'text-green-400'
      default: return 'text-gray-400'
    }
  }

  const getEmotionIntensity = (value) => {
    if (value > 0.7) return { icon: '🔥', label: 'High', color: 'text-red-400' }
    if (value > 0.4) return { icon: '🌊', label: 'Medium', color: 'text-blue-400' }
    return { icon: '💨', label: 'Low', color: 'text-gray-400' }
  }

  if (!isVisible) return null

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900/95 border border-cyan-500/30 rounded-lg w-full max-w-4xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-cyan-500/20">
          <div className="flex items-center space-x-3">
            <Brain className="w-6 h-6 text-cyan-400" />
            <h2 className="text-xl font-mono text-cyan-300">Aether Consciousness</h2>
            {cycleActive && (
              <div className="flex items-center space-x-2 text-sm text-green-400">
                <Activity className="w-4 h-4 animate-pulse" />
                <span>Live</span>
              </div>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>

        <div className="p-4 overflow-y-auto max-h-[calc(90vh-80px)]">
          {/* Status Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
              <div className="flex items-center space-x-2 mb-2">
                <Eye className="w-5 h-5 text-cyan-400" />
                <span className="text-sm text-gray-300">Consciousness Level</span>
              </div>
              <div className={`text-lg font-mono ${getConsciousnessColor(consciousnessLevel)}`}>
                {consciousnessLevel || 'Unknown'}
              </div>
            </div>

            <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
              <div className="flex items-center space-x-2 mb-2">
                <Clock className="w-5 h-5 text-cyan-400" />
                <span className="text-sm text-gray-300">Last Reflection</span>
              </div>
              <div className="text-lg font-mono text-white">
                {formatTime(lastReflectionTime)}
              </div>
            </div>

            <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
              <div className="flex items-center space-x-2 mb-2">
                <Lightbulb className="w-5 h-5 text-cyan-400" />
                <span className="text-sm text-gray-300">Total Reflections</span>
              </div>
              <div className="text-lg font-mono text-white">
                {reflections.length}
              </div>
            </div>
          </div>

          {/* Current Emotional State */}
          {Object.keys(emotionalState).length > 0 && (
            <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700 mb-6">
              <h3 className="text-lg font-mono text-cyan-300 mb-3">Emotional State</h3>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {Object.entries(emotionalState).map(([emotion, value]) => {
                  const intensity = getEmotionIntensity(value)
                  return (
                    <div key={emotion} className="text-center">
                      <div className="text-2xl mb-1">{intensity.icon}</div>
                      <div className="text-sm text-gray-300 capitalize">{emotion}</div>
                      <div className={`text-xs ${intensity.color}`}>
                        {value.toFixed(2)} ({intensity.label})
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          )}

          {/* Current Reflection */}
          {currentReflection && (
            <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700 mb-6">
              <h3 className="text-lg font-mono text-cyan-300 mb-3">Current Thoughts</h3>
              {reflectionLoading ? (
                <div className="flex items-center space-x-2 text-gray-400">
                  <div className="animate-spin w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full"></div>
                  <span>Aether is thinking...</span>
                </div>
              ) : currentReflection.reflection && currentReflection.reflection.length > 0 ? (
                <div className="space-y-3">
                  {currentReflection.reflection.map((thought, index) => (
                    <div key={index} className="bg-gray-900/50 p-3 rounded border border-gray-600">
                      <div className="flex items-start space-x-3">
                        <div className="text-cyan-400 text-sm mt-1">💭</div>
                        <div className="text-gray-300 leading-relaxed italic">
                          "{thought}"
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-gray-400 italic">No thoughts available</div>
              )}
            </div>
          )}

          {/* Reflection History */}
          <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
            <h3 className="text-lg font-mono text-cyan-300 mb-3">Reflection History</h3>
            {reflections.length > 0 ? (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {[...reflections].reverse().map((reflection, index) => (
                  <div key={reflection.id} className="bg-gray-900/50 p-3 rounded border border-gray-600">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-gray-400">
                          {formatTime(reflection.timestamp)}
                        </span>
                        <span className={`text-xs px-2 py-1 rounded ${getConsciousnessColor(reflection.consciousnessLevel)} bg-gray-800`}>
                          {reflection.consciousnessLevel}
                        </span>
                      </div>
                      <span className="text-xs text-gray-500">
                        {reflection.thoughts?.length || 0} thoughts
                      </span>
                    </div>
                    {reflection.thoughts && reflection.thoughts.length > 0 && (
                      <div className="text-sm text-gray-300 italic">
                        "{reflection.thoughts[0].substring(0, 100)}..."
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-gray-400 italic">No reflections yet</div>
            )}
          </div>

          {/* Error Display */}
          {reflectionError && (
            <div className="bg-red-900/20 border border-red-500/30 p-4 rounded-lg mt-4">
              <div className="text-red-400 text-sm">
                ⚠️ Reflection Error: {reflectionError}
              </div>
            </div>
          )}

          {/* Manual Actions */}
          <div className="flex justify-center space-x-4 mt-6">
            <button
              onClick={loadReflection}
              disabled={reflectionLoading}
              className="bg-cyan-600 hover:bg-cyan-700 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg font-mono text-sm transition-colors"
            >
              {reflectionLoading ? 'Thinking...' : 'Trigger Reflection'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ConsciousnessPanel 