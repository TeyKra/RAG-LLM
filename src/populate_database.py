import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from src.get_embedding import get_embedding_function
from langchain_chroma import Chroma
import logging
# Import the existing query_rag function
from src.query_data import query_rag

# Configure logging to display messages at the INFO level and above.
logging.basicConfig(
    level=logging.INFO,  # Display log messages starting at INFO level
    format="%(asctime)s [%(levelname)s] %(message)s"  # Log message format with timestamp, level, and message
)

logger = logging.getLogger(__name__)

# Define paths for the Chroma database and the directory containing data
CHROMA_PATH = "chroma"
DATA_PATH = "data"

def populate(reset=False):
    """
    Populate the Chroma database with document chunks.

    Args:
        reset (bool): If True, clears the database before populating it.
    """
    # Load documents from the data directory
    documents = load_documents()
    # Split the loaded documents into smaller chunks
    chunks = split_documents(documents)
    # Add the chunks to the Chroma database
    add_to_chroma(chunks)

def load_documents():
    """
    Load all PDF documents from the specified data directory.

    Returns:
        list[Document]: List of documents loaded from the directory.
    """
    # Create a loader for PDF documents from the DATA_PATH directory
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    # Load and return the documents
    return document_loader.load()

def split_documents(documents: list[Document]):
    """
    Split documents into smaller chunks for easier processing.

    Args:
        documents (list[Document]): List of documents to split.

    Returns:
        list[Document]: List of document chunks.
    """
    # Create a text splitter that breaks text into chunks of up to 800 characters
    # with an overlap of 80 characters between chunks.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,      # Maximum size of each chunk
        chunk_overlap=80,    # Overlap between consecutive chunks
        length_function=len, # Function to measure text length
        is_separator_regex=False,  # Use plain string separators
    )
    # Split the documents and return the resulting chunks
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    """
    Add document chunks to the Chroma database, avoiding duplicates.

    Args:
        chunks (list[Document]): List of document chunks to add.
    """
    # Load or create the local Chroma database using the specified persist directory and embedding function.
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )

    # Generate unique IDs for each chunk based on its source, page, and index.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Fetch the existing document IDs from the database.
    # The "get" method returns a dictionary where the "ids" key contains the list of document IDs.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Filter out the chunks that are already present in the database.
    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        logger.info(f"👉 Adding new documents: {len(new_chunks)}")
        # Extract IDs for the new chunks.
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        # Add the new chunks to the Chroma database using their unique IDs.
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

    # Iterate over each chunk to assign a unique ID.
    for chunk in chunks:
        # Retrieve the source and page information from the chunk's metadata.
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        # Create an identifier for the current page based on its source and page number.
        current_page_id = f"{source}:{page}"

        # If the current page is the same as the previous one, increment the chunk index.
        # Otherwise, reset the chunk index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Construct a unique chunk ID by combining the page ID and the chunk index.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        # Update the last page ID for comparison in the next iteration.
        last_page_id = current_page_id
        # Store the unique ID in the chunk's metadata.
        chunk.metadata["id"] = chunk_id

    return chunks

# The following function is commented out.
# It would clear the existing Chroma database by deleting its directory.
"""def clear_database():
    # Clear the existing Chroma database by deleting its directory.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)"""

if __name__ == "__main__":
    # Parse command-line arguments.
    parser = argparse.ArgumentParser()
    # Add an argument to reset the database.
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    # Populate the Chroma database with document chunks, optionally resetting it.
    populate(reset=args.reset)
