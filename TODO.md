# Roadmap e Sprint

## ✅ Sprint 1: Setup Backend e Integrazione AI
- [x] Inizializzazione progetto (`uv venv`, `pytest.ini`, `.gitignore`).
- [x] Scrittura test TDD per endpoint base.
- [x] Creazione `main.py` con FastAPI (endpoint `/health`, mock `/api/chat`).
- [x] Test integrazione API di Google Gemini tramite `.env`.
- [x] Creazione `rag_engine.py` e integrazione con il modello `gemini-3.5-flash-lite`.
- [x] Collegamento finale tra `main.py` e `rag_engine.py`.

## ✅ Sprint 2: Database Vettoriale e RAG
- [x] Installazione ChromaDB e python-multipart.
- [x] TDD: Test per l'endpoint `/api/upload` (caricamento file di testo).
- [x] Implementazione `/api/upload` in FastAPI (`main.py`) usando `Annotated`.
- [x] `rag_engine.py`: Funzione per spezzettare (chunking) il documento.
- [x] `rag_engine.py`: Inizializzazione di ChromaDB e salvataggio dei vettori (usando `GoogleGeminiEmbeddingFunction` e `gemini-embedding-001`).
- [x] Modifica `/api/chat`: Cercare il contesto in ChromaDB prima di chiamare Gemini.

## 🚧 Sprint 3: Interfaccia Utente (Next.js) - In Partenza
- [x] Inizializzazione progetto Next.js (separato dal backend).
- [ ] Creazione UI per la chat (gestione stato dei messaggi).
- [ ] Creazione UI per caricare un documento (`<input type="file">`).
- [ ] Collegamento delle chiamate `fetch` tra Frontend e Backend.
- [ ] Gestione del CORS in FastAPI per permettere le chiamate.

## 📅 Sprint 4: Dockerizzazione e Deployment (Raspberry Pi 5)
- [ ] Creazione `Dockerfile` per backend e frontend.
- [ ] Configurazione `docker-compose.yml`.
- [ ] Regole di Traefik per il reverse proxy su Tailscale.
