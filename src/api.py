from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import traceback

# Create a Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) if you expect cross-origin requests
CORS(app)

# Variables
LLM_SERVICE_POPULATE_URL = "http://llm:5001/populate"
LLM_SERVICE_QUERY_URL = "http://llm:5001/query"

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    """
    API health check endpoint.
    Returns a simple status message to confirm the API is running correctly.
    """
    return jsonify({"status": "ok"}), 200

@app.route("/api/populate", methods=["POST"])
def api_populate():
    """
    Endpoint to populate (and optionally reset) the Chroma database.
    To reset the database, send a JSON payload like: {"reset": true}.
    """
    try:
        # Extract JSON payload from the request
        data = request.get_json(force=True)

        # Faire une requête POST HTTP vers le LLM service
        response = requests.post(LLM_SERVICE_POPULATE_URL, json=data)

        # Respond with a success message
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        # Handle errors and print the stack trace for debugging purposes
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/query", methods=["POST"])
def api_query():
    """
    Endpoint to query the RAG system.
    Expects a JSON payload like: {"query": "..."} and returns the response along with sources.
    """
    try:
        # Extract JSON payload from the request
        data = request.get_json(force=True)
        
        # Faire une requête POST HTTP vers le LLM service
        response = requests.post(LLM_SERVICE_QUERY_URL, json=data)
        
        # Return the response from the LLM service
        return jsonify(response.json()), response.status_code
    except Exception as e:
        # Handle errors and print the stack trace for debugging purposes
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    """
    Entry point of the Flask application.
    By default, Flask listens on port 5000.
    """
    app.run(host="0.0.0.0", port=5002, debug=False)