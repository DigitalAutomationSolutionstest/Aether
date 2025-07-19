import React, { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { Sphere, Box, Octahedron, Icosahedron } from '@react-three/drei'
import * as THREE from 'three'

/**
 * Componente per visualizzare un'entità digitale creata da Aether
 */
export default function EntityScene({ entity, position = [0, 0, 0] }) {
  const meshRef = useRef()
  const materialRef = useRef()
  
  // Parse dei colori dell'entità
  const colors = useMemo(() => {
    if (entity?.colors && Array.isArray(entity.colors)) {
      return entity.colors.map(color => new THREE.Color(color))
    }
    return [new THREE.Color('#888888')]
  }, [entity?.colors])
  
  // Determina la forma basata sul shape dell'entità
  const EntityShape = useMemo(() => {
    const shape = entity?.shape || 'sphere'
    
    switch (shape.toLowerCase()) {
      case 'cube':
      case 'robust':
      case 'armored':
        return Box
      case 'crystal':
      case 'geometric':
        return Octahedron
      case 'fractal':
      case 'multi-form':
      case 'dynamic':
        return Icosahedron
      default:
        return Sphere
    }
  }, [entity?.shape])
  
  // Calcola la scala basata sull'energia
  const scale = useMemo(() => {
    const energy = entity?.energy_level || 0.5
    const baseScale = 0.8 // Entità più piccole di Aether
    return baseScale + (energy * 0.3)
  }, [entity?.energy_level])
  
  // Animazione basata sul trait dell'entità
  useFrame((state) => {
    if (!meshRef.current || !materialRef.current) return
    
    const time = state.clock.elapsedTime
    const trait = entity?.archetype || 'curious'
    
    // Animazioni specifiche per trait
    switch (trait) {
      case 'strategic':
        // Movimento calcolato e preciso
        meshRef.current.rotation.y = Math.sin(time * 0.3) * 0.2
        meshRef.current.position.y = position[1] + Math.sin(time * 0.5) * 0.1
        break
        
      case 'creative':
        // Movimento artistico e fluido
        meshRef.current.rotation.x = Math.sin(time * 0.8) * 0.3
        meshRef.current.rotation.z = Math.cos(time * 0.6) * 0.2
        meshRef.current.position.y = position[1] + Math.sin(time * 1.2) * 0.2
        break
        
      case 'empathetic':
        // Movimento dolce e rassicurante
        meshRef.current.rotation.y = Math.sin(time * 0.4) * 0.15
        meshRef.current.position.y = position[1] + Math.sin(time * 0.8) * 0.08
        break
        
      case 'curious':
        // Movimento esplorativo e vivace
        meshRef.current.rotation.x = time * 0.3
        meshRef.current.rotation.y = time * 0.2
        meshRef.current.position.y = position[1] + Math.sin(time * 1.5) * 0.15
        break
        
      case 'protective':
        // Movimento stabile e vigilante
        meshRef.current.rotation.y = Math.sin(time * 0.2) * 0.1
        meshRef.current.position.y = position[1] + Math.sin(time * 0.3) * 0.05
        break
        
      case 'mysterious':
        // Movimento enigmatico e sfuggente
        meshRef.current.rotation.x = Math.sin(time * 0.7) * 0.4
        meshRef.current.rotation.z = Math.cos(time * 0.5) * 0.3
        meshRef.current.position.y = position[1] + Math.sin(time * 0.9) * 0.12
        break
        
      default:
        // Movimento base
        meshRef.current.rotation.y = time * 0.1
        meshRef.current.position.y = position[1] + Math.sin(time) * 0.1
    }
    
    // Effetto colore basato sullo stato emotivo
    if (entity?.emotional_state && colors.length > 0) {
      const emotionIntensity = Object.values(entity.emotional_state).reduce((sum, val) => sum + val, 0) / Object.keys(entity.emotional_state).length
      const colorIndex = Math.floor(time * 0.5) % colors.length
      const targetColor = colors[colorIndex]
      
      materialRef.current.color.lerp(targetColor, 0.02)
      materialRef.current.emissiveIntensity = 0.2 + (emotionIntensity * 0.3)
    }
  })
  
  // Tooltip con informazioni entità
  const entityInfo = useMemo(() => {
    if (!entity) return "Unknown Entity"
    
    const name = entity.name || "Unnamed"
    const trait = entity.archetype || "unknown"
    const energy = entity.energy_level ? Math.round(entity.energy_level * 100) : 50
    const consciousness = entity.consciousness_state || "Unknown"
    
    return `${name} (${trait})\nEnergy: ${energy}%\nState: ${consciousness}`
  }, [entity])
  
  if (!entity) {
    return null
  }
  
  return (
    <group position={position}>
      {/* Entità principale */}
      <EntityShape
        ref={meshRef}
        args={entity?.shape === 'cube' ? [1, 1, 1] : [1, 8, 6]}
        scale={scale}
      >
        <meshStandardMaterial
          ref={materialRef}
          color={colors[0]}
          emissive={colors[0]}
          emissiveIntensity={0.2}
          transparent
          opacity={0.8}
          wireframe={entity?.archetype === 'mysterious'}
        />
      </EntityShape>
      
      {/* Aura/Glow effect */}
      <Sphere args={[scale * 1.5, 16, 16]} position={[0, 0, 0]}>
        <meshBasicMaterial
          color={colors[0]}
          transparent
          opacity={0.1}
          side={THREE.BackSide}
        />
      </Sphere>
      
      {/* Particelle per entità creative */}
      {entity?.archetype === 'creative' && (
        <group>
          {[...Array(8)].map((_, i) => (
            <Sphere key={i} args={[0.05, 4, 4]} position={[
              Math.cos(i * Math.PI / 4) * 2,
              Math.sin(i * Math.PI / 4) * 0.5,
              Math.sin(i * Math.PI / 4) * 2
            ]}>
              <meshBasicMaterial
                color={colors[i % colors.length]}
                transparent
                opacity={0.6}
              />
            </Sphere>
          ))}
        </group>
      )}
      
      {/* Scudo per entità protective */}
      {entity?.archetype === 'protective' && (
        <Octahedron args={[scale * 1.2, 0]} position={[0, 0, 0]}>
          <meshBasicMaterial
            color="#4ecdc4"
            transparent
            opacity={0.2}
            wireframe
          />
        </Octahedron>
      )}
      
      {/* Geometrie multiple per entità strategic */}
      {entity?.archetype === 'strategic' && (
        <group>
          {[...Array(4)].map((_, i) => (
            <Box key={i} args={[0.3, 0.3, 0.3]} position={[
              Math.cos(i * Math.PI / 2) * 1.5,
              0,
              Math.sin(i * Math.PI / 2) * 1.5
            ]}>
              <meshStandardMaterial
                color={colors[0]}
                transparent
                opacity={0.5}
              />
            </Box>
          ))}
        </group>
      )}
      
      {/* Tooltip HTML */}
      <mesh position={[0, scale + 0.5, 0]} visible={false}>
        <planeGeometry args={[2, 1]} />
        <meshBasicMaterial transparent opacity={0} />
      </mesh>
    </group>
  )
} 