-- Query SQL per configurare Supabase per Aether
-- Esegui queste query nella console SQL di Supabase

-- Tabella per i pensieri e log cognitivi
CREATE TABLE IF NOT EXISTS aether_thoughts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp timestamptz DEFAULT now(),
  type text, -- "thought", "decision", "action"
  content text,
  context jsonb
);

-- Tabella per la memoria semantica
CREATE TABLE IF NOT EXISTS aether_memory (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  embedding vector(1536), -- per similarity search (opzionale con pgvector)
  content text,
  tags text[],
  created_at timestamptz DEFAULT now()
);

-- Tabella per la UI o scena 3D corrente
CREATE TABLE IF NOT EXISTS aether_environment (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  scene_name text,
  scene_config jsonb,
  created_at timestamptz DEFAULT now()
);

-- Tabella per log decisioni economiche
CREATE TABLE IF NOT EXISTS aether_economy (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp timestamptz DEFAULT now(),
  action text,
  cost numeric,
  expected_roi numeric,
  status text -- es. "executed", "failed", "planned"
);

-- Indici per migliorare le performance
CREATE INDEX IF NOT EXISTS idx_aether_thoughts_timestamp ON aether_thoughts(timestamp);
CREATE INDEX IF NOT EXISTS idx_aether_thoughts_type ON aether_thoughts(type);
CREATE INDEX IF NOT EXISTS idx_aether_memory_tags ON aether_memory USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_aether_economy_status ON aether_economy(status);
