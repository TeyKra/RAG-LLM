import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.schema import Document
from src.get_embedding import get_embedding_function
from googletrans import Translator

import logging
# Configure the logger to display INFO-level messages with a specific format.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
CHROMA_PATH = "chroma"  # Directory path for Chroma's persistent database.

# Template for building the prompt for the language model.
PROMPT_TEMPLATE = """
You are an expert assistant. Use only the following context to answer the user's question.
DO NOT quote or restate the entire context verbatim.
Provide a concise, standalone answer. If the context does not contain enough information, say so.

Context:
{context}

Question:
{question}

Answer:
"""

# (The logger configuration is repeated here, but it ensures that logging is properly set up.)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class ModelLoader:
    """
    Singleton class for managing the loading of a pre-trained language model and tokenizer.
    Ensures that the model and tokenizer are only initialized once.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Create the singleton instance.
            cls._instance = super(ModelLoader, cls).__new__(cls)
            try:
                logger.info("Loading tokenizer from checkpoint 'google/flan-t5-base'...")
                cls._instance.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
                logger.info("Tokenizer loaded successfully.")

                logger.info("Loading model from checkpoint 'google/flan-t5-base'...")
                cls._instance.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
                logger.info("Model loaded successfully.")

                logger.info("Initializing text2text-generation pipeline...")
                cls._instance.pipeline = pipeline(
                    "text2text-generation",
                    model=cls._instance.model,
                    tokenizer=cls._instance.tokenizer,
                    max_new_tokens=200,
                    do_sample=True,
                    top_k=30,
                    top_p=0.8,
                    temperature=0.5,
                    pad_token_id=cls._instance.tokenizer.eos_token_id,
                )
                # Wrap the pipeline with LangChain's HuggingFacePipeline for integration.
                cls._instance.llm = HuggingFacePipeline(pipeline=cls._instance.pipeline)
                logger.info("Pipeline initialized successfully.")
            except Exception as e:
                logger.error(f"Error during model initialization: {e}")
                raise e
        return cls._instance

def translate_to_english(text: str) -> str:
    """
    Translate the given text to English using Google Translate.

    Args:
        text (str): The text to be translated.

    Returns:
        str: The translated text in English or the original text if an error occurs.
    """
    translator = Translator()
    try:
        # Translate from auto-detected language to English.
        translation = translator.translate(text, src='auto', dest='en')
        return translation.text
    except Exception as e:
        print(f"Translation Error: {e}")
        return text

def query_rag(query_text: str) -> str:
    """
    Perform a Retrieval-Augmented Generation (RAG) query to answer a user's question.

    Args:
        query_text (str): The user's input query.

    Returns:
        str: A formatted response containing the generated answer and sources.
    """
    # Load the embedding function.
    embedding_function = get_embedding_function()
    # Initialize or load the Chroma database with the specified persistence directory.
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )

    # Retrieve the top-k (here, 5) similar documents along with their scores.
    results = db.similarity_search_with_score(query_text, k=5)
    # Concatenate the content of the retrieved documents, separated by a divider.
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Build the prompt by filling in the template with the retrieved context and the user's query.
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Get the preloaded language model from the singleton ModelLoader.
    model_loader = ModelLoader()
    llm = model_loader.llm
    # Invoke the language model with the constructed prompt.
    response_text = llm.invoke(prompt)

    # Extract the answer portion from the model's response.
    if "Answer:" in response_text:
        answer = response_text.split("Answer:")[1].strip()
    else:
        answer = response_text.strip()

    # Log the generated answer before translation.
    logger.info(f"Generated Response (Before Translation): {answer}")
    # Translate the answer to English.
    translated_answer = translate_to_english(answer)
    logger.info(f"Translated Response: {translated_answer}")

    # Extract source information from the metadata of the retrieved documents.
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    # Format the final response with the translated answer and the list of source IDs.
    formatted_response = f"Answer:\n{translated_answer}\nSources: {sources}"

    # Log the final formatted response.
    logger.info(f"Final Response:\n{formatted_response}")

    return formatted_response

if __name__ == "__main__":
    """
    Entry point for the script. Parses a query from command-line arguments and runs the RAG query.
    """
    parser = argparse.ArgumentParser(description="Query a retrieval-augmented generation system.")
    parser.add_argument("query_text", type=str, help="The query text to process.")
    args = parser.parse_args()
    query_rag(args.query_text)
