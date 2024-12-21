# ingestion/data_ingestion.py
import os
from typing import List
from ingestion.pdf_parser import parse_pdf
from embeddings.embedder import Embedder
from retriever.retriever import Retriever

CHUNK_SIZE = 800  # Nombre de caractères (ou tokens) par chunk
CHUNK_OVERLAP = 100

def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Découpe le texte en segments.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def ingest_data(data_dir: str, vector_db_path: str):
    """
    Parcourt les PDF, extrait contenu texte, chunk le contenu,
    génère les embeddings et alimente la base vecteur.
    """
    embedder = Embedder()
    retriever = Retriever(vector_db_path)

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(data_dir, file_name)
            parsed = parse_pdf(file_path)

            # On concatène le texte brut + le texte des tableaux
            full_text = parsed["text"]
            for table_str in parsed["tables"]:
                # On peut choisir de préfixer "Table: " pour info
                full_text += "\nTable:\n" + table_str

            # chunk du texte
            chunks = chunk_text(full_text, CHUNK_SIZE, CHUNK_OVERLAP)

            # Ajout dans l’index vectoriel
            for chunk in chunks:
                if chunk.strip():
                    embedding = embedder.get_text_embedding(chunk)
                    retriever.add_document(chunk, embedding)

            # (Optionnel) Gestion des images
            # -> Vous pourriez soit faire de l’OCR dessus, soit des embeddings CLIP, etc.
            # -> Ex: embedder.get_image_embedding(image_path)

    # Sauvegarde de l’index
    retriever.save_index()
    print("Data ingestion completed!")
