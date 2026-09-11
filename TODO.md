# Roadmap e Sprint

## ✅ Sprint Completati (1-5)
- Inizializzazione progetto (`uv`, Next.js, FastAPI, Docker, Traefik).
- Implementazione RAG base con ChromaDB e Gemini API.
- Gestione configurazione con `pydantic-settings` e Dependency Injection (`Depends`).
- Test E2E con override delle dipendenze.
- Integrazione SQLite per la gestione della memoria delle chat.

## ✅ Sprint 6: Evoluzione MVP (Migliorie)
- [x] Cronologia Chat (integrazione base con SQLite).
- [x] UI/UX: Loader (Spinner) mentre Gemini "sta pensando".
- [x] UI/UX: Supporto formattazione Markdown nelle risposte dell'AI.
- [x] Abbandono supporto `.docx` (YAGNI) per concentrarsi sull'ingestione avanzata dei PDF.

## 📅 Sprint 7: Ingestione PDF Avanzata (Multimodale & Pulizia) - *Sprint Attuale*
- [ ] **Pulizia Testo:** Implementare logica per ignorare header, footer, nomi dei docenti e loghi ricorrenti in ogni slide.
- [ ] **Deduplicazione Slide Animate:** Rilevare e unire le slide con stile "animazione" (dove il testo si aggiunge progressivamente) conservando solo la slide finale completa.
- [ ] **Estrazione Multimodale:** Sfruttare modelli visuali (es. `gemini-flash` multimodale) o parser avanzati per estrarre il contesto reale da tabelle, grafici e liste presenti nei PDF.
- [ ] **Chunking Semantico:** Suddividere il documento in base al significato logico (es. per singola slide completa) invece che per numero di caratteri.

## 📅 Sprint 8: Gestione Multi-Chat (Frontend & Backend)
- [ ] **Backend:** Esporre endpoint CRUD (Creazione, Lettura, Aggiornamento, Cancellazione) per le sessioni di chat (es. `/api/chats`, `/api/chats/{id}/messages`).
- [ ] **Frontend:** Creare una Sidebar per la navigazione tra le diverse sessioni di chat.
- [ ] **Frontend:** Integrare lo stato delle conversazioni con le API multi-chat.

## 📅 Sprint 9: Ottimizzazioni e Deploy Finale
- [ ] Supporto Streaming per le risposte dell'AI (SSE).
- [ ] Limiti risorse Docker (RAM/CPU) per la stabilità su Raspberry Pi.
- [ ] Setup di uno script per il backup automatico del database SQLite e dei vettori ChromaDB.
