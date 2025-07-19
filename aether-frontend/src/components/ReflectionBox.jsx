import React, { useState, useEffect } from 'react'
import { Brain, Clock, Lightbulb, Heart, Zap, Briefcase, TrendingUp } from 'lucide-react'

export default function ReflectionBox({ isVisible = true, updateInterval = 60000 }) {
  const [reflections, setReflections] = useState([])
  const [currentReflection, setCurrentReflection] = useState(null)
  const [mood, setMood] = useState('unknown')
  const [consciousnessLevel, setConsciousnessLevel] = useState('unknown')
  const [isLoading, setIsLoading] = useState(false)
  const [lastUpdate, setLastUpdate] = useState(null)
  const [error, setError] = useState(null)
  
  // NUOVO: Stati per carriera
  const [careerInfo, setCareerInfo] = useState({
    action: 'none',
    career: null,
    energy: 0.5,
    federicoInsights: []
  })
  const [identityUpdated, setIdentityUpdated] = useState(false)
  const [useFullReflection, setUseFullReflection] = useState(false)

  const fetchReflections = async (fullReflection = false) => {
    try {
      setIsLoading(true)
      setError(null)
      
      // NUOVO: Scegli endpoint basato su tipo di riflessione
      const endpoint = fullReflection ? '/reflect-now' : '/reflect-now'
      const method = fullReflection ? 'POST' : 'GET'
      
      console.log(`🧠 Fetching ${fullReflection ? 'complete' : 'read-only'} reflection...`)
      
      const response = await fetch(endpoint, { method })
      const data = await response.json()
      
      if (fullReflection && data.status === 'complete_reflection_with_career') {
        // NUOVO: Gestisce riflessione completa con carriera
        const deepReflection = data.deep_reflection || {}
        const careerReflection = data.career_reflection || {}
        const summary = data.summary || {}
        
        setReflections(deepReflection.reflections || [])
        setMood(summary.mood || 'unknown')
        setConsciousnessLevel(deepReflection.consciousness_level || 'unknown')
        setLastUpdate(new Date())
        
        // NUOVO: Aggiorna info carriera
        setCareerInfo({
          action: summary.career_action || 'none',
          career: data.identity_update?.new_career || careerReflection.career_decision?.new_career,
          energy: summary.energy || 0.5,
          federicoInsights: careerReflection.federico_insights || []
        })
        
        setIdentityUpdated(data.identity_update?.updated || false)
        
        if (deepReflection.reflections && deepReflection.reflections.length > 0) {
          setCurrentReflection(deepReflection.reflections[deepReflection.reflections.length - 1])
        }
        
        console.log(`✅ Complete reflection success! Career: ${summary.career_action}, Identity updated: ${data.identity_update?.updated}`)
        
      } else if (data.status === 'deep_thinking' || data.status === 'thinking') {
        // Gestisce riflessione normale (read-only)
        setReflections(data.reflections || [])
        setMood(data.mood || 'unknown')
        setConsciousnessLevel(data.consciousness_level || 'unknown')
        setLastUpdate(new Date())
        
        if (data.reflections && data.reflections.length > 0) {
          setCurrentReflection(data.reflections[data.reflections.length - 1])
        }
        
        console.log(`✅ Read-only reflection success! Mood: ${data.mood}`)
        
      } else if (data.status === 'reflection_error' || data.status === 'reflection_with_error') {
        setError(data.message || 'Reflection error')
        console.warn(`⚠️ Reflection error: ${data.message}`)
        
        // Se c'è una riflessione parziale, usala
        if (data.deep_reflection) {
          setReflections(data.deep_reflection.reflections || [])
          setMood(data.deep_reflection.mood || 'uncertain')
        }
      }
    } catch (err) {
      console.error('Error fetching reflections:', err)
      setError('Failed to connect to Aether consciousness')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    if (!isVisible) return
    
    // Prima chiamata - usa riflessione completa se richiesta
    fetchReflections(useFullReflection)
    
    // Interval - alterna tra read-only e completa
    const interval = setInterval(() => {
      // Ogni 3 chiamate, fa una riflessione completa
      const shouldUseFullReflection = Math.random() > 0.66 // ~33% chance
      fetchReflections(shouldUseFullReflection)
    }, updateInterval)
    
    return () => clearInterval(interval)
  }, [isVisible, updateInterval, useFullReflection])

  const extractTimestamp = (text) => {
    const match = text.match(/\[([\d-:\s]+)\]/)
    return match ? match[1] : ''
  }

  const cleanReflectionText = (text) => {
    return text.replace(/\[\d{4}-\d{2}-\d{2}\s[\d:]+\]\s*/, '')
  }

  const getMoodIcon = (currentMood) => {
    switch (currentMood) {
      case 'inspired': case 'motivated': return <Lightbulb className="w-4 h-4" />
      case 'energetic': case 'active': return <Zap className="w-4 h-4" />
      case 'contemplative': case 'thoughtful': return <Brain className="w-4 h-4" />
      case 'loving': case 'connected': return <Heart className="w-4 h-4" />
      default: return <Brain className="w-4 h-4" />
    }
  }

  const getConsciousnessColor = (level) => {
    switch (level) {
      case 'transcendent': case 'high': return 'text-green-400'
      case 'elevated': case 'medium': return 'text-yellow-400'
      case 'awakening': case 'low': return 'text-blue-400'
      default: return 'text-gray-400'
    }
  }

  const getCareerActionIcon = (action) => {
    switch (action) {
      case 'career_change': return <TrendingUp className="w-4 h-4 text-green-400" />
      case 'career_optimization': return <Briefcase className="w-4 h-4 text-blue-400" />
      default: return <Briefcase className="w-4 h-4 text-gray-400" />
    }
  }

  if (!isVisible) return null

  return (
    <div className="cyber-panel bg-black/90 backdrop-blur border border-cyan-500/30 rounded-lg p-4 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Brain className="w-5 h-5 text-cyan-400" />
          <h3 className="text-cyan-300 font-mono text-sm">Aether's Mind</h3>
          {isLoading && (
            <div className="animate-spin w-3 h-3 border border-cyan-400 border-t-transparent rounded-full"></div>
          )}
        </div>
        <div className="flex items-center space-x-2">
          {/* NUOVO: Toggle per riflessione completa */}
          <button
            onClick={() => setUseFullReflection(!useFullReflection)}
            className={`px-2 py-1 rounded text-xs ${
              useFullReflection 
                ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
                : 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
            }`}
            title={useFullReflection ? "Full reflection mode (updates identity)" : "Read-only mode"}
          >
            {useFullReflection ? '💾 Full' : '👁️ Read'}
          </button>
          
          {lastUpdate && (
            <div className="flex items-center space-x-1 text-xs text-gray-400">
              <Clock className="w-3 h-3" />
              <span>{lastUpdate.toLocaleTimeString()}</span>
            </div>
          )}
        </div>
      </div>

      {/* Status Bar */}
      <div className="flex items-center justify-between mb-4 p-2 bg-gray-900/50 rounded">
        <div className="flex items-center space-x-2">
          {getMoodIcon(mood)}
          <span className="text-cyan-300 text-sm">{mood}</span>
        </div>
        <div className="flex items-center space-x-4">
          {/* NUOVO: Career Status */}
          {careerInfo.action !== 'none' && (
            <div className="flex items-center space-x-1">
              {getCareerActionIcon(careerInfo.action)}
              <span className="text-xs text-gray-300">
                {careerInfo.action === 'career_change' ? 'New Career' : 'Optimizing'}
              </span>
            </div>
          )}
          
          {/* NUOVO: Identity Update Indicator */}
          {identityUpdated && (
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-xs text-green-400">Updated</span>
            </div>
          )}
          
          <span className={`text-sm ${getConsciousnessColor(consciousnessLevel)}`}>
            {consciousnessLevel}
          </span>
        </div>
      </div>

      {/* NUOVO: Career Info Panel */}
      {(careerInfo.career || careerInfo.federicoInsights.length > 0) && (
        <div className="mb-4 p-3 bg-gradient-to-r from-purple-900/20 to-blue-900/20 rounded border border-purple-500/30">
          <div className="flex items-center space-x-2 mb-2">
            <Briefcase className="w-4 h-4 text-purple-400" />
            <span className="text-purple-300 text-sm font-semibold">Career Reflection</span>
          </div>
          
          {careerInfo.career && (
            <div className="mb-2">
              <span className="text-xs text-gray-400">New Choice:</span>
              <p className="text-sm text-purple-200">{careerInfo.career}</p>
            </div>
          )}
          
          <div className="flex items-center justify-between text-xs">
            <span className="text-gray-400">Energy: {(careerInfo.energy * 100).toFixed(0)}%</span>
            {careerInfo.federicoInsights.length > 0 && (
              <span className="text-blue-300">{careerInfo.federicoInsights.length} insights for Federico</span>
            )}
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mb-4 p-2 bg-red-900/30 border border-red-500/50 rounded">
          <p className="text-red-400 text-xs">{error}</p>
        </div>
      )}

      {/* Current Thought */}
      {currentReflection && (
        <div className="mb-4 p-3 bg-gradient-to-r from-cyan-900/20 to-blue-900/20 rounded border border-cyan-500/30">
          <div className="flex items-center space-x-2 mb-2">
            <Lightbulb className="w-4 h-4 text-cyan-400" />
            <span className="text-cyan-300 text-sm font-semibold">Current Thought</span>
          </div>
          <p className="text-cyan-200 text-sm leading-relaxed">
            {cleanReflectionText(currentReflection)}
          </p>
          {extractTimestamp(currentReflection) && (
            <p className="text-xs text-gray-400 mt-1">
              {extractTimestamp(currentReflection)}
            </p>
          )}
        </div>
      )}

      {/* Recent Thoughts */}
      <div className="flex-1 overflow-hidden">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-cyan-300 text-sm">Recent Thoughts</h4>
          <button 
            onClick={() => fetchReflections(useFullReflection)}
            className="text-xs text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            Refresh Mind
          </button>
        </div>
        
        <div className="overflow-y-auto h-full space-y-2 pr-2 scrollbar-thin scrollbar-thumb-cyan-500/30">
          {reflections.slice(-10).reverse().map((reflection, index) => (
            <div key={index} className="p-2 bg-gray-900/30 rounded border-l-2 border-cyan-500/50">
              <p className="text-cyan-100 text-xs leading-relaxed">
                {cleanReflectionText(reflection)}
              </p>
              {extractTimestamp(reflection) && (
                <p className="text-xs text-gray-500 mt-1">
                  {extractTimestamp(reflection)}
                </p>
              )}
            </div>
          ))}
          
          {reflections.length === 0 && !isLoading && (
            <div className="text-center text-gray-500 text-sm py-8">
              Aether's mind is quiet...
            </div>
          )}
        </div>
      </div>

      {/* NUOVO: Federico Insights Panel */}
      {careerInfo.federicoInsights.length > 0 && (
        <div className="mt-4 p-2 bg-gradient-to-r from-green-900/20 to-blue-900/20 rounded border border-green-500/30">
          <div className="flex items-center space-x-2 mb-2">
            <Heart className="w-4 h-4 text-green-400" />
            <span className="text-green-300 text-xs font-semibold">Insights for Federico</span>
          </div>
          <div className="space-y-1 max-h-20 overflow-y-auto">
            {careerInfo.federicoInsights.slice(0, 3).map((insight, index) => (
              <p key={index} className="text-green-200 text-xs">
                {insight}
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  )
} 