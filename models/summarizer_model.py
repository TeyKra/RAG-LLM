# models/summarizer_model.py
from transformers import pipeline
import torch

class SummarizerModel:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialise un modèle de summarization
        """
        self.device = 0 if torch.cuda.is_available() else -1
        self.summarizer = pipeline("summarization", 
                                   model=model_name, 
                                   device=self.device)

    def summarize(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """
        Retourne un résumé du texte fourni
        """
        summary = self.summarizer(
            text, 
            max_length=max_length, 
            min_length=min_length, 
            do_sample=False
        )
        return summary[0]["summary_text"]
