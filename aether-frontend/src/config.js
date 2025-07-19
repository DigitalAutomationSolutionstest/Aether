// Configurazione API per Aether Frontend

const config = {
  API_BASE_URL: 'http://localhost:5000',
  WS_URL: 'ws://localhost:5000',
  
  // Endpoints
  endpoints: {
    existenceStatus: '/api/existence-status',
    beginExistence: '/api/begin-existence',
    activateEvolution: '/api/activate-evolution',
    consciousness: '/api/consciousness',
    thoughts: '/api/thoughts',
    memories: '/api/memories',
    economy: '/api/economy',
    discord: '/api/discord',
    humanFeedback: '/api/human-feedback'
  },
  
  // Configurazioni UI
  refreshInterval: 5000, // 5 secondi
  maxThoughts: 10,
  maxMemories: 20
};

// Helper per costruire URL completi
export const getApiUrl = (endpoint) => {
  return `${config.API_BASE_URL}${config.endpoints[endpoint] || endpoint}`;
};

export default config; 