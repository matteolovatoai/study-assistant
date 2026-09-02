# Architettura di Sistema

Il progetto è un sistema RAG (Retrieval-Augmented Generation) locale e modulare, ottimizzato per poter girare in futuro su un Raspberry Pi 5 (8GB RAM) con Traefik e Tailscale.

## Stack Tecnologico (V0.1)

### Backend (Microservizio API)
- **Linguaggio:** Python 3.12+
- **Framework Web:** FastAPI (basato su Starlette e Pydantic).
- **Tool di Testing:** Pytest
- **Integrazione AI:** `google-genai` SDK (usando il modello `gemini-3.5-flash-lite` per massima velocità e minor costo).
- **Database Vettoriale:** ChromaDB (modalità in-memory/locale).

### Frontend (Prossimo Sprint)
- **Framework:** Next.js (React)
- **Comunicazione:** Chiamate REST HTTP standard (JSON) dirette al backend FastAPI.

## Diagramma del Flusso RAG (Retrieval-Augmented Generation)

1. **Ingestione (Upload):**
   L'utente carica un file `.txt` -> Il Web Server (FastAPI) lo riceve -> Passa il testo a `rag_engine` -> Il testo viene diviso in Chunk -> I Chunk diventano Vettori salvati in ChromaDB.
2. **Interrogazione (Chat):**
   L'utente fa una domanda -> FastAPI riceve la domanda -> Il sistema cerca in ChromaDB il contesto più simile alla domanda -> Domanda + Contesto vengono inviati a Gemini API -> La risposta generata torna all'utente.
