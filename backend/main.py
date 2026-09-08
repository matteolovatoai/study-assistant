from typing import Annotated

from config import Settings, get_settings
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import RagEngine

app = FastAPI(title="RAG Backend")

# Abilitiamo CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In produzione andrebbe limitato al dominio del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from functools import lru_cache


# Dipendenza per ottenere il motore RAG
@lru_cache
def get_rag_engine(settings: Annotated[Settings, Depends(get_settings)]) -> RagEngine:
    return RagEngine(settings)


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/chat")
def chat(request: ChatRequest, engine: Annotated[RagEngine, Depends(get_rag_engine)]):
    response: str = engine.generate_ai_response(request.message)
    return {"reply": response}


@app.post("/api/upload")
async def upload(
    file: Annotated[UploadFile, File(...)],
    engine: Annotated[RagEngine, Depends(get_rag_engine)],
):
    # 1. Leggiamo fisicamente il contenuto del file .txt
    content = await file.read()
    text = content.decode("utf-8")

    # 2. Lo spezzettiamo tramite la nostra funzione in rag_engine
    chunks = engine.chunk_text(text)

    # 3. Lo salviamo nel database ChromaDB!
    engine.store_chunks(chunks, file.filename or "sconosciuto")

    return {
        "filename": file.filename,
        "message": f"Caricati {len(chunks)} frammenti nel RAG!",
    }
