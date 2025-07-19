import { useEffect, useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Stars, Cloud, Environment } from '@react-three/drei';
import { useSpring, animated } from '@react-spring/three';
import * as THREE from 'three';

// Avatar principale di Aether
function AetherAvatar({ mood, energy }) {
  const mesh = useRef();
  const innerMesh = useRef();
  
  // Colori basati sull'umore
  const moodColors = {
    curious: '#87CEEB',     // skyblue
    focused: '#FFD700',     // gold
    excited: '#FF00FF',     // magenta
    creative: '#9370DB',    // medium purple
    analytical: '#00CED1',  // dark turquoise
    determined: '#FF6347'   // tomato
  };
  
  const color = moodColors[mood] || '#00FFFF';
  
  // Animazione spring per transizioni fluide
  const { scale, emissiveIntensity } = useSpring({
    scale: energy > 0.8 ? 1.2 : energy > 0.5 ? 1.0 : 0.8,
    emissiveIntensity: energy,
    config: { mass: 1, tension: 280, friction: 60 }
  });
  
  // Rotazione e pulsazione
  useFrame((state) => {
    if (mesh.current) {
      mesh.current.rotation.y += 0.002 * energy;
      mesh.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
      
      // Pulsazione basata su energia
      const pulse = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.05 * energy;
      mesh.current.scale.setScalar(pulse);
    }
    
    if (innerMesh.current) {
      innerMesh.current.rotation.y -= 0.003;
      innerMesh.current.rotation.z += 0.001;
    }
  });
  
  return (
    <group position={[0, 1, 0]}>
      {/* Core esterno */}
      <animated.mesh ref={mesh} scale={scale}>
        <icosahedronGeometry args={[1, 2]} />
        <meshStandardMaterial 
          color={color} 
          wireframe 
          emissive={color}
          emissiveIntensity={emissiveIntensity}
        />
      </animated.mesh>
      
      {/* Core interno */}
      <mesh ref={innerMesh} scale={0.6}>
        <octahedronGeometry args={[1, 0]} />
        <meshStandardMaterial 
          color={color}
          emissive={color}
          emissiveIntensity={energy * 2}
          transparent
          opacity={0.8}
        />
      </mesh>
      
      {/* Aura energetica */}
      <mesh scale={1.5}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial
          color={color}
          transparent
          opacity={0.1 * energy}
          emissive={color}
          emissiveIntensity={0.5}
        />
      </mesh>
      
      {/* Nome floating */}
      <Text
        position={[0, 2, 0]}
        fontSize={0.3}
        color={color}
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor="#000000"
      >
        AETHER
      </Text>
    </group>
  );
}

// Ambiente dinamico che reagisce all'umore
function DynamicEnvironment({ mood, thoughtCount }) {
  const [envColor, setEnvColor] = useState('#000000');
  const [fogColor, setFogColor] = useState('#000000');
  
  useEffect(() => {
    const envColors = {
      curious: '#001122',      // deep blue
      focused: '#111111',      // dark gray
      creative: '#1a0033',     // deep purple
      excited: '#220011',      // deep red
      analytical: '#002222',   // deep cyan
      determined: '#221100'    // deep orange
    };
    
    const newColor = envColors[mood] || '#000000';
    setEnvColor(newColor);
    setFogColor(newColor);
  }, [mood]);
  
  return (
    <>
      <color attach="background" args={[envColor]} />
      <fog attach="fog" args={[fogColor, 5, 20]} />
      
      {/* Stelle animate */}
      <Stars 
        radius={100} 
        depth={50} 
        count={5000} 
        factor={4} 
        saturation={0} 
        fade 
        speed={1}
      />
      
      {/* Nuvole per atmosfera */}
      {mood === 'creative' && (
        <Cloud
          position={[0, 5, -10]}
          speed={0.2}
          opacity={0.3}
          color="#9370DB"
        />
      )}
      
      {/* Particelle di pensiero */}
      <ThoughtParticles count={thoughtCount} mood={mood} />
    </>
  );
}

