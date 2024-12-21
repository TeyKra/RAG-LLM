# embeddings/embedder.py
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

class Embedder:
    def __init__(self, 
                 text_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
                 image_model_name: str = "openai/clip-vit-base-patch32"):
        """
        Initialise deux modèles :
          - un modèle de embeddings texte (SentenceTransformers)
          - un modèle CLIP pour images
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Modèle pour le texte
        self.text_model = SentenceTransformer(text_model_name, device=self.device)

        # Modèle pour les images (CLIP)
        self.image_model = CLIPModel.from_pretrained(image_model_name).to(self.device)
        self.clip_processor = CLIPProcessor.from_pretrained(image_model_name)

    def get_text_embedding(self, text: str) -> np.ndarray:
        """
        Génère l'embedding d'un texte
        """
        embedding = self.text_model.encode(text, show_progress_bar=False)
        return embedding

    def get_image_embedding(self, image_path: str) -> np.ndarray:
        """
        Génère l'embedding d'une image via CLIP
        """
        image = Image.open(image_path).convert("RGB")
        inputs = self.clip_processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.image_model.get_image_features(**inputs)
        embedding = outputs[0].cpu().numpy()
        return embedding
