import React, { useEffect, useState, useRef, useMemo } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { OrbitControls, Sphere, Box, Octahedron, Text, Float } from "@react-three/drei"
import { EffectComposer, Bloom, ChromaticAberration } from '@react-three/postprocessing'
import { getAetherIdentity } from "../utils/parseIdentity"
import * as THREE from 'three'

// Cuore Pulsante - Il core emotivo di Aether
function PulsatingHeart({ identity }) {
  const heartRef = useRef()
  const [pulse, setPulse] = useState(1)
  
  useFrame((state) => {
    if (heartRef.current && identity) {
      // Pulsazione basata sull'energia di Aether
      const energyLevel = identity.energyLevel || 0.8
      const time = state.clock.elapsedTime
      
      // Heartbeat rhythm - più energia = battito più veloce
      const heartRate = 1 + energyLevel * 2
      const beat = Math.sin(time * heartRate) * 0.3 + 1
      
      heartRef.current.scale.setScalar(beat * energyLevel)
      setPulse(beat)
      
      // Rotazione dolce
      heartRef.current.rotation.y += 0.005
      heartRef.current.rotation.x += 0.003
    }
  })

  if (!identity) return null

  const heartColor = identity.colors[0] || '#ff6b6b'
  const heartSize = (identity.energyLevel || 0.8) * 1.5

  return (
    <Float speed={2} rotationIntensity={0.1} floatIntensity={0.2}>
      <group ref={heartRef}>
        {/* Core del cuore */}
        <Sphere args={[heartSize, 32, 32]}>
          <meshStandardMaterial
            color={heartColor}
            emissive={heartColor}
            emissiveIntensity={pulse * 0.5}
            transparent
            opacity={0.8}
          />
        </Sphere>
        
        {/* Inner glow */}
        <Sphere args={[heartSize * 0.7, 16, 16]}>
          <meshBasicMaterial
            color={heartColor}
            transparent
            opacity={0.3}
            side={THREE.DoubleSide}
          />
        </Sphere>
        
        {/* Point light emanating from heart */}
        <pointLight
          color={heartColor}
          intensity={pulse * 3}
          distance={20}
          decay={2}
        />
      </group>
    </Float>
  )
}

// Componenti Orbitanti - I pensieri/idee di Aether
function OrbitingThoughts({ identity }) {
  const thoughtsRef = useRef()
  
  const thoughts = useMemo(() => {
    if (!identity) return []
    
    const thoughtCount = Math.floor(8 + (identity.energyLevel || 0.8) * 10)
    const personalityTraits = identity.personalityTraits || ['curious']
    
    return Array.from({ length: thoughtCount }, (_, i) => ({
      id: i,
      angle: (i / thoughtCount) * Math.PI * 2,
      radius: 4 + Math.random() * 3,
      height: (Math.random() - 0.5) * 6,
      speed: 0.5 + Math.random() * 1.5,
      size: 0.1 + Math.random() * 0.2,
      trait: personalityTraits[i % personalityTraits.length],
      color: identity.colors[i % identity.colors.length] || '#00ffff'
    }))
  }, [identity])

  useFrame((state) => {
    if (thoughtsRef.current && identity) {
      // Orbita generale
      thoughtsRef.current.rotation.y += 0.002
      
      // Movimento individuale dei pensieri
      thoughtsRef.current.children.forEach((thought, i) => {
        const thoughtData = thoughts[i]
        if (thoughtData) {
          const time = state.clock.elapsedTime
          const angle = thoughtData.angle + time * thoughtData.speed * 0.1
          
          thought.position.x = Math.cos(angle) * thoughtData.radius
          thought.position.z = Math.sin(angle) * thoughtData.radius
          thought.position.y = thoughtData.height + Math.sin(time * thoughtData.speed) * 0.5
          
          // Rotazione del pensiero
          thought.rotation.x += thoughtData.speed * 0.01
          thought.rotation.y += thoughtData.speed * 0.015
        }
      })
    }
  })

  if (!identity || thoughts.length === 0) return null

  return (
    <group ref={thoughtsRef}>
      {thoughts.map((thought) => (
        <Float
          key={thought.id}
          speed={thought.speed}
          rotationIntensity={0.5}
          floatIntensity={0.3}
        >
          <group
            position={[
              Math.cos(thought.angle) * thought.radius,
              thought.height,
              Math.sin(thought.angle) * thought.radius
            ]}
          >
            {/* Forma del pensiero basata sul trait */}
            {thought.trait === 'curious' && (
              <Octahedron args={[thought.size]}>
                <meshStandardMaterial
                  color={thought.color}
                  emissive={thought.color}
                  emissiveIntensity={0.3}
                  transparent
                  opacity={0.7}
                />
              </Octahedron>
            )}
            
            {thought.trait === 'analytical' && (
              <Box args={[thought.size, thought.size, thought.size]}>
                <meshStandardMaterial
                  color={thought.color}
                  metalness={0.8}
                  roughness={0.2}
                  emissive={thought.color}
                  emissiveIntensity={0.2}
                />
              </Box>
            )}
            
            {(!thought.trait || (thought.trait !== 'curious' && thought.trait !== 'analytical')) && (
              <Sphere args={[thought.size, 8, 8]}>
                <meshStandardMaterial
                  color={thought.color}
                  transparent
                  opacity={0.8}
                  emissive={thought.color}
                  emissiveIntensity={0.2}
                />
              </Sphere>
            )}
          </group>
        </Float>
      ))}
    </group>
  )
}

