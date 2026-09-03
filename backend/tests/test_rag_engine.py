import os

from dotenv import load_dotenv

# Carichiamo le variabili dal file .env prima di eseguire i test
load_dotenv()


def test_generate_ai_response():
    """
    Test di Integrazione: verifica che la nostra funzione riesca a
    comunicare con i server di Google e ottenere una risposta reale.
    """
    from rag_engine import generate_ai_response

    # Verifichiamo che la chiave esista (altrimenti il test fallisce subito)
    assert os.getenv("GEMINI_API_KEY") is not None, "API Key non trovata nel file .env!"

    # Facciamo una domanda semplice per testare la connessione
    risposta = generate_ai_response(
        "Dimmi ciao in italiano. Rispondi solo con una parola."
    )

    # Verifichiamo che la risposta non sia vuota
    assert risposta is not None
    assert isinstance(risposta, str)
    assert len(risposta) > 0
    assert "ciao" in risposta.lower()


def test_chunk_text():
    """Verifica che un testo lungo venga spezzettato in chunk piu' piccoli"""
    from rag_engine import chunk_text

    long_text = "A" * 100
    chunks = chunk_text(long_text, chunk_size=50)

    assert isinstance(chunks, list)
    assert len(chunks) == 2
    assert len(chunks[0]) == 50
