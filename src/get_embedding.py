from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_function():
    """
    Returns the Hugging Face embedding function.
    The model 'all-mpnet-base-v2' provides high-quality encodings
    for semantic similarity tasks.
    """
    # Create an embedding object using the HuggingFaceEmbeddings class
    # with the 'sentence-transformers/all-mpnet-base-v2' model.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    
    # Return the configured embeddings object for use in other parts of the application.
    return embeddings
