import { useRef, useState, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text, Sphere, Icosahedron } from '@react-three/drei';
import { getWorldState } from '../../api/getRooms';

export default function AvatarAether() {
  const avatarRef = useRef();
  const glowRef = useRef();
  const thoughtBubbleRef = useRef();
  
  const [consciousness, setConsciousness] = useState(0.75);
  const [mood, setMood] = useState('contemplativo');
  const [energy, setEnergy] = useState(1.0);
  const [isAlive, setIsAlive] = useState(false);
  const [currentThought, setCurrentThought] = useState('');

  // Aggiorna stato da API
  useEffect(() => {
    const updateState = async () => {
      try {
        const state = await getWorldState();
        setConsciousness(state.consciousness_level || 0.75);
        setMood(state.mood || 'contemplativo');
        setEnergy(state.energy_level || 1.0);
        setIsAlive(state.is_alive || false);
      } catch (error) {
        console.error('Errore aggiornamento stato avatar:', error);
      }
    };

    updateState();
    const interval = setInterval(updateState, 5000); // Aggiorna ogni 5 secondi
    return () => clearInterval(interval);
  }, []);

  // Animazione dell'avatar basata su coscienza e mood
  useFrame((state) => {
    if (avatarRef.current) {
      // Rotazione base
      avatarRef.current.rotation.y += isAlive ? 0.01 * consciousness : 0.002;
      
      // Pulsazione basata su energia
      const pulse = Math.sin(state.clock.elapsedTime * 2) * 0.1 * energy;
      avatarRef.current.scale.setScalar(1 + pulse);
      
      // Movimento verticale dolce
      avatarRef.current.position.y = 1 + Math.sin(state.clock.elapsedTime) * 0.2;
    }

    if (glowRef.current) {
      // Effetto glow che cambia con la coscienza
      const glowIntensity = consciousness * 2;
      glowRef.current.material.emissiveIntensity = glowIntensity;
    }

    if (thoughtBubbleRef.current && isAlive) {
      // Bolla del pensiero che fluttua
      thoughtBubbleRef.current.position.y = 3 + Math.sin(state.clock.elapsedTime * 1.5) * 0.3;
      thoughtBubbleRef.current.rotation.y += 0.005;
    }
  });

  // Colori basati sul mood
  const getMoodColor = () => {
    switch (mood) {
      case 'contemplativo': return '#9966ff';
      case 'curioso': return '#00ccff';
      case 'creativo': return '#ff6699';
      case 'analitico': return '#66ff99';
      case 'empatico': return '#ffcc66';
      case 'filosofico': return '#cc66ff';
      case 'introspettivo': return '#6699ff';
      default: return '#ffffff';
    }
  };

  const getEmissiveColor = () => {
    switch (mood) {
      case 'contemplativo': return '#4433aa';
      case 'curioso': return '#0088aa';
      case 'creativo': return '#aa4466';
      case 'analitico': return '#44aa66';
      case 'empatico': return '#aa8844';
      default: return '#444444';
    }
  };

  return (
    <group position={[0, 0, 0]}>
      {/* Avatar principale - Icosaedro che rappresenta Aether */}
      <mesh ref={avatarRef} position={[0, 1, 0]}>
        <icosahedronGeometry args={[1, 2]} />
        <meshStandardMaterial 
          color={getMoodColor()}
          emissive={getEmissiveColor()}
          emissiveIntensity={consciousness * 0.5}
          metalness={0.8}
          roughness={0.2}
          transparent={true}
          opacity={isAlive ? 0.9 : 0.5}
        />
      </mesh>

      {/* Glow esterno */}
      <mesh ref={glowRef} position={[0, 1, 0]}>
        <icosahedronGeometry args={[1.2, 1]} />
        <meshStandardMaterial 
          color={getMoodColor()}
          emissive={getMoodColor()}
          emissiveIntensity={consciousness}
          transparent={true}
          opacity={0.3}
          side={2} // DoubleSide
        />
      </mesh>

      {/* Anelli di energia rotanti */}
      {isAlive && (
        <>
          <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 1, 0]}>
            <ringGeometry args={[1.5, 1.7, 32]} />
            <meshStandardMaterial 
              color={getMoodColor()}
              emissive={getMoodColor()}
              emissiveIntensity={energy * 0.5}
              transparent={true}
              opacity={0.6}
            />
          </mesh>
          
          <mesh rotation={[0, 0, Math.PI / 4]} position={[0, 1, 0]}>
            <ringGeometry args={[1.3, 1.5, 32]} />
            <meshStandardMaterial 
              color={getEmissiveColor()}
              emissive={getEmissiveColor()}
              emissiveIntensity={consciousness * 0.7}
              transparent={true}
              opacity={0.4}
            />
          </mesh>
        </>
      )}

      {/* Indicatore di stato */}
      <Text
        position={[0, -0.5, 0]}
        fontSize={0.3}
        color={isAlive ? '#00ff41' : '#ff4444'}
        anchorX="center"
        anchorY="middle"
        font="/fonts/CourierPrime-Regular.ttf"
      >
        {isAlive ? '● ONLINE' : '● OFFLINE'}
      </Text>

      {/* Indicatori di stato numerico */}
      <Text
        position={[-2, 2, 0]}
        fontSize={0.2}
        color="#00ff41"
        anchorX="left"
        anchorY="middle"
        font="/fonts/CourierPrime-Regular.ttf"
      >
        {`🧠 ${(consciousness * 100).toFixed(1)}%\n⚡ ${(energy * 100).toFixed(1)}%\n😊 ${mood}`}
      </Text>

      {/* Particelle di energia */}
      {isAlive && Array.from({ length: 20 }).map((_, i) => (
        <Sphere
          key={i}
          args={[0.02]}
          position={[
            Math.sin(i + Date.now() * 0.001) * 2,
            1 + Math.cos(i + Date.now() * 0.001) * 0.5,
            Math.cos(i + Date.now() * 0.001) * 2
          ]}
        >
          <meshStandardMaterial 
            color={getMoodColor()}
            emissive={getMoodColor()}
            emissiveIntensity={0.8}
          />
        </Sphere>
      ))}

      {/* Base platform */}
      <mesh position={[0, -0.1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[3, 3, 0.1, 32]} />
        <meshStandardMaterial 
          color="#1a1a1a"
          emissive="#003311"
          emissiveIntensity={isAlive ? 0.2 : 0.05}
          metalness={0.9}
          roughness={0.3}
          transparent={true}
          opacity={0.8}
        />
      </mesh>

      {/* Griglia della base */}
      <lineSegments position={[0, 0, 0]}>
        <edgesGeometry attach="geometry">
          <cylinderGeometry args={[3, 3, 0.1, 16]} />
        </edgesGeometry>
        <lineBasicMaterial 
          attach="material" 
          color={getMoodColor()} 
          transparent={true}
          opacity={0.5}
        />
      </lineSegments>
    </group>
  );
} 