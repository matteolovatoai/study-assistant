from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()


def generate_ai_response(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite", contents=prompt
    )
    return response.text or "Errore: Il modello non ha generato una risposta."


def chunk_text(text: str, chunk_size: int = 1000) -> list[str]:
    return [""]
