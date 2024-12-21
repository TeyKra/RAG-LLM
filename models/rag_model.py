# models/rag_model.py
from embeddings.embedder import Embedder
from retriever.retriever import Retriever
from models.summarizer_model import SummarizerModel

class RAGModel:
    def __init__(self, vector_db_path: str, summarizer_model_name: str = "facebook/bart-large-cnn"):
        """
        Initialise le pipeline RAG
        """
        self.embedder = Embedder()
        self.retriever = Retriever(vector_db_path)
        self.summarizer = SummarizerModel(model_name=summarizer_model_name)

    def answer_query(self, query: str, top_k: int = 3) -> str:
        # 1) Obtenir embedding de la requête
        query_embedding = self.embedder.get_text_embedding(query)
        # 2) Récupérer les chunks pertinents
        retrieved_results = self.retriever.search(query_embedding, k=top_k)

        # 3) Concaténer le texte des chunks
        #    (on peut pondérer par le score si on veut)
        context_text = "\n".join([res[0] for res in retrieved_results])

        # 4) Summarizer du contexte
        summary = self.summarizer.summarize(context_text)
        return summary
