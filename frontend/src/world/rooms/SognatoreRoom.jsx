import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, Box, Torus, Text } from '@react-three/drei';

export default function SognatoreRoom() {
  const cloudRef1 = useRef();
  const cloudRef2 = useRef();
  const starfieldRef = useRef();
  
  useFrame((state) => {
    // Nuvole che fluttuano dolcemente
    if (cloudRef1.current) {
      cloudRef1.current.position.x = Math.sin(state.clock.elapsedTime * 0.3) * 5;
      cloudRef1.current.rotation.y += 0.001;
    }
    
    if (cloudRef2.current) {
      cloudRef2.current.position.x = Math.cos(state.clock.elapsedTime * 0.2) * 4;
      cloudRef2.current.position.z = Math.sin(state.clock.elapsedTime * 0.1) * 3;
    }
    
    // Stelle che pulsano
    if (starfieldRef.current) {
      starfieldRef.current.rotation.y += 0.0005;
    }
  });

  return (
    <group position={[0, 0, 0]}>
      {/* Sfondo stellato */}
      <mesh ref={starfieldRef}>
        <sphereGeometry args={[50, 32, 32]} />
        <meshBasicMaterial 
          color="#050515" 
          transparent={true} 
          opacity={0.8}
          side={2} // DoubleSide
        />
      </mesh>

      {/* Stelle */}
      {Array.from({ length: 100 }).map((_, i) => (
        <Sphere
          key={i}
          args={[0.02]}
          position={[
            (Math.random() - 0.5) * 80,
            (Math.random() - 0.5) * 40 + 10,
            (Math.random() - 0.5) * 80
          ]}
        >
          <meshBasicMaterial 
            color="#ffffff"
            emissive="#ffffff"
            emissiveIntensity={Math.random() * 0.5 + 0.3}
          />
        </Sphere>
      ))}

      {/* Nuvole fluttuanti */}
      <group ref={cloudRef1} position={[0, 8, -10]}>
        <Sphere args={[2, 16, 16]}>
          <meshStandardMaterial 
            color="#9966ff"
            emissive="#6644aa"
            emissiveIntensity={0.3}
            transparent={true}
            opacity={0.4}
          />
        </Sphere>
        <Sphere args={[1.5, 16, 16]} position={[2, 0, 0]}>
          <meshStandardMaterial 
            color="#aa77ff"
            emissive="#7755bb"
            emissiveIntensity={0.2}
            transparent={true}
            opacity={0.3}
          />
        </Sphere>
      </group>

      <group ref={cloudRef2} position={[5, 6, 8]}>
        <Sphere args={[1.8, 16, 16]}>
          <meshStandardMaterial 
            color="#bb88ff"
            emissive="#8866cc"
            emissiveIntensity={0.25}
            transparent={true}
            opacity={0.35}
          />
        </Sphere>
        <Sphere args={[1.2, 16, 16]} position={[-1.5, 0.5, 0]}>
          <meshStandardMaterial 
            color="#cc99ff"
            emissive="#9977dd"
            emissiveIntensity={0.2}
            transparent={true}
            opacity={0.3}
          />
        </Sphere>
      </group>

      {/* Strutture geometriche fluttuanti */}
      <Torus 
        args={[3, 0.5, 16, 32]} 
        position={[-8, 5, -5]}
        rotation={[Math.PI / 4, 0, Math.PI / 6]}
      >
        <meshStandardMaterial 
          color="#6644ff"
          emissive="#4422aa"
          emissiveIntensity={0.4}
          transparent={true}
          opacity={0.7}
          wireframe={true}
        />
      </Torus>

      <Box args={[2, 2, 2]} position={[8, 7, 5]} rotation={[0.5, 0.5, 0]}>
        <meshStandardMaterial 
          color="#8855ff"
          emissive="#5533bb"
          emissiveIntensity={0.3}
          transparent={true}
          opacity={0.6}
          wireframe={true}
        />
      </Box>

      {/* Piattaforme fluttuanti */}
      <mesh position={[-6, 3, 0]} rotation={[-0.1, 0, 0]}>
        <cylinderGeometry args={[2, 2, 0.2, 8]} />
        <meshStandardMaterial 
          color="#4433aa"
          emissive="#221166"
          emissiveIntensity={0.3}
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>

      <mesh position={[6, 4, -3]} rotation={[0.1, 0, 0.1]}>
        <cylinderGeometry args={[1.5, 1.5, 0.15, 6]} />
        <meshStandardMaterial 
          color="#5544bb"
          emissive="#3322777"
          emissiveIntensity={0.25}
          metalness={0.7}
          roughness={0.3}
        />
      </mesh>

      {/* Luci ambientali */}
      <pointLight 
        position={[0, 10, 0]} 
        color="#9966ff" 
        intensity={0.8} 
        distance={30} 
      />
      
      <pointLight 
        position={[-10, 5, -10]} 
        color="#6644aa" 
        intensity={0.5} 
        distance={20} 
      />
      
      <pointLight 
        position={[10, 8, 10]} 
        color="#aa77cc" 
        intensity={0.6} 
        distance={25} 
      />

      {/* Etichetta della stanza */}
      <Text
        position={[0, 12, 0]}
        fontSize={1}
        color="#9966ff"
        anchorX="center"
        anchorY="middle"
        font="/fonts/CourierPrime-Regular.ttf"
      >
        🌙 Stanza del Sognatore
      </Text>

      {/* Pavimento nebbioso */}
      <mesh position={[0, -1, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[40, 40]} />
        <meshStandardMaterial 
          color="#1a0d2e"
          emissive="#0f0620"
          emissiveIntensity={0.1}
          transparent={true}
          opacity={0.6}
        />
      </mesh>
    </group>
  );
} 