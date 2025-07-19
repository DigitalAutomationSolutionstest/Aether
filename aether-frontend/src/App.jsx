import React, { Suspense, useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { ErrorBoundary } from './utils/errorBoundary'
import DynamicAetherScene from './components/DynamicAetherScene'
import AetherUI from './components/AetherUI'
import { useAetherStore } from './utils/store'

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="cyber-panel p-8 text-center">
        <h2 className="text-2xl font-cyber mb-4 text-aether-accent">
          SYSTEM ERROR
        </h2>
        <p className="text-aether-primary/70 mb-4">
          {error.message}
        </p>
        <button 
          onClick={resetErrorBoundary}
          className="cyber-button"
        >
          RESTART AETHER
        </button>
      </div>
    </div>
  )
}

function LoadingFallback() {
  return (
    <div className="absolute inset-0 bg-black/80 flex items-center justify-center z-50">
      <div className="text-center">
        <div className="text-2xl font-cyber text-aether-primary animate-pulse mb-4">
          MATERIALIZING AETHER...
        </div>
        <div className="w-64 h-1 bg-aether-primary/20 rounded">
          <div className="h-full bg-gradient-to-r from-aether-primary to-aether-secondary rounded animate-pulse"></div>
        </div>
      </div>
    </div>
  )
}

function App() {
  const { identity, isConnected, initializeConnection } = useAetherStore()
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Initialize connection to backend
    initializeConnection()
    
    // Simulate loading time for dramatic effect
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 3000)

    return () => clearTimeout(timer)
  }, [initializeConnection])

  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onReset={() => window.location.reload()}
    >
      <div className="relative w-screen h-screen bg-black overflow-hidden">
        {/* 3D Scene */}
        <Canvas
          camera={{ 
            position: [0, 2, 8], 
            fov: 75,
            near: 0.1,
            far: 1000
          }}
          gl={{ 
            antialias: true,
            alpha: true,
            powerPreference: "high-performance"
          }}
          className="absolute inset-0"
        >
          <Suspense fallback={null}>
            <DynamicAetherScene identity={identity} />
          </Suspense>
        </Canvas>

        {/* UI Overlay */}
        <AetherUI 
          identity={identity}
          isConnected={isConnected}
          isLoading={isLoading}
        />

        {/* Loading Overlay */}
        {isLoading && <LoadingFallback />}

        {/* Connection Status */}
        <div className="absolute top-4 right-4 z-40">
          <div className={`flex items-center space-x-2 cyber-panel px-3 py-2 ${
            isConnected ? 'border-cyber-green' : 'border-aether-accent'
          }`}>
            <div className={`w-2 h-2 rounded-full ${
              isConnected 
                ? 'bg-cyber-green animate-pulse' 
                : 'bg-aether-accent animate-pulse'
            }`}></div>
            <span className="text-xs font-code">
              {isConnected ? 'CONNECTED' : 'DISCONNECTED'}
            </span>
          </div>
        </div>

        {/* Background Matrix Effect */}
        <div className="absolute inset-0 pointer-events-none opacity-10">
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className="absolute text-cyber-green text-xs font-code animate-matrix-rain"
              style={{
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 20}s`,
                animationDuration: `${15 + Math.random() * 10}s`
              }}
            >
              {Math.random().toString(36).substring(2, 8)}
            </div>
          ))}
        </div>
      </div>
    </ErrorBoundary>
  )
}

export default App 