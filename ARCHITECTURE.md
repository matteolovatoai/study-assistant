# Architettura di Sistema

Il progetto è un sistema RAG (Retrieval-Augmented Generation) locale e modulare, ottimizzato per poter girare in futuro su un Raspberry Pi 5 (8GB RAM) con Traefik e Tailscale.

## Stack Tecnologico (V0.1)

### Backend (Microservizio API)
- **Linguaggio:** Python 3.12+
- **Framework Web:** FastAPI (basato su Starlette e Pydantic).
- **Tool di Testing:** Pytest
- **Integrazione AI (Generazione Testo):** `google-genai` SDK (usando il modello `gemini-3.5-flash-lite` per massima velocità e minor costo).
- **Database Vettoriale:** ChromaDB (modalità in-memory persistente su disco).
- **Integrazione AI (Embeddings):** Funzione integrata in ChromaDB `GoogleGeminiEmbeddingFunction` (utilizzando il modello `gemini-embedding-001`).

### Frontend (Completato V1)
- **Framework:** Next.js (React) con App Router.
- **Styling & UI:** Tailwind CSS + shadcn/ui.
- **Comunicazione:** Chiamate REST HTTP standard (JSON) dirette al backend FastAPI.

## Diagramma del Flusso RAG (Retrieval-Augmented Generation)

1. **Ingestione (Upload):**
   L'utente carica un file `.txt` -> Il Web Server (FastAPI) lo riceve -> Passa il testo a `rag_engine` -> Il testo viene diviso in Chunk -> I Chunk diventano Vettori salvati in ChromaDB.
2. **Interrogazione (Chat):**
   L'utente fa una domanda -> FastAPI riceve la domanda -> Il sistema cerca in ChromaDB i 2 contesti più simili alla domanda -> Domanda + Contesto vengono formattati in un super-prompt -> Inviati a Gemini API -> La risposta generata torna all'utente via HTTP.

## Deployment & Infrastruttura (Produzione)
- **Containerizzazione:** Docker (Multi-stage build per Next.js, single-stage per Python ottimizzato).
- **API Gateway & Routing:** Traefik v3 (con Docker Socket Auto-discovery e Zero Trust).
- **Networking e Sicurezza HTTPS:** Tailscale + Traefik `tsresolver` (Connessione VPN Mesh e certificati TLS automatici).