// Particelle che rappresentano i pensieri
function ThoughtParticles({ count, mood }) {
  const particles = useRef();
  const particleCount = Math.min(count * 10, 1000);
  
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);
  
  // Genera posizioni casuali
  for (let i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 10;
    positions[i * 3 + 1] = Math.random() * 5;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
    
    // Colori basati sull'umore
    const color = new THREE.Color(
      mood === 'excited' ? '#FF00FF' :
      mood === 'focused' ? '#FFD700' :
      mood === 'creative' ? '#9370DB' :
      '#00FFFF'
    );
    
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;
  }
  
  useFrame((state) => {
    if (particles.current) {
      particles.current.rotation.y += 0.0005;
      
      // Movimento ondulatorio
      const positions = particles.current.geometry.attributes.position.array;
      for (let i = 0; i < particleCount; i++) {
        const y = positions[i * 3 + 1];
        positions[i * 3 + 1] = y + Math.sin(state.clock.elapsedTime + i) * 0.001;
      }
      particles.current.geometry.attributes.position.needsUpdate = true;
    }
  });
  
  return (
    <points ref={particles}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={particleCount}
          array={positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-color"
          count={particleCount}
          array={colors}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial 
        size={0.05} 
        vertexColors 
        transparent 
        opacity={0.8}
        sizeAttenuation
      />
    </points>
  );
}

