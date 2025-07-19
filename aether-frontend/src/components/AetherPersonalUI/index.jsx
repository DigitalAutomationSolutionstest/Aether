import React, { useState } from 'react';
import AetherDashboard from './AetherDashboard';
import AetherChat from './AetherChat';
import './AetherUI.css';

const AetherPersonalUI = () => {
  const [activeView, setActiveView] = useState('dashboard');
  
  return (
    <div className="aether-personal-ui">
      <nav className="ui-nav">
        <button 
          className={activeView === 'dashboard' ? 'active' : ''}
          onClick={() => setActiveView('dashboard')}
        >
          Dashboard
        </button>
        <button 
          className={activeView === 'chat' ? 'active' : ''}
          onClick={() => setActiveView('chat')}
        >
          Chat
        </button>
      </nav>
      
      <div className="ui-content">
        {activeView === 'dashboard' ? <AetherDashboard /> : <AetherChat />}
      </div>
    </div>
  );
};

export default AetherPersonalUI; 