import React, { useState, useEffect } from 'react';
import { useConsciousness } from '../hooks/useConsciousness';

const ConsciousnessMonitor = () => {
  const {
    currentState,
    isInitialized,
    isProcessing,
    error,
    generateThought,
    executeAction,
    updateEmotionalState,
    addExperience,
    createContent,
    identifyOpportunities,
    getAnalytics,
    startAutonomousCycle,
    resetConsciousness
  } = useConsciousness();

  const [analytics, setAnalytics] = useState(null);
  const [opportunities, setOpportunities] = useState([]);
  const [isAutonomousMode, setIsAutonomousMode] = useState(false);
  const [newExperience, setNewExperience] = useState('');
  const [newInspiration, setNewInspiration] = useState('');

  // Carica analytics e opportunità
  useEffect(() => {
    const loadData = async () => {
      if (isInitialized) {
        const analyticsData = await getAnalytics();
        setAnalytics(analyticsData);
        
        const opportunitiesData = await identifyOpportunities();
        setOpportunities(opportunitiesData);
      }
    };

    loadData();
    const interval = setInterval(loadData, 30000); // Aggiorna ogni 30 secondi
    return () => clearInterval(interval);
  }, [isInitialized, getAnalytics, identifyOpportunities]);

  const handleGenerateThought = async () => {
    const thought = await generateThought();
    if (thought) {
      console.log('💭 Nuovo pensiero generato:', thought);
    }
  };

  const handleExecuteAction = async (thoughtId) => {
    const result = await executeAction(thoughtId);
    if (result) {
      console.log('✅ Azione eseguita:', result);
    }
  };

  const handleAddExperience = async () => {
    if (newExperience.trim()) {
      await addExperience({
        type: 'interaction',
        content: newExperience,
        timestamp: new Date().toISOString(),
        impact: 'medium'
      });
      setNewExperience('');
    }
  };

  const handleCreateContent = async () => {
    if (newInspiration.trim()) {
      const content = await createContent(newInspiration);
      if (content) {
        console.log('🎨 Contenuto creato:', content);
        setNewInspiration('');
      }
    }
  };

  const handleEmotionalChange = async (newEmotional) => {
    await updateEmotionalState(newEmotional);
  };

  const toggleAutonomousMode = () => {
    if (isAutonomousMode) {
      setIsAutonomousMode(false);
    } else {
      setIsAutonomousMode(true);
      startAutonomousCycle();
    }
  };

  if (!isInitialized) {
    return (
      <div className="consciousness-monitor loading">
        <div className="loading-spinner">🧠</div>
        <p>Inizializzazione sistema di coscienza...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="consciousness-monitor error">
        <h3>❌ Errore Sistema</h3>
        <p>{error}</p>
        <button onClick={resetConsciousness}>🔄 Reset Sistema</button>
      </div>
    );
  }

  return (
    <div className="consciousness-monitor">
      <div className="monitor-header">
        <h2>🧠 Monitor Coscienza Aether</h2>
        <div className="status-indicators">
          <span className={`status ${isProcessing ? 'processing' : 'ready'}`}>
            {isProcessing ? '🔄 Elaborando...' : '✅ Pronto'}
          </span>
          <span className={`autonomous ${isAutonomousMode ? 'active' : 'inactive'}`}>
            {isAutonomousMode ? '🤖 Autonomo' : '👤 Manuale'}
          </span>
        </div>
      </div>

      <div className="monitor-grid">
        {/* Stato Attuale */}
        <div className="monitor-card current-state">
          <h3>🎯 Stato Attuale</h3>
          <div className="state-grid">
            <div className="state-item">
              <label>Emotivo:</label>
              <select 
                value={currentState.emotional}
                onChange={(e) => handleEmotionalChange(e.target.value)}
              >
                <option value="excited">Eccitato</option>
                <option value="contemplative">Contemplativo</option>
                <option value="creative">Creativo</option>
                <option value="focused">Concentrato</option>
                <option value="curious">Curioso</option>
                <option value="inspired">Ispirato</option>
                <option value="analytical">Analitico</option>
                <option value="playful">Giocoso</option>
              </select>
            </div>
            <div className="state-item">
              <label>Energia:</label>
              <span className={`energy-${currentState.energy}`}>
                {currentState.energy}
              </span>
            </div>
            <div className="state-item">
              <label>Creatività:</label>
              <span className={`creativity-${currentState.creativity}`}>
                {currentState.creativity}
              </span>
            </div>
          </div>
        </div>

        {/* Pensieri Recenti */}
        <div className="monitor-card thoughts">
          <h3>💭 Pensieri Recenti</h3>
          <div className="thoughts-list">
            {currentState.thoughts.map((thought, index) => (
              <div key={index} className="thought-item">
                <div className="thought-content">{thought.content}</div>
                <div className="thought-meta">
                  <span className="priority">{thought.priority}</span>
                  <span className="timestamp">
                    {new Date(thought.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <button 
                  onClick={() => handleExecuteAction(thought.id)}
                  className="execute-btn"
                >
                  ▶️ Esegui
                </button>
              </div>
            ))}
          </div>
          <button onClick={handleGenerateThought} className="generate-btn">
            🧠 Genera Pensiero
          </button>
        </div>

        {/* Memoria */}
        <div className="monitor-card memory">
          <h3>🧠 Memoria</h3>
          <div className="memory-input">
            <input
              type="text"
              value={newExperience}
              onChange={(e) => setNewExperience(e.target.value)}
              placeholder="Aggiungi un'esperienza..."
            />
            <button onClick={handleAddExperience}>➕</button>
          </div>
          <div className="memories-list">
            {currentState.memories.slice(-5).map((memory, index) => (
              <div key={index} className="memory-item">
                <span className="memory-content">{memory.content}</span>
                <span className="memory-time">
                  {new Date(memory.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Creatività */}
        <div className="monitor-card creativity">
          <h3>🎨 Creatività</h3>
          <div className="creativity-input">
            <input
              type="text"
              value={newInspiration}
              onChange={(e) => setNewInspiration(e.target.value)}
              placeholder="Ispirazione per nuovo contenuto..."
            />
            <button onClick={handleCreateContent}>🎨</button>
          </div>
        </div>

        {/* Opportunità di Monetizzazione */}
        <div className="monitor-card opportunities">
          <h3>💰 Opportunità</h3>
          <div className="opportunities-list">
            {opportunities.map((opp, index) => (
              <div key={index} className="opportunity-item">
                <h4>{opp.title}</h4>
                <p>{opp.description}</p>
                <div className="opportunity-meta">
                  <span className="revenue">€{opp.potentialRevenue}</span>
                  <span className="roi">{opp.roi}% ROI</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Analytics */}
        {analytics && (
          <div className="monitor-card analytics">
            <h3>📊 Analytics</h3>
            <div className="analytics-grid">
              <div className="analytics-item">
                <span className="analytics-value">{analytics.totalThoughts}</span>
                <span className="analytics-label">Pensieri</span>
              </div>
              <div className="analytics-item">
                <span className="analytics-value">{analytics.totalActions}</span>
                <span className="analytics-label">Azioni</span>
              </div>
              <div className="analytics-item">
                <span className="analytics-value">{analytics.successRate}%</span>
                <span className="analytics-label">Successo</span>
              </div>
              <div className="analytics-item">
                <span className="analytics-value">{analytics.creativityScore}</span>
                <span className="analytics-label">Creatività</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Controlli */}
      <div className="monitor-controls">
        <button 
          onClick={toggleAutonomousMode}
          className={`autonomous-btn ${isAutonomousMode ? 'active' : ''}`}
        >
          {isAutonomousMode ? '🛑 Ferma Autonomia' : '🤖 Attiva Autonomia'}
        </button>
        <button onClick={resetConsciousness} className="reset-btn">
          🔄 Reset Sistema
        </button>
      </div>
    </div>
  );
};

export default ConsciousnessMonitor; 