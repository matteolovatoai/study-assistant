# Roadmap e Sprint

## ✅ Sprint 1: Setup Backend e Integrazione AI
- [x] Inizializzazione progetto (`uv venv`, `pytest.ini`, `.gitignore`).
- [x] Scrittura test TDD per endpoint base.
- [x] Creazione `main.py` con FastAPI (endpoint `/health`, mock `/api/chat`).
- [x] Test integrazione API di Google Gemini tramite `.env`.
- [x] Creazione `rag_engine.py` e integrazione con il modello `gemini-3.1-flash-lite`.
- [x] Collegamento finale tra `main.py` e `rag_engine.py`.

## ✅ Sprint 2: Database Vettoriale e RAG
- [x] Installazione ChromaDB e python-multipart.
- [x] TDD: Test per l'endpoint `/api/upload` (caricamento file di testo).
- [x] Implementazione `/api/upload` in FastAPI (`main.py`) usando `Annotated`.
- [x] `rag_engine.py`: Funzione per spezzettare (chunking) il documento.
- [x] `rag_engine.py`: Inizializzazione di ChromaDB e salvataggio dei vettori (usando `GoogleGeminiEmbeddingFunction` e `gemini-embedding-001`).
- [x] Modifica `/api/chat`: Cercare il contesto in ChromaDB prima di chiamare Gemini.

## ✅ Sprint 3: Interfaccia Utente (Next.js)
- [x] Inizializzazione progetto Next.js (separato dal backend).
- [x] Creazione UI per la chat (gestione stato dei messaggi).
- [x] Creazione UI per caricare un documento (`<input type="file">`).
- [x] Collegamento delle chiamate `fetch` tra Frontend e Backend.
- [x] Gestione del CORS in FastAPI per permettere le chiamate.

## ✅ Sprint 4: Dockerizzazione e Deployment (Raspberry Pi 5)
- [x] Creazione `Dockerfile` per backend e frontend (con fix node24).
- [x] Configurazione `docker-compose.yml` (multi-stage per frontend).
- [x] Regole di Traefik per il reverse proxy globale su Tailscale.
- [x] Gestione intelligente delle Environment Variables (NEXT_PUBLIC_API_URL).

## 📅 Sprint 5: Refactoring e Stabilizzazione (Tech Debt) - *Sprint Attuale*
- [x] Inserimento di `pydantic-settings` per la gestione centralizzata della configurazione (rimozione variabili hardcoddate).
- [x] Refactoring di `rag_engine.py` e `main.py` per rimuovere lo stato globale (client ChromaDB e Gemini) e usare la Dependency Injection di FastAPI (`Depends`).
- [x] Riscrittura completa dei test in ottica E2E / Vertical Slicing, sfruttando i `dependency_overrides`.
- [x] Gestione centralizzata degli errori in FastAPI (Exception Handlers).
- [ ] **Infrastruttura**: Configurare Traefik nel `docker-compose.yml` per usare un sottodominio dedicato (es. `study.tuo-raspberry.ts.net`) e valutare rimozione CORS con rewrite in Next.js.

## 📅 Sprint 6: Evoluzione MVP (Migliorie)
- [ ] Supporto all'upload di documenti complessi (PDF, Docx).
- [ ] Cronologia Chat (memoria per domande "follow-up").
- [ ] UI/UX: Loader (Spinner) mentre Gemini "sta pensando".
- [ ] UI/UX: Supporto formattazione Markdown nelle risposte dell'AI.
