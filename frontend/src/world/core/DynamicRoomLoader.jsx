import { useState, useEffect, Suspense, lazy } from 'react';
import { Text, Sphere } from '@react-three/drei';
import { getRooms, getWorldState } from '../../api/getRooms';

// Componente di fallback per il caricamento
function RoomLoadingFallback({ position = [0, 0, 0] }) {
  return (
    <group position={position}>
      <Sphere args={[0.5]}>
        <meshStandardMaterial 
          color="#444444"
          emissive="#222222"
          emissiveIntensity={0.3}
          transparent={true}
          opacity={0.6}
        />
      </Sphere>
      <Text
        position={[0, 1, 0]}
        fontSize={0.3}
        color="#888888"
        anchorX="center"
        anchorY="middle"
      >
        Caricamento stanza...
      </Text>
    </group>
  );
}

// Componente per stanza non trovata
function RoomNotFound({ roomId, position = [0, 0, 0] }) {
  return (
    <group position={position}>
      <Sphere args={[1]}>
        <meshStandardMaterial 
          color="#ff4444"
          emissive="#aa2222"
          emissiveIntensity={0.4}
          transparent={true}
          opacity={0.7}
          wireframe={true}
        />
      </Sphere>
      <Text
        position={[0, 1.5, 0]}
        fontSize={0.4}
        color="#ff4444"
        anchorX="center"
        anchorY="middle"
      >
        Stanza {roomId} non trovata
      </Text>
    </group>
  );
}

export default function DynamicRoomLoader() {
  const [rooms, setRooms] = useState([]);
  const [worldState, setWorldState] = useState({ mood: 'contemplativo', is_alive: false });
  const [loadedComponents, setLoadedComponents] = useState(new Map());
  const [lastUpdate, setLastUpdate] = useState(Date.now());

  // Carica i dati dal backend
  useEffect(() => {
    const loadData = async () => {
      try {
        const [roomsData, stateData] = await Promise.all([
          getRooms(),
          getWorldState()
        ]);
        
        setRooms(roomsData);
        setWorldState(stateData);
        setLastUpdate(Date.now());
      } catch (error) {
        console.error('Errore nel caricamento dati mondo:', error);
      }
    };

    loadData();
    
    // Aggiorna ogni 5 secondi
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  // Carica dinamicamente i componenti delle stanze
  useEffect(() => {
    const loadRoomComponents = async () => {
      const newComponents = new Map(loadedComponents);
      
      for (const room of rooms) {
        const componentName = room.component || `${room.id}Room.jsx`;
        const roomKey = room.id;
        
        if (!newComponents.has(roomKey)) {
          try {
            // Prova a caricare dalla cartella rooms
            const Component = lazy(() => 
              import(`../rooms/${componentName.replace('.jsx', '')}.jsx`)
                .catch(() => 
                  // Fallback su stanze predefinite basate sul mood
                  import(`../rooms/${getMoodRoomComponent(room.mood || worldState.mood)}.jsx`)
                    .catch(() => 
                      // Fallback finale su SognatoreRoom
                      import('../rooms/SognatoreRoom.jsx')
                    )
                )
            );
            
            newComponents.set(roomKey, Component);
          } catch (error) {
            console.error(`Errore nel caricamento stanza ${roomKey}:`, error);
            newComponents.set(roomKey, null);
          }
        }
      }
      
      setLoadedComponents(newComponents);
    };

    if (rooms.length > 0) {
      loadRoomComponents();
    }
  }, [rooms, worldState.mood]);

  // Mappa mood a componenti stanza
  const getMoodRoomComponent = (mood) => {
    const moodMap = {
      'contemplativo': 'SognatoreRoom',
      'curioso': 'CuriosoRoom',
      'creativo': 'CreativoRoom',
      'analitico': 'AnalisiRoom',
      'empatico': 'EmpaticoRoom',
      'filosofico': 'SognatoreRoom',
      'introspettivo': 'SognatoreRoom'
    };
    
    return moodMap[mood] || 'SognatoreRoom';
  };

  // Posiziona le stanze in base al numero
  const getRoomPosition = (index, total) => {
    if (total === 1) return [0, 0, 0];
    
    const angle = (index / total) * Math.PI * 2;
    const radius = Math.max(15, total * 3);
    
    return [
      Math.cos(angle) * radius,
      0,
      Math.sin(angle) * radius
    ];
  };

  return (
    <group>
      {/* Stanza principale basata sul mood corrente */}
      {worldState.is_alive && (
        <Suspense fallback={<RoomLoadingFallback position={[0, 0, 0]} />}>
          {(() => {
            const MoodComponent = loadedComponents.get('main_mood_room');
            if (!MoodComponent) {
              // Carica dinamicamente la stanza del mood corrente
              const CurrentMoodRoom = lazy(() => 
                import(`../rooms/${getMoodRoomComponent(worldState.mood)}.jsx`)
                  .catch(() => import('../rooms/SognatoreRoom.jsx'))
              );
              
              setLoadedComponents(prev => new Map(prev).set('main_mood_room', CurrentMoodRoom));
              return <RoomLoadingFallback position={[0, 0, 0]} />;
            }
            
            return <MoodComponent />;
          })()}
        </Suspense>
      )}

      {/* Stanze dinamiche dal backend */}
      {rooms.map((room, index) => {
        const position = getRoomPosition(index, rooms.length);
        const Component = loadedComponents.get(room.id);
        
        if (!Component) {
          return <RoomLoadingFallback key={room.id} position={position} />;
        }
        
        if (Component === null) {
          return <RoomNotFound key={room.id} roomId={room.id} position={position} />;
        }
        
        return (
          <Suspense key={room.id} fallback={<RoomLoadingFallback position={position} />}>
            <group position={position}>
              <Component />
              
              {/* Etichetta della stanza */}
              <Text
                position={[0, 15, 0]}
                fontSize={0.8}
                color="#ffffff"
                anchorX="center"
                anchorY="middle"
                font="/fonts/CourierPrime-Regular.ttf"
              >
                {room.name || room.id}
              </Text>
              
              {/* Descrizione */}
              {room.description && (
                <Text
                  position={[0, 13, 0]}
                  fontSize={0.4}
                  color="#cccccc"
                  anchorX="center"
                  anchorY="middle"
                  font="/fonts/CourierPrime-Regular.ttf"
                  maxWidth={20}
                >
                  {room.description}
                </Text>
              )}
            </group>
          </Suspense>
        );
      })}

      {/* Indicatore di stato del mondo */}
      <Text
        position={[0, 20, 0]}
        fontSize={1.2}
        color={worldState.is_alive ? "#00ff41" : "#ff4444"}
        anchorX="center"
        anchorY="middle"
        font="/fonts/CourierPrime-Regular.ttf"
      >
        🌍 Mondo di Aether | {worldState.is_alive ? 'ATTIVO' : 'DORMIENTE'}
      </Text>
      
      <Text
        position={[0, 18, 0]}
        fontSize={0.6}
        color="#888888"
        anchorX="center"
        anchorY="middle"
        font="/fonts/CourierPrime-Regular.ttf"
      >
        Mood: {worldState.mood} | Stanze: {rooms.length}
      </Text>

      {/* Particelle ambientali che cambiano con il mood */}
      {worldState.is_alive && Array.from({ length: 50 }).map((_, i) => (
        <Sphere
          key={`particle-${i}`}
          args={[0.02]}
          position={[
            (Math.random() - 0.5) * 100,
            Math.random() * 30,
            (Math.random() - 0.5) * 100
          ]}
        >
          <meshBasicMaterial 
            color={getMoodColor(worldState.mood)}
            emissive={getMoodColor(worldState.mood)}
            emissiveIntensity={Math.random() * 0.5 + 0.3}
          />
        </Sphere>
      ))}
    </group>
  );
}

// Funzione helper per colori mood
function getMoodColor(mood) {
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
} 