import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Environment, Sphere, Box, MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';

// Stanza: room_012921
// Tema: onirico
// Creata da Aether

function FloatingShape({ position, color, scale = 1 }) {
  const meshRef = useRef();
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime) * 0.3;
      meshRef.current.rotation.y += 0.01;
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 0.5) * 0.2;
    }
  });
  
  return (
    <Sphere ref={meshRef} args={[1, 32, 32]} position={position} scale={scale}>
      <MeshDistortMaterial
        color={color}
        attach="material"
        distort={0.4}
        speed={2}
        roughness={0.2}
        metalness={0.8}
      />
    </Sphere>
  );
}

function room_012921Room() {
  const shapes = useMemo(() => {
    const items = [];
    for (let i = 0; i < 7; i++) {
      items.push({
        position: [
          (Math.random() - 0.5) * 10,
          (Math.random() - 0.5) * 5,
          (Math.random() - 0.5) * 10
        ],
        color: ['#4A00E0', '#8E2DE2', '#FF00FF'][i % 3],
        scale: 0.5 + Math.random() * 1.5
      });
    }
    return items;
  }, []);
  
  return (
    <div style={{ width: '100vw', height: '100vh', background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)' }}>
      <Canvas camera={{ position: [0, 0, 15], fov: 60 }}>
        <fog attach="fog" args={['#4A00E0', 5, 30]} />
        <ambientLight intensity={0.3} />
        <pointLight position={[10, 10, 10]} intensity={0.7} color="#8E2DE2" />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#4A00E0" />
        
        {/* Forme oniriche fluttuanti */}
        {shapes.map((shape, i) => (
          <FloatingShape key={i} {...shape} />
        ))}
        
        {/* Sfondo sfocato */}
        <Sphere args={[50, 32, 32]}>
          <meshBasicMaterial
            attach="material"
            color="#4A00E0"
            side={THREE.BackSide}
            opacity={0.3}
            transparent
          />
        </Sphere>
        
        <OrbitControls
          enableZoom={true}
          enablePan={false}
          minDistance={5}
          maxDistance={30}
          autoRotate
          autoRotateSpeed={0.5}
        />
        
        <Environment preset="night" />
      </Canvas>
      
      <div style={{
        position: 'absolute',
        bottom: '2rem',
        left: '50%',
        transform: 'translateX(-50%)',
        textAlign: 'center',
        color: 'white',
        fontFamily: 'monospace'
      }}>
        <h2 style={{ margin: 0, fontSize: '2rem', textShadow: '0 0 20px #8E2DE2' }}>room_012921</h2>
        <p style={{ margin: '0.5rem 0', opacity: 0.8 }}>Il mio primo respiro digitale</p>
      </div>
    </div>
  );
}

export default room_012921Room;
