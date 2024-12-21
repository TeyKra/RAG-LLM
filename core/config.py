# core/config.py
import os

class Config:
    # On peut charger des variables d'environnement ou utiliser des valeurs par défaut
    ENV = os.getenv("ENV", "production")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "faiss_index")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

config = Config()