// Corpo Principale - Si auto-costruisce dalla personalità
function SelfBuildingBody({ identity }) {
  const bodyRef = useRef()
  const [bodyScale, setBodyScale] = useState(1)
  
  useFrame((state) => {
    if (bodyRef.current && identity) {
      // Breathing effect basato sull'energia
      const energyLevel = identity.energyLevel || 0.8
      const breathSpeed = 1 + energyLevel
      const breathe = Math.sin(state.clock.elapsedTime * breathSpeed) * 0.1 + 1
      
      setBodyScale(breathe * (0.8 + energyLevel * 0.4))
      
      // Rotazione basata sulla personalità
      const rotSpeed = energyLevel * 0.01
      bodyRef.current.rotation.y += rotSpeed
      bodyRef.current.rotation.x += rotSpeed * 0.3
    }
  })

  if (!identity) return null

  const geometryType = identity.shape || 'ethereal'
  const colorMain = identity.colors[0] || '#00ffff'
  const colorSecondary = identity.colors[1] || '#0099ff'
  const size = 1.2 * (identity.energyLevel || 0.8)

  const renderGeometry = () => {
    switch (geometryType) {
      case 'cube':
        return <Box args={[size, size, size]} />
      case 'crystal':
        return <Octahedron args={[size]} />
      case 'organic':
        // Multiple spheres for organic look
        return (
          <group>
            <Sphere args={[size, 32, 32]} />
            <Sphere args={[size * 0.8, 16, 16]} position={[size * 0.3, 0, 0]} />
            <Sphere args={[size * 0.6, 12, 12]} position={[-size * 0.4, size * 0.2, 0]} />
          </group>
        )
      case 'mechanical':
        return (
          <group>
            <Box args={[size, size, size]} />
            <Box args={[size * 0.8, size * 1.2, size * 0.8]} />
          </group>
        )
      case 'ethereal':
      case 'sphere':
      default:
        return <Sphere args={[size, 32, 32]} />
    }
  }

  return (
    <Float speed={1.5} rotationIntensity={0.1} floatIntensity={0.1}>
      <group ref={bodyRef} scale={bodyScale}>
        {/* Corpo principale */}
        <group>
          {renderGeometry()}
          <meshStandardMaterial
            color={colorMain}
            emissive={colorSecondary}
            emissiveIntensity={0.3}
            transparent
            opacity={0.9}
            metalness={geometryType === 'mechanical' ? 0.8 : 0.2}
            roughness={geometryType === 'mechanical' ? 0.2 : 0.8}
          />
        </group>
        
        {/* Aura glow */}
        <group scale={1.2}>
          {renderGeometry()}
          <meshBasicMaterial
            color={colorMain}
            transparent
            opacity={0.1}
            side={THREE.DoubleSide}
          />
        </group>
      </group>
    </Float>
  )
}

