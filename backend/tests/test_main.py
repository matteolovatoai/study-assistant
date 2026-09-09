from fastapi.testclient import TestClient
from main import app, get_rag_engine


class MockRagEngine:
    def __init__(self):
        self.memory = []

    def chunk_text(self, text: str, chunk_size: int = 1000) -> list[str]:
        # Logica reale o semplificata
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    def store_chunks(self, chunks: list[str], filename: str = "doc"):
        # Salvataggio finto in memoria
        self.memory.extend(chunks)

    def generate_ai_response(self, prompt: str) -> str:
        # Risposta fittizia controllabile
        return "Risposta generata dal mock RAG!"


# Creiamo un'istanza condivisa per poter ispezionare lo stato interno (opzionale)
mock_engine = MockRagEngine()


def override_get_rag_engine():
    return mock_engine


# Sostituiamo la dipendenza reale con il nostro mock
app.dependency_overrides[get_rag_engine] = override_get_rag_engine

client = TestClient(app)


def test_health_check():
    """Verifica che l'API sia attiva e risponda con status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_document_e2e():
    """Testa l'intero flusso di upload passando dal mock, senza toccare disco/API"""
    file_content = b"Il cielo e' sempre piu' blu."
    files = {"file": ("documento.txt", file_content, "text/plain")}

    response = client.post("/api/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "documento.txt"
    assert data["message"] == "Caricati 1 frammenti nel RAG!"

    # Verifica che il motore mock abbia effettivamente ricevuto i dati
    assert "Il cielo e' sempre piu' blu." in mock_engine.memory[0]


def test_chat_real_e2e():
    """Testa l'endpoint chat verificando che restituisca la risposta del mock."""
    payload = {"message": "Di che colore e' il cielo?"}
    response = client.post("/api/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["reply"] == "Risposta generata dal mock RAG!"
