# models/summarizer_model.py
from transformers import pipeline
import torch

class SummarizerModel:
    def __init__(
        self,
        model_name: str = "facebook/bart-large-cnn",
        max_input_tokens: int = 1024,
        summary_chunk_size: int = 1024,  # Nombre max de tokens pour le chunk
        second_pass: bool = True  # Si True, on fait une 2e passe pour résumer les résumés
    ):
        """
        Initialise un pipeline Bart pour la summarization.
        - max_input_tokens : la limite de tokens pour Bart (environ 1024).
        - summary_chunk_size : on va découper le texte en segments de cette taille (en tokens).
        - second_pass : si on fait un 2e résumé global après avoir résumé chaque chunk.
        """
        self.device = 0 if torch.cuda.is_available() else -1
        self.summarizer = pipeline("summarization", model=model_name, device=self.device)
        self.max_input_tokens = max_input_tokens
        self.summary_chunk_size = summary_chunk_size
        self.second_pass = second_pass

    def _chunk_text_by_tokens(self, text: str) -> list[str]:
        """
        Découpe 'text' en sous-chunks de taille self.summary_chunk_size (en tokens).
        """
        tokens = text.split()
        chunks = []
        start = 0
        while start < len(tokens):
            chunk = tokens[start:start + self.summary_chunk_size]
            chunk_str = " ".join(chunk)
            chunks.append(chunk_str)
            start += self.summary_chunk_size
        return chunks

    def _summarize_single_chunk(self, text: str, max_length=150, min_length=30) -> str:
        """
        Résume un chunk (déjà <= summary_chunk_size tokens).
        """
        # On re-tronque ici si jamais ça dépasse (sécurité).
        tokens = text.split()
        if len(tokens) > self.max_input_tokens:
            tokens = tokens[:self.max_input_tokens]
            text = " ".join(tokens)

        result = self.summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        return result[0]["summary_text"]

    def summarize(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """
        Summarize potentially long text by chunking (multi-step approach).
        1. Split the text into sub-chunks.
        2. Summarize each chunk => get partial summaries.
        3. (optionally) Summarize the concatenation of partial summaries.
        """
        # 1) Chunk text
        chunks = self._chunk_text_by_tokens(text)

        # 2) Summarize each chunk
        partial_summaries = []
        for chunk in chunks:
            summary_chunk = self._summarize_single_chunk(chunk, max_length, min_length)
            partial_summaries.append(summary_chunk)

        # 3) Optionnel : 2e passe
        if self.second_pass and len(partial_summaries) > 1:
            combined_text = " ".join(partial_summaries)
            # On peut limiter la longueur du 2e résumé (max_length)
            final_summary = self._summarize_single_chunk(combined_text, max_length=200, min_length=50)
            return final_summary
        else:
            # S'il n'y a qu'un chunk ou second_pass=False, on renvoie directement
            return partial_summaries[0] if partial_summaries else ""
