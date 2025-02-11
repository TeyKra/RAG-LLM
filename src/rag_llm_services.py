from flask import Flask, request, jsonify
import argparse
import traceback

# Import functions from your existing modules.
# Make sure that the import paths match your project's folder structure.
from src.populate_database import populate  # Function to populate the database
from src.query_data import query_rag         # Function to perform a RAG query

import logging
# Configure logging to capture log messages from this module and others.
logging.basicConfig(
    level=logging.INFO,  # Log messages with level INFO and above
    format="%(asctime)s [%(levelname)s] %(message)s"  # Log format including timestamp and log level
)
logger = logging.getLogger(__name__)

# Create the Flask application instance.
app = Flask(__name__)

@app.route("/populate", methods=["POST"])
def populate_route():
    """
    Route to populate the database.
    Expects a JSON payload with an optional "reset" parameter.
    If "reset" is True, the database will be cleared before populating.
    """
    try:
        # Force parse JSON data from the request body.
        data = request.get_json(force=True)
        # Retrieve the "reset" parameter from the JSON data (default is False).
        reset = data.get("reset", False)
        # Call the populate function with the reset parameter.
        populate(reset=reset)
        # Return a success message along with the reset status.
        return jsonify({"message": "Database populated successfully", "reset": reset}), 200
    except Exception as e:
        # Print the stack trace for debugging if an exception occurs.
        traceback.print_exc()
        # Return an error message and a 500 status code.
        return jsonify({"error": str(e)}), 500

@app.route("/query", methods=["POST"])
def query_route():
    """
    Route to perform a RAG (Retrieval-Augmented Generation) query.
    Expects a JSON payload with a "query" parameter.
    Returns the generated response.
    """
    try:
        # Parse JSON data from the request body.
        data = request.get_json(force=True)
        # Retrieve the query text from the JSON data and remove any extra whitespace.
        query_text = data.get("query", "").strip()
        # If the query text is empty, return a 400 error.
        if not query_text:
            return jsonify({"error": "Empty query parameter"}), 400

        # Perform the RAG query using the imported function.
        response = query_rag(query_text)
        # Return the response in JSON format with a 200 status code.
        return jsonify({"response": response}), 200
    except Exception as e:
        # Print the stack trace for debugging in case of an exception.
        traceback.print_exc()
        # Return an error message and a 500 status code.
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask application on all network interfaces (0.0.0.0) and on port 5001.
    app.run(host="0.0.0.0", port=5001)
