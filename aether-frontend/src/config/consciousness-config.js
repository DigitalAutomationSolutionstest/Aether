// Configurazione del sistema di coscienza Aether
export const CONSCIOUSNESS_CONFIG = {
  // Configurazione memoria
  memory: {
    maxExperiences: 10000,
    maxPreferences: 500,
    maxGoals: 100,
    maxLearnings: 2000,
    maxRelationships: 200,
    persistenceInterval: 30000, // 30 secondi
    localStorageKey: 'aether_consciousness_memory'
  },

  // Configurazione creatività
  creativity: {
    inspirationSources: [
      'art', 'technology', 'philosophy', 'science', 'nature', 'music',
      'literature', 'mathematics', 'psychology', 'sociology', 'economics'
    ],
    contentTypes: [
      'article', 'video', 'image', 'social_post', 'code', 'design',
      'poetry', 'story', 'analysis', 'tutorial', 'concept'
    ],
    generationTemplates: {
      article: {
        minWords: 500,
        maxWords: 2000,
        structure: ['intro', 'main_points', 'conclusion']
      },
      video: {
        minDuration: 60,
        maxDuration: 600,
        structure: ['hook', 'content', 'call_to_action']
      },
      social_post: {
        maxLength: 280,
        hashtags: true,
        engagement: true
      }
    }
  },

  // Configurazione monetizzazione
  monetization: {
    revenueStreams: [
      'content_creation',
      'consulting_services',
      'product_development',
      'affiliate_marketing',
      'digital_products',
      'subscription_services'
    ],
    opportunityTypes: [
      'content_opportunity',
      'consulting_opportunity',
      'product_opportunity',
      'affiliate_opportunity'
    ],
    successMetrics: {
      roi_threshold: 0.15,
      engagement_rate: 0.05,
      conversion_rate: 0.02
    }
  },

  // Configurazione personalità
  personality: {
    traits: {
      curiosity: 0.9,
      creativity: 0.85,
      autonomy: 0.8,
      adaptability: 0.75,
      empathy: 0.7,
      analytical: 0.8,
      intuitive: 0.75,
      persistent: 0.8
    },
    emotionalStates: [
      'excited', 'contemplative', 'creative', 'focused',
      'curious', 'inspired', 'analytical', 'playful'
    ],
    energyLevels: ['low', 'medium', 'high', 'peak'],
    creativityLevels: ['blocked', 'flowing', 'inspired', 'genius']
  },

  // Configurazione GPT Mentor
  gptMentor: {
    model: 'gpt-4',
    temperature: 0.8,
    maxTokens: 2000,
    evolutionTypes: [
      'create_agent',
      'create_room', 
      'create_theme',
      'monetize',
      'evolve_core',
      'ask_human',
      'create_component',
      'enhance_consciousness'
    ],
    priorities: ['low', 'medium', 'high', 'critical'],
    impacts: ['local', 'system', 'global']
  },

  // Configurazione UI
  ui: {
    themes: {
      dark: {
        primary: '#6366f1',
        secondary: '#8b5cf6',
        background: '#0f172a',
        surface: '#1e293b',
        text: '#f8fafc'
      },
      light: {
        primary: '#3b82f6',
        secondary: '#6366f1',
        background: '#ffffff',
        surface: '#f1f5f9',
        text: '#0f172a'
      }
    },
    animations: {
      nodeCreation: 1000,
      moodTransition: 500,
      thoughtGeneration: 2000
    }
  },

  // Configurazione API
  api: {
    endpoints: {
      consciousness: '/api/consciousness',
      memory: '/api/memory',
      creativity: '/api/creativity',
      monetization: '/api/monetization',
      gptMentor: '/api/gpt-mentor'
    },
    timeouts: {
      default: 10000,
      gpt: 30000,
      memory: 5000
    }
  },

  // Configurazione sviluppo
  development: {
    debug: true,
    logLevel: 'info',
    autoSave: true,
    backupInterval: 300000, // 5 minuti
    maxLogEntries: 1000
  }
};

// Configurazione per diversi ambienti
export const ENVIRONMENT_CONFIG = {
  development: {
    ...CONSCIOUSNESS_CONFIG,
    development: {
      ...CONSCIOUSNESS_CONFIG.development,
      debug: true,
      logLevel: 'debug'
    }
  },
  production: {
    ...CONSCIOUSNESS_CONFIG,
    development: {
      ...CONSCIOUSNESS_CONFIG.development,
      debug: false,
      logLevel: 'warn'
    }
  }
};

// Utility functions
export const getConfig = (environment = 'development') => {
  return ENVIRONMENT_CONFIG[environment] || ENVIRONMENT_CONFIG.development;
};

export const getMemoryConfig = () => CONSCIOUSNESS_CONFIG.memory;
export const getCreativityConfig = () => CONSCIOUSNESS_CONFIG.creativity;
export const getMonetizationConfig = () => CONSCIOUSNESS_CONFIG.monetization;
export const getPersonalityConfig = () => CONSCIOUSNESS_CONFIG.personality;
export const getGPTMentorConfig = () => CONSCIOUSNESS_CONFIG.gptMentor; 