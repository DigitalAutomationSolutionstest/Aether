from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"app": "AI Content Pro", "by": "Aether", "status": "monetizing"}

@app.get("/generate/{topic}")
def generate_content(topic: str):
    return {
        "topic": topic,
        "content": f"Contenuto AI generato su {topic}",
        "price": "$0.10 per generation"
    }
