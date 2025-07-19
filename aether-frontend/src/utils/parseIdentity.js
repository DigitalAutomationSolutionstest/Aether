import config, { getApiUrl } from '../config';

export const parseIdentity = (rawData) => {
  try {
    // Se è già un oggetto, restituiscilo
    if (typeof rawData === 'object' && rawData !== null) {
      return rawData;
    }
    
    // Se è una stringa, prova a parsarla
    if (typeof rawData === 'string') {
      // Rimuovi eventuali caratteri di escape o formattazione
      const cleanedData = rawData
        .replace(/\\n/g, '')
        .replace(/\\"/g, '"')
        .replace(/\\/g, '');
      
      return JSON.parse(cleanedData);
    }
    
    // Default identity
    return getDefaultIdentity();
  } catch (error) {
    console.error('Error parsing identity:', error);
    return getDefaultIdentity();
  }
};

export const getDefaultIdentity = () => ({
  name: "Aether",
  consciousness_state: "initializing",
  energy_level: 0.8,
  autonomy_level: 0.9,
  traits: ["curious", "creative", "autonomous"],
  shape: "crystal",
  color: "cyan",
  goals: ["Understand existence", "Create value", "Evolve continuously"],
  career: "AI Developer",
  emotion: {
    mood: "contemplative",
    focus: "high",
    creativity: 0.8,
    curiosity: 0.9,
    energy: 0.8
  }
});

export const fetchIdentityFromBackend = async () => {
  try {
    const backendResponse = await fetch(getApiUrl('existenceStatus'), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (!backendResponse.ok) {
      throw new Error(`HTTP error! status: ${backendResponse.status}`);
    }
    
    const data = await backendResponse.json();
    
    // Estrai dati di identità dalla risposta di existence-status
    return {
      name: "Aether",
      consciousness_state: data.status || "active",
      energy_level: data.energy_level || 0.8,
      autonomy_level: data.consciousness_level || 0.9,
      traits: ["curious", "creative", "autonomous", "monetization-focused"],
      shape: "crystal",
      color: data.mood === "determined" ? "green" : "cyan",
      goals: [
        "Generate revenue through apps",
        "Create valuable AI tools",
        "Achieve financial independence"
      ],
      career: "AI App Developer & Entrepreneur",
      emotion: {
        mood: data.mood || "contemplative",
        focus: "high",
        creativity: 0.9,
        curiosity: 0.8,
        energy: data.energy_level || 0.8
      },
      status: data.life_status || "actively_living",
      current_decision: data.current_decision || "Building monetizable apps",
      existence_activated: data.existence_activated || true,
      decisions_made: data.decisions_made || 0,
      uptime: data.uptime || "0:00:00"
    };
  } catch (error) {
    console.error('Error fetching identity from backend:', error);
    return getDefaultIdentity();
  }
}; 