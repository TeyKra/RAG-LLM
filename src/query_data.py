import argparse
import logging
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.schema import Document
from src.get_embedding import get_embedding_function
from googletrans import Translator
import torch

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
CHROMA_PATH = "chroma"  # Path for Chroma's persistent database.
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"  # Nouveau modèle Mistral

PROMPT_TEMPLATE = """
### Instruction:
You are an expert AI assistant specialized in retrieving information from documents. 
Use the provided context to answer the question concisely and accurately. 
Do NOT make up answers.

### Context:
{context}

### Question:
{question}

### Answer:
"""

class ModelLoader:
    """
    Singleton class for managing the loading of a pre-trained language model and tokenizer.
    Ensures that the model and tokenizer are only initialized once.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            
            try:
                device = "cuda" if torch.cuda.is_available() else "cpu"
                
                logger.info(f"Loading tokenizer from checkpoint '{MODEL_NAME}'...")
                cls._instance.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
                logger.info("Tokenizer loaded successfully.")

                logger.info(f"Loading model from checkpoint '{MODEL_NAME}'...")
                cls._instance.model = AutoModelForCausalLM.from_pretrained(
                    MODEL_NAME,
                    device_map="auto",
                    torch_dtype=torch.float16 if device == "cuda" else torch.float32
                )
                logger.info("Model loaded successfully.")

                logger.info("Initializing text generation pipeline...")
                cls._instance.pipeline = pipeline(
                    "text-generation",
                    model=cls._instance.model,
                    tokenizer=cls._instance.tokenizer,
                    max_new_tokens=512,
                    do_sample=True,
                    top_k=30,
                    top_p=0.8,
                    temperature=0.5,
                    pad_token_id=cls._instance.tokenizer.eos_token_id,
                )
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
        translation = translator.translate(text, src='auto', dest='en')
        return translation.text
    except Exception as e:
        logger.error(f"Translation Error: {e}")
        return text


def query_rag(query_text: str) -> str:
    """
    Perform a Retrieval-Augmented Generation (RAG) query to answer a user's question.

    Args:
        query_text (str): The user's input query.

    Returns:
        str: A formatted response containing the generated answer and sources.
    """
    # Load the embedding function and Chroma database.
    embedding_function = get_embedding_function()
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )

    # Retrieve top-k similar documents from the database.
    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Build the prompt using a template.
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=query_text)

    # Generate a response using the preloaded model.
    model_loader = ModelLoader()
    llm = model_loader.pipeline
    response = llm(prompt, max_new_tokens=512, return_full_text=False)

    # Extract the answer portion of the response.
    answer = response[0]['generated_text'].split("### Answer:")[-1].strip()
    
    # Translate the generated answer to English.
    logger.info(f"Generated Response (Before Translation): {answer}")
    translated_answer = translate_to_english(answer)
    logger.info(f"Translated Response: {translated_answer}")

    # Format the response with source information.
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Answer:\n{translated_answer}\n\nSources:\n {sources}"

    # Log the final formatted response and sources.
    logger.info(f"Final Response:\n{formatted_response}")

    return formatted_response

if __name__ == "__main__":
    """
    Entry point for the script. Parses a query from command-line arguments and runs the RAG query.
    """
    parser = argparse.ArgumentParser(description="Query a retrieval-augmented generation system.")
    parser.add_argument("query_text", type=str, help="The query text to process.")
    args = parser.parse_args()
    print(query_rag(args.query_text))