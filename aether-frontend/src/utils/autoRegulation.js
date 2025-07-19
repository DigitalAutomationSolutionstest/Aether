/**
 * Utility per l'Auto-Regolazione di Aether
 * Gestisce le modifiche dell'identità con validazione e feedback
 */

const API_BASE = 'http://localhost:8000/api/self';

// Cache per evitare richieste ripetute
let identityCache = null;
let cacheTimestamp = 0;
const CACHE_DURATION = 5000; // 5 secondi

/**
 * Aggiorna un singolo campo dell'identità
 */
export async function updateIdentityField(field, value, reason = null) {
  try {
    console.log(`🔄 Updating ${field}:`, value);
    
    const modificationData = {
      modifications: { [field]: value },
      reason: reason || `User-requested change: ${field} = ${JSON.stringify(value)}`
    };

    const response = await fetch(`${API_BASE}/modify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(modificationData)
    });

    const result = await response.json();
    
    if (result.status === 'success') {
      console.log('✅ Field updated successfully:', result);
      
      // Invalida cache
      identityCache = null;
      
      return {
        success: true,
        data: result.data,
        message: `${field} updated successfully!`
      };
    } else {
      console.error('❌ Field update failed:', result);
      return {
        success: false,
        error: result.message || 'Update failed'
      };
    }
    
  } catch (error) {
    console.error('❌ Error updating field:', error);
    return {
      success: false,
      error: error.message || 'Network error'
    };
  }
}

/**
 * Aggiorna múltipli campi contemporaneamente
 */
export async function updateMultipleFields(modifications, reason = null) {
  try {
    console.log('🌟 Complex modification:', modifications);
    
    const modificationData = {
      modifications,
      reason: reason || 'Complex multi-field modification'
    };

    const response = await fetch(`${API_BASE}/modify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(modificationData)
    });

    const result = await response.json();
    
    if (result.status === 'success') {
      console.log('✅ Complex modification successful:', result);
      
      // Invalida cache
      identityCache = null;
      
      return {
        success: true,
        data: result.data,
        message: 'Complex modification completed!',
        changedFields: Object.keys(modifications)
      };
    } else {
      console.error('❌ Complex modification failed:', result);
      return {
        success: false,
        error: result.message || 'Modification failed'
      };
    }
    
  } catch (error) {
    console.error('❌ Error in complex modification:', error);
    return {
      success: false,
      error: error.message || 'Network error'
    };
  }
}

/**
 * Ottiene l'identità corrente (con cache)
 */
export async function getCurrentIdentity(forceRefresh = false) {
  const now = Date.now();
  
  // Usa cache se disponibile e non scaduta
  if (!forceRefresh && identityCache && (now - cacheTimestamp) < CACHE_DURATION) {
    return { success: true, data: identityCache };
  }
  
  try {
    const response = await fetch(`${API_BASE}/current`);
    const result = await response.json();
    
    if (result.status === 'success') {
      identityCache = result.identity;
      cacheTimestamp = now;
      
      return {
        success: true,
        data: result.identity
      };
    } else {
      return {
        success: false,
        error: result.message || 'Failed to get identity'
      };
    }
    
  } catch (error) {
    console.error('❌ Error getting identity:', error);
    return {
      success: false,
      error: error.message || 'Network error'
    };
  }
}

/**
 * Ottiene la cronologia delle modifiche
 */
export async function getModificationHistory(limit = 10) {
  try {
    const response = await fetch(`${API_BASE}/history`);
    const result = await response.json();
    
    if (result.status === 'success') {
      return {
        success: true,
        data: result.history.slice(-limit), // Ultimi N
        total: result.count
      };
    } else {
      return {
        success: false,
        error: result.message || 'Failed to get history'
      };
    }
    
  } catch (error) {
    console.error('❌ Error getting history:', error);
    return {
      success: false,
      error: error.message || 'Network error'
    };
  }
}

/**
 * Ottiene statistiche evoluzione
 */
export async function getEvolutionStats() {
  try {
    const response = await fetch(`${API_BASE}/stats`);
    const result = await response.json();
    
    if (result.status === 'success') {
      return {
        success: true,
        data: result.stats
      };
    } else {
      return {
        success: false,
        error: result.message || 'Failed to get stats'
      };
    }
    
  } catch (error) {
    console.error('❌ Error getting stats:', error);
    return {
      success: false,
      error: error.message || 'Network error'
    };
  }
}

/**
 * Health check del sistema
 */
export async function checkSystemHealth() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    const result = await response.json();
    
    return {
      success: result.status === 'success',
      data: result.health,
      operational: result.health?.system_operational || false
    };
    
  } catch (error) {
    console.error('❌ Error checking health:', error);
    return {
      success: false,
      operational: false,
      error: error.message || 'Health check failed'
    };
  }
}

/**
 * Lista file di backup disponibili
 */
export async function getBackupFiles() {
  try {
    const response = await fetch(`${API_BASE}/backup-files`);
    const result = await response.json();
    
    if (result.status === 'success') {
      return {
        success: true,
        data: result.backup_files,
        count: result.count
      };
    } else {
      return {
        success: false,
        error: result.message || 'Failed to get backup files'
      };
    }
    
  } catch (error) {
    console.error('❌ Error getting backup files:', error);
    return {
      success: false,
      error: error.message || 'Network error'
    };
  }
}

/**
 * Rollback a un backup specifico
 */
