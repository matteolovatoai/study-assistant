import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

chroma_client = chromadb.PersistentClient(path="./chroma_db")

documents = chroma_client.get_or_create_collection(name="documenti")


def generate_ai_response(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=prompt
    )
    return response.text or "Errore: Il modello non ha generato una risposta."


def chunk_text(text: str, chunk_size: int = 1000) -> list[str]:
    """crea chunk fissi e ne ritorna una lista"""
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
