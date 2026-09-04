from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import generate_ai_response

app = FastAPI(title="RAG Backend")

# Abilitiamo CORS (Cross-Origin Resource Sharing)
# Questo permette al frontend Next.js (che gira su localhost:3000)
# di fare chiamate verso il backend (localhost:8000) senza essere bloccato dal browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In produzione andrebbe limitato al dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
