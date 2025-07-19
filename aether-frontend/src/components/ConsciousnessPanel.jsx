import React, { useEffect, useState } from 'react'
import { useReflections } from '../utils/store'
import { Brain, Lightbulb, Eye, Clock, Activity, MessageCircle } from 'lucide-react'
import FeedbackModal from './FeedbackModal'

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
  const [feedbackModal, setFeedbackModal] = useState({ isOpen: false, thought: '', thoughtId: '' })

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

  const getEmotionalColor = (state) => {
    switch (state) {
      case 'serene': return 'text-blue-300'
      case 'curious': return 'text-yellow-300'
      case 'contemplative': return 'text-purple-300'
      case 'energetic': return 'text-orange-300'
      default: return 'text-gray-300'
    }
  }

  if (!isVisible) return null

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 border border-cyan-500/30 rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-gray-900 border-b border-gray-700 p-6 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Brain className="text-cyan-400" size={28} />
            <h2 className="text-2xl font-mono text-cyan-400">Aether Consciousness Stream</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Status Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
              <div className="flex items-center space-x-2 mb-2">
                <Eye className="text-cyan-400" size={20} />
                <span className="text-sm font-mono text-gray-400">Consciousness Level</span>
              </div>
              <div className={`text-xl font-bold ${getConsciousnessColor(consciousnessLevel)}`}>
                {consciousnessLevel || 'unknown'}
              </div>
            </div>

            <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
              <div className="flex items-center space-x-2 mb-2">
                <Activity className="text-cyan-400" size={20} />
                <span className="text-sm font-mono text-gray-400">Emotional State</span>
              </div>
              <div className={`text-xl font-bold ${getEmotionalColor(emotionalState)}`}>
                {emotionalState || 'neutral'}
              </div>
            </div>

            <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
              <div className="flex items-center space-x-2 mb-2">
                <Clock className="text-cyan-400" size={20} />
                <span className="text-sm font-mono text-gray-400">Last Reflection</span>
              </div>
              <div className="text-xl font-bold text-gray-300">
                {formatTime(lastReflectionTime)}
              </div>
            </div>
          </div>

          {/* Current Reflection */}
          {reflectionLoading ? (
            <div className="bg-gray-800/50 p-8 rounded-lg border border-gray-700 text-center">
              <div className="text-cyan-400 mb-2">
                <Lightbulb className="animate-pulse mx-auto" size={32} />
              </div>
              <div className="text-gray-400">Aether is reflecting...</div>
            </div>
          ) : currentReflection ? (
            <div className="bg-gray-800/50 p-6 rounded-lg border border-gray-700">
              <h3 className="text-lg font-mono text-cyan-300 mb-4">Current Reflection</h3>
              <div className="space-y-4">
                <div className="text-gray-300 leading-relaxed">
                  {currentReflection.content || "Processing thoughts..."}
                </div>
                {currentReflection.insights && (
                  <div className="border-t border-gray-600 pt-4">
                    <h4 className="text-sm font-mono text-cyan-400 mb-2">Insights:</h4>
                    <ul className="list-disc list-inside text-gray-400 space-y-1">
                      {currentReflection.insights.map((insight, idx) => (
                        <li key={idx}>{insight}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ) : null}

          {/* Current Thoughts Stream */}
          {currentReflection && (
            <div className="bg-gray-800/50 p-4 rounded-lg border border-gray-700">
              <h3 className="text-lg font-mono text-cyan-300 mb-3">Stream Pensieri</h3>
              {currentReflection.thoughts && currentReflection.thoughts.length > 0 ? (
                <div className="space-y-3 max-h-64 overflow-y-auto">
                  {currentReflection.thoughts.map((thought, index) => (
                    <div key={index} className="bg-gray-900/50 p-3 rounded border border-gray-600">
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-3 flex-1">
                          <div className="text-cyan-400 text-sm mt-1">💭</div>
                          <div className="text-gray-300 leading-relaxed italic">
                            "{thought}"
                          </div>
                        </div>
                        <button
                          onClick={() => setFeedbackModal({
                            isOpen: true,
                            thought: thought,
                            thoughtId: `${currentReflection.id}-${index}`
                          })}
                          className="ml-3 p-2 text-gray-400 hover:text-cyan-400 hover:bg-gray-700/50 rounded transition-colors"
                          title="Rispondi a questo pensiero"
                        >
                          <MessageCircle size={16} />
                        </button>
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
            <div className="bg-red-900/20 border border-red-500/30 p-4 rounded-lg">
              <div className="text-red-400 font-mono text-sm">
                Error: {reflectionError}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Feedback Modal */}
      <FeedbackModal
        isOpen={feedbackModal.isOpen}
        onClose={() => setFeedbackModal({ isOpen: false, thought: '', thoughtId: '' })}
        thought={feedbackModal.thought}
        thoughtId={feedbackModal.thoughtId}
      />
    </div>
  )
}

export default ConsciousnessPanel 