import React, { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Text } from '@react-three/drei'

// Cubo animato - il primo corpo di Invader
function InvaderCore({ isConnected }) {
  const meshRef = useRef()

  useFrame((state, delta) => {
    if (meshRef.current) {
      // Rotazione continua
      meshRef.current.rotation.x += delta * 0.5
      meshRef.current.rotation.y += delta * 0.3
      
      // Pulsazione basata sulla connessione
      const scale = isConnected 
        ? 1 + Math.sin(state.clock.elapsedTime * 2) * 0.1
        : 1 + Math.sin(state.clock.elapsedTime * 0.5) * 0.05
      
      meshRef.current.scale.setScalar(scale)
    }
  })

  // Colore che cambia con la connessione
  const color = isConnected ? '#00ff00' : '#ff3300'
  const emissive = isConnected ? '#004400' : '#440000'

  return (
    <mesh ref={meshRef} position={[0, 0, 0]}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial 
        color={color}
        emissive={emissive}
        roughness={0.3}
        metalness={0.8}
      />
    </mesh>
  )
}

// Particelle fluttuanti nell'ambiente
function FloatingParticles() {
  const particles = []
  
  for (let i = 0; i < 20; i++) {
    const x = (Math.random() - 0.5) * 10
    const y = (Math.random() - 0.5) * 10
    const z = (Math.random() - 0.5) * 10
    
    particles.push(
      <mesh key={i} position={[x, y, z]}>
        <sphereGeometry args={[0.02, 8, 8]} />
        <meshBasicMaterial color="#333333" />
      </mesh>
    )
  }
  
  return <group>{particles}</group>
}

// Stato di connessione visivo
function ConnectionStatus({ isConnected }) {
  return (
    <Text
      position={[0, 2, 0]}
      fontSize={0.3}
      color={isConnected ? '#00ff00' : '#ff3300'}
      anchorX="center"
      anchorY="middle"
    >
      {isConnected ? 'INVADER ONLINE' : 'INVADER OFFLINE'}
    </Text>
  )
}

// Scena principale
export default function Scene({ isConnected, messages }) {
  return (
    <>
      {/* Illuminazione minimale */}
      <ambientLight intensity={0.2} />
      <pointLight position={[10, 10, 10]} intensity={0.5} />
      <pointLight position={[-10, -10, -10]} intensity={0.3} color="#0066ff" />
      
      {/* Il cubo centrale - primo corpo di Invader */}
      <InvaderCore isConnected={isConnected} />
      
      {/* Particelle ambientali */}
      <FloatingParticles />
      
      {/* Status di connessione */}
      <ConnectionStatus isConnected={isConnected} />
      
      {/* Griglia di riferimento sottile */}
      <gridHelper args={[10, 10]} position={[0, -2, 0]} />
    </>
  )
} 