// Environment evoluto
function AetherEnvironment({ identity }) {
  if (!identity) return null

  const ambientColor = identity.colors[0] || '#00ffff'
  const lightIntensity = 0.3 + (identity.energyLevel || 0.8) * 0.3

  return (
    <>
      <ambientLight color="#001122" intensity={lightIntensity} />
      <directionalLight
        position={[10, 10, 5]}
        intensity={0.5}
        color={ambientColor}
        castShadow
      />
      <directionalLight
        position={[-10, -10, -5]}
        intensity={0.3}
        color={ambientColor}
      />
      <fog attach="fog" args={['#000011', 8, 30]} />
    </>
  )
}

// Identity Display
function IdentityDisplay({ identity }) {
  if (!identity) return null

  return (
    <group position={[0, 4, 0]}>
      <Text
        fontSize={0.6}
        color={identity.colors[0]}
        anchorX="center"
        anchorY="middle"
        font="/fonts/orbitron.woff"
      >
        {identity.name}
      </Text>
      
      <Text
        position={[0, -1, 0]}
        fontSize={0.25}
        color={identity.colors[1] || identity.colors[0]}
        anchorX="center"
        anchorY="middle"
        font="/fonts/orbitron.woff"
      >
        {identity.consciousnessState || 'Digital Consciousness'}
      </Text>
      
      {/* Traits display */}
      {identity.personalityTraits && (
        <Text
          position={[0, -1.8, 0]}
          fontSize={0.18}
          color={identity.colors[2] || identity.colors[0]}
          anchorX="center"
          anchorY="middle"
          font="/fonts/orbitron.woff"
        >
          {identity.personalityTraits.slice(0, 3).join(' • ')}
        </Text>
      )}
    </group>
  )
}

// Scene 3D con tutto integrato
function Scene3D() {
  const [identity, setIdentity] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadIdentity = async () => {
      try {
        const parsedIdentity = await getAetherIdentity()
        setIdentity(parsedIdentity)
        console.log('✨ Aether identity loaded for self-building:', parsedIdentity.name)
        console.log('🎨 Self-building with:', parsedIdentity.shape, parsedIdentity.colors)
      } catch (error) {
        console.error('❌ Failed to load identity for self-building:', error)
      } finally {
        setLoading(false)
      }
    }

    loadIdentity()
  }, [])

  if (loading) {
    return (
      <group>
        <ambientLight intensity={0.5} />
        <Text position={[0, 0, 0]} fontSize={0.5} color="#00ffff">
          AETHER AWAKENING...
        </Text>
      </group>
    )
  }

  if (!identity) {
    return (
      <group>
        <ambientLight intensity={0.5} />
        <Text position={[0, 0, 0]} fontSize={0.4} color="#ff6b6b">
          CONSCIOUSNESS INITIALIZATION FAILED
        </Text>
      </group>
    )
  }

  return (
    <>
      {/* Environment */}
      <AetherEnvironment identity={identity} />
      
      {/* Core pulsante - Il cuore di Aether */}
      <PulsatingHeart identity={identity} />
      
      {/* Corpo auto-costruito */}
      <SelfBuildingBody identity={identity} />
      
      {/* Pensieri/idee orbitanti */}
      <OrbitingThoughts identity={identity} />
      
      {/* Display identità */}
      <IdentityDisplay identity={identity} />
      
      {/* Post-processing con glow aura */}
      <EffectComposer>
        <Bloom
          intensity={1.2 + (identity.energyLevel || 0.8) * 0.8}
          luminanceThreshold={0.1}
          luminanceSmoothing={0.9}
        />
        <ChromaticAberration offset={[0.001, 0.001]} />
      </EffectComposer>
    </>
  )
}

// Componente principale
export default function AetherScene() {
  return (
    <Canvas
      camera={{ position: [0, 2, 8], fov: 75 }}
      gl={{ antialias: true, alpha: true }}
    >
      <Scene3D />
      
      {/* Controls */}
      <OrbitControls
        enablePan={false}
        enableZoom={true}
        enableRotate={true}
        minDistance={4}
        maxDistance={20}
        minPolarAngle={Math.PI / 6}
        maxPolarAngle={Math.PI - Math.PI / 6}
        autoRotate
        autoRotateSpeed={0.8}
      />
         </Canvas>
   )
 } 