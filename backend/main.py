from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from rag_engine import generate_ai_response

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
def chat(request: ChatRequest):
    """Endpoint per la chat."""
    response: str = generate_ai_response(request.message)
    return {"reply": response}


@app.post("/api/upload")
def upload(file: Annotated[UploadFile, File(...)]):
    return {"filename": file.filename, "message": "File caricato con successo"}
