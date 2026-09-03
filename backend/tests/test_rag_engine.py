from dotenv import load_dotenv

# Carichiamo le variabili dal file .env prima di eseguire i test
load_dotenv()


def test_chunk_text():
    """Verifica che un testo lungo venga spezzettato in chunk piu' piccoli"""
    from rag_engine import chunk_text

    long_text = "A" * 100
    chunks = chunk_text(long_text, chunk_size=50)

    assert isinstance(chunks, list)
    assert len(chunks) == 2
    assert len(chunks[0]) == 50


def test_store_and_query_chunks():
    """Verifica il salvataggio su chromaDB e la ricerca semantica"""
    from rag_engine import collection, store_chunks

    if collection.count() > 0:
        collection.delete(collection.get()["ids"])

    chunks = ["Il cielo è blu", "L'erba è verde", "Il sole è giallo"]

    store_chunks(chunks)

    assert collection.count() == 3

    results = collection.query(query_texts="Di che colore e' il prato?", n_results=1)
    assert results["documents"] is not None
    found_document = results["documents"][0][0]
    assert "erba" in found_document.lower()
