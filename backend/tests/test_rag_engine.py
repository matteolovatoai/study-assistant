import chromadb
import pytest
from chromadb.utils import embedding_functions
from config import Settings
from rag_engine import RagEngine


# Creiamo una fixture pytest per avere un RagEngine "usa e getta" e sicuro per i test
@pytest.fixture
def test_engine(monkeypatch):
    # 1. Iniettiamo finti parametri nell'ambiente per superare la validazione
    monkeypatch.setenv("GEMINI_API_KEY", "finta_api_key")

    # 2. Intercettiamo la creazione del client persistente di ChromaDB
    # in modo che restituisca un client effimero (in memoria),
    # così non scriviamo mai su disco durante i test.
    monkeypatch.setattr(
        chromadb, "PersistentClient", lambda path: chromadb.EphemeralClient()
    )

    # 3. Mockiamo la funzione di embedding per evitare chiamate vere a Google
    # quando ChromaDB salva i documenti e cerca di calcolare i vettori.
    class MockEmbeddingFunction:
        def __init__(self, **kwargs):
            pass

        def __call__(self, input):
            # Restituiamo un vettore finto per ogni stringa in input
            return [[0.1, 0.2, 0.3] for _ in input]

        def embed_query(self, input):
            return self(input)

        def name(self):
            return "default"

    monkeypatch.setattr(
        embedding_functions,
        "GoogleGeminiEmbeddingFunction",
        MockEmbeddingFunction,
    )

    # Inizializziamo le impostazioni (che leggeranno le variabili mockate)
    test_settings = Settings()

    # Inizializziamo il motore che userà il client in memoria
    return RagEngine(test_settings)


def test_chunk_text(test_engine):
    """Verifica che un testo lungo venga spezzettato in chunk piu' piccoli"""
    long_text = "A" * 100
    chunks = test_engine.chunk_text(long_text, chunk_size=50)

    assert isinstance(chunks, list)
    assert len(chunks) == 2
    assert len(chunks[0]) == 50


def test_store_and_query_chunks(test_engine, monkeypatch):
    """Verifica il salvataggio su ChromaDB e simula l'interrogazione RAG"""

    # Simuliamo il comportamento della chiamata a Gemini
    # così da evitare di fare vere richieste HTTP a pagamento
    def mock_generate_content(model, contents):
        class MockResponse:
            text = "Ho letto nel contesto che l'erba è verde."

        return MockResponse()

    # Usiamo monkeypatch per sostituire il metodo invece dell'intera property
    monkeypatch.setattr(
        test_engine.client.models, "generate_content", mock_generate_content
    )

    # Dati in pasto a Chroma
    chunks = ["Il cielo è blu", "L'erba è verde", "Il sole è giallo"]
    test_engine.store_chunks(chunks)

    # Verifica che siano stati salvati tutti e 3
    assert test_engine.collection.count() == 3

    # Verifica che la logica interna di `generate_ai_response`
    # riesca ad andare a buon fine e restituire il testo mockato.
    # NB: Non potremo verificare l'esatta correttezza del retrieval vettoriale
    # perché l'embedding function finta usata da Chroma potrebbe non essere accurata senza API key.
    response_text = test_engine.generate_ai_response("Di che colore e' il prato?")
    assert "verde" in response_text


@pytest.mark.parametrize("extension", ["pdf", "txt"])
def test_extract_text_from_file(extension, test_engine, monkeypatch):
    """Verifica che il testo venga estratto correttamente dai vari formati usando i byte"""
    from pathlib import Path

    # Mock della risposta di Gemini per i PDF
    class MockResponse:
        text = f"Questo e un {extension} mockato da Gemini."

    def mock_generate_content(*args, **kwargs):
        return MockResponse()

    # Intercettiamo la chiamata a Gemini per l'estrazione PDF
    monkeypatch.setattr(
        test_engine.client.models, "generate_content", mock_generate_content
    )

    file_path = Path(f"tests/test_data/dummy.{extension}").resolve()

    # Leggiamo il file come farebbe FastAPI (bytes in memoria)
    file_bytes = file_path.read_bytes()
    filename = f"dummy.{extension}"

    # Chiamiamo la funzione (ora d'istanza)
    extracted_text = test_engine.extract_text(file_bytes, filename)

    assert isinstance(extracted_text, str)
    assert len(extracted_text) > 0
    assert "questo e un" in extracted_text.lower()
    assert extension in extracted_text.lower()
