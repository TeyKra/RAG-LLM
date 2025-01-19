import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from src.get_embedding import get_embedding_function
from langchain_chroma import Chroma
import logging
# Import existing query_rag function
from src.query_data import query_rag

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Affiche les messages à partir du niveau INFO
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)

# Path to the Chroma database and data directory
CHROMA_PATH = "chroma"
DATA_PATH = "data"

def populate(reset=False):
    """
    Populate the Chroma database with document chunks.

    Args:
        reset (bool): If True, clears the database before populating it.
    """
    # Load and process documents, then store them in Chroma
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

def load_documents():
    """
    Load all PDF documents from the specified data directory.

    Returns:
        list[Document]: List of documents loaded from the directory.
    """
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

def split_documents(documents: list[Document]):
    """
    Split documents into smaller chunks for easier processing.

    Args:
        documents (list[Document]): List of documents to split.

    Returns:
        list[Document]: List of document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,  # Maximum size of each chunk
        chunk_overlap=80,  # Overlap between consecutive chunks
        length_function=len,  # Function to measure text length
        is_separator_regex=False,  # Use plain separators
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    """
    Add document chunks to the Chroma database, avoiding duplicates.

    Args:
        chunks (list[Document]): List of document chunks to add.
    """
    # Load or create the local Chroma database
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )

    # Assign unique IDs to chunks
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Fetch existing document IDs from the databasex
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Filter new chunks that are not already in the database
    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        logger.info(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        logger.info("✅ No new documents to add")


def calculate_chunk_ids(chunks):
    """
    Generate unique IDs for document chunks based on their source, page, and index.

    Args:
        chunks (list[Document]): List of document chunks.

    Returns:
        list[Document]: List of chunks with updated metadata containing unique IDs.
    """
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        chunk.metadata["id"] = chunk_id

    return chunks

"""def clear_database():

    Clear the existing Chroma database by deleting its directory.

    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)"""

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    populate(reset=args.reset)