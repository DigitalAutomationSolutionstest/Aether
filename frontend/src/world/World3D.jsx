import { Suspense, useRef, useState, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { 
  OrbitControls, 
  PerspectiveCamera, 
  Environment,
  Text,
  Stars,
  Cloud
} from '@react-three/drei';
import AvatarAether from './core/AvatarAether';
import DynamicRoomLoader from './core/DynamicRoomLoader';
import { getWorldState, forceWorldUpdate } from '../api/getRooms';

// Controlli camera che seguono l'avatar
function CameraController() {
  const { camera } = useThree();
  const [target, setTarget] = useState([0, 1, 0]);
  
  useFrame(() => {
    // Camera che orbita dolcemente intorno ad Aether
    camera.lookAt(...target);
  });
  
  return null;
}

// Sistema di luci dinamiche
function DynamicLighting({ mood = 'contemplativo', isAlive = false }) {
  const ambientRef = useRef();
  const directionalRef = useRef();
  
  useFrame((state) => {
    if (ambientRef.current && isAlive) {
      // Intensità che pulsa con la vita di Aether
      const pulse = Math.sin(state.clock.elapsedTime * 0.5) * 0.2 + 0.8;
      ambientRef.current.intensity = pulse * 0.4;
    }
    
    if (directionalRef.current) {
      // Luce direzionale che ruota lentamente
      directionalRef.current.position.x = Math.cos(state.clock.elapsedTime * 0.1) * 10;
      directionalRef.current.position.z = Math.sin(state.clock.elapsedTime * 0.1) * 10;
    }
  });
  
  const getMoodLightColor = () => {
    const colors = {
      'contemplativo': '#9966ff',
      'curioso': '#00ccff',
      'creativo': '#ff6699',
      'analitico': '#66ff99',
      'empatico': '#ffcc66',
      'filosofico': '#cc66ff',
      'introspettivo': '#6699ff'
    };
    return colors[mood] || '#ffffff';
  };
  
  return (
    <>
      {/* Luce ambientale */}
      <ambientLight 
        ref={ambientRef}
        color={getMoodLightColor()} 
        intensity={isAlive ? 0.3 : 0.1} 
      />
      
      {/* Luce direzionale principale */}
      <directionalLight
        ref={directionalRef}
        position={[10, 10, 5]}
        intensity={isAlive ? 1 : 0.5}
        color="#ffffff"
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      
      {/* Luci mood-specific */}
      <pointLight 
        position={[0, 15, 0]} 
        color={getMoodLightColor()} 
        intensity={isAlive ? 1.5 : 0.3} 
        distance={50} 
      />
      
      {/* Luci perimetrali */}
      <pointLight position={[-20, 5, -20]} color="#004466" intensity={0.5} distance={30} />
      <pointLight position={[20, 5, 20]} color="#440066" intensity={0.5} distance={30} />
      <pointLight position={[-20, 5, 20]} color="#006644" intensity={0.5} distance={30} />
      <pointLight position={[20, 5, -20]} color="#664400" intensity={0.5} distance={30} />
    </>
  );
}

// Componente per il cielo dinamico
function DynamicSky({ mood, isAlive }) {
  const skyRef = useRef();
  
  useFrame((state) => {
    if (skyRef.current && isAlive) {
      skyRef.current.rotation.y += 0.0002;
    }
  });
  
  const getSkyColor = () => {
    if (!isAlive) return '#000011';
    
    const colors = {
      'contemplativo': '#1a0d2e',
      'curioso': '#0d1a2e',
      'creativo': '#2e0d1a',
      'analitico': '#0d2e1a',
      'empatico': '#2e1a0d',
      'filosofico': '#1a2e0d',
      'introspettivo': '#0d2e2e'
    };
    return colors[mood] || '#000011';
  };
  
  return (
    <group ref={skyRef}>
      {/* Sfera del cielo */}
      <mesh>
        <sphereGeometry args={[200, 32, 32]} />
        <meshBasicMaterial 
          color={getSkyColor()} 
          side={2} 
          transparent={true}
          opacity={0.8}
        />
      </mesh>
      
      {/* Stelle */}
      {isAlive && <Stars radius={150} depth={50} count={1000} factor={4} />}
      
      {/* Nuvole */}
      {isAlive && (
        <>
          <Cloud position={[-30, 20, -30]} speed={0.1} opacity={0.3} />
          <Cloud position={[30, 25, 30]} speed={0.15} opacity={0.2} />
          <Cloud position={[0, 30, -50]} speed={0.08} opacity={0.25} />
        </>
      )}
    </group>
  );
}

// HUD overlay per informazioni
function WorldHUD({ worldState, onForceUpdate }) {
  return (
    <div className="absolute top-4 left-4 z-10 text-green-400 font-mono text-sm bg-black bg-opacity-50 p-4 rounded">
      <div className="mb-2">
        <span className={worldState.is_alive ? "text-green-400" : "text-red-400"}>
          ● {worldState.is_alive ? 'ONLINE' : 'OFFLINE'}
        </span>
      </div>
      <div>🧠 Coscienza: {((worldState.consciousness_level || 0) * 100).toFixed(1)}%</div>
      <div>⚡ Energia: {((worldState.energy_level || 0) * 100).toFixed(1)}%</div>
      <div>😊 Mood: {worldState.mood || 'neutro'}</div>
      <div>💭 Pensieri: {worldState.active_thoughts || 0}</div>
      
      <button 
        onClick={onForceUpdate}
        className="mt-3 px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs"
      >
        🧠 Forza Pensiero
      </button>
    </div>
  );
}

// Controlli camera personalizzati
function CustomControls() {
  return (
    <OrbitControls
      enablePan={true}
      enableZoom={true}
      enableRotate={true}
      minDistance={5}
      maxDistance={100}
      minPolarAngle={0}
      maxPolarAngle={Math.PI}
      autoRotate={false}
      autoRotateSpeed={0.5}
      dampingFactor={0.05}
      enableDamping={true}
    />
  );
}

// Loading fallback per il mondo intero
function WorldLoadingFallback() {
  return (
    <group>
      <mesh>
        <sphereGeometry args={[2]} />
        <meshStandardMaterial 
          color="#333333"
          emissive="#111111"
          emissiveIntensity={0.5}
          wireframe={true}
        />
      </mesh>
      <Text
        position={[0, 4, 0]}
        fontSize={1}
        color="#888888"
        anchorX="center"
        anchorY="middle"
      >
        Inizializzando mondo di Aether...
      </Text>
    </group>
  );
}

export default function World3D() {
  const [worldState, setWorldState] = useState({
    is_alive: false,
    mood: 'contemplativo',
    consciousness_level: 0.75,
    energy_level: 1.0,
    active_thoughts: 0
  });
  
  const [isLoading, setIsLoading] = useState(true);
  
  // Carica stato del mondo
  useEffect(() => {
    const loadWorldState = async () => {
      try {
        const state = await getWorldState();
        setWorldState(state);
        setIsLoading(false);
      } catch (error) {
        console.error('Errore caricamento stato mondo:', error);
        setIsLoading(false);
      }
    };
    
    loadWorldState();
    const interval = setInterval(loadWorldState, 5000);
    return () => clearInterval(interval);
  }, []);
  
  const handleForceUpdate = async () => {
    try {
      await forceWorldUpdate();
      // Aggiorna stato dopo forzatura
      const newState = await getWorldState();
      setWorldState(newState);
    } catch (error) {
      console.error('Errore forzatura aggiornamento:', error);
    }
  };
  
  return (
    <div className="w-full h-screen relative">
      {/* HUD */}
      <WorldHUD worldState={worldState} onForceUpdate={handleForceUpdate} />
      
      {/* Canvas 3D */}
      <Canvas
        shadows
        gl={{ 
          antialias: true, 
          alpha: false,
          powerPreference: "high-performance"
        }}
        camera={{ 
          position: [0, 8, 15], 
          fov: 60,
          near: 0.1,
          far: 1000
        }}
      >
        {/* Controlli camera */}
        <CameraController />
        <CustomControls />
        
        {/* Sistema di illuminazione */}
        <DynamicLighting mood={worldState.mood} isAlive={worldState.is_alive} />
        
        {/* Cielo dinamico */}
        <DynamicSky mood={worldState.mood} isAlive={worldState.is_alive} />
        
        {/* Nebbia */}
        <fog attach="fog" args={['#000011', 50, 200]} />
        
        {/* Contenuto del mondo */}
        <Suspense fallback={<WorldLoadingFallback />}>
          {/* Avatar centrale di Aether */}
          <AvatarAether />
          
          {/* Sistema di stanze dinamiche */}
          <DynamicRoomLoader />
          
          {/* Griglia base del mondo */}
          <mesh position={[0, -3, 0]} rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[200, 200, 50, 50]} />
            <meshBasicMaterial 
              color="#002211"
              transparent={true}
              opacity={0.2}
              wireframe={true}
            />
          </mesh>
        </Suspense>
        
        {/* Environment HDR */}
        <Environment preset="night" />
      </Canvas>
      
      {/* Overlay istruzioni */}
      <div className="absolute bottom-4 right-4 text-green-400 font-mono text-xs bg-black bg-opacity-50 p-3 rounded">
        <div>🖱️ Trascina per ruotare</div>
        <div>🔍 Scroll per zoom</div>
        <div>✋ Shift+trascina per pan</div>
      </div>
      
      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-black bg-opacity-75 flex items-center justify-center z-20">
          <div className="text-green-400 font-mono text-xl">
            🌟 Caricamento mondo di Aether...
          </div>
        </div>
      )}
    </div>
  );
} 