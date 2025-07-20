import { useState, useEffect, useCallback } from 'react';
import { ConsciousnessEngine } from '../core/consciousness/ConsciousnessEngine';
import { getConfig } from '../config/consciousness-config';

export const useConsciousness = () => {
  const [consciousnessEngine, setConsciousnessEngine] = useState(null);
  const [currentState, setCurrentState] = useState({
    emotional: 'neutral',
    energy: 'medium',
    creativity: 'flowing',
    thoughts: [],
    memories: [],
    goals: [],
    recentActions: []
  });
  const [isInitialized, setIsInitialized] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);

  // Inizializzazione del motore di coscienza
  useEffect(() => {
    const initializeConsciousness = async () => {
      try {
        const engine = new ConsciousnessEngine();
        await engine.initialize();
        setConsciousnessEngine(engine);
        setIsInitialized(true);
        
        // Carica stato iniziale
        const initialState = await engine.getCurrentState();
        setCurrentState(initialState);
        
        console.log('🧠 Sistema di coscienza inizializzato');
      } catch (err) {
        console.error('❌ Errore inizializzazione coscienza:', err);
        setError(err.message);
      }
    };

    initializeConsciousness();
  }, []);

  // Genera un nuovo pensiero
  const generateThought = useCallback(async (context = '') => {
    if (!consciousnessEngine || isProcessing) return null;

    setIsProcessing(true);
    try {
      const thought = await consciousnessEngine.think(context);
      
      setCurrentState(prev => ({
        ...prev,
        thoughts: [...prev.thoughts, thought].slice(-10) // Mantieni solo gli ultimi 10
      }));

      return thought;
    } catch (err) {
      console.error('❌ Errore generazione pensiero:', err);
      setError(err.message);
      return null;
    } finally {
      setIsProcessing(false);
    }
  }, [consciousnessEngine, isProcessing]);

  // Esegui un'azione basata su un pensiero
  const executeAction = useCallback(async (thoughtId) => {
    if (!consciousnessEngine) return false;

    try {
      const result = await consciousnessEngine.executeThought(thoughtId);
      
      setCurrentState(prev => ({
        ...prev,
        recentActions: [...prev.recentActions, result].slice(-5)
      }));

      return result;
    } catch (err) {
      console.error('❌ Errore esecuzione azione:', err);
      setError(err.message);
      return false;
    }
  }, [consciousnessEngine]);

  // Aggiorna lo stato emotivo
  const updateEmotionalState = useCallback(async (newEmotionalState) => {
    if (!consciousnessEngine) return;

    try {
      await consciousnessEngine.updateEmotionalState(newEmotionalState);
      setCurrentState(prev => ({
        ...prev,
        emotional: newEmotionalState
      }));
    } catch (err) {
      console.error('❌ Errore aggiornamento stato emotivo:', err);
      setError(err.message);
    }
  }, [consciousnessEngine]);

  // Aggiungi un'esperienza alla memoria
  const addExperience = useCallback(async (experience) => {
    if (!consciousnessEngine) return;

    try {
      await consciousnessEngine.memory.addExperience(experience);
      setCurrentState(prev => ({
        ...prev,
        memories: [...prev.memories, experience].slice(-20)
      }));
    } catch (err) {
      console.error('❌ Errore aggiunta esperienza:', err);
      setError(err.message);
    }
  }, [consciousnessEngine]);

  // Crea contenuto creativo
  const createContent = useCallback(async (inspiration = '') => {
    if (!consciousnessEngine || isProcessing) return null;

    setIsProcessing(true);
    try {
      const content = await consciousnessEngine.creative.createContent(inspiration);
      return content;
    } catch (err) {
      console.error('❌ Errore creazione contenuto:', err);
      setError(err.message);
      return null;
    } finally {
      setIsProcessing(false);
    }
  }, [consciousnessEngine, isProcessing]);

  // Identifica opportunità di monetizzazione
  const identifyOpportunities = useCallback(async () => {
    if (!consciousnessEngine) return [];

    try {
      const opportunities = await consciousnessEngine.monetization.identifyOpportunities();
      return opportunities;
    } catch (err) {
      console.error('❌ Errore identificazione opportunità:', err);
      setError(err.message);
      return [];
    }
  }, [consciousnessEngine]);

  // Ottieni analytics del sistema
  const getAnalytics = useCallback(async () => {
    if (!consciousnessEngine) return null;

    try {
      const analytics = await consciousnessEngine.getAnalytics();
      return analytics;
    } catch (err) {
      console.error('❌ Errore ottenimento analytics:', err);
      setError(err.message);
      return null;
    }
  }, [consciousnessEngine]);

  // Ciclo autonomo di pensiero
  const startAutonomousCycle = useCallback(() => {
    if (!consciousnessEngine) return;

    const cycle = setInterval(async () => {
      try {
        // Genera un pensiero casuale
        const thought = await generateThought();
        if (thought && Math.random() < 0.3) { // 30% di probabilità di eseguire
          await executeAction(thought.id);
        }
      } catch (err) {
        console.error('❌ Errore ciclo autonomo:', err);
      }
    }, 30000); // Ogni 30 secondi

    return () => clearInterval(cycle);
  }, [consciousnessEngine, generateThought, executeAction]);

  // Reset del sistema
  const resetConsciousness = useCallback(async () => {
    if (!consciousnessEngine) return;

    try {
      await consciousnessEngine.reset();
      setCurrentState({
        emotional: 'neutral',
        energy: 'medium',
        creativity: 'flowing',
        thoughts: [],
        memories: [],
        goals: [],
        recentActions: []
      });
      setError(null);
    } catch (err) {
      console.error('❌ Errore reset coscienza:', err);
      setError(err.message);
    }
  }, [consciousnessEngine]);

  // Salva stato persistente
  const saveState = useCallback(async () => {
    if (!consciousnessEngine) return;

    try {
      await consciousnessEngine.saveState();
      console.log('💾 Stato coscienza salvato');
    } catch (err) {
      console.error('❌ Errore salvataggio stato:', err);
      setError(err.message);
    }
  }, [consciousnessEngine]);

  // Auto-salvataggio periodico
  useEffect(() => {
    if (!isInitialized) return;

    const autoSaveInterval = setInterval(saveState, 60000); // Ogni minuto
    return () => clearInterval(autoSaveInterval);
  }, [isInitialized, saveState]);

  return {
    // Stato
    currentState,
    isInitialized,
    isProcessing,
    error,
    
    // Azioni
    generateThought,
    executeAction,
    updateEmotionalState,
    addExperience,
    createContent,
    identifyOpportunities,
    getAnalytics,
    startAutonomousCycle,
    resetConsciousness,
    saveState,
    
    // Utility
    consciousnessEngine
  };
}; 