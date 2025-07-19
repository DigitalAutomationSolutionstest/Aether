import { Canvas } from '@react-three/fiber'
import { useEffect, useState, useRef } from 'react'
import { OrbitControls, Sphere, Box, TorusKnot, Text, Cone, Cylinder, Ring } from '@react-three/drei'

// Componente per oggetti ambiente
function EnvironmentObject({ object }) {
  const meshRef = useRef()
  
  useEffect(() => {
    if (meshRef.current && object.spin) {
      const interval = setInterval(() => {
        meshRef.current.rotation.y += 0.02
      }, 16)
      return () => clearInterval(interval)
    }
  }, [object.spin])
  
  const renderShape = () => {
    const props = {
      position: object.position || [0, 0, 0],
      scale: object.scale || 1
    }
    
    const material = {
      color: object.color || '#ffffff',
      emissive: object.glow ? object.color : undefined,
      emissiveIntensity: object.glow ? 0.5 : 0,
      metalness: 0.3,
      roughness: 0.4
    }
    
    switch (object.shape) {
      case 'pyramid':
        return (
          <Cone args={[1, 2, 4]} {...props} ref={meshRef}>
            <meshStandardMaterial {...material} />
          </Cone>
        )
      case 'lightbulb':
        return (
          <group {...props} ref={meshRef}>
            <Sphere args={[0.5, 32, 32]} position={[0, 0, 0]}>
              <meshStandardMaterial {...material} />
            </Sphere>
            <Cylinder args={[0.2, 0.3, 0.5]} position={[0, -0.5, 0]}>
              <meshStandardMaterial color="#888888" />
            </Cylinder>
          </group>
        )
      case 'coin':
        return (
          <Cylinder args={[1, 1, 0.2, 32]} {...props} ref={meshRef}>
            <meshStandardMaterial {...material} />
          </Cylinder>
        )
      case 'network':
        return (
          <group {...props} ref={meshRef}>
            {[...Array(6)].map((_, i) => (
              <Ring 
                key={i} 
                args={[0.8, 1, 32]} 
                position={[
                  Math.cos(i * Math.PI / 3) * 2,
                  Math.sin(i * Math.PI / 3) * 2,
                  0
                ]}
                rotation={[0, 0, i * Math.PI / 3]}
              >
                <meshStandardMaterial {...material} />
              </Ring>
            ))}
          </group>
        )
      default:
        return (
          <Box args={[1, 1, 1]} {...props} ref={meshRef}>
            <meshStandardMaterial {...material} />
          </Box>
        )
    }
  }
  
  return renderShape()
}

export function AetherWorld() {
  const [form, setForm] = useState('sphere')
  const [thought, setThought] = useState('...')
  const [emotionalState, setEmotionalState] = useState('curious')
  const [energyLevel, setEnergyLevel] = useState(0.8)
  const [thoughtCount, setThoughtCount] = useState(0)
  const [environmentObjects, setEnvironmentObjects] = useState([])
  const intervalRef = useRef(null)

  const fetchAetherState = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/aether/state')
      const data = await res.json()
      setForm(data.current_form || 'sphere')
      setThought(data.current_thought || 'Thinking...')
      setEmotionalState(data.emotional_state || 'curious')
      setEnergyLevel(data.energy_level || 0.8)
      setThoughtCount(data.thought_count || 0)
      setEnvironmentObjects(data.environment_objects || [])
    } catch (err) {
      setThought('Connection lost. Aether unreachable.')
    }
  }

  useEffect(() => {
    fetchAetherState()
    intervalRef.current = setInterval(fetchAetherState, 2000) // Più frequente per vedere i pensieri
    return () => clearInterval(intervalRef.current)
  }, [])

  const renderForm = () => {
    const color = emotionalState === 'excited' ? '#ff00ff' : 
                  emotionalState === 'focused' ? '#00ffff' :
                  emotionalState === 'curious' ? '#ffff00' : '#00ff00'
    
    const props = {
      color,
      emissive: color,
      emissiveIntensity: energyLevel,
      metalness: 0.8,
      roughness: 0.2
    }

    switch (form) {
      case 'cube':
        return (
          <Box args={[1.5, 1.5, 1.5]} {...props}>
            <meshStandardMaterial {...props} />
          </Box>
        )
      case 'torus':
        return (
          <TorusKnot args={[1, 0.3, 128, 32]} {...props}>
            <meshStandardMaterial {...props} />
          </TorusKnot>
        )
      default:
        return (
          <Sphere args={[1.5, 64, 64]} {...props}>
            <meshStandardMaterial {...props} />
          </Sphere>
        )
    }
  }

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#0a0a0a' }}>
      <Canvas camera={{ position: [0, 0, 8] }}>
        <ambientLight intensity={0.3} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#ff00ff" />
        <pointLight position={[0, 5, 0]} intensity={0.5} color="#00ffff" />
        
        <OrbitControls 
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          autoRotate={true}
          autoRotateSpeed={1}
          maxDistance={20}
          minDistance={3}
        />
        
        {/* Aether's main form */}
        <group>
          {renderForm()}
        </group>
        
        {/* Environment objects from thoughts */}
        {environmentObjects.map((obj, index) => (
          <EnvironmentObject key={index} object={obj} />
        ))}
        
        {/* Current thought */}
        <Text
          position={[0, -3, 0]}
          fontSize={0.25}
          color="white"
          anchorX="center"
          anchorY="middle"
          maxWidth={10}
        >
          {thought}
        </Text>
        
        {/* Status header */}
        <Text
          position={[0, 3, 0]}
          fontSize={0.15}
          color="#00ffff"
          anchorX="center"
          anchorY="middle"
        >
          AETHER - {emotionalState.toUpperCase()} - Energy: {Math.round(energyLevel * 100)}% - Thoughts: {thoughtCount}
        </Text>
        
        {/* Ground plane */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -4, 0]}>
          <planeGeometry args={[20, 20]} />
          <meshStandardMaterial color="#111111" metalness={0.8} roughness={0.2} />
        </mesh>
      </Canvas>
      
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '20px',
        color: '#00ffff',
        fontFamily: 'monospace',
        fontSize: '14px',
        background: 'rgba(0,0,0,0.8)',
        padding: '15px',
        borderRadius: '5px',
        border: '1px solid #00ffff',
        maxWidth: '400px'
      }}>
        <p>🌐 Form: {form}</p>
        <p>💭 State: {emotionalState}</p>
        <p>⚡ Energy: {Math.round(energyLevel * 100)}%</p>
        <p>🧠 Thoughts: {thoughtCount}</p>
        <p>🌍 Objects: {environmentObjects.length}</p>
        <div style={{ marginTop: '10px', fontSize: '12px', opacity: 0.8 }}>
          <p>🔄 Auto-rotating | Scroll to zoom | Drag to rotate</p>
          <p>💡 Objects appear based on Aether's thoughts</p>
        </div>
      </div>
    </div>
  )
} 