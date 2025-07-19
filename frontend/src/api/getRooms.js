/**
 * API per ottenere stanze 3D dinamiche generate da Aether
 */

const API_BASE = 'http://localhost:5000/api';

export const getRooms = async () => {
  try {
    const response = await fetch(`${API_BASE}/rooms`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    
    // Il backend ora restituisce un oggetto con rooms array
    if (data.rooms && Array.isArray(data.rooms)) {
      return data.rooms;
    }
    
    // Fallback per compatibilità
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error('Errore nel caricamento stanze:', error);
    return [];
  }
};

export const getWorldState = async () => {
  try {
    const response = await fetch(`${API_BASE}/consciousness/status`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Errore nel caricamento stato mondo:', error);
    return { is_alive: false, mood: 'contemplativo' };
  }
};

export const getThoughts = async () => {
  try {
    const response = await fetch(`${API_BASE}/thoughts`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.thoughts || [];
  } catch (error) {
    console.error('Errore nel caricamento pensieri:', error);
    return [];
  }
};

export const getAgents = async () => {
  try {
    const response = await fetch(`${API_BASE}/agents`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error('Errore nel caricamento agenti:', error);
    return [];
  }
};

export const getEvents = async () => {
  try {
    const response = await fetch(`${API_BASE}/events`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.error('Errore nel caricamento eventi:', error);
    return [];
  }
};

export const forceWorldUpdate = async () => {
  try {
    const response = await fetch(`${API_BASE}/consciousness/force-think`, {
      method: 'POST'
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Errore nel forzare aggiornamento mondo:', error);
    return null;
  }
};

export const forceDecision = async () => {
  try {
    const response = await fetch(`${API_BASE}/consciousness/force-decision`, {
      method: 'POST'
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Errore nel forzare decisione:', error);
    return null;
  }
};

export const forceEvolution = async () => {
  try {
    const response = await fetch(`${API_BASE}/consciousness/force-evolution`, {
      method: 'POST'
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Errore nel forzare evoluzione:', error);
    return null;
  }
};

export const wakeUpAether = async () => {
  try {
    const response = await fetch(`${API_BASE}/consciousness/wake-up`, {
      method: 'POST'
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Errore nel risvegliare Aether:', error);
    return null;
  }
};

export const putAetherToSleep = async () => {
  try {
    const response = await fetch(`${API_BASE}/consciousness/sleep`, {
      method: 'POST'
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Errore nell\'addormentare Aether:', error);
    return null;
  }
};

// Hook personalizzato per React
export const useAetherAPI = () => {
  return {
    getRooms,
    getWorldState,
    getThoughts,
    getAgents,
    getEvents,
    forceWorldUpdate,
    forceDecision,
    forceEvolution,
    wakeUpAether,
    putAetherToSleep
  };
};

export default { 
  getRooms, 
  getWorldState, 
  getThoughts, 
  getAgents,
  getEvents,
  forceWorldUpdate,
  forceDecision,
  forceEvolution,
  wakeUpAether,
  putAetherToSleep,
  useAetherAPI
}; 