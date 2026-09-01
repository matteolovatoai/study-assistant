import os

from dotenv import load_dotenv
from rag_engine import generate_ai_response

# Carichiamo le variabili dal file .env prima di eseguire i test
load_dotenv()


def test_generate_ai_response():
    """
    Test di Integrazione: verifica che la nostra funzione riesca a
    comunicare con i server di Google e ottenere una risposta reale.
    """
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
