# app.py
import os
import sys
# Ajouter explicitement le chemin de la racine du projet au PYTHONPATH
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

import streamlit as st
from ingestion.data_ingestion import ingest_data
from models.rag_model import RAGModel

VECTOR_DB_PATH = "faiss_index"  # On stockera "faiss_index.faiss" et "faiss_index_texts.txt"

def main():
    st.title("RAG LLM Multimodal - Résumé de PDF")
    st.write("Exemple de pipeline local pour récupérer et résumer du contenu PDF (texte, tableaux, images).")

    # Bouton pour lancer l'ingestion
    if st.button("Lancer l'ingestion des données"):
        with st.spinner("Ingestion en cours..."):
            data_dir = os.path.join(os.getcwd(), "data")
            ingest_data(data_dir, VECTOR_DB_PATH)
        st.success("Ingestion terminée !")

    # Saisie de la requête
    query = st.text_input("Entrez votre requête / question :")

    if st.button("Obtenir un résumé"):
        if not query.strip():
            st.warning("Veuillez saisir une requête.")
        else:
            with st.spinner("Recherche des passages pertinents & génération du résumé..."):
                rag_model = RAGModel(VECTOR_DB_PATH)
                response = rag_model.answer_query(query)
            st.subheader("Résumé / Réponse :")
            st.write(response)

if __name__ == "__main__":
    main()
