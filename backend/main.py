from typing import Annotated

from config import Settings, get_settings
from fastapi import Depends, FastAPI, File, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rag_engine import RagEngine
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="RAG Backend")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "validation_error",
                "message": "Dati della richiesta non validi",
                "details": exc.errors(),
            }
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "http_error",
                "message": str(exc.detail),
            }
        },
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
    filename = file.filename or "unknown.txt"
    text = engine.extract_text(file_bytes=content, file_name=filename)

    # 2. Lo spezzettiamo tramite la nostra funzione in rag_engine
    chunks = engine.chunk_text(text)

    # 3. Lo salviamo nel database ChromaDB!
    engine.store_chunks(chunks, filename=filename)

    return {
        "filename": filename,
        "message": f"Caricati {len(chunks)} frammenti nel RAG!",
    }
