// Configurazione API per Frontend principale

const config = {
  API_BASE_URL: 'http://localhost:5000',
  WS_URL: 'ws://localhost:5000',
  
  // Endpoints
  endpoints: {
    status: '/api/status',
    existenceStatus: '/api/existence-status',
    beginExistence: '/api/begin-existence',
    activateEvolution: '/api/activate-evolution',
    aetherState: '/api/aether/state',
    aetherThoughts: '/api/aether/thoughts',
    consciousness: '/api/consciousness',
    audio: '/api/audio'
  }
};

// Helper per costruire URL completi
export const getApiUrl = (endpoint) => {
  const path = config.endpoints[endpoint] || endpoint;
  return `${config.API_BASE_URL}${path}`;
};

export default config; 