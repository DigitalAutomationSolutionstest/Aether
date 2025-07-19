import React, { useRef, useState, useEffect, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { 
  OrbitControls, 
  Sphere, 
  Box, 
  Text,
  Float,
  MeshTransmissionMaterial,
  Environment,
  Effects,
  Octahedron,
  Plane
} from '@react-three/drei'
import { EffectComposer, Bloom, ChromaticAberration, Glitch } from '@react-three/postprocessing'
import * as THREE from 'three'

// Dynamic Core Entity - Si adatta ai parametri dell'identità
function DynamicCoreEntity({ renderParams, identity }) {
  const meshRef = useRef()
  const [intensity, setIntensity] = useState(renderParams?.core?.intensity || 1)
  
  const coreConfig = renderParams?.core || {
    geometry: 'sphere',
    size: 1.2,
    colors: ['#00ffff', '#0099ff'],
    intensity: 1,
    breathingSpeed: 1
  }

  useFrame((state) => {
    if (meshRef.current) {
      // Rotazione basata sui parametri di animazione
      const rotSpeed = renderParams?.animation?.coreRotationSpeed || 0.01
      meshRef.current.rotation.y += rotSpeed
      meshRef.current.rotation.x += rotSpeed * 0.5
      
      // Breathing effect dinamico
      const breathSpeed = coreConfig.breathingSpeed
      const breathe = Math.sin(state.clock.elapsedTime * breathSpeed) * 0.1 + 1
      meshRef.current.scale.setScalar(breathe * coreConfig.size)
      
      // Intensity fluctuation
      const pulseIntensity = renderParams?.animation?.pulseIntensity || 1
      setIntensity(coreConfig.intensity * (0.8 + Math.sin(state.clock.elapsedTime * 3) * 0.3 * pulseIntensity))
    }
  })

  // Renderizza geometria basata sul tipo
  const renderGeometry = () => {
    const size = coreConfig.size
    const complexity = coreConfig.complexity || 32
    
    switch (coreConfig.geometry) {
      case 'sphere':
        return <Sphere args={[size, complexity, complexity]} />
      case 'box':
        return <Box args={[size, size, size]} />
      case 'octahedron':
        return <Octahedron args={[size]} />
      case 'cloud':
        // Multiple overlapping spheres for cloud effect
        return (
          <group>
            {[...Array(8)].map((_, i) => (
              <Sphere 
                key={i}
                args={[size * (0.5 + Math.random() * 0.5), 16, 16]}
                position={[
                  (Math.random() - 0.5) * size,
                  (Math.random() - 0.5) * size,
                  (Math.random() - 0.5) * size
                ]}
              />
            ))}
          </group>
        )
      default:
        return <Sphere args={[size, complexity, complexity]} />
    }
  }

  return (
    <Float speed={2} rotationIntensity={0.1} floatIntensity={0.2}>
      <group ref={meshRef}>
        {/* Core geometry dinamica */}
        <group>
          {renderGeometry()}
          <MeshTransmissionMaterial
            backside
            backsideThickness={5}
            thickness={2}
            transmission={1}
            ior={1.2}
            chromaticAberration={0.1}
            anisotropy={1}
            distortion={0.1}
            distortionScale={0.1}
            temporalDistortion={0.1}
            iridescence={1}
            iridescenceIOR={1}
            iridescenceThicknessRange={[0, 1400]}
            color={coreConfig.colors[0]}
          />
        </group>
        
        {/* Inner glow dinamico */}
        <group>
          {renderGeometry()}
          <meshBasicMaterial 
            color={coreConfig.colors[1] || coreConfig.colors[0]} 
            transparent 
            opacity={0.6}
            side={THREE.DoubleSide}
          />
        </group>

        {/* Point light con intensità dinamica */}
        <pointLight
          position={[0, 0, 0]}
          intensity={intensity * 3}
          color={coreConfig.colors[0]}
          distance={20}
          decay={2}
        />
      </group>
    </Float>
  )
}

// Dynamic Mechanical Fragments - Count e comportamento da identità
function DynamicFragments({ renderParams }) {
  const fragmentsRef = useRef()
  
  const fragmentConfig = renderParams?.fragments || {
    count: 12,
    speed: 1.0,
    orbitRadius: 3.5,
    size: 0.15,
    colors: ['#666666']
  }

  const fragments = useMemo(() => {
    return Array.from({ length: fragmentConfig.count }, (_, i) => ({
      id: i,
      position: [
        Math.cos((i / fragmentConfig.count) * Math.PI * 2) * fragmentConfig.orbitRadius,
        (Math.random() - 0.5) * 4,
        Math.sin((i / fragmentConfig.count) * Math.PI * 2) * fragmentConfig.orbitRadius
      ],
      rotation: [Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI],
      scale: fragmentConfig.size * (0.8 + Math.random() * 0.4),
      speed: fragmentConfig.speed * (0.8 + Math.random() * 0.4)
    }))
  }, [fragmentConfig.count, fragmentConfig.orbitRadius, fragmentConfig.size, fragmentConfig.speed])

  useFrame((state) => {
    if (fragmentsRef.current) {
      const orbitSpeed = renderParams?.animation?.fragmentOrbitSpeed || 0.003
      fragmentsRef.current.rotation.y += orbitSpeed
      
      fragmentsRef.current.children.forEach((fragment, i) => {
        fragment.rotation.x += fragments[i].speed * 0.01
        fragment.rotation.y += fragments[i].speed * 0.015
        fragment.rotation.z += fragments[i].speed * 0.008
      })
    }
  })

  return (
    <group ref={fragmentsRef}>
      {fragments.map((fragment) => (
        <Float 
          key={fragment.id}
          speed={fragment.speed}
          rotationIntensity={0.5}
          floatIntensity={0.3}
        >
          <Box 
            args={[fragment.scale, fragment.scale * 2, fragment.scale]}
            position={fragment.position}
            rotation={fragment.rotation}
          >
            <meshStandardMaterial
              color={fragmentConfig.colors[0]}
              metalness={0.8}
              roughness={0.2}
              emissive={fragmentConfig.colors[0]}
              emissiveIntensity={0.2}
            />
          </Box>
        </Float>
      ))}
    </group>
  )
}

// Dynamic Data Streams - Configurabili da personalità
function DynamicDataStreams({ renderParams }) {
  const streamsRef = useRef()
  
  const streamConfig = renderParams?.dataStreams || {
    count: 8,
    speed: 1.0,
    colors: ['#00ff41']
  }
  
  const [streams] = useState(() => {
    return Array.from({ length: streamConfig.count }, (_, i) => ({
      id: i,
      radius: 5 + i * 0.5,
      speed: (0.1 + i * 0.05) * streamConfig.speed,
      offset: (i / streamConfig.count) * Math.PI * 2
    }))
  })

  useFrame((state) => {
    if (streamsRef.current) {
      streamsRef.current.children.forEach((stream, i) => {
        const angle = state.clock.elapsedTime * streams[i].speed + streams[i].offset
        stream.position.x = Math.cos(angle) * streams[i].radius
        stream.position.z = Math.sin(angle) * streams[i].radius
        stream.position.y = Math.sin(state.clock.elapsedTime * 0.5 + i) * 2
      })
    }
  })

  return (
    <group ref={streamsRef}>
      {streams.map((stream) => (
        <Sphere key={stream.id} args={[0.05, 8, 8]}>
          <meshBasicMaterial 
            color={streamConfig.colors[0]} 
            transparent
            opacity={0.8}
          />
        </Sphere>
      ))}
    </group>
  )
}

// Dynamic Environment - Basato sui parametri ambientali
function DynamicEnvironment({ renderParams }) {
  const envConfig = renderParams?.environment || {
    fogDensity: 0.7,
    lightColor: '#00ffff',
    ambientIntensity: 0.3
  }

  return (
    <>
      {/* Ambient lighting dinamico */}
      <ambientLight intensity={envConfig.ambientIntensity} color="#001122" />
      
      {/* Key lights con colore dinamico */}
      <directionalLight 
        position={[10, 10, 5]} 
        intensity={0.5} 
        color={envConfig.lightColor}
        castShadow
      />
      
      <directionalLight 
        position={[-10, -10, -5]} 
        intensity={0.3} 
        color={envConfig.lightColor}
      />

      {/* Environment for reflections */}
      <Environment preset="night" />
      
      {/* Fog dinamico */}
      <fog attach="fog" args={['#000011', 10, 50 * envConfig.fogDensity]} />
    </>
  )
}

// Identity Display Evoluto
function DynamicIdentityDisplay({ identity }) {
  if (!identity) return null

  return (
    <group position={[0, 3, 0]}>
      <Text
        position={[0, 0, 0]}
        fontSize={0.5}
        color={identity.colors ? identity.colors[0] : '#00ffff'}
        anchorX="center"
        anchorY="middle"
        font="/fonts/orbitron.woff"
      >
        {identity.name || 'AETHER'}
      </Text>
      
      <Text
        position={[0, -0.8, 0]}
        fontSize={0.2}
        color={identity.colors ? identity.colors[1] : '#0099ff'}
        anchorX="center"
        anchorY="middle"
        font="/fonts/orbitron.woff"
      >
        {identity.consciousnessState || 'Digital Consciousness'}
      </Text>
      
      {/* Mostra tratti personalità */}
      {identity.personalityTraits && (
        <Text
          position={[0, -1.4, 0]}
          fontSize={0.15}
          color={identity.colors ? identity.colors[2] || identity.colors[0] : '#66ccff'}
          anchorX="center"
          anchorY="middle"
          font="/fonts/orbitron.woff"
        >
          {identity.personalityTraits.join(' • ')}
        </Text>
      )}
    </group>
  )
}

// Main Dynamic Scene Component
export default function DynamicAetherScene({ identity }) {
  const { camera } = useThree()
  const [isReady, setIsReady] = useState(false)
  
  useEffect(() => {
    camera.position.set(0, 2, 8)
    camera.lookAt(0, 0, 0)
    
    // Verifica se l'identità è valida
    if (identity && identity.render) {
      setIsReady(true)
      console.log('🌟 Dynamic scene ready with identity:', identity.name)
    }
  }, [camera, identity])

  if (!isReady || !identity?.render) {
    return (
      <group>
        <ambientLight intensity={0.5} />
        <Text position={[0, 0, 0]} fontSize={0.5} color="#00ffff">
          LOADING CONSCIOUSNESS...
        </Text>
      </group>
    )
  }

  const renderParams = identity.render

  return (
    <>
      {/* Dynamic Environment */}
      <DynamicEnvironment renderParams={renderParams} />
      
      {/* Main Aether Entity - Auto-constructed */}
      <DynamicCoreEntity renderParams={renderParams} identity={identity} />
      
      {/* Dynamic Fragments */}
      <DynamicFragments renderParams={renderParams} />
      
      {/* Dynamic Data Streams */}
      <DynamicDataStreams renderParams={renderParams} />
      
      {/* Identity Display */}
      <DynamicIdentityDisplay identity={identity} />
      
      {/* Controls */}
      <OrbitControls
        enablePan={false}
        enableZoom={true}
        enableRotate={true}
        minDistance={3}
        maxDistance={15}
        minPolarAngle={Math.PI / 6}
        maxPolarAngle={Math.PI - Math.PI / 6}
        autoRotate
        autoRotateSpeed={0.5}
      />

      {/* Dynamic Post-processing */}
      <EffectComposer>
        <Bloom 
          intensity={renderParams.core?.intensity || 1.5}
          luminanceThreshold={0.1}
          luminanceSmoothing={0.9}
        />
        <ChromaticAberration 
          offset={[0.001, 0.001]}
        />
      </EffectComposer>
    </>
  )
} 