from flask import Flask, request, jsonify
import argparse
import traceback

# Import functions from your existing scripts
# Ensure the import paths match your folder structure
from src.populate_database import populate
from src.query_data import query_rag

import logging
# Configure Flask logging to capture logs from other modules
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


app = Flask(__name__)

@app.route("/populate", methods=["POST"])
def populate_route():
    try:
        data = request.get_json(force=True)
        reset = data.get("reset", False)
        populate(reset=reset)
        return jsonify({"message": "Database populated successfully", "reset": reset}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/query", methods=["POST"])
def query_route():
    try:
        data = request.get_json(force=True)
        query_text = data.get("query", "").strip()
        if not query_text:
            return jsonify({"error": "Empty query parameter"}), 400

        response = query_rag(query_text)
        return jsonify({"response": response}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)