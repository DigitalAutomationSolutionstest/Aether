import React, { useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment } from '@react-three/drei'
import AetherScene from './AetherScene'
import EntityScene from './EntityScene'
import { useAetherStore } from '../utils/store'

export default function Scene() {
  const { identity, isConnected } = useAetherStore()
  const [entities, setEntities] = useState([])
  const [entitiesLoading, setEntitiesLoading] = useState(false)

  // Carica entità quando l'identità cambia o la connessione si stabilisce
  useEffect(() => {
    if (isConnected) {
      loadEntities()
      
      // Ricarica entità ogni 30 secondi per vedere nuove creazioni autonome
      const interval = setInterval(loadEntities, 30000)
      return () => clearInterval(interval)
    }
  }, [isConnected])

  const loadEntities = async () => {
    if (entitiesLoading) return
    
    setEntitiesLoading(true)
    try {
      const response = await fetch('/api/entities/')
      const data = await response.json()
      
      if (data.status === 'success') {
        setEntities(data.entities || [])
      }
    } catch (error) {
      console.error('Error loading entities for scene:', error)
    } finally {
      setEntitiesLoading(false)
    }
  }

  // Calcola posizioni per le entità in cerchio attorno ad Aether
  const getEntityPosition = (index, total) => {
    if (total === 0) return [0, 0, 0]
    
    const radius = Math.max(8, 4 + total * 1.2) // Raggio basato su numero entità
    const angle = (index / total) * Math.PI * 2
    const x = Math.cos(angle) * radius
    const z = Math.sin(angle) * radius
    const y = Math.sin(index * 0.5) * 2 // Variazione in altezza
    
    return [x, y, z]
  }

  return (
    <div className="w-full h-full">
      <Canvas
        camera={{ position: [0, 5, 10], fov: 75 }}
        gl={{ antialias: true, alpha: true }}
      >
        {/* Illuminazione */}
        <ambientLight intensity={0.6} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#4a9eff" />
        
        {/* Controlli orbita */}
        <OrbitControls 
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          maxDistance={50}
          minDistance={5}
        />
        
        {/* Ambiente */}
        <Environment preset="night" />
        
        {/* Nebbia atmosferica */}
        <fog attach="fog" args={['#1a1a2e', 20, 100]} />
        
        {/* Aether al centro */}
        {identity && (
          <AetherScene 
            identity={identity} 
            position={[0, 0, 0]}
          />
        )}
        
        {/* Entità generate disposte in cerchio */}
        {entities.map((entity, index) => (
          <EntityScene
            key={entity.name || `entity-${index}`}
            entity={entity}
            position={getEntityPosition(index, entities.length)}
          />
        ))}
        
        {/* Piano di base */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -5, 0]}>
          <planeGeometry args={[200, 200]} />
          <meshStandardMaterial 
            color="#0a0a1a" 
            transparent 
            opacity={0.3}
            wireframe
          />
        </mesh>
        
        {/* Griglia di riferimento */}
        <gridHelper 
          args={[50, 20, '#333366', '#222244']} 
          position={[0, -4.9, 0]} 
        />
        
        {/* Particelle di atmosfera se ci sono entità */}
        {entities.length > 0 && (
          <group>
            {[...Array(20)].map((_, i) => (
              <mesh
                key={i}
                position={[
                  (Math.random() - 0.5) * 60,
                  Math.random() * 20 - 5,
                  (Math.random() - 0.5) * 60
                ]}
              >
                <sphereGeometry args={[0.1, 4, 4]} />
                <meshBasicMaterial
                  color="#4a9eff"
                  transparent
                  opacity={0.3}
                />
              </mesh>
            ))}
          </group>
        )}
        
        {/* Luci dinamiche per ogni entità */}
        {entities.map((entity, index) => {
          const position = getEntityPosition(index, entities.length)
          const color = entity.colors && entity.colors[0] ? entity.colors[0] : '#ffffff'
          
          return (
            <pointLight
              key={`light-${entity.name || index}`}
              position={[position[0], position[1] + 2, position[2]]}
              color={color}
              intensity={0.5}
              distance={10}
            />
          )
        })}
      </Canvas>
      
      {/* Overlay informazioni entità */}
      {entities.length > 0 && (
        <div className="absolute bottom-4 left-4 bg-gray-900 bg-opacity-90 rounded border border-gray-600 p-3 max-w-xs">
          <h4 className="text-cyan-400 font-semibold mb-2">Digital Society</h4>
          <div className="text-sm text-gray-300">
            <p>{entities.length} entity{entities.length !== 1 ? 'ies' : ''} active</p>
            
            {/* Mostra distribuzione traits */}
            {entities.length > 0 && (
              <div className="mt-2">
                <div className="text-xs text-gray-400">Traits:</div>
                <div className="flex flex-wrap gap-1 mt-1">
                  {[...new Set(entities.map(e => e.trait))].map(trait => {
                    const count = entities.filter(e => e.trait === trait).length
                    const colors = {
                      strategic: 'bg-blue-600',
                      creative: 'bg-pink-600',
                      empathetic: 'bg-green-600',
                      curious: 'bg-yellow-600',
                      protective: 'bg-red-600',
                      mysterious: 'bg-purple-600'
                    }
                    
                    return (
                      <span
                        key={trait}
                        className={`text-xs px-2 py-1 rounded ${colors[trait] || 'bg-gray-600'} text-white`}
                      >
                        {trait}: {count}
                      </span>
                    )
                  })}
                </div>
              </div>
            )}
            
            {/* Mostra ultima entità creata */}
            {identity?.last_entity_generated && (
              <div className="mt-2 pt-2 border-t border-gray-700">
                <div className="text-xs text-gray-400">Latest:</div>
                <div className="text-xs text-cyan-300">
                  {identity.last_entity_generated.name} ({identity.last_entity_generated.trait})
                </div>
              </div>
            )}
          </div>
        </div>
      )}
      
      {/* Indicatore caricamento entità */}
      {entitiesLoading && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-900 bg-opacity-90 rounded border border-cyan-400 p-4">
          <div className="flex items-center space-x-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-cyan-400"></div>
            <span className="text-cyan-400">Loading entities...</span>
          </div>
        </div>
      )}
    </div>
  )
} 