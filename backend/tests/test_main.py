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


def test_upload_document():
    """Verifica che l'API riesca a ricevere e leggere un file di testo"""
    file_content = b"Roma e' la capitale d'Italia."
    files = {"file": ("documento.txt", file_content, "text/plain")}
    response = client.post("/api/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "filename" in data
    assert data["filename"] == "documento.txt"
    assert data["message"] == "File caricato con successo"
