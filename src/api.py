from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import traceback

# Create a Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) to allow requests from different origins
CORS(app)

# Define service URLs for the LLM service endpoints
LLM_SERVICE_POPULATE_URL = "http://llm:5001/populate"
LLM_SERVICE_QUERY_URL = "http://llm:5001/query"

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    """
    Health check endpoint for the API.
    Returns a simple status message confirming that the API is running correctly.
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

        # Make an HTTP POST request to the LLM service for population
        response = requests.post(LLM_SERVICE_POPULATE_URL, json=data)

        # Return the JSON response from the LLM service along with its HTTP status code
        return jsonify(response.json()), response.status_code

    except Exception as e:
        # In case of errors, print the stack trace for debugging purposes
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
        
        # Make an HTTP POST request to the LLM service for querying
        response = requests.post(LLM_SERVICE_QUERY_URL, json=data)
        
        # Return the JSON response from the LLM service along with its HTTP status code
        return jsonify(response.json()), response.status_code

    except Exception as e:
        # In case of errors, print the stack trace for debugging purposes
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    """
    Entry point of the Flask application.
    The application listens on all network interfaces (0.0.0.0) and port 5002.
    """
    app.run(host="0.0.0.0", port=5002, debug=False)
