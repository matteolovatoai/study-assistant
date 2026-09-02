from fastapi.testclient import TestClient
from main import app

# Il TestClient permette di simulare richieste HTTP senza avviare il server
client = TestClient(app)


def test_health_check():
    """Verifica che l'API sia attiva e risponda con status ok."""
    response = client.get("/health")

    # Assert controlla che una condizione sia vera. Se è falsa, il test fallisce.
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_char_real():
    """Verifica che l'API restituisca una risposta generata da Gemini."""
    payload = {"message": "Rispondi solo con la parola 'Pomodoro'"}
    response = client.post("/api/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "pomodoro" in data["reply"].lower()
