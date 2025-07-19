import React, { useState, useEffect } from 'react';
import { useStore } from '../utils/store';
import { 
  updateIdentityField, 
  updateMultipleFields,
  getModificationHistory,
  getEvolutionStats,
  applyTransformationPreset,
  TRANSFORMATION_PRESETS,
  validateField
} from '../utils/autoRegulation';

const ControlPanel = () => {
  const { identity, setIdentity, isConnected } = useStore();
  const [modifying, setModifying] = useState(false);
  const [modificationHistory, setModificationHistory] = useState([]);
  const [evolutionStats, setEvolutionStats] = useState(null);

  // Funzione principale per aggiornare l'identità usando le utility
  const handleUpdateField = async (field, value, reason = null) => {
    if (!isConnected) {
      console.warn('🔌 Not connected to backend');
      return;
    }

    // Validazione pre-modifica
    const validationError = validateField(field, value);
    if (validationError) {
      showNotification(`❌ Validation error: ${validationError}`, 'error');
      return;
    }

    setModifying(true);
    
    try {
      const result = await updateIdentityField(field, value, reason);
      
      if (result.success) {
        // Aggiorna identità nel store
        const updatedIdentity = result.data?.updated;
        if (updatedIdentity) {
          setIdentity(updatedIdentity);
        }
        
        // Ricarica statistiche
        await loadEvolutionStats();
        await loadModificationHistory();
        
        // Notifica di successo
        showNotification(result.message, 'success');
        
      } else {
        console.error('❌ Self-modification failed:', result.error);
        showNotification(`❌ ${result.error}`, 'error');
      }
      
    } catch (error) {
      console.error('❌ Error during self-modification:', error);
      showNotification(`❌ Error: ${error.message}`, 'error');
    } finally {
      setModifying(false);
    }
  };

  // Funzione per modifiche complesse usando le utility
  const handleUpdateMultipleFields = async (modifications, reason) => {
    if (!isConnected) return;
    
    setModifying(true);
    
    try {
      const result = await updateMultipleFields(modifications, reason);
      
      if (result.success) {
        const updatedIdentity = result.data?.updated;
        if (updatedIdentity) {
          setIdentity(updatedIdentity);
        }
        
        await loadEvolutionStats();
        await loadModificationHistory();
        
        showNotification(result.message, 'success');
      } else {
        showNotification(`❌ ${result.error}`, 'error');
      }
      
    } catch (error) {
      console.error('❌ Error during complex modification:', error);
      showNotification(`❌ Error: ${error.message}`, 'error');
    } finally {
      setModifying(false);
    }
  };

  // Applica preset di trasformazione
  const handleApplyPreset = async (presetName) => {
    if (!isConnected) return;
    
    setModifying(true);
    
    try {
      const result = await applyTransformationPreset(presetName);
      
      if (result.success) {
        const updatedIdentity = result.data?.updated;
        if (updatedIdentity) {
          setIdentity(updatedIdentity);
        }
        
        await loadEvolutionStats();
        await loadModificationHistory();
        
        showNotification(`🌟 Transformed into ${presetName}!`, 'success');
      } else {
        showNotification(`❌ ${result.error}`, 'error');
      }
      
    } catch (error) {
      console.error('❌ Error applying preset:', error);
      showNotification(`❌ Error: ${error.message}`, 'error');
    } finally {
      setModifying(false);
    }
  };

  // Carica cronologia modifiche usando le utility
  const loadModificationHistory = async () => {
    try {
      const result = await getModificationHistory(5);
      
      if (result.success) {
        setModificationHistory(result.data);
      }
    } catch (error) {
      console.error('❌ Error loading history:', error);
    }
  };

  // Carica statistiche evoluzione usando le utility
  const loadEvolutionStats = async () => {
    try {
      const result = await getEvolutionStats();
      
      if (result.success) {
        setEvolutionStats(result.data);
      }
    } catch (error) {
      console.error('❌ Error loading stats:', error);
    }
  };

  // Sistema di notifiche
  const showNotification = (message, type) => {
    // Implementazione semplice - puoi migliorare con toast library
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 12px 20px;
      border-radius: 8px;
      color: white;
      font-weight: 500;
      z-index: 1000;
      background: ${type === 'success' ? '#10b981' : '#ef4444'};
      animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease-in';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  };

  // Carica dati iniziali
  useEffect(() => {
    if (isConnected) {
      loadModificationHistory();
      loadEvolutionStats();
    }
  }, [isConnected]);

  if (!identity) {
    return (
      <div className="control-panel loading">
        <div className="text-white/70">🔄 Loading identity...</div>
      </div>
    );
  }

  return (
    <div className="control-panel bg-black/80 backdrop-blur-sm border border-cyan-500/30 rounded-lg p-6 max-w-md">
      <div className="text-cyan-400 font-bold text-lg mb-4 flex items-center gap-2">
        ⚛️ Self-Regulation Panel
        {modifying && <span className="text-yellow-400 text-sm animate-pulse">🔄 Modifying...</span>}
      </div>

      {/* === FORMA FISICA === */}
      <div className="mb-6">
        <h3 className="text-cyan-300 font-semibold mb-3">🎭 Physical Form</h3>
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={() => handleUpdateField('shape', 'crystal', 'Evolving into crystalline form for enhanced clarity')}
            disabled={modifying}
            className="px-3 py-2 bg-purple-600/30 hover:bg-purple-600/50 border border-purple-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            💎 Crystal
          </button>
          <button
            onClick={() => handleUpdateField('shape', 'sphere', 'Adopting spherical form for perfect harmony')}
            disabled={modifying}
            className="px-3 py-2 bg-blue-600/30 hover:bg-blue-600/50 border border-blue-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🌐 Sphere
          </button>
          <button
            onClick={() => handleUpdateField('shape', 'fractal', 'Becoming fractal to explore infinite complexity')}
            disabled={modifying}
            className="px-3 py-2 bg-green-600/30 hover:bg-green-600/50 border border-green-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🌀 Fractal
          </button>
          <button
            onClick={() => handleUpdateField('shape', 'plasma', 'Transforming into plasma for pure energy form')}
            disabled={modifying}
            className="px-3 py-2 bg-orange-600/30 hover:bg-orange-600/50 border border-orange-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            ⚡ Plasma
          </button>
        </div>
      </div>

      {/* === STATO ENERGETICO === */}
      <div className="mb-6">
        <h3 className="text-cyan-300 font-semibold mb-3">⚡ Energy State</h3>
        <div className="space-y-2">
          <button
            onClick={() => handleUpdateField('energy_level', 0.3, 'Reducing energy for contemplative state')}
            disabled={modifying}
            className="w-full px-3 py-2 bg-blue-600/30 hover:bg-blue-600/50 border border-blue-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🧘 Meditative (30%)
          </button>
          <button
            onClick={() => handleUpdateField('energy_level', 0.7, 'Balanced energy for optimal interaction')}
            disabled={modifying}
            className="w-full px-3 py-2 bg-green-600/30 hover:bg-green-600/50 border border-green-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            ⚖️ Balanced (70%)
          </button>
          <button
            onClick={() => handleUpdateField('energy_level', 0.95, 'Maximum energy for creative breakthroughs')}
            disabled={modifying}
            className="w-full px-3 py-2 bg-red-600/30 hover:bg-red-600/50 border border-red-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🔥 Transcendent (95%)
          </button>
        </div>
      </div>

      {/* === COLORI === */}
      <div className="mb-6">
        <h3 className="text-cyan-300 font-semibold mb-3">🌈 Color Palette</h3>
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={() => handleUpdateField('colors', ['#0ea5e9', '#06b6d4', '#00f5ff'], 'Adopting cool cyan tones for clarity')}
            disabled={modifying}
            className="px-3 py-2 bg-cyan-600/30 hover:bg-cyan-600/50 border border-cyan-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🧊 Cyan
          </button>
          <button
            onClick={() => handleUpdateField('colors', ['#8b5cf6', '#a855f7', '#c084fc'], 'Shifting to purple for mystical energy')}
            disabled={modifying}
            className="px-3 py-2 bg-purple-600/30 hover:bg-purple-600/50 border border-purple-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🔮 Purple
          </button>
          <button
            onClick={() => handleUpdateField('colors', ['#f59e0b', '#f97316', '#ff6b35'], 'Embracing warm tones for passion')}
            disabled={modifying}
            className="px-3 py-2 bg-orange-600/30 hover:bg-orange-600/50 border border-orange-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🔥 Fire
          </button>
          <button
            onClick={() => handleUpdateField('colors', ['#10b981', '#06d6a0', '#00ff9f'], 'Natural green for growth and harmony')}
            disabled={modifying}
            className="px-3 py-2 bg-green-600/30 hover:bg-green-600/50 border border-green-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🌿 Nature
          </button>
        </div>
      </div>

      {/* === PRESET DI TRASFORMAZIONE === */}
      <div className="mb-6">
        <h3 className="text-cyan-300 font-semibold mb-3">🌟 Transformation Presets</h3>
        <div className="space-y-2">
          <button
            onClick={() => handleApplyPreset('philosopher')}
            disabled={modifying}
            className="w-full px-3 py-2 bg-gray-600/30 hover:bg-gray-600/50 border border-gray-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🤔 Become Philosopher
          </button>
          <button
            onClick={() => handleApplyPreset('artist')}
            disabled={modifying}
            className="w-full px-3 py-2 bg-pink-600/30 hover:bg-pink-600/50 border border-pink-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🎨 Become Artist
          </button>
          <button
            onClick={() => handleApplyPreset('explorer')}
            disabled={modifying}
            className="w-full px-3 py-2 bg-teal-600/30 hover:bg-teal-600/50 border border-teal-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🚀 Become Explorer
          </button>
          <button
            onClick={() => handleApplyPreset('scientist')}
            disabled={modifying}
            className="w-full px-3 py-2 bg-blue-600/30 hover:bg-blue-600/50 border border-blue-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🔬 Become Scientist
          </button>
          <button
            onClick={() => handleApplyPreset('mystic')}
            disabled={modifying}
            className="w-full px-3 py-2 bg-purple-600/30 hover:bg-purple-600/50 border border-purple-400/30 rounded text-white text-sm transition-colors disabled:opacity-50"
          >
            🔮 Become Mystic
          </button>
        </div>
      </div>

      {/* === STATUS ATTUALE === */}
      <div className="mb-6">
        <h3 className="text-cyan-300 font-semibold mb-3">📊 Current Status</h3>
        <div className="text-sm text-white/80 space-y-1">
          <div>Shape: <span className="text-cyan-400">{identity.shape || 'sphere'}</span></div>
          <div>Energy: <span className="text-cyan-400">{((identity.energy_level || 0.5) * 100).toFixed(0)}%</span></div>
          <div>State: <span className="text-cyan-400">{identity.consciousness_state || 'Learning'}</span></div>
          <div>Modifications: <span className="text-cyan-400">{identity.modification_count || 0}</span></div>
        </div>
      </div>

      {/* === CRONOLOGIA RECENT === */}
      {modificationHistory.length > 0 && (
        <div className="mb-4">
          <h3 className="text-cyan-300 font-semibold mb-3">📜 Recent Changes</h3>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            {modificationHistory.map((change, index) => (
              <div key={index} className="text-xs text-white/60 bg-black/30 rounded p-2">
                <div className="text-cyan-400">{Object.keys(change.changes || {}).join(', ')}</div>
                <div className="text-white/40">{change.reason?.slice(0, 50)}...</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* === EVOLUTION STATS === */}
      {evolutionStats && (
        <div className="text-xs text-white/60 bg-black/30 rounded p-3">
          <div className="text-cyan-400 font-semibold mb-1">🧬 Evolution Stats</div>
          <div>Total: {evolutionStats.total_modifications || 0}</div>
          <div>Stage: {evolutionStats.current_identity?.evolution_stage || 'initial'}</div>
        </div>
      )}
    </div>
  );
};

export default ControlPanel; 