import os
import uuid

import chromadb
import pypdfium2 as pdfium
from chromadb.utils import embedding_functions
from config import Settings
from google import genai
from google.genai import errors


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

    def extract_text(self, file_bytes: bytes, file_name: str) -> str:
        """Estrae il testo da un file PDF (usando Gemini Vision) o TXT"""
        if file_name.endswith(".pdf"):
            import typing
            from itertools import batched

            pdf = pdfium.PdfDocument(file_bytes)
            all_text = []

            # Batch di 10 immagini per chiamata per rispettare i Rate Limits
            for batch_index, page_batch in enumerate(batched(pdf, 10), start=1):
                batch_images: list[typing.Any] = []
                for page in page_batch:
                    pil_image = page.render(scale=2).to_pil()
                    batch_images.append(pil_image)

                prompt = (
                    f"Ti sto fornendo {len(batch_images)} slide/pagine consecutive di un documento PDF. "
                    "Per ogni immagine, estrai tutto il testo educativo in formato Markdown. "
                    "Ignora numeri di pagina, loghi ripetitivi e intestazioni ricorrenti. "
                    "Se ci sono grafici o tabelle, descrivili in modo chiaro. "
                    "REGOLE TASSATIVE PER IL CODICE: Se vedi degli snippet di codice sorgente (es. Python, SQL, Java), "
                    "NON descriverli a parole. Devi trascriverli e ricopiarli ESATTAMENTE riga per riga, "
                    "mantenendo l'indentazione originale e racchiudendoli nei classici blocchi di codice Markdown (```). "
                    "Separa chiaramente il contenuto di ogni pagina."
                )

                contents: list[typing.Any] = [prompt]
                contents.extend(batch_images)

                try:
                    response = self.client.models.generate_content(
                        model=self.settings.GEMINI_MODEL,
                        contents=contents,  # type: ignore
                    )
                    if response.text:
                        all_text.append(response.text.strip())
                except errors.APIError as e:
                    print(
                        f"Errore API durante l'estrazione multimodale del batch {batch_index}: {e}"
                    )
                except ValueError as e:
                    print(
                        f"Errore di validazione durante l'estrazione multimodale del batch {batch_index}: {e}"
                    )

            return "\n\n".join(all_text)
        elif file_name.endswith(".txt"):
            return file_bytes.decode("utf-8")
        else:
            raise ValueError("Formato di file non supportato. Usa PDF o TXT.")
