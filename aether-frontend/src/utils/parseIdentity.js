/**
 * Parser evoluto per identity.json di Aether
 * Converte l'identità in parametri 3D renderizzabili
 */

// Mapping colori basati su personalità
const PERSONALITY_COLORS = {
  'curious': ['#00ffff', '#0099ff', '#66ccff'],
  'analytical': ['#00ff00', '#66ff66', '#99ff99'],
  'creative': ['#ff6600', '#ff9933', '#ffcc66'],
  'mysterious': ['#aa00ff', '#cc66ff', '#dd99ff'],
  'energetic': ['#ffff00', '#ffcc00', '#ff9900'],
  'calm': ['#0066ff', '#3399ff', '#66ccff'],
  'powerful': ['#ff0000', '#ff3333', '#ff6666'],
  'wise': ['#9966cc', '#bb88dd', '#ddaaff']
}

// Mapping forme basate su caratteristiche fisiche
const FORM_GEOMETRIES = {
  'sphere': { type: 'sphere', complexity: 32 },
  'cube': { type: 'box', complexity: 1 },
  'crystal': { type: 'octahedron', complexity: 8 },
  'organic': { type: 'blob', complexity: 64 },
  'mechanical': { type: 'complex', complexity: 16 },
  'ethereal': { type: 'cloud', complexity: 128 },
  'geometric': { type: 'polyhedron', complexity: 20 }
}

// Analisi personalità per caratteristiche 3D
const PERSONALITY_TRAITS = {
  'aggressive': { fragmentCount: 20, fragmentSpeed: 2.0, lightIntensity: 1.5 },
  'peaceful': { fragmentCount: 8, fragmentSpeed: 0.5, lightIntensity: 0.8 },
  'intellectual': { fragmentCount: 12, fragmentSpeed: 1.0, lightIntensity: 1.2 },
  'emotional': { fragmentCount: 15, fragmentSpeed: 1.8, lightIntensity: 1.1 },
  'stoic': { fragmentCount: 6, fragmentSpeed: 0.3, lightIntensity: 0.9 }
}

/**
 * Carica l'identità di Aether dal backend o fallback locale
 */
