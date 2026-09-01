from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="RAG Backend")

# Definiamo la struttura dei dati in ingresso usando Pydantic.
# Questo fa parte della logica "SDD" (Schema-Driven Development):
# dichiariamo esplicitamente cosa ci aspettiamo.
class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health_check():
    """Endpoint per verificare che il server sia attivo."""
    # FastAPI converte automaticamente il dizionario Python in JSON
    return {"status": "ok"}

@app.post("/api/chat")
def chat_mock(request: ChatRequest):
    """Endpoint mock per la chat."""
    # Accediamo al messaggio inviato tramite request.message
    # e costruiamo la risposta che il test si aspetta.
    return {"reply": f"Ricevuto: {request.message}"}
