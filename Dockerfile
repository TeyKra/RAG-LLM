# Dockerfile
FROM python:3.9-slim

# 1. Installer dépendances système (pour pdf, etc.)
RUN apt-get update && apt-get install -y \
    libpoppler-cpp-dev \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# 2. Créer un répertoire de travail
WORKDIR /app

# 3. Copier les fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copier tout le code
COPY . /app

# 5. Définir la commande par défaut (exemple pour Streamlit ou FastAPI)
CMD ["streamlit", "run", "app/main.py", "--server.port=80", "--server.address=0.0.0.0"]
