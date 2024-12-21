rag_llm_multimodal/
├── .github/workflows/ci.yml
├──data/
├──.venv/
├── app/
│   ├── main.py             # Code principal (API)
│   ├── __init__.py         # Ne contient pas de code actuellement
├── core/
│   ├── config.py           # Configuration globale (environnements, etc.)
│   ├── logger.py           # Configuration du logger
│   └── utils.py            # Fonctions utilitaires : Ne contient pas de code actuellement
├── ingestion/
│   ├── pdf_parser.py       # Contient le code fourni sur le premier proof-of-concept avancé fourni
│   └── data_ingestion.py   # Contient le code fourni sur le premier proof-of-concept avancé fourni
├── embeddings/
│   └── embedder.py         # Contient le code fourni sur le premier proof-of-concept avancé fourni
├── models/
│   ├── rag_model.py        # Contient le code fourni sur le premier proof-of-concept avancé fourni
│   └── summarizer_model.py # Contient le code fourni sur le premier proof-of-concept avancé fourni
├── retriever/
│   └── retriever.py        # Contient le code fourni sur le premier proof-of-concept avancé fourni
├── scripts/
│   ├── run_ingestion.sh    # Script shell pour ingestion : Ne contient pas de code actuellement
│   └── run_server.sh       # Script shell pour lancer l'API/app : Ne contient pas de code actuellement
├── tests/
│   ├── test_api.py         # Ne contient pas de code actuellement
│   ├── test_ingestion.py
│   └── ...
├──app.py                   # Contient le code fourni sur le premier proof-of-concept avancé fourni
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
