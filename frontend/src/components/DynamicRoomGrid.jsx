// src/components/DynamicRoomGrid.jsx - Grid dinamica delle stanze di Aether

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDynamicComponents } from '../hooks/useDynamicComponents';
import { Loader2, Home, Calendar, User } from 'lucide-react';

const RoomCard = ({ roomData, onSelect, isSelected }) => {
  const { component: Component, metadata, loadedAt } = roomData;
  
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      whileHover={{ scale: 1.02 }}
      className={`
        relative bg-gray-900 bg-opacity-50 backdrop-blur-sm border border-gray-700 
        rounded-lg overflow-hidden cursor-pointer transition-all duration-300
        ${isSelected ? 'ring-2 ring-cyan-400 border-cyan-400' : 'hover:border-gray-500'}
      `}
      onClick={() => onSelect(roomData)}
    >
      {/* Room Preview */}
      <div className="h-32 bg-gradient-to-br from-gray-800 to-gray-900 relative overflow-hidden">
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-4xl">
            {metadata.mood === 'creativo' && '🎨'}
            {metadata.mood === 'analitico' && '📊'}
            {metadata.mood === 'curioso' && '🔍'}
            {metadata.mood === 'sognatore' && '☁️'}
            {metadata.mood === 'ambizioso' && '🚀'}
          </div>
        </div>
        
        {/* Mood color overlay */}
        <div 
          className={`absolute inset-0 opacity-20 ${getMoodGradient(metadata.mood)}`}
        />
      </div>

      {/* Room Info */}
      <div className="p-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-white font-semibold text-sm">
            {metadata.name || 'Unknown Room'}
          </h3>
          <span className={`px-2 py-1 rounded-full text-xs ${getMoodBadgeColor(metadata.mood)}`}>
            {metadata.mood || 'neutral'}
          </span>
        </div>
        
        <p className="text-gray-400 text-xs mb-3 line-clamp-2">
          {metadata.description || 'Stanza generata dinamicamente da Aether'}
        </p>
        
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            <span>{new Date(loadedAt).toLocaleTimeString()}</span>
          </div>
          <div className="flex items-center gap-1">
            <User className="w-3 h-3" />
            <span>Aether</span>
          </div>
        </div>
      </div>

      {/* Status indicator */}
      <div className="absolute top-2 right-2">
        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
      </div>
    </motion.div>
  );
};

const FullRoomView = ({ roomData, onClose }) => {
  const { component: Component } = roomData;
  
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 bg-black bg-opacity-90 backdrop-blur-sm"
      onClick={onClose}
    >
      <div className="absolute inset-4 bg-gray-900 rounded-lg overflow-hidden">
        <div className="relative h-full">
          {/* Close button */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 z-10 bg-black bg-opacity-50 hover:bg-opacity-70 rounded-full p-2 text-white transition-colors"
          >
            ✕
          </button>
          
          {/* Room component */}
          <div className="h-full overflow-auto">
            {Component && <Component />}
          </div>
        </div>
      </div>
    </motion.div>
  );
};

const DynamicRoomGrid = () => {
  const { loadedComponents, loading, error, refreshComponents } = useDynamicComponents();
  const [selectedRoom, setSelectedRoom] = useState(null);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-cyan-400 mx-auto mb-2" />
          <p className="text-gray-400">Caricamento stanze di Aether...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-4 text-red-400">
        <h3 className="font-bold mb-2">⚠️ Errore Caricamento Stanze</h3>
        <p className="text-sm">{error}</p>
        <button
          onClick={refreshComponents}
          className="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-white text-sm transition-colors"
        >
          Riprova
        </button>
      </div>
    );
  }

  if (loadedComponents.length === 0) {
    return (
      <div className="text-center py-12">
        <Home className="w-12 h-12 text-gray-600 mx-auto mb-4" />
        <h3 className="text-gray-400 text-lg mb-2">Nessuna Stanza Disponibile</h3>
        <p className="text-gray-500 text-sm">
          Aether non ha ancora creato stanze. Attendere l'auto-evoluzione...
        </p>
        <button
          onClick={refreshComponents}
          className="mt-4 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 rounded text-white text-sm transition-colors"
        >
          Aggiorna
        </button>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-white">
            Stanze di Aether ({loadedComponents.length})
          </h2>
          <button
            onClick={refreshComponents}
            className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm text-white transition-colors"
          >
            Aggiorna
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <AnimatePresence>
            {loadedComponents.map((roomData, index) => (
              <RoomCard
                key={roomData.metadata.name || index}
                roomData={roomData}
                onSelect={setSelectedRoom}
                isSelected={selectedRoom?.metadata.name === roomData.metadata.name}
              />
            ))}
          </AnimatePresence>
        </div>
      </div>

      {/* Full room view modal */}
      <AnimatePresence>
        {selectedRoom && (
          <FullRoomView
            roomData={selectedRoom}
            onClose={() => setSelectedRoom(null)}
          />
        )}
      </AnimatePresence>
    </>
  );
};

// Utility functions
const getMoodGradient = (mood) => {
  const gradients = {
    creativo: 'bg-gradient-to-br from-pink-500 to-orange-500',
    analitico: 'bg-gradient-to-br from-blue-500 to-green-500',
    curioso: 'bg-gradient-to-br from-blue-500 to-purple-500',
    sognatore: 'bg-gradient-to-br from-purple-500 to-pink-500',
    ambizioso: 'bg-gradient-to-br from-yellow-500 to-red-500'
  };
  return gradients[mood] || 'bg-gradient-to-br from-gray-500 to-gray-600';
};

const getMoodBadgeColor = (mood) => {
  const colors = {
    creativo: 'bg-pink-900 text-pink-300',
    analitico: 'bg-blue-900 text-blue-300',
    curioso: 'bg-purple-900 text-purple-300',
    sognatore: 'bg-indigo-900 text-indigo-300',
    ambizioso: 'bg-yellow-900 text-yellow-300'
  };
  return colors[mood] || 'bg-gray-900 text-gray-300';
};

export default DynamicRoomGrid; 