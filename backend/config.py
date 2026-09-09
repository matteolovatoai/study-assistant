from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field(default="", min_length=1)
    CHROMA_DB_PATH: Path = Path("./chroma_db")
    GEMINI_MODEL: str = "gemini-3.1-flash-lite"
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"

    model_config = SettingsConfigDict(
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignora altre variabili d'ambiente non definite qui
    )


from functools import lru_cache


@lru_cache
def get_settings():
    return Settings()
