import pytest
from chat_history import ChatHistory


@pytest.fixture
def history_db():
    # Passiamo :memory: così il DB è finto e svanisce dopo il test
    db = ChatHistory(db_path=":memory:")
    yield db
    db.close()  # Buona pratica chiudere la connessione


def test_chat_history_flow(history_db):
    session_id = "test-session-123"

    # 1. All'inizio la cronologia deve essere vuota
    messages = history_db.get_messages(session_id)
    assert len(messages) == 0

    # 2. Aggiungiamo una domanda dell'utente
    history_db.add_message(session_id, "user", "Qual è la capitale dell'Italia?")

    # 3. Aggiungiamo la risposta dell'AI
    history_db.add_message(session_id, "ai", "La capitale dell'Italia è Roma.")

    # 4. Recuperiamo la cronologia aggiornata
    messages = history_db.get_messages(session_id)

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["message"] == "Qual è la capitale dell'Italia?"
    assert messages[1]["role"] == "ai"
    assert messages[1]["message"] == "La capitale dell'Italia è Roma."
