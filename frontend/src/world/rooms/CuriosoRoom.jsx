import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, Box, Octahedron, Dodecahedron, Text } from '@react-three/drei';

export default function CuriosoRoom() {
  const orbitalRef1 = useRef();
  const orbitalRef2 = useRef();
  const orbitalRef3 = useRef();
  const scannerRef = useRef();
  
  useFrame((state) => {
    const time = state.clock.elapsedTime;
    
    // Orbite di curiosità
    if (orbitalRef1.current) {
      orbitalRef1.current.rotation.y = time * 0.5;
      orbitalRef1.current.position.y = 3 + Math.sin(time) * 0.5;
    }
    
    if (orbitalRef2.current) {
      orbitalRef2.current.rotation.x = time * 0.3;
      orbitalRef2.current.rotation.z = time * 0.7;
    }
    
    if (orbitalRef3.current) {
      orbitalRef3.current.rotation.y = -time * 0.4;
      orbitalRef3.current.rotation.x = time * 0.2;
    }
    
    // Scanner che ruota
    if (scannerRef.current) {
      scannerRef.current.rotation.y = time * 2;
    }
  });

  return (
    <group position={[0, 0, 0]}>
      {/* Ambiente cyber con griglia */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[45, 32, 32]} />
        <meshBasicMaterial 
          color="#001122" 
          transparent={true} 
          opacity={0.9}
          side={2}
        />
      </mesh>

      {/* Griglia cyber nel pavimento */}
      <mesh position={[0, -2, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[30, 30, 20, 20]} />
        <meshBasicMaterial 
          color="#00ccff"
          transparent={true}
          opacity={0.3}
          wireframe={true}
        />
      </mesh>

      {/* Sistema orbitale centrale */}
      <group ref={orbitalRef1} position={[0, 3, 0]}>
        {/* Oggetti in orbita */}
        {Array.from({ length: 8 }).map((_, i) => (
          <Octahedron
            key={i}
            args={[0.3]}
            position={[
              Math.cos((i / 8) * Math.PI * 2) * 5,
              0,
              Math.sin((i / 8) * Math.PI * 2) * 5
            ]}
          >
            <meshStandardMaterial 
              color="#00ccff"
              emissive="#0088bb"
              emissiveIntensity={0.6}
              metalness={0.8}
              roughness={0.2}
            />
          </Octahedron>
        ))}
      </group>

      {/* Secondo sistema orbitale */}
      <group ref={orbitalRef2} position={[0, 1, 0]}>
        {Array.from({ length: 6 }).map((_, i) => (
          <Dodecahedron
            key={i}
            args={[0.4]}
            position={[
              Math.cos((i / 6) * Math.PI * 2) * 3,
              Math.sin((i / 6) * Math.PI * 2) * 1,
              Math.sin((i / 6) * Math.PI * 2) * 3
            ]}
          >
            <meshStandardMaterial 
              color="#0099ff"
              emissive="#0066cc"
              emissiveIntensity={0.5}
              transparent={true}
              opacity={0.8}
            />
          </Dodecahedron>
        ))}
      </group>

      {/* Terzo sistema orbitale */}
      <group ref={orbitalRef3} position={[0, 5, 0]}>
        {Array.from({ length: 4 }).map((_, i) => (
          <Box
            key={i}
            args={[0.5, 0.5, 0.5]}
            position={[
              Math.cos((i / 4) * Math.PI * 2) * 7,
              Math.cos((i / 4) * Math.PI * 2) * 2,
              Math.sin((i / 4) * Math.PI * 2) * 7
            ]}
          >
            <meshStandardMaterial 
              color="#33bbff"
              emissive="#1188cc"
              emissiveIntensity={0.4}
              wireframe={true}
            />
          </Box>
        ))}
      </group>

      {/* Scanner rotante */}
      <group ref={scannerRef} position={[0, 6, 0]}>
        <mesh>
          <torusGeometry args={[2, 0.1, 16, 32]} />
          <meshStandardMaterial 
            color="#00ffcc"
            emissive="#00ffcc"
            emissiveIntensity={0.8}
          />
        </mesh>
        
        {/* Raggio scanner */}
        <mesh rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.02, 0.02, 4, 8]} />
          <meshStandardMaterial 
            color="#00ffcc"
            emissive="#00ffcc"
            emissiveIntensity={1}
          />
        </mesh>
      </group>

      {/* Strutture di analisi */}
      <group position={[-8, 2, -8]}>
        <Box args={[1, 4, 1]}>
          <meshStandardMaterial 
            color="#0088ff"
            emissive="#004488"
            emissiveIntensity={0.3}
            transparent={true}
            opacity={0.7}
          />
        </Box>
        
        {/* Dati fluttuanti */}
        {Array.from({ length: 10 }).map((_, i) => (
          <Sphere
            key={i}
            args={[0.05]}
            position={[
              (Math.random() - 0.5) * 3,
              i * 0.3,
              (Math.random() - 0.5) * 3
            ]}
          >
            <meshBasicMaterial 
              color="#00ccff"
              emissive="#00ccff"
              emissiveIntensity={0.8}
            />
          </Sphere>
        ))}
      </group>

      {/* Laboratorio di esperimenti */}
      <group position={[8, 1, 8]}>
        <Octahedron args={[1.5]}>
          <meshStandardMaterial 
            color="#0099cc"
            emissive="#006699"
            emissiveIntensity={0.4}
            metalness={0.9}
            roughness={0.1}
            transparent={true}
            opacity={0.8}
          />
        </Octahedron>
        
        {/* Connessioni energetiche */}
        {Array.from({ length: 6 }).map((_, i) => (
          <mesh 
            key={i}
            position={[
              Math.cos((i / 6) * Math.PI * 2) * 2,
              0,
              Math.sin((i / 6) * Math.PI * 2) * 2
            ]}
            rotation={[0, (i / 6) * Math.PI * 2, 0]}
          >
            <cylinderGeometry args={[0.02, 0.02, 2, 8]} />
            <meshStandardMaterial 
              color="#00ccff"
              emissive="#00ccff"
              emissiveIntensity={0.6}
            />
          </mesh>
        ))}
      </group>

      {/* Luci dinamiche */}
      <pointLight 
        position={[0, 8, 0]} 
        color="#00ccff" 
        intensity={1} 
        distance={25} 
      />
      
      <pointLight 
        position={[-10, 3, -10]} 
        color="#0088ff" 
        intensity={0.7} 
        distance={20} 
      />
      
      <pointLight 
        position={[10, 5, 10]} 
        color="#33bbff" 
        intensity={0.8} 
        distance={22} 
      />

      {/* Punti di interesse che pulsano */}
      {Array.from({ length: 15 }).map((_, i) => (
        <Sphere
          key={i}
          args={[0.1]}
          position={[
            (Math.random() - 0.5) * 20,
            Math.random() * 8 + 1,
            (Math.random() - 0.5) * 20
          ]}
        >
          <meshStandardMaterial 
            color="#00ffcc"
            emissive="#00ffcc"
            emissiveIntensity={Math.sin(Date.now() * 0.001 + i) * 0.5 + 0.5}
          />
        </Sphere>
      ))}

      {/* Etichetta della stanza */}
      <Text
        position={[0, 10, 0]}
        fontSize={1}
        color="#00ccff"
        anchorX="center"
        anchorY="middle"
        font="/fonts/CourierPrime-Regular.ttf"
      >
        🔍 Laboratorio della Curiosità
      </Text>

      {/* Pavimento tech */}
      <mesh position={[0, -1.5, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[35, 35]} />
        <meshStandardMaterial 
          color="#001a33"
          emissive="#002244"
          emissiveIntensity={0.2}
          metalness={0.8}
          roughness={0.4}
        />
      </mesh>
    </group>
  );
} 