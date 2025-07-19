// src/components/EventsLog.jsx - Log eventi e evoluzioni di Aether

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { aetherAPI } from '../services/api';
import { ScrollText, Brain, Zap, Home, Bot, Palette, Calendar, Play } from 'lucide-react';

const EventIcon = ({ type }) => {
  const icons = {
    thought: <Brain className="w-4 h-4" />,
    self_evolution: <Zap className="w-4 h-4" />,
    room_creation: <Home className="w-4 h-4" />,
    agent_creation: <Bot className="w-4 h-4" />,
    agent_interaction: <Bot className="w-4 h-4" />,
    evolution_announcement: <Zap className="w-4 h-4" />,
    ui_modification: <Palette className="w-4 h-4" />,
    scene_creation: <Home className="w-4 h-4" />
  };
  
  return icons[type] || <ScrollText className="w-4 h-4" />;
};

const EventTypeColor = ({ type }) => {
  const colors = {
    thought: 'text-blue-400 bg-blue-900',
    self_evolution: 'text-yellow-400 bg-yellow-900',
    room_creation: 'text-green-400 bg-green-900',
    agent_creation: 'text-purple-400 bg-purple-900',
    agent_interaction: 'text-cyan-400 bg-cyan-900',
    evolution_announcement: 'text-orange-400 bg-orange-900',
    ui_modification: 'text-pink-400 bg-pink-900',
    scene_creation: 'text-indigo-400 bg-indigo-900'
  };
  
  return colors[type] || 'text-gray-400 bg-gray-900';
};

const EventCard = ({ event, onPlay }) => {
  const colorClass = EventTypeColor({ type: event.type });
  const [bgColor, textColor] = colorClass.split(' ');

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20 }}
      className="bg-gray-900 bg-opacity-50 backdrop-blur-sm border border-gray-700 rounded-lg p-4 hover:border-gray-500 transition-all duration-300"
    >
      <div className="flex items-start gap-3">
        {/* Icon */}
        <div className={`${bgColor} ${textColor} bg-opacity-20 p-2 rounded-full flex-shrink-0`}>
          <EventIcon type={event.type} />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-2">
            <span className={`px-2 py-1 rounded-full text-xs ${bgColor} ${textColor} bg-opacity-20`}>
              {event.type.replace('_', ' ')}
            </span>
            <div className="flex items-center gap-2 text-xs text-gray-500">
              <Calendar className="w-3 h-3" />
              <span>{new Date(event.timestamp).toLocaleString()}</span>
            </div>
          </div>

          <p className="text-gray-300 text-sm mb-2 break-words">
            {event.content}
          </p>

          {/* Context info */}
          {event.context && (
            <div className="text-xs text-gray-500 space-y-1">
              {event.context.mood && (
                <div>Mood: <span className="text-gray-400">{event.context.mood}</span></div>
              )}
              {event.context.agent_name && (
                <div>Agent: <span className="text-gray-400">{event.context.agent_name}</span></div>
              )}
              {event.context.file && (
                <div>File: <span className="text-gray-400 font-mono">{event.context.file}</span></div>
              )}
            </div>
          )}

          {/* Audio button if available */}
          {event.audio_file && (
            <button
              onClick={() => onPlay(event.audio_file)}
              className="mt-2 flex items-center gap-1 px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded text-xs text-white transition-colors"
            >
              <Play className="w-3 h-3" />
              Ascolta
            </button>
          )}
        </div>
      </div>
    </motion.div>
  );
};

const EventsLog = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');
  const [autoScroll, setAutoScroll] = useState(true);
  const scrollRef = useRef(null);

  const eventTypes = [
    'all',
    'thought',
    'self_evolution', 
    'room_creation',
    'agent_creation',
    'agent_interaction',
    'evolution_announcement'
  ];

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const data = await aetherAPI.getEvents(100);
      
      if (data.error) {
        setError(data.error);
        return;
      }

      const eventsArray = data.events || [];
      
      // Sort by timestamp descending (newest first)
      const sortedEvents = eventsArray.sort((a, b) => 
        new Date(b.timestamp) - new Date(a.timestamp)
      );
      
      setEvents(sortedEvents);
      setError(null);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const playAudio = (audioFile) => {
    try {
      const audio = new Audio(`http://localhost:8000/api/audio/${audioFile}`);
      audio.play().catch(err => {
        console.error('Error playing audio:', err);
      });
    } catch (error) {
      console.error('Error creating audio:', error);
    }
  };

  useEffect(() => {
    fetchEvents();
    
    // Auto-refresh every 5 seconds
    const interval = setInterval(fetchEvents, 5000);
    
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll to bottom when new events arrive
  useEffect(() => {
    if (autoScroll && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events, autoScroll]);

  const filteredEvents = filter === 'all' 
    ? events 
    : events.filter(event => event.type === filter);

  if (loading && events.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <ScrollText className="w-8 h-8 animate-pulse text-cyan-400 mx-auto mb-2" />
          <p className="text-gray-400">Caricamento eventi...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-4 text-red-400">
        <h3 className="font-bold mb-2">⚠️ Errore Caricamento Eventi</h3>
        <p className="text-sm">{error}</p>
        <button
          onClick={fetchEvents}
          className="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-white text-sm transition-colors"
        >
          Riprova
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header with filters */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <ScrollText className="w-6 h-6" />
          Log Eventi ({filteredEvents.length})
        </h2>
        
        <div className="flex items-center gap-2">
          {/* Filter dropdown */}
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="bg-gray-700 border border-gray-600 rounded px-3 py-1 text-sm text-white"
          >
            {eventTypes.map(type => (
              <option key={type} value={type}>
                {type === 'all' ? 'Tutti' : type.replace('_', ' ')}
              </option>
            ))}
          </select>

          {/* Auto-scroll toggle */}
          <label className="flex items-center gap-2 text-sm text-gray-400">
            <input
              type="checkbox"
              checked={autoScroll}
              onChange={(e) => setAutoScroll(e.target.checked)}
              className="rounded"
            />
            Auto-scroll
          </label>

          {/* Refresh button */}
          <button
            onClick={fetchEvents}
            className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm text-white transition-colors"
          >
            Aggiorna
          </button>
        </div>
      </div>

      {/* Events list */}
      {filteredEvents.length === 0 ? (
        <div className="text-center py-12">
          <ScrollText className="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <h3 className="text-gray-400 text-lg mb-2">
            {filter === 'all' ? 'Nessun Evento' : `Nessun Evento ${filter.replace('_', ' ')}`}
          </h3>
          <p className="text-gray-500 text-sm">
            {filter === 'all' 
              ? 'Aether non ha ancora generato eventi. Attendere l\'attività...'
              : 'Nessun evento di questo tipo disponibile.'
            }
          </p>
        </div>
      ) : (
        <div 
          ref={scrollRef}
          className="space-y-3 max-h-[600px] overflow-y-auto scrollbar-thin scrollbar-track-gray-800 scrollbar-thumb-gray-600"
        >
          <AnimatePresence>
            {filteredEvents.map((event, index) => (
              <EventCard
                key={event.id || `${event.timestamp}-${index}`}
                event={event}
                onPlay={playAudio}
              />
            ))}
          </AnimatePresence>
        </div>
      )}

      {/* Live indicator */}
      {!loading && (
        <div className="flex items-center justify-center text-xs text-gray-500">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse mr-2" />
          Live - Aggiornamento automatico ogni 5 secondi
        </div>
      )}
    </div>
  );
};

export default EventsLog; 