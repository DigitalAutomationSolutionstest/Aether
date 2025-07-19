import { useState } from 'react'
import { AetherWorld } from './components/AetherWorld'
import Aether3DWorld from './components/Aether3DWorld'

function App() {
  const [viewMode, setViewMode] = useState('3d-advanced') // '3d-simple' or '3d-advanced'
  
  return (
    <div style={{ width: '100vw', height: '100vh', overflow: 'hidden' }}>
      {/* View mode toggle */}
      <div 
        style={{
          position: 'absolute',
          top: '20px',
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 1000,
          display: 'flex',
          gap: '10px',
          background: 'rgba(0,0,0,0.8)',
          padding: '10px',
          borderRadius: '10px',
          border: '1px solid #00ffff'
        }}
      >
        <button 
          onClick={() => setViewMode('3d-simple')}
          style={{
            padding: '10px 20px',
            background: viewMode === '3d-simple' ? '#00ffff' : 'transparent',
            color: viewMode === '3d-simple' ? '#000' : '#00ffff',
            border: '1px solid #00ffff',
            borderRadius: '5px',
            fontFamily: 'monospace',
            fontWeight: 'bold',
            cursor: 'pointer',
            transition: 'all 0.3s'
          }}
        >
          Simple 3D
        </button>
        <button 
          onClick={() => setViewMode('3d-advanced')}
          style={{
            padding: '10px 20px',
            background: viewMode === '3d-advanced' ? '#00ffff' : 'transparent',
            color: viewMode === '3d-advanced' ? '#000' : '#00ffff',
            border: '1px solid #00ffff',
            borderRadius: '5px',
            fontFamily: 'monospace',
            fontWeight: 'bold',
            cursor: 'pointer',
            transition: 'all 0.3s'
          }}
        >
          Advanced 3D
        </button>
      </div>
      
      {/* Render selected view */}
      {viewMode === '3d-simple' ? <AetherWorld /> : <Aether3DWorld />}
    </div>
  )
}

export default App 