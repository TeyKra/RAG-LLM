from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os

# Initialisation de Flask avec un seul dossier pour tout
app = Flask(
    __name__,
    static_folder="frontend",
    template_folder="frontend"
)

API_BASE_URL = "http://api:5002/api"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    """
    Route pour servir les fichiers statiques (CSS, JS).
    """
    return send_from_directory(os.path.join(app.root_path, "frontend"), filename)

@app.route("/populate", methods=["POST"])
def populate():
    """
    Envoie une requête pour peupler la base de données.
    """
    try:
        reset = request.form.get("reset", "false").lower() == "true"
        payload = {"reset": reset}
        response = requests.post(f"{API_BASE_URL}/populate", json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/query", methods=["POST"])
def query():
    """
    Envoie une requête pour interroger la base de données.
    """
    try:
        query_text = request.form.get("query")
        payload = {"query": query_text}
        response = requests.post(f"{API_BASE_URL}/query", json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
