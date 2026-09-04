from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import chunk_text, generate_ai_response, store_chunks

app = FastAPI(title="RAG Backend")

# Abilitiamo CORS (Cross-Origin Resource Sharing)
# Questo permette al frontend Next.js (che gira su localhost:3000)
# di fare chiamate verso il backend (localhost:8000) senza essere bloccato dal browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione andrebbe limitato al dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Definiamo la struttura dei dati in ingresso usando Pydantic.
class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/chat")
def chat(request: ChatRequest):
    response: str = generate_ai_response(request.message)
    return {"reply": response}


@app.post("/api/upload")
async def upload(file: Annotated[UploadFile, File(...)]):
    # 1. Leggiamo fisicamente il contenuto del file .txt
    content = await file.read()
    text = content.decode("utf-8")

    # 2. Lo spezzettiamo tramite la nostra funzione in rag_engine
    chunks = chunk_text(text)

    # 3. Lo salviamo nel database ChromaDB!
    store_chunks(chunks, file.filename or "sconosciuto")

    return {
        "filename": file.filename,
        "message": f"Caricati {len(chunks)} frammenti nel RAG!",
    }
