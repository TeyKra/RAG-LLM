# retriever/retriever.py
import faiss
import numpy as np
import os

class Retriever:
    def __init__(self, index_path: str, dimension: int = 384):
        """
        index_path : base du chemin (ex: "faiss_index") 
                     => on stockera "faiss_index.faiss" et "faiss_index_texts.txt"
        dimension : dimension des embeddings (ex. 384 pour all-MiniLM-L6-v2)
        """
        self.index_path = index_path
        self.dimension = dimension
        self.index = None
        self.texts = []

        # Chargement existant si présent
        if os.path.exists(self.index_path + ".faiss"):
            self._load_index()
        else:
            self.index = faiss.IndexFlatIP(self.dimension)

    def add_document(self, text: str, embedding: np.ndarray):
        if len(embedding.shape) == 1:
            embedding = np.array([embedding])
        if self.index is None:
            self.index = faiss.IndexFlatIP(self.dimension)
        # On caste en float32 pour FAISS
        self.index.add(embedding.astype(np.float32))
        self.texts.append(text)

    def search(self, query_embedding: np.ndarray, k: int = 3):
        if len(query_embedding.shape) == 1:
            query_embedding = np.array([query_embedding])
        scores, indexes = self.index.search(query_embedding.astype(np.float32), k)
        results = []
        # On peut renvoyer (chunk, score)
        for i, idx in enumerate(indexes[0]):
            text_chunk = self.texts[idx]
            score = scores[0][i]
            results.append((text_chunk, float(score)))
        return results

    def save_index(self):
        # Sauvegarde l'index
        faiss.write_index(self.index, self.index_path + ".faiss")
        # Sauvegarde des textes correspondants
        with open(self.index_path + "_texts.txt", "w", encoding="utf-8") as f:
            for t in self.texts:
                # On retire les \n
                f.write(t.replace("\n", " ") + "\n")

    def _load_index(self):
        self.index = faiss.read_index(self.index_path + ".faiss")
        # Chargement des textes
        self.texts = []
        with open(self.index_path + "_texts.txt", "r", encoding="utf-8") as f:
            for line in f:
                self.texts.append(line.strip())
