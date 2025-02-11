from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_function():
    """
    Returns a Hugging Face embedding function.
    The model 'all-mpnet-base-v2' provides high-quality encodings
    for semantic similarity tasks.
    """
    # Create an embedding object using the HuggingFaceEmbeddings class
    # with the 'sentence-transformers/all-mpnet-base-v2' model.
    # This model is well-suited for generating vector representations of text,
    # which are useful for various NLP tasks such as semantic similarity.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    
    # Return the configured embeddings object so that it can be used in other
    # parts of the application to generate text embeddings.
    return embeddings
