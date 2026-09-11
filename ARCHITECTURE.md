# Architettura di Sistema

Il progetto è un sistema RAG (Retrieval-Augmented Generation) locale e modulare, ottimizzato per poter girare su un Raspberry Pi 5 (8GB RAM) con Traefik e Tailscale.

## Stack Tecnologico (V1.0)

### Backend (Microservizio API)
- **Linguaggio:** Python 3.12+
- **Framework Web:** FastAPI (basato su Starlette e Pydantic).
- **Gestione Configurazione:** `pydantic-settings` per la gestione tipizzata e centralizzata dell'ambiente (environment variables).
- **Database Relazionale (Memoria & Sessioni):** SQLite, utilizzato per memorizzare le conversazioni e gestire la funzionalità multi-chat.
- **Database Vettoriale:** ChromaDB (modalità in-memory persistente su disco).
- **Integrazione AI (Generazione Testo & Multimodale):** `google-genai` SDK (usando il modello della famiglia `gemini-flash` per bilanciare velocità, costo e capacità visive).
- **Integrazione AI (Embeddings):** Funzione integrata in ChromaDB `GoogleGeminiEmbeddingFunction` (utilizzando il modello `gemini-embedding-001`).
- **Tool di Testing:** Pytest (approccio architetturale basato su Vertical Slicing per i test E2E con override della Dependency Injection).

### Frontend
- **Framework:** Next.js (React) con App Router.
- **Styling & UI:** Tailwind CSS + shadcn/ui.
- **Comunicazione:** Chiamate REST HTTP standard (JSON) dirette al backend FastAPI.

## Diagramma del Flusso RAG (Retrieval-Augmented Generation)

1. **Ingestione (Upload PDF Avanzato):**
   L'utente carica un file `.pdf` -> Il Web Server (FastAPI) lo riceve -> Il parser processa il documento (gestendo slide animate, escludendo loghi/header ripetitivi, ed estraendo testo/immagini in ottica multimodale) -> Il contenuto ripulito viene diviso in Chunk -> I Chunk diventano Vettori salvati in ChromaDB.
2. **Interrogazione (Chat & Multi-chat):**
   L'utente seleziona una sessione o ne crea una nuova -> Invia una domanda -> FastAPI riceve la domanda e recupera la history da SQLite -> Il sistema cerca in ChromaDB i contesti più simili alla domanda -> Domanda + History + Contesto formano il prompt -> Inviato a Gemini API -> La risposta generata torna all'utente e viene salvata in SQLite.

## Deployment & Infrastruttura (Produzione)
- **Containerizzazione:** Docker (Multi-stage build per Next.js, single-stage per Python ottimizzato).
- **API Gateway & Routing:** Traefik v3 (con Docker Socket Auto-discovery e Zero Trust).
- **Networking e Sicurezza HTTPS:** Tailscale + Traefik `tsresolver` (Connessione VPN Mesh e certificati TLS automatici).
