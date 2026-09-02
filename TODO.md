# Roadmap e Sprint

## ✅ Sprint 1: Setup Backend e Integrazione AI
- [x] Inizializzazione progetto (`uv venv`, `pytest.ini`, `.gitignore`).
- [x] Scrittura test TDD per endpoint base.
- [x] Creazione `main.py` con FastAPI (endpoint `/health`, mock `/api/chat`).
- [x] Test integrazione API di Google Gemini tramite `.env`.
- [x] Creazione `rag_engine.py` e integrazione con il modello `gemini-3.5-flash-lite`.
- [x] Collegamento finale tra `main.py` e `rag_engine.py`.

## 🚧 Sprint 2: Database Vettoriale e RAG (In Corso)
- [ ] Installazione ChromaDB e python-multipart.
- [ ] TDD: Test per l'endpoint `/api/upload` (caricamento file di testo).
- [ ] Implementazione `/api/upload` in FastAPI (`main.py`).
- [ ] `rag_engine.py`: Funzione per spezzettare (chunking) il documento.
- [ ] `rag_engine.py`: Inizializzazione di ChromaDB e salvataggio dei vettori (Embeddings).
- [ ] Modifica `/api/chat`: Cercare il contesto in ChromaDB prima di chiamare Gemini.

## 📅 Sprint 3: Interfaccia Utente (Next.js)
- [ ] Inizializzazione progetto Next.js (separato dal backend).
- [ ] Creazione UI per la chat (gestione stato dei messaggi).
- [ ] Creazione UI per caricare un documento (`<input type="file">`).
- [ ] Collegamento delle chiamate `fetch` tra Frontend e Backend.
- [ ] Gestione del CORS in FastAPI per permettere le chiamate.

## 📅 Sprint 4: Dockerizzazione e Deployment (Raspberry Pi 5)
- [ ] Creazione `Dockerfile` per backend e frontend.
- [ ] Configurazione `docker-compose.yml`.
- [ ] (Opzionale) Regole di Traefik per il reverse proxy su Tailscale.
