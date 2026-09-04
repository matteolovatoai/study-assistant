import uuid

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

chroma_client = chromadb.PersistentClient(path="./chroma_db")

google_ef = embedding_functions.GoogleGeminiEmbeddingFunction(
    model_name="gemini-embedding-001",
    task_type="RETRIEVAL_DOCUMENT",
)

collection = chroma_client.get_or_create_collection(
    name="documenti",
    embedding_function=google_ef,  # type: ignore
)


def generate_ai_response(prompt: str) -> str:
    # 1. Cerchiamo nel database i pezzetti di documento relativi alla domanda
    risultati = collection.query(
        query_texts=[prompt],
        n_results=2,  # Prendiamo i 2 frammenti più rilevanti
    )

    # 2. Estraiamo il testo (aggiungendo il nostro type narrowing per sicurezza)
    assert risultati["documents"] is not None
    documenti_trovati = risultati["documents"][0]

    # 3. Uniamo i frammenti trovati in un unico grande testo
    contesto = "\n".join(documenti_trovati)

    # 4. Creiamo il super-prompt (RAG = Retrieval-Augmented Generation)
    prompt_aumentato = f"""
        Sei un assistente allo studio. Rispondi alla domanda dell'utente
        basandoti SOLO sul seguente contesto.
        Se la risposta non è nel contesto, di' 'non lo so'.

        CONTESTO:
        {contesto}

        DOMANDA: {prompt}
        """

    # 5. Mandiamo il super-prompt a Gemini
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=prompt_aumentato
    )

    return response.text or "Errore: Il modello non ha generato una risposta."


def chunk_text(text: str, chunk_size: int = 1000) -> list[str]:
    """crea chunk fissi e ne ritorna una lista"""
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def store_chunks(chunks: list[str], filename: str = "doc"):
    """Salva i chunk in ChromaDB con un ID univoco"""
    ids = [f"{filename}_{uuid.uuid4()}" for _ in chunks]
    collection.add(ids=ids, documents=chunks)
