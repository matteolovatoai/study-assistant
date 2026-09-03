import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

chroma_client = chromadb.PersistentClient(path="./chroma_db")


class ModernGoogleEmbedding(EmbeddingFunction):
    def __init__(self) -> None:
        self.client = client

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []

        # Iteriamo su ogni singolo documento (chunk) passato da ChromaDB
        for testo in input:
            response = self.client.models.embed_content(
                model="gemini-embedding-2", contents=testo
            )
            # Estraiamo il vettore di questa specifica stringa
            if response.embeddings and response.embeddings[0].values is not None:
                embeddings.append(response.embeddings[0].values)

        return embeddings


collection = chroma_client.get_or_create_collection(
    name="documenti",
    embedding_function=ModernGoogleEmbedding(),  # type: ignore
)


def generate_ai_response(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=prompt
    )
    return response.text or "Errore: Il modello non ha generato una risposta."


def chunk_text(text: str, chunk_size: int = 1000) -> list[str]:
    """crea chunk fissi e ne ritorna una lista"""
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def store_chunks(chunks: list[str]):
    collection.add(
        ids=[str(i) for i in range(len(chunks))], documents=[chunk for chunk in chunks]
    )
