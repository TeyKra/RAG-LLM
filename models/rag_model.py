from embeddings.embedder import Embedder
from retriever.retriever import Retriever
from models.summarizer_model import SummarizerModel

class RAGModel:
    def __init__(self, vector_db_path: str, summarizer_model_name: str = "facebook/bart-large-cnn"):
        self.embedder = Embedder()
        self.retriever = Retriever(vector_db_path)
        # On peut configurer la multi-step summarization
        self.summarizer = SummarizerModel(
            model_name=summarizer_model_name,
            max_input_tokens=1024,
            summary_chunk_size=1024,
            second_pass=True
        )

    def answer_query(self, query: str, top_k: int = 3) -> str:
        # 1) Embedding query
        query_embedding = self.embedder.get_text_embedding(query)

        # 2) Retrieve chunks
        retrieved_results = self.retriever.search(query_embedding, k=top_k)
        # Concat chunk texts
        context_text = "\n".join([res[0] for res in retrieved_results])

        # 3) Summarize
        summary = self.summarizer.summarize(context_text)
        return summary
