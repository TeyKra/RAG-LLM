# tests/test_ingestion.py
import pytest
from ingestion.data_ingestion import chunk_text

def test_chunk_text():
    text = "Lorem ipsum" * 300
    chunks = chunk_text(text, 1000, 100)
    assert len(chunks) > 0
    # Vérifier que la taille de chaque chunk ≤ 1000
    for c in chunks:
        assert len(c) <= 1000
