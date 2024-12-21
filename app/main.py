# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.config import config
from core.logger import get_logger
from models.rag_model import RAGModel

app = FastAPI(title="RAG LLM Production API")
logger = get_logger(__name__)

# On initialise la RAGModel (réutilisation du vecteur store en mémoire)
rag_model = RAGModel(vector_db_path=config.VECTOR_DB_PATH)

class QueryPayload(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "RAG LLM API is running!"}

@app.post("/summarize")
def summarize(payload: QueryPayload):
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    logger.info(f"Received query: {query}")
    try:
        answer = rag_model.answer_query(query)
        return {"query": query, "summary": answer}
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while summarizing.")