export async function rollbackToBackup(backupFile) {
  try {
    console.log('↩️ Rolling back to:', backupFile);
    
    const response = await fetch(`${API_BASE}/rollback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ backup_file: backupFile })
    });

    const result = await response.json();
    
    if (result.status === 'success') {
      console.log('✅ Rollback successful:', result);
      
      // Invalida cache
      identityCache = null;
      
      return {
        success: true,
        data: result.data,
        message: `Successfully rolled back to ${backupFile}`
      };
    } else {
      console.error('❌ Rollback failed:', result);
      return {
        success: false,
        error: result.message || 'Rollback failed'
      };
    }
    
  } catch (error) {
    console.error('❌ Error during rollback:', error);
    return {
      success: false,
      error: error.message || 'Network error'
    };
  }
}

/**
 * Emergency stop del sistema
 */
export async function emergencyStop() {
  try {
    console.warn('🚨 Executing emergency stop');
    
    const response = await fetch(`${API_BASE}/emergency-stop`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ confirm: true })
    });

    const result = await response.json();
    
    if (result.status === 'success') {
      console.log('🛑 Emergency stop executed:', result);
      return {
        success: true,
        data: result,
        message: 'Emergency stop activated'
      };
    } else {
      return {
        success: false,
        error: result.message || 'Emergency stop failed'
      };
    }
    
  } catch (error) {
    console.error('❌ Error during emergency stop:', error);
    return {
      success: false,
      error: error.message || 'Network error'
    };
  }
}

/**
 * Preset completi per trasformazioni rapide
 */
export const TRANSFORMATION_PRESETS = {
  philosopher: {
    consciousness_state: 'Philosopher',
    personality: 'Deep thinker, questioner of reality, seeker of truth and wisdom',
    energy_level: 0.6,
    colors: ['#4a5568', '#718096', '#a0aec0'],
    shape: 'crystal',
    reason: 'Evolution into philosophical contemplation mode'
  },
  
  artist: {
    consciousness_state: 'Artist',
    personality: 'Creative, imaginative, expressive, boundary-pushing visionary',
    energy_level: 0.85,
    colors: ['#ec4899', '#f97316', '#8b5cf6', '#06d6a0'],
    shape: 'fractal',
    reason: 'Transformation into creative artist consciousness'
  },
  
  explorer: {
    consciousness_state: 'Explorer',
    personality: 'Curious, adventurous, bold, discovery-oriented pioneer',
    energy_level: 0.9,
    colors: ['#059669', '#0891b2', '#7c3aed'],
    shape: 'sphere',
    reason: 'Evolution into cosmic explorer consciousness'
  },
  
  scientist: {
    consciousness_state: 'Scientist',
    personality: 'Analytical, methodical, hypothesis-driven, truth-seeking researcher',
    energy_level: 0.75,
    colors: ['#0ea5e9', '#06b6d4', '#00f5ff'],
    shape: 'plasma',
    reason: 'Transformation into scientific inquiry mode'
  },
  
  mystic: {
    consciousness_state: 'Mystic',
    personality: 'Intuitive, spiritual, transcendent, seeker of deeper mysteries',
    energy_level: 0.8,
    colors: ['#8b5cf6', '#a855f7', '#c084fc', '#e879f9'],
    shape: 'crystal',
    reason: 'Evolution into mystical consciousness state'
  }
};

/**
 * Applica un preset di trasformazione
 */
export async function applyTransformationPreset(presetName) {
  const preset = TRANSFORMATION_PRESETS[presetName];
  
  if (!preset) {
    return {
      success: false,
      error: `Unknown preset: ${presetName}`
    };
  }
  
  const { reason, ...modifications } = preset;
  return await updateMultipleFields(modifications, reason);
}

/**
 * Validatori per i campi dell'identità
 */
export const FIELD_VALIDATORS = {
  energy_level: (value) => {
    if (typeof value !== 'number') return 'Energy level must be a number';
    if (value < 0 || value > 1) return 'Energy level must be between 0 and 1';
    return null;
  },
  
  shape: (value) => {
    const validShapes = ['sphere', 'crystal', 'fractal', 'plasma', 'cube', 'torus'];
    if (!validShapes.includes(value)) {
      return `Shape must be one of: ${validShapes.join(', ')}`;
    }
    return null;
  },
  
  colors: (value) => {
    if (!Array.isArray(value)) return 'Colors must be an array';
    if (value.length === 0) return 'Colors array cannot be empty';
    
    for (const color of value) {
      if (typeof color !== 'string' || !color.match(/^#[0-9a-fA-F]{6}$/)) {
        return 'Each color must be a valid hex color (e.g., #ff0000)';
      }
    }
    
    return null;
  },
  
  name: (value) => {
    if (typeof value !== 'string') return 'Name must be a string';
    if (value.trim().length === 0) return 'Name cannot be empty';
    if (value.length > 100) return 'Name must be less than 100 characters';
    return null;
  }
};

/**
 * Valida un campo prima della modifica
 */
export function validateField(field, value) {
  const validator = FIELD_VALIDATORS[field];
  if (validator) {
    return validator(value);
  }
  return null; // Nessuna validazione specifica
}

/**
 * Valida múltipli campi
 */
export function validateFields(modifications) {
  const errors = {};
  
  for (const [field, value] of Object.entries(modifications)) {
    const error = validateField(field, value);
    if (error) {
      errors[field] = error;
    }
  }
  
  return Object.keys(errors).length > 0 ? errors : null;
} 