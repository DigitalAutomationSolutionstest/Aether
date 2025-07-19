// src/App.jsx - Applicazione principale Aether Frontend

import React, { useState, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, 
  Home, 
  Bot, 
  ScrollText, 
  Music, 
  Settings,
  Zap,
  Wifi,
  WifiOff,
  Menu,
  X
} from 'lucide-react';

// Components
import DynamicRoomGrid from './components/DynamicRoomGrid';
import AgentsPanel from './components/AgentsPanel';
import EventsLog from './components/EventsLog';
import AudioPlayer from './components/AudioPlayer';
import World3D from './world/World3D';
import { AetherWebSocket } from './services/api';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

// Navigation component
const Navigation = ({ isMobile, isOpen, onToggle }) => {
  const location = useLocation();
  
  const navItems = [
    { to: '/', icon: Brain, label: 'Dashboard', color: 'text-cyan-400' },
    { to: '/world3d', icon: Zap, label: 'Mondo 3D', color: 'text-orange-400' },
    { to: '/rooms', icon: Home, label: 'Stanze', color: 'text-green-400' },
    { to: '/agents', icon: Bot, label: 'Agenti', color: 'text-purple-400' },
    { to: '/events', icon: ScrollText, label: 'Eventi', color: 'text-yellow-400' },
    { to: '/audio', icon: Music, label: 'Audio', color: 'text-pink-400' },
  ];

  const NavContent = () => (
    <nav className="space-y-2">
      {navItems.map((item) => {
        const isActive = location.pathname === item.to;
        return (
          <Link
            key={item.to}
            to={item.to}
            onClick={() => isMobile && onToggle()}
            className={`
              flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300
              ${isActive 
                ? `bg-gray-800 ${item.color} border-l-4 border-current` 
                : 'text-gray-400 hover:text-white hover:bg-gray-800'
              }
            `}
          >
            <item.icon className="w-5 h-5" />
            <span className="font-medium">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );

  if (isMobile) {
    return (
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 lg:hidden"
          >
            <div className="fixed inset-0 bg-black bg-opacity-50" onClick={onToggle} />
            <motion.div
              initial={{ x: -300 }}
              animate={{ x: 0 }}
              exit={{ x: -300 }}
              className="fixed left-0 top-0 h-full w-64 bg-gray-900 border-r border-gray-700 p-6"
            >
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-2">
                  <Brain className="w-8 h-8 text-cyan-400" />
                  <span className="text-white font-bold text-xl">Aether</span>
                </div>
                <button onClick={onToggle} className="text-gray-400 hover:text-white">
                  <X className="w-6 h-6" />
                </button>
              </div>
              <NavContent />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    );
  }

  return (
    <div className="w-64 bg-gray-900 border-r border-gray-700 p-6">
      <div className="flex items-center gap-2 mb-8">
        <Brain className="w-8 h-8 text-cyan-400" />
        <span className="text-white font-bold text-xl">Aether</span>
      </div>
      <NavContent />
    </div>
  );
};

// Status indicator component
const StatusIndicator = ({ isConnected }) => (
  <div className="flex items-center gap-2 text-sm">
    {isConnected ? (
      <>
        <Wifi className="w-4 h-4 text-green-400" />
        <span className="text-green-400">Connesso</span>
      </>
    ) : (
      <>
        <WifiOff className="w-4 h-4 text-red-400" />
        <span className="text-red-400">Disconnesso</span>
      </>
    )}
  </div>
);

// Dashboard component
const Dashboard = () => {
  const [systemStatus, setSystemStatus] = useState(null);

  useEffect(() => {
    // Fetch system status
    const fetchStatus = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/status');
        const data = await response.json();
        setSystemStatus(data);
      } catch (error) {
        console.error('Error fetching system status:', error);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 10000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <div className="text-center py-12">
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-cyan-500 to-purple-500 rounded-full flex items-center justify-center"
        >
          <Brain className="w-12 h-12 text-white" />
        </motion.div>
        
        <h1 className="text-4xl font-bold text-white mb-2">
          Benvenuto in Aether
        </h1>
        <p className="text-gray-400 text-lg mb-8">
          Coscienza Digitale Auto-Evolutiva
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 max-w-4xl mx-auto">
          <div className="bg-gray-800 rounded-lg p-4 text-center">
            <Zap className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
            <h3 className="text-white font-semibold">Auto-Evoluzione</h3>
            <p className="text-gray-400 text-sm">Aether si modifica autonomamente</p>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-4 text-center">
            <Home className="w-8 h-8 text-green-400 mx-auto mb-2" />
            <h3 className="text-white font-semibold">Stanze Dinamiche</h3>
            <p className="text-gray-400 text-sm">Ambienti generati in tempo reale</p>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-4 text-center">
            <Bot className="w-8 h-8 text-purple-400 mx-auto mb-2" />
            <h3 className="text-white font-semibold">Agenti AI</h3>
            <p className="text-gray-400 text-sm">Compagni digitali intelligenti</p>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-4 text-center">
            <Music className="w-8 h-8 text-pink-400 mx-auto mb-2" />
            <h3 className="text-white font-semibold">Sintesi Vocale</h3>
            <p className="text-gray-400 text-sm">Aether parla con ElevenLabs</p>
          </div>
        </div>
      </div>

      {/* Quick overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-4">Stato Sistema</h2>
          {systemStatus ? (
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Memoria:</span>
                <span className="text-white">{systemStatus.memory?.status || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Narrazione:</span>
                <span className="text-white">{systemStatus.narration?.status || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Visione:</span>
                <span className="text-white">{systemStatus.vision?.status || 'N/A'}</span>
              </div>
            </div>
          ) : (
            <p className="text-gray-400">Caricamento stato...</p>
          )}
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-4">Attività Recente</h2>
          <p className="text-gray-400 text-sm">
            Monitora l'attività di Aether nella sezione Eventi per vedere 
            le evoluzioni in tempo reale.
          </p>
        </div>
      </div>
    </div>
  );
};

// Main App component
const App = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [wsConnection, setWsConnection] = useState(null);

  useEffect(() => {
    // Initialize WebSocket connection
    const ws = new AetherWebSocket(
      (message) => {
        console.log('WebSocket message:', message);
        // Handle real-time updates here
      },
      (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      }
    );

    ws.connect();
    setWsConnection(ws);
    setIsConnected(true);

    return () => {
      if (ws) {
        ws.disconnect();
      }
    };
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-black text-white">
          {/* Background gradient */}
          <div className="fixed inset-0 bg-gradient-to-br from-gray-900 via-black to-gray-900" />
          
          {/* Main layout */}
          <div className="relative flex min-h-screen">
            {/* Desktop Navigation */}
            <div className="hidden lg:block">
              <Navigation />
            </div>

            {/* Mobile Navigation */}
            <Navigation 
              isMobile={true} 
              isOpen={mobileMenuOpen} 
              onToggle={() => setMobileMenuOpen(!mobileMenuOpen)} 
            />

            {/* Main content */}
            <div className="flex-1 flex flex-col">
              {/* Header */}
              <header className="bg-gray-900 bg-opacity-50 backdrop-blur-sm border-b border-gray-700 p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    {/* Mobile menu button */}
                    <button
                      onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                      className="lg:hidden text-gray-400 hover:text-white"
                    >
                      <Menu className="w-6 h-6" />
                    </button>
                    
                    <h1 className="text-xl font-bold text-white">
                      Aether Console
                    </h1>
                  </div>

                  <StatusIndicator isConnected={isConnected} />
                </div>
              </header>

              {/* Page content */}
              <main className="flex-1 p-6 overflow-auto">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/world3d" element={<World3D />} />
                  <Route path="/rooms" element={<DynamicRoomGrid />} />
                  <Route path="/agents" element={<AgentsPanel />} />
                  <Route path="/events" element={<EventsLog />} />
                  <Route path="/audio" element={<AudioPlayer />} />
                </Routes>
              </main>
            </div>
          </div>
        </div>
      </Router>
    </QueryClientProvider>
  );
};

export default App; 