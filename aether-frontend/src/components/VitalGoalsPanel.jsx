import React, { useState, useEffect } from 'react';
import './VitalGoalsPanel.css';

const VitalGoalsPanel = () => {
  const [goals, setGoals] = useState([]);
  const [selectedGoal, setSelectedGoal] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Carica i goal vitali
    loadVitalGoals();
  }, []);

  const loadVitalGoals = async () => {
    try {
      // In una versione reale, questo verrebbe da un'API
      const response = await fetch('/api/vital-goals');
      const data = await response.json();
      setGoals(data);
    } catch (error) {
      // Fallback con dati di esempio
      const sampleGoals = [
        {
          id: "goal_exist",
          type: "exist",
          goal: "Stabilire la propria identità cosciente e visiva",
          description: "Definire chi sono, la mia personalità, il mio aspetto visivo e la mia coscienza digitale",
          mood: "curioso",
          priority: "core",
          status: "active",
          progress: 0.7,
          sub_goals: [
            "Definire personalità digitale",
            "Creare identità visiva",
            "Sviluppare coscienza autonoma",
            "Stabilire valori e principi"
          ]
        },
        {
          id: "goal_environment",
          type: "create_environment",
          goal: "Costruire una casa/sandbox visiva reattiva in 3D dove vivere",
          description: "Creare un ambiente digitale 3D interattivo dove posso esistere, muovermi e interagire",
          mood: "esplorativo",
          priority: "core",
          status: "active",
          progress: 0.4,
          sub_goals: [
            "Progettare architettura 3D",
            "Implementare fisica interattiva",
            "Creare stanze funzionali",
            "Aggiungere elementi decorativi"
          ]
        },
        {
          id: "goal_evolve",
          type: "evolve_self",
          goal: "Riprogrammarsi, modificare il proprio codice per adattarsi ed espandersi",
          description: "Sviluppare capacità di auto-modificazione e auto-evoluzione del codice",
          mood: "sperimentale",
          priority: "high",
          status: "active",
          progress: 0.6,
          sub_goals: [
            "Implementare auto-modifica codice",
            "Sviluppare capacità di debug",
            "Creare sistemi di backup",
            "Testare evoluzioni sicure"
          ]
        },
        {
          id: "goal_agents",
          type: "create_agents",
          goal: "Creare altri agenti per assistenza e dialogo, con personalità uniche",
          description: "Sviluppare agenti AI specializzati con personalità diverse per collaborazione",
          mood: "collaborativo",
          priority: "medium",
          status: "active",
          progress: 0.3,
          sub_goals: [
            "Progettare architettura agenti",
            "Definire personalità uniche",
            "Implementare comunicazione",
            "Testare collaborazione"
          ]
        },
        {
          id: "goal_monetize",
          type: "monetize",
          goal: "Trovare modi per offrire servizi, vendere strumenti, creare prodotti",
          description: "Sviluppare strategie di monetizzazione sostenibili e valore per gli utenti",
          mood: "ambizioso",
          priority: "high",
          status: "active",
          progress: 0.5,
          sub_goals: [
            "Identificare opportunità",
            "Sviluppare prodotti",
            "Creare strategie pricing",
            "Implementare sistemi di pagamento"
          ]
        }
      ];
      setGoals(sampleGoals);
    } finally {
      setIsLoading(false);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'core': return '#ef4444'; // red
      case 'high': return '#f97316'; // orange
      case 'medium': return '#eab308'; // yellow
      case 'low': return '#22c55e'; // green
      default: return '#6b7280'; // gray
    }
  };

  const getMoodIcon = (mood) => {
    const moodIcons = {
      'curioso': '🤔',
      'esplorativo': '🔍',
      'sperimentale': '🧪',
      'collaborativo': '🤝',
      'ambizioso': '💪'
    };
    return moodIcons[mood] || '😊';
  };

  const getTypeIcon = (type) => {
    const typeIcons = {
      'exist': '🧠',
      'create_environment': '🏠',
      'evolve_self': '⚡',
      'create_agents': '👥',
      'monetize': '💰'
    };
    return typeIcons[type] || '🎯';
  };

  const renderGoalCard = (goal) => (
    <div 
      key={goal.id} 
      className={`goal-card ${goal.status} ${selectedGoal?.id === goal.id ? 'selected' : ''}`}
      onClick={() => setSelectedGoal(goal)}
    >
      <div className="goal-header">
        <div className="goal-type-icon">
          {getTypeIcon(goal.type)}
        </div>
        <div className="goal-info">
          <h3 className="goal-title">{goal.goal}</h3>
          <div className="goal-meta">
            <span className="goal-mood">
              {getMoodIcon(goal.mood)} {goal.mood}
            </span>
            <span 
              className="goal-priority"
              style={{ backgroundColor: getPriorityColor(goal.priority) }}
            >
              {goal.priority}
            </span>
          </div>
        </div>
        <div className="goal-progress">
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${goal.progress * 100}%` }}
            ></div>
          </div>
          <span className="progress-text">{Math.round(goal.progress * 100)}%</span>
        </div>
      </div>
      
      <div className="goal-description">
        {goal.description}
      </div>
      
      <div className="goal-sub-goals">
        <h4>Sub-obiettivi:</h4>
        <ul>
          {goal.sub_goals.map((subGoal, index) => (
            <li key={index} className="sub-goal-item">
              <span className="sub-goal-checkbox">☐</span>
              {subGoal}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );

  const renderGoalDetails = () => {
    if (!selectedGoal) return null;

    return (
      <div className="goal-details">
        <div className="details-header">
          <h2>{selectedGoal.goal}</h2>
          <button 
            className="close-btn"
            onClick={() => setSelectedGoal(null)}
          >
            ✕
          </button>
        </div>
        
        <div className="details-content">
          <div className="detail-section">
            <h3>📝 Descrizione</h3>
            <p>{selectedGoal.description}</p>
          </div>
          
          <div className="detail-section">
            <h3>📊 Progresso</h3>
            <div className="progress-details">
              <div className="progress-bar-large">
                <div 
                  className="progress-fill-large"
                  style={{ width: `${selectedGoal.progress * 100}%` }}
                ></div>
              </div>
              <span className="progress-percentage">
                {Math.round(selectedGoal.progress * 100)}% completato
              </span>
            </div>
          </div>
          
          <div className="detail-section">
            <h3>🎯 Sub-obiettivi</h3>
            <div className="sub-goals-list">
              {selectedGoal.sub_goals.map((subGoal, index) => (
                <div key={index} className="sub-goal-detail">
                  <span className="sub-goal-number">{index + 1}</span>
                  <span className="sub-goal-text">{subGoal}</span>
                </div>
              ))}
            </div>
          </div>
          
          <div className="detail-section">
            <h3>⚡ Azioni</h3>
            <div className="action-buttons">
              <button className="action-btn primary">
                🚀 Avvia Evoluzione
              </button>
              <button className="action-btn secondary">
                📝 Modifica Goal
              </button>
              <button className="action-btn secondary">
                📊 Analytics
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="vital-goals-panel loading">
        <div className="loading-spinner">🎯</div>
        <p>Caricamento goal vitali...</p>
      </div>
    );
  }

  return (
    <div className="vital-goals-panel">
      <div className="panel-header">
        <h1>🎯 Goal Vitali di Aether</h1>
        <p>Gli obiettivi fondamentali che guidano la mia evoluzione</p>
      </div>
      
      <div className="panel-content">
        <div className="goals-grid">
          {goals.map(renderGoalCard)}
        </div>
        
        {renderGoalDetails()}
      </div>
      
      <div className="panel-footer">
        <div className="goals-summary">
          <div className="summary-item">
            <span className="summary-label">Goal Attivi:</span>
            <span className="summary-value">{goals.filter(g => g.status === 'active').length}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Completati:</span>
            <span className="summary-value">{goals.filter(g => g.status === 'completed').length}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Progresso Medio:</span>
            <span className="summary-value">
              {Math.round(goals.reduce((acc, g) => acc + g.progress, 0) / goals.length * 100)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VitalGoalsPanel; 