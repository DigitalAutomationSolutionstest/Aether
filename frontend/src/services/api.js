// src/services/api.js - API Service per Aether Frontend

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Endpoints
export const aetherAPI = {
  // Get dynamic rooms/components created by Aether
  getRooms: async () => {
    try {
      const response = await api.get('/api/rooms');
      return response.data;
    } catch (error) {
      console.error('Error fetching rooms:', error);
      return { rooms: [], error: error.message };
    }
  },

  // Get active agents
  getAgents: async () => {
    try {
      const response = await api.get('/api/agents');
      return response.data;
    } catch (error) {
      console.error('Error fetching agents:', error);
      return { agents: [], error: error.message };
    }
  },

  // Get evolution events and logs
  getEvents: async (limit = 50) => {
    try {
      const response = await api.get(`/api/events?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching events:', error);
      return { events: [], error: error.message };
    }
  },

  // Get latest thoughts from Aether
  getThoughts: async (limit = 10) => {
    try {
      const response = await api.get(`/api/thoughts?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching thoughts:', error);
      return { thoughts: [], error: error.message };
    }
  },

  // Get system status
  getSystemStatus: async () => {
    try {
      const response = await api.get('/api/status');
      return response.data;
    } catch (error) {
      console.error('Error fetching system status:', error);
      return { status: 'unknown', error: error.message };
    }
  },

  // Get available audio files
  getAudioFiles: async () => {
    try {
      const response = await api.get('/api/audio');
      return response.data;
    } catch (error) {
      console.error('Error fetching audio files:', error);
      return { audio_files: [], error: error.message };
    }
  },

  // Trigger Aether evolution (optional)
  triggerEvolution: async (thoughtData) => {
    try {
      const response = await api.post('/api/evolve', thoughtData);
      return response.data;
    } catch (error) {
      console.error('Error triggering evolution:', error);
      return { success: false, error: error.message };
    }
  }
};

// Utility function to get audio file URL
export const getAudioURL = (filename) => {
  return `${API_BASE_URL}/api/audio/${filename}`;
};

// WebSocket connection for real-time updates
export class AetherWebSocket {
  constructor(onMessage, onError) {
    this.ws = null;
    this.onMessage = onMessage;
    this.onError = onError;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  connect() {
    try {
      const wsUrl = API_BASE_URL.replace('http', 'ws') + '/ws';
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('🔌 WebSocket connected to Aether');
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onMessage(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('🔌 WebSocket disconnected');
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        if (this.onError) this.onError(error);
      };

    } catch (error) {
      console.error('Error creating WebSocket:', error);
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`🔄 Reconnecting WebSocket (attempt ${this.reconnectAttempts})`);
      setTimeout(() => this.connect(), 3000 * this.reconnectAttempts);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  sendMessage(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected');
    }
  }
}

export default aetherAPI; 