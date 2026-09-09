from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_validation_error_format():
    """Testa che un errore di validazione Pydantic ritorni il formato standard"""
    # Invia un payload errato a /api/chat (manca il campo obbligatorio 'message')
    response = client.post("/api/chat", json={"chiave_sbagliata": "ciao"})
    
    assert response.status_code == 422
    data = response.json()
    
    # Verifichiamo la nostra struttura "standard"
    assert "error" in data
    assert data["error"]["type"] == "validation_error"
    assert "message" in data["error"]
    assert "details" in data["error"]

def test_http_exception_format():
    """Testa che un HTTPException generico ritorni il formato standard"""
    # Chiamiamo un endpoint inesistente per scatenare un 404
    response = client.get("/api/endpoint-che-non-esiste")
    
    assert response.status_code == 404
    data = response.json()
    
    # Verifichiamo la nostra struttura "standard"
    assert "error" in data
    assert data["error"]["type"] == "http_error"
    assert "Not Found" in data["error"]["message"]
