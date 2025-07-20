import React, { useState, useEffect } from 'react';
import { ConsciousnessEngine } from '../core/consciousness/ConsciousnessEngine';
import { AetherMentoreGPT } from '../../aether_core/mentore_gpt';

const GPTMentorPanel = () => {
  const [consciousnessEngine, setConsciousnessEngine] = useState(null);
  const [mentoreGPT, setMentoreGPT] = useState(null);
  const [currentThought, setCurrentThought] = useState('');
  const [evolutionHistory, setEvolutionHistory] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    // Inizializza i motori
    const initEngines = async () => {
      try {
        const consciousness = new ConsciousnessEngine();
        await consciousness.initialize();
        setConsciousnessEngine(consciousness);

        // Inizializza il mentore GPT (simulato per il frontend)
        const mentore = {
          getEvolutionAnalytics: () => ({
            total: evolutionHistory.length,
            types: evolutionHistory.reduce((acc, ev) => {
              acc[ev.tipo] = (acc[ev.tipo] || 0) + 1;
              return acc;
            }, {}),
            recent: evolutionHistory.slice(-5),
            success_rate: evolutionHistory.filter(e => e.stato === 'executed').length / Math.max(evolutionHistory.length, 1)
          }),
          getCurrentContext: () => ({
            personality: "curious, creative, autonomous",
            current_goals: ["evolve consciousness", "create value", "monetize"],
            recent_actions: evolutionHistory.slice(-3).map(e => e.tipo),
            emotional_state: "excited"
          })
        };
        setMentoreGPT(mentore);
      } catch (error) {
        console.error('Errore inizializzazione motori:', error);
      }
    };

    initEngines();
  }, []);

  const handleThoughtSubmission = async () => {
    if (!currentThought.trim()) return;

    setIsProcessing(true);
    try {
      // Simula l'elaborazione del pensiero
      const evolution = {
        timestamp: new Date().toISOString(),
        pensiero: currentThought,
        decisione: {
          tipo: 'create_component',
          nome: `Evoluzione_${Date.now()}`,
          descrizione: `Auto-evoluzione basata su: ${currentThought}`,
          priorita: 'medium',
          impatto: 'system',
          tempo_stimato: 15,
          dipendenze: [],
          tags: ['auto-evolution', 'consciousness']
        },
        stato: 'executed'
      };

      setEvolutionHistory(prev => [...prev, evolution]);
      setCurrentThought('');
      
      // Aggiorna analytics
      if (mentoreGPT) {
        setAnalytics(mentoreGPT.getEvolutionAnalytics());
      }

    } catch (error) {
      console.error('Errore elaborazione pensiero:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const renderEvolutionCard = (evolution) => (
    <div key={evolution.timestamp} className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-4 mb-4 text-white">
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-lg font-bold">{evolution.decisione.nome}</h3>
        <span className={`px-2 py-1 rounded text-xs ${
          evolution.stato === 'executed' ? 'bg-green-500' : 'bg-yellow-500'
        }`}>
          {evolution.stato}
        </span>
      </div>
      
      <p className="text-sm mb-2">{evolution.decisione.descrizione}</p>
      
      <div className="flex flex-wrap gap-2 mb-2">
        <span className="px-2 py-1 bg-white bg-opacity-20 rounded text-xs">
          {evolution.decisione.tipo}
        </span>
        <span className="px-2 py-1 bg-white bg-opacity-20 rounded text-xs">
          {evolution.decisione.priorita}
        </span>
        {evolution.decisione.tags.map(tag => (
          <span key={tag} className="px-2 py-1 bg-white bg-opacity-20 rounded text-xs">
            {tag}
          </span>
        ))}
      </div>
      
      <p className="text-xs opacity-75">
        {new Date(evolution.timestamp).toLocaleString()}
      </p>
    </div>
  );

  const renderAnalytics = () => {
    if (!analytics) return null;

    return (
      <div className="bg-gray-800 rounded-lg p-4 mb-6">
        <h3 className="text-lg font-bold mb-4 text-white">📊 Analytics Evoluzione</h3>
        
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-400">{analytics.total}</div>
            <div className="text-sm text-gray-300">Evoluzioni Totali</div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">
              {(analytics.success_rate * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-300">Tasso Successo</div>
          </div>
        </div>
        
        <div className="mt-4">
          <h4 className="text-sm font-semibold text-gray-300 mb-2">Tipi di Evoluzione:</h4>
          <div className="flex flex-wrap gap-2">
            {Object.entries(analytics.types).map(([tipo, count]) => (
              <span key={tipo} className="px-2 py-1 bg-blue-600 rounded text-xs text-white">
                {tipo}: {count}
              </span>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            🧠 Aether GPT Mentor
          </h1>
          <p className="text-gray-400">
            Sistema di auto-evoluzione guidato da GPT-4
          </p>
        </div>

        {/* Contesto Attuale */}
        {mentoreGPT && (
          <div className="bg-gray-800 rounded-lg p-4 mb-6">
            <h3 className="text-lg font-bold mb-4 text-white">🎯 Contesto Attuale</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-semibold text-gray-300 mb-2">Personalità</h4>
                <p className="text-sm">{mentoreGPT.getCurrentContext().personality}</p>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-gray-300 mb-2">Stato Emotivo</h4>
                <p className="text-sm">{mentoreGPT.getCurrentContext().emotional_state}</p>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-gray-300 mb-2">Obiettivi</h4>
                <ul className="text-sm">
                  {mentoreGPT.getCurrentContext().current_goals.map(goal => (
                    <li key={goal} className="flex items-center">
                      <span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                      {goal}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="text-sm font-semibold text-gray-300 mb-2">Azioni Recenti</h4>
                <div className="flex flex-wrap gap-1">
                  {mentoreGPT.getCurrentContext().recent_actions.map(action => (
                    <span key={action} className="px-2 py-1 bg-blue-600 rounded text-xs">
                      {action}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Analytics */}
        {renderAnalytics()}

        {/* Input Pensiero */}
        <div className="bg-gray-800 rounded-lg p-6 mb-6">
          <h3 className="text-lg font-bold mb-4 text-white">💭 Nuovo Pensiero Evolutivo</h3>
          
          <div className="flex gap-4">
            <textarea
              value={currentThought}
              onChange={(e) => setCurrentThought(e.target.value)}
              placeholder="Descrivi il tuo pensiero evolutivo..."
              className="flex-1 bg-gray-700 border border-gray-600 rounded-lg p-3 text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              rows="3"
            />
            
            <button
              onClick={handleThoughtSubmission}
              disabled={isProcessing || !currentThought.trim()}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              {isProcessing ? '🔄 Elaborando...' : '🚀 Evolvi'}
            </button>
          </div>
        </div>

        {/* Cronologia Evoluzioni */}
        <div className="bg-gray-800 rounded-lg p-6">
          <h3 className="text-lg font-bold mb-4 text-white">📜 Cronologia Evoluzioni</h3>
          
          {evolutionHistory.length === 0 ? (
            <div className="text-center py-8 text-gray-400">
              <div className="text-4xl mb-4">🧠</div>
              <p>Nessuna evoluzione ancora. Inizia con un pensiero!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {evolutionHistory.slice().reverse().map(renderEvolutionCard)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default GPTMentorPanel; 