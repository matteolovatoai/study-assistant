import os
import uuid
from io import BytesIO

import chromadb
from chromadb.utils import embedding_functions
from config import Settings
from google import genai
from google.genai import errors
from pypdf import PdfReader


class RagEngine:
    def __init__(self, settings: Settings):
        self.settings = settings
        # ChromaDB legge la chiave ESCLUSIVAMENTE da os.environ, non accetta parametri diretti
        os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.chroma_client = chromadb.PersistentClient(
            path=str(settings.CHROMA_DB_PATH)
        )

        self.google_ef = embedding_functions.GoogleGeminiEmbeddingFunction(
            model_name=settings.GEMINI_EMBEDDING_MODEL,
            task_type="RETRIEVAL_DOCUMENT",
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name="documenti",
            embedding_function=self.google_ef,  # type: ignore
        )

    def generate_ai_response(
        self, prompt: str, history: list[dict] | None = None
    ) -> str:
        # 1. Cerchiamo nel database i pezzetti di documento relativi alla domanda
        risultati = self.collection.query(
            query_texts=[prompt],
            n_results=2,  # Prendiamo i 2 frammenti più rilevanti
        )

        # 2. Estraiamo il testo (aggiungendo il nostro type narrowing per sicurezza)
        documents = risultati["documents"]
        if documents is None:
            raise RuntimeError("ChromaDB non ha restituito i documenti attesi.")
        documenti_trovati = documents[0]

        # 3. Uniamo i frammenti trovati in un unico grande testo
        contesto = "\n".join(documenti_trovati)
        history_messages = ""
        if history is not None:
            history_messages = "CRONOLOGIA DELLA CONVERSAZIONE:\n"
            for msg in history:
                history_messages += f"{msg['role'].upper()}: {msg['message']}\n"

        # 4. Creiamo il super-prompt (RAG = Retrieval-Augmented Generation)
        prompt_aumentato = f"""
            Sei un assistente allo studio. Rispondi alla domanda dell'utente
            basandoti SOLO sul seguente contesto.
            Se la risposta non è nel contesto, di' 'non lo so'.

            CONTESTO:
            {contesto}
            {history_messages}
            DOMANDA: {prompt}
            """

        # 5. Mandiamo il super-prompt a Gemini e gestiamo eventuali crash di Google
        try:
            response = self.client.models.generate_content(
                model=self.settings.GEMINI_MODEL, contents=prompt_aumentato
            )
            return response.text or "Errore: Il modello non ha generato una risposta."
        except errors.APIError as e:
            print(f"Errore Gemini API: {e}")
            return "Scusa, in questo momento Gemini è a farsi un caffè nei datacenter di Google. Riprova tra un minuto!"

    def chunk_text(self, text: str, chunk_size: int = 1000) -> list[str]:
        """crea chunk fissi e ne ritorna una lista"""
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    def store_chunks(self, chunks: list[str], filename: str = "doc"):
        """Salva i chunk in ChromaDB con un ID univoco"""
        ids = [f"{filename}_{uuid.uuid4()}" for _ in chunks]
        self.collection.add(ids=ids, documents=chunks)

    @staticmethod
    def extract_text(file_bytes: bytes, file_name: str) -> str:
        """Estrae il testo da un file PDF o TXT"""
        if file_name.endswith(".pdf"):
            reader = PdfReader(BytesIO(file_bytes))
            text = "\n".join(page.extract_text() for page in reader.pages)
            return text
        elif file_name.endswith(".txt"):
            return file_bytes.decode("utf-8")
        else:
            raise ValueError("Formato di file non supportato. Usa PDF, DOCX o TXT.")
