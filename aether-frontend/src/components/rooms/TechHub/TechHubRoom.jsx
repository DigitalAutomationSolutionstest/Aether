import React, { useRef, useFrame } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Text, Box, Sphere } from '@react-three/drei'

function TechHubScene() {
  const meshRef = useRef()

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x = state.clock.elapsedTime * 0.3
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.2
    }
  })

  return (
    <group>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      
      <Sphere ref={meshRef} args={[1, 32, 32]} position={[0, 0, 0]}>
        <meshStandardMaterial color="#ff6b6b" />
      </Sphere>
      
      <Box args={[2, 0.1, 2]} position={[0, -2, 0]}>
        <meshStandardMaterial color="#4ecdc4" />
      </Box>
      
      <Text
        position={[0, 3, 0]}
        fontSize={0.5}
        color="#ffffff"
        anchorX="center"
      >
        TechHub
      </Text>
    </group>
  )
}

export default function TechHubRoom() {
  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <Canvas camera={{ position: [5, 5, 5] }}>
        <OrbitControls />
        <TechHubScene />
      </Canvas>
    </div>
  )
}
