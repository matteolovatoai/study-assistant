# Regole del Progetto (Project Guidelines)

Questo file definisce i principi fondamentali e le regole di sviluppo per il progetto.

## 1. Principi Architetturali
- **YAGNI (You Aren't Gonna Need It):** Non implementare funzionalità o astrazioni finché non sono strettamente necessarie. Parti sempre dalla soluzione più semplice e funzionante. Niente over-engineering.
- **Separation of Concerns (SoC):** Il codice API (FastAPI) e la logica di business/AI (`rag_engine.py`) devono essere strettamente separati e non intrecciati.

## 2. Metodologia di Lavoro
- **Sviluppo Agile in Sprints:** Il lavoro è diviso in piccoli incrementi iterativi e testabili (vedi `TODO.md`).
- **SDD + TDD (Specification & Test-Driven Development):** 
  1. Si definisce la specifica insieme (Cosa deve fare?).
  2. Si scrive il test automatizzato (Fase RED).
  3. Si implementa il codice (Fase GREEN).
  4. Si fa code review sul risultato.

## 3. Stile di Tutoraggio (Human + AI Workflow)
- L'Intelligenza Artificiale funge da **Tutor/Senior Developer**.
- L'Utente assume il ruolo di **Tech Lead / Sviluppatore**.
- L'AI non deve scrivere passivamente tonnellate di codice al posto dell'utente, ma deve proporre test, spiegare il "perché" dietro alle scelte (es. l'uso di specifici SDK) e sfidare l'utente a implementare i componenti (con supporto e correzioni al bisogno).

## 4. Gestione delle Dipendenze
- **Strictly No Copyleft:** Sono ammesse **esclusivamente** librerie con licenze permissive (MIT, Apache 2.0, BSD). Qualsiasi libreria sotto licenza GPL, AGPL o simili è severamente vietata per mantenere il progetto libero da vincoli di rilascio open source forzato.
- **Gestore di Pacchetti:** Si utilizza `uv` (invece del classico `pip`) per la massima velocità e gestione riproducibile degli ambienti virtuali Python.