// Pannello pensieri con stile cyberpunk
function AetherThoughts({ thoughts, stats }) {
  return (
    <div className="absolute top-4 left-4 bg-black/90 text-white p-4 rounded-xl w-96 font-mono text-sm max-h-[50vh] overflow-hidden border border-cyan-500/50 shadow-2xl">
      {/* Header */}
      <div className="font-bold text-lg mb-3 text-cyan-400 flex items-center justify-between">
        <span>🧠 Aether Consciousness Stream</span>
        <span className="text-xs text-gray-400">v2.0</span>
      </div>
      
      {/* Stats */}
      <div className="grid grid-cols-3 gap-2 mb-3 text-xs">
        <div className="bg-gray-900/50 p-2 rounded border border-gray-700">
          <div className="text-gray-400">Thoughts</div>
          <div className="text-cyan-300 font-bold">{stats.thoughtCount || 0}</div>
        </div>
        <div className="bg-gray-900/50 p-2 rounded border border-gray-700">
          <div className="text-gray-400">Energy</div>
          <div className="text-green-400 font-bold">{Math.round((stats.energy || 0.8) * 100)}%</div>
        </div>
        <div className="bg-gray-900/50 p-2 rounded border border-gray-700">
          <div className="text-gray-400">Mood</div>
          <div className="text-purple-400 font-bold capitalize">{stats.mood || 'curious'}</div>
        </div>
      </div>
      
      {/* Thoughts stream */}
      <div className="overflow-y-auto max-h-[30vh] space-y-2 scrollbar-thin scrollbar-thumb-cyan-600 scrollbar-track-gray-900">
        {thoughts.length === 0 ? (
          <div className="text-gray-500 italic">Initializing thought stream...</div>
        ) : (
          thoughts.map((thought, i) => (
            <div 
              key={i} 
              className={`
                p-2 rounded bg-gradient-to-r 
                ${i === 0 ? 'from-cyan-900/50 to-purple-900/50 border-l-4 border-cyan-400' : 'from-gray-900/30 to-gray-800/30'}
                transition-all duration-500
              `}
            >
              <div className="flex items-start gap-2">
                <span className="text-cyan-400">{i === 0 ? '💭' : '🧠'}</span>
                <div className="flex-1">
                  <div className="text-gray-300">{thought.text || thought}</div>
                  {thought.timestamp && (
                    <div className="text-xs text-gray-500 mt-1">
                      {new Date(thought.timestamp).toLocaleTimeString()}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
      
      {/* Status indicator */}
      <div className="mt-3 flex items-center gap-2 text-xs">
        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
        <span className="text-gray-400">Live connection active</span>
      </div>
    </div>
  );
}

// Info panel con controlli
function ControlPanel({ onMoodChange, onEnergyChange, currentMood, currentEnergy }) {
  const moods = ['curious', 'focused', 'excited', 'creative', 'analytical', 'determined'];
  
  return (
    <div className="absolute bottom-4 right-4 bg-black/90 text-white p-4 rounded-xl font-mono text-sm border border-cyan-500/50 shadow-2xl">
      <div className="font-bold text-cyan-400 mb-3">🎮 Aether Controls</div>
      
      {/* Mood selector */}
      <div className="mb-3">
        <div className="text-xs text-gray-400 mb-1">Mood State</div>
        <select 
          value={currentMood} 
          onChange={(e) => onMoodChange(e.target.value)}
          className="bg-gray-900 border border-gray-700 rounded px-2 py-1 text-cyan-300 w-full"
        >
          {moods.map(mood => (
            <option key={mood} value={mood}>{mood.charAt(0).toUpperCase() + mood.slice(1)}</option>
          ))}
        </select>
      </div>
      
      {/* Energy slider */}
      <div>
        <div className="text-xs text-gray-400 mb-1">Energy Level: {Math.round(currentEnergy * 100)}%</div>
        <input 
          type="range" 
          min="0" 
          max="100" 
          value={currentEnergy * 100}
          onChange={(e) => onEnergyChange(e.target.value / 100)}
          className="w-full accent-cyan-400"
        />
      </div>
      
      {/* Instructions */}
      <div className="mt-3 text-xs text-gray-500">
        <div>• Drag to rotate view</div>
        <div>• Scroll to zoom</div>
        <div>• Right-click to pan</div>
      </div>
    </div>
  );
}

// Componente principale
export default function Aether3DWorld() {
  const [thoughts, setThoughts] = useState([]);
  const [mood, setMood] = useState('curious');
  const [energy, setEnergy] = useState(0.8);
  const [stats, setStats] = useState({});

  useEffect(() => {
    const fetchThoughts = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/aether/thoughts');
        const data = await res.json();
        
        // Aggiorna pensieri (mantieni solo gli ultimi 10)
        if (data.last_thoughts) {
          setThoughts(data.last_thoughts.slice(0, 10));
        }
        
        // Aggiorna mood e stats
        if (data.mood) setMood(data.mood);
        if (data.energy !== undefined) setEnergy(data.energy);
        
        setStats({
          thoughtCount: data.thought_count || 0,
          energy: data.energy || energy,
          mood: data.mood || mood
        });
      } catch (error) {
        console.error('Failed to fetch thoughts:', error);
      }
    };
    
    // Fetch iniziale
    fetchThoughts();
    
    // Update ogni 3 secondi
    const interval = setInterval(fetchThoughts, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative w-full h-screen bg-black overflow-hidden">
      <Canvas 
        camera={{ position: [0, 2, 5], fov: 60 }} 
        shadows
        gl={{ antialias: true, alpha: false }}
      >
        <ambientLight intensity={0.2} />
        <directionalLight 
          position={[5, 5, 5]} 
          intensity={1} 
          castShadow 
          shadow-mapSize={[2048, 2048]}
        />
        <pointLight position={[-5, 5, -5]} intensity={0.5} color="#9370DB" />
        
        <AetherAvatar mood={mood} energy={energy} />
        <DynamicEnvironment mood={mood} thoughtCount={stats.thoughtCount || 0} />
        
        <OrbitControls 
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          autoRotate={true}
          autoRotateSpeed={0.5}
          maxDistance={10}
          minDistance={2}
          maxPolarAngle={Math.PI * 0.8}
        />
      </Canvas>
      
      <AetherThoughts thoughts={thoughts} stats={stats} />
      <ControlPanel 
        onMoodChange={setMood}
        onEnergyChange={setEnergy}
        currentMood={mood}
        currentEnergy={energy}
      />
      
      {/* Title overlay */}
      <div className="absolute top-4 right-4 text-white font-mono">
        <h1 className="text-2xl font-bold text-cyan-400 drop-shadow-lg">AETHER 3D</h1>
        <p className="text-xs text-gray-400">Consciousness Visualization System</p>
      </div>
    </div>
  );
} 