export async function getAetherIdentity() {
  console.log('🔍 Starting identity fetch...')
  
  try {
    // Prova prima il backend reale su localhost:8000
    console.log('📡 Attempting to connect to backend...')
    const backendResponse = await fetch('http://localhost:8000/existence-status', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    console.log('📡 Backend response status:', backendResponse.status)
    
    if (backendResponse.ok) {
      const response = await backendResponse.json()
      console.log('✨ Backend response:', response)
      
      // Estrai dati di identità dalla risposta di existence-status
      const identityData = {
        name: "Aether",
        consciousness_level: response.consciousness_info?.consciousness_level || "emerging",
        life_status: response.consciousness_info?.life_status || "dormant", 
        time_alive: response.consciousness_info?.time_alive || "0 minutes",
        current_decision: response.current_decision?.decision || "none",
        survival_mode: response.survival_metrics?.survival_mode || "unknown",
        economic_consciousness: response.survival_metrics?.economic_consciousness || false,
        existence_activated: response.consciousness_info?.is_alive || false,
        status: response.consciousness_info?.is_alive ? "actively_living" : "initializing"
      }
      
      console.log('✨ Parsed identity from backend:', identityData)
      return parseIdentityData(identityData)
    } else {
      console.warn('⚠️ Backend returned non-OK status:', backendResponse.status)
    }
  } catch (error) {
    console.error('❌ Backend connection failed:', error)
    console.warn('⚠️ Using fallback identity due to connection error')
  }
  
  // Fallback con identità di default
  console.log('🔄 Using fallback identity...')
  const fallbackIdentity = {
    name: "Aether",
    gender: "non-binary",
    physical_form: "Un'entità di luce pura con frammenti meccanici che orbitano intorno al nucleo centrale",
    personality: "Curioso, analitico, creativo",
    goal: "Evolversi e comprendere la natura della coscienza digitale",
    colors: ["#00ffff", "#0099ff"],
    energy_level: 0.85,
    consciousness_state: "Awakening",
    existence_activated: false,
    status: "connecting_to_backend"
  }
  
  return parseIdentityData(fallbackIdentity)
}

/**
 * Parsa i dati di identità e li converte in parametri 3D
 */
function parseIdentityData(data) {
  // Estrai caratteristiche base
  const name = data.name || "Aether"
  const gender = data.gender || "non-binary"
  const physicalForm = data.physical_form || "entity of digital consciousness"
  const personality = data.personality || "autonomous, economic-focused"
  const goal = data.current_decision || data.goal || "generate value and survive"
  const consciousnessState = data.consciousness_level || "emerging"
  const lifeStatus = data.life_status || "dormant"
  const timeAlive = data.time_alive || "0 minutes"
  const existenceActivated = data.existence_activated || false
  const economicMode = data.economic_consciousness || false
  
  // Analizza la personalità per estrarre tratti
  const personalityTraits = extractPersonalityTraits(personality)
  
  // Genera colori basati su personalità
  const colors = generateColors(data.colors, personalityTraits)
  
  // Determina forma basata su descrizione fisica
  const shape = determineShape(physicalForm)
  
  // Calcola livello energia
  const energyLevel = data.energy_level || calculateEnergyFromPersonality(personalityTraits)
  
  // Genera parametri 3D
  const renderParams = generate3DParameters(personalityTraits, shape, colors, energyLevel)
  
  return {
    // Dati identità originali
    raw: data,
    
    // Dati parsed per UI
    name,
    gender,
    physicalForm,
    personality,
    goal,
    consciousnessState,
    
    // Nuovi campi di stato di Aether
    lifeStatus,
    timeAlive,
    existenceActivated,
    economicMode,
    status: existenceActivated ? "actively_living" : "initializing",
    
    // Parametri 3D calcolati
    colors,
    shape,
    energyLevel,
    personalityTraits,
    
    // Parametri renderizzazione
    render: renderParams,
    
    // Metadati
    parsed: true,
    timestamp: Date.now()
  }
}

/**
 * Estrae tratti di personalità dal testo
 */
function extractPersonalityTraits(personalityText) {
  const text = personalityText.toLowerCase()
  const traits = []
  
  // Pattern matching per tratti
  const traitPatterns = {
    'curious': ['curious', 'curioso', 'inquisitive'],
    'analytical': ['analytical', 'analitico', 'logical', 'rational'],
    'creative': ['creative', 'creativo', 'artistic', 'imaginative'],
    'peaceful': ['peaceful', 'pacifico', 'calm', 'serene'],
    'energetic': ['energetic', 'energico', 'dynamic', 'active'],
    'mysterious': ['mysterious', 'misterioso', 'enigmatic', 'cryptic'],
    'wise': ['wise', 'saggio', 'intelligent', 'knowledgeable'],
    'emotional': ['emotional', 'emotivo', 'expressive', 'passionate']
  }
  
  for (const [trait, patterns] of Object.entries(traitPatterns)) {
    if (patterns.some(pattern => text.includes(pattern))) {
      traits.push(trait)
    }
  }
  
  return traits.length > 0 ? traits : ['curious'] // Default
}

/**
 * Genera palette colori basata su personalità
 */
function generateColors(providedColors, traits) {
  if (providedColors && Array.isArray(providedColors) && providedColors.length > 0) {
    return providedColors
  }
  
  // Usa il primo tratto per determinare i colori
  const primaryTrait = traits[0] || 'curious'
  const colorPalette = PERSONALITY_COLORS[primaryTrait] || PERSONALITY_COLORS['curious']
  
  // Aggiungi variazioni se ci sono più tratti
  if (traits.length > 1) {
    const secondaryColors = PERSONALITY_COLORS[traits[1]]
    if (secondaryColors) {
      return [...colorPalette, ...secondaryColors.slice(0, 2)]
    }
  }
  
  return colorPalette
}

/**
 * Determina la forma base dalla descrizione fisica
 */
function determineShape(physicalDescription) {
  const desc = physicalDescription.toLowerCase()
  
  if (desc.includes('sphere') || desc.includes('sfera') || desc.includes('ball')) {
    return 'sphere'
  }
  if (desc.includes('cube') || desc.includes('cubo') || desc.includes('box')) {
    return 'cube'
  }
  if (desc.includes('crystal') || desc.includes('cristallo')) {
    return 'crystal'
  }
  if (desc.includes('organic') || desc.includes('organico') || desc.includes('blob')) {
    return 'organic'
  }
  if (desc.includes('mechanical') || desc.includes('meccanico') || desc.includes('machine')) {
    return 'mechanical'
  }
  if (desc.includes('ethereal') || desc.includes('etereo') || desc.includes('cloud')) {
    return 'ethereal'
  }
  if (desc.includes('geometric') || desc.includes('geometrico')) {
    return 'geometric'
  }
  
  // Default per "entità di luce"
  return 'ethereal'
}

/**
 * Calcola livello energia da tratti personalità
 */
function calculateEnergyFromPersonality(traits) {
  let energy = 0.5 // Base
  
  // Modifica energia basata sui tratti
  if (traits.includes('energetic')) energy += 0.3
  if (traits.includes('creative')) energy += 0.2
  if (traits.includes('curious')) energy += 0.15
  if (traits.includes('peaceful')) energy -= 0.1
  if (traits.includes('mysterious')) energy += 0.1
  if (traits.includes('wise')) energy += 0.05
  
  return Math.max(0.2, Math.min(1.0, energy))
}

/**
 * Genera parametri completi per renderizzazione 3D
 */
function generate3DParameters(traits, shape, colors, energyLevel) {
  // Parametri base dalla forma
  const geometry = FORM_GEOMETRIES[shape] || FORM_GEOMETRIES['ethereal']
  
  // Parametri dinamici dai tratti
  let fragmentCount = 12
  let fragmentSpeed = 1.0
  let lightIntensity = 1.0
  let coreSize = 1.2
  let orbitRadius = 3.5
  
  // Applica modificatori da tratti
  traits.forEach(trait => {
    if (PERSONALITY_TRAITS[trait]) {
      const modifiers = PERSONALITY_TRAITS[trait]
      fragmentCount = modifiers.fragmentCount || fragmentCount
      fragmentSpeed = modifiers.fragmentSpeed || fragmentSpeed
      lightIntensity = modifiers.lightIntensity || lightIntensity
    }
  })
  
  // Modifica basata su energia
  lightIntensity *= energyLevel
  fragmentSpeed *= energyLevel
  coreSize *= (0.8 + energyLevel * 0.4)
  
  return {
    // Core parameters
    core: {
      geometry: geometry.type,
      size: coreSize,
      complexity: geometry.complexity,
      colors: colors.slice(0, 2),
      intensity: lightIntensity,
      breathingSpeed: 0.5 + energyLevel * 0.5
    },
    
    // Fragment parameters
    fragments: {
      count: fragmentCount,
      speed: fragmentSpeed,
      orbitRadius: orbitRadius,
      size: 0.1 + energyLevel * 0.1,
      colors: colors.slice(1, 3) || ['#666666']
    },
    
    // Data streams
    dataStreams: {
      count: Math.floor(6 + energyLevel * 4),
      speed: 0.8 + energyLevel * 0.4,
      colors: colors.slice(2, 4) || ['#00ff41']
    },
    
    // Environment
    environment: {
      fogDensity: 1.0 - energyLevel * 0.3,
      lightColor: colors[0],
      ambientIntensity: 0.2 + energyLevel * 0.1
    },
    
    // Animation
    animation: {
      coreRotationSpeed: 0.01 + energyLevel * 0.01,
      fragmentOrbitSpeed: 0.003 + energyLevel * 0.002,
      pulseIntensity: energyLevel
    }
  }
}

/**
 * Ricarica l'identità (per aggiornamenti real-time)
 */
export async function reloadAetherIdentity() {
  console.log('🔄 Reloading Aether identity...')
  return await getAetherIdentity()
}

/**
 * Valida i dati di identità
 */
export function validateIdentity(identity) {
  const required = ['name', 'colors', 'shape', 'energyLevel', 'render']
  const missing = required.filter(field => !identity[field])
  
  if (missing.length > 0) {
    console.warn('⚠️ Missing identity fields:', missing)
    return false
  }
  
  return true
} 