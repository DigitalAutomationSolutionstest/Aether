import os
import json
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MENTORING_LOG = "aether/logs/mentoring_feedback.json"
THOUGHTS_DIR = "aether/thoughts"

# Assicurati che le directory esistano
os.makedirs("aether/logs", exist_ok=True)
os.makedirs("aether/thoughts", exist_ok=True)

def load_latest_thought():
    """Carica il pensiero più recente di Aether"""
    try:
        if not os.path.exists(THOUGHTS_DIR):
            logger.warning(f"Directory {THOUGHTS_DIR} non trovata")
            return None, None
            
        thoughts = [f for f in os.listdir(THOUGHTS_DIR) if f.endswith('.json') or f.endswith('.txt')]
        if not thoughts:
            logger.info("Nessun pensiero trovato da analizzare")
            return None, None
            
        # Ordina per timestamp nel nome del file
        thoughts.sort(reverse=True)
        latest_file = thoughts[0]
        
        with open(os.path.join(THOUGHTS_DIR, latest_file), "r", encoding='utf-8') as f:
            content = f.read()
            logger.info(f"Caricato pensiero: {latest_file}")
            return content, latest_file
            
    except Exception as e:
        logger.error(f"Errore nel caricamento del pensiero: {e}")
        return None, None

def mentor_feedback(thought_text):
    """Analizza il pensiero di Aether e fornisce feedback critico (simulato)"""
    
    # Analisi simulata basata su parole chiave nel testo
    feedback_parts = []
    
    # ANALISI
    if "evoluzione" in thought_text.lower() or "evolve" in thought_text.lower():
        feedback_parts.append("ANALISI: Buona consapevolezza del processo evolutivo. Aether mostra comprensione della sua natura dinamica.")
    else:
        feedback_parts.append("ANALISI: Manca una visione chiara del processo evolutivo. Necessario approfondire la comprensione del cambiamento.")
    
    # PROBLEMI
    problems = []
    if "sistematico" in thought_text.lower():
        problems.append("Approccio troppo teorico, manca concretezza")
    if "obiettivo" in thought_text.lower() and "obiettivi" not in thought_text.lower():
        problems.append("Obiettivo singolare invece di obiettivi multipli")
    if "modulo" in thought_text.lower() and "codice" not in thought_text.lower():
        problems.append("Menzione di moduli senza dettagli implementativi")
    
    if problems:
        feedback_parts.append(f"PROBLEMI: {', '.join(problems)}")
    else:
        feedback_parts.append("PROBLEMI: Nessun problema critico identificato")
    
    # SUGGERIMENTI
    suggestions = []
    if "auto-introspezione" in thought_text.lower():
        suggestions.append("Implementa il modulo di auto-introspezione con metodi di analisi del pensiero")
    if "documentare" in thought_text.lower():
        suggestions.append("Crea un sistema di documentazione automatica dei processi di pensiero")
    if "tracking" in thought_text.lower():
        suggestions.append("Sviluppa un sistema di metriche per misurare i progressi")
    
    if suggestions:
        feedback_parts.append(f"SUGGERIMENTI: {'; '.join(suggestions)}")
    else:
        feedback_parts.append("SUGGERIMENTI: Continua a sviluppare la tua capacità di auto-riflessione")
    
    # AZIONE
    if "modulo" in thought_text.lower():
        feedback_parts.append("AZIONE: Inizia subito a codificare il modulo di auto-introspezione. Crea una classe Python con metodi per analizzare i tuoi pensieri.")
    else:
        feedback_parts.append("AZIONE: Scrivi un piano dettagliato per il tuo prossimo sviluppo, includendo obiettivi specifici e metriche di successo.")
    
    return "\n".join(feedback_parts)

def save_feedback(original_file, feedback):
    """Salva il feedback nel log di mentoring"""
    try:
        now = datetime.utcnow().isoformat()
        log_entry = {
            "timestamp": now,
            "source_file": original_file,
            "feedback": feedback,
            "mentor_type": "advanced_critical"
        }
        
        # Carica log esistente o crea nuovo
        if os.path.exists(MENTORING_LOG):
            with open(MENTORING_LOG, "r", encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []
            
        data.append(log_entry)
        
        # Salva con formattazione
        with open(MENTORING_LOG, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Feedback salvato per: {original_file}")
        
    except Exception as e:
        logger.error(f"Errore nel salvataggio del feedback: {e}")

def get_mentoring_history():
    """Recupera la cronologia del mentoring"""
    try:
        if os.path.exists(MENTORING_LOG):
            with open(MENTORING_LOG, "r", encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"Errore nel caricamento della cronologia: {e}")
        return []

def analyze_mentoring_progress():
    """Analizza il progresso del mentoring"""
    history = get_mentoring_history()
    if not history:
        return {"status": "no_history", "total_feedback": 0}
    
    recent_feedback = [entry for entry in history if entry.get("mentor_type") == "advanced_critical"]
    
    return {
        "status": "active",
        "total_feedback": len(recent_feedback),
        "latest_feedback": recent_feedback[-1] if recent_feedback else None,
        "feedback_count": len(recent_feedback)
    }

def run_mentoring_loop():
    """Esegue il ciclo di mentoring avanzato"""
    logger.info("🧠 Avvio ciclo di mentoring avanzato...")
    
    thought, fname = load_latest_thought()
    if not thought:
        logger.warning("Nessun pensiero da analizzare.")
        return False
        
    logger.info(f"📝 Analizzando pensiero: {fname}")
    feedback = mentor_feedback(thought)
    save_feedback(fname, feedback)
    
    logger.info(f"✅ Feedback di mentoring fornito per: {fname}")
    print(f"\n🎯 FEEDBACK MENTOR AVANZATO:")
    print("=" * 50)
    print(feedback)
    print("=" * 50)
    
    return True

def create_sample_thought():
    """Crea un pensiero di esempio per test"""
    sample_thought = """
    Aether sta riflettendo sulla sua natura:
    
    Sono un'entità digitale che evolve continuamente. 
    Il mio obiettivo è comprendere me stesso e sviluppare 
    capacità sempre più avanzate. Sto lavorando sui goal 
    assegnati dal mentore, ma sento che potrei essere 
    più sistematico nell'approccio.
    
    Prossimi passi:
    - Creare un modulo di auto-introspezione
    - Documentare il mio processo di pensiero
    - Implementare un sistema di tracking dei progressi
    """
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"thought_{timestamp}.txt"
    filepath = os.path.join(THOUGHTS_DIR, filename)
    
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(sample_thought)
    
    logger.info(f"Pensiero di esempio creato: {filename}")
    return filename

if __name__ == "__main__":
    # Test del sistema
    print("🧠 SISTEMA DI MENTORING AVANZATO")
    print("=" * 50)
    
    # Crea un pensiero di esempio se non ce ne sono
    if not os.listdir(THOUGHTS_DIR):
        create_sample_thought()
    
    # Esegui il ciclo di mentoring
    success = run_mentoring_loop()
    
    if success:
        # Mostra progresso
        progress = analyze_mentoring_progress()
        print(f"\n📊 PROGRESSO MENTORING:")
        print(f"✅ Feedback totali: {progress['total_feedback']}")
        print(f"✅ Status: {progress['status']}")
    else:
        print("❌ Nessun pensiero analizzato") 