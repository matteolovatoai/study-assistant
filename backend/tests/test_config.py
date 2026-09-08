from pathlib import Path

import pytest
from config import Settings
from pydantic import ValidationError


def test_settings_override_via_env(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "override_key")
    monkeypatch.setenv("CHROMA_DB_PATH", "/custom/path")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-pro")

    settings = Settings()

    assert settings.GEMINI_API_KEY == "override_key"
    assert settings.CHROMA_DB_PATH == Path("/custom/path")
    assert settings.GEMINI_MODEL == "gemini-pro"


def test_settings_default_values(monkeypatch):
    # Dobbiamo assicurarci che GEMINI_API_KEY sia impostata,
    # altrimenti la validazione fallirà prima di poter controllare i default
    monkeypatch.setenv("GEMINI_API_KEY", "test_key_123")

    settings = Settings()

    assert settings.GEMINI_API_KEY == "test_key_123"
    assert settings.CHROMA_DB_PATH == Path("./chroma_db")
    assert settings.GEMINI_MODEL == "gemini-3.1-flash-lite"
    assert settings.GEMINI_EMBEDDING_MODEL == "gemini-embedding-001"


def test_settings_missing_api_key(monkeypatch):
    # Assicuriamoci che l'API_KEY non sia presente nell'ambiente
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(ValidationError) as exc_info:
        # Usiamo un dizionario in una variabile separata per non far arrabbiare né Pyright né Ruff
        kwargs: dict = {"_env_file": None}
        Settings(**kwargs)

    # Verifichiamo che l'errore indichi specificamente che manca GEMINI_API_KEY
    assert "GEMINI_API_KEY" in str(exc_info.value)
