from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os

# Initialize the Flask application
# The 'static_folder' and 'template_folder' are both set to "frontend", meaning that
# static files (e.g., CSS, JS) and HTML templates will be loaded from the "frontend" directory.
app = Flask(
    __name__,
    static_folder="frontend",
    template_folder="frontend"
)

# Define the base URL for the API endpoints.
# This URL points to the API service running on port 5002.
API_BASE_URL = "http://api:5002/api"

@app.route("/")
def home():
    """
    Render the main homepage.
    This function returns the 'index.html' template located in the "frontend" folder.
    """
    return render_template("index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    """
    Serve static files such as CSS, JavaScript, or images.
    
    The route captures any file path provided after the "/" and serves the corresponding
    file from the "frontend" directory.
    """
    return send_from_directory(os.path.join(app.root_path, "frontend"), filename)

@app.route("/populate", methods=["POST"])
def populate():
    """
    Endpoint to send a request to populate (or optionally reset) the database.
    
    It reads the 'reset' parameter from the form data, constructs a JSON payload,
    and makes a POST request to the API's populate endpoint.
    """
    try:
        # Retrieve the 'reset' parameter from the form data.
        # If not provided, default to "false". The value is then compared to "true" (case-insensitive).
        reset = request.form.get("reset", "false").lower() == "true"
        payload = {"reset": reset}
        
        # Send a POST request to the API populate endpoint with the JSON payload.
        response = requests.post(f"{API_BASE_URL}/populate", json=payload)
        
        # Return the JSON response received from the API.
        return jsonify(response.json())
    except Exception as e:
        # In case of an error, return an error message with a 500 status code.
        return jsonify({"error": str(e)}), 500

@app.route("/query", methods=["POST"])
def query():
    """
    Endpoint to send a request to query the database.
    
    It retrieves the 'query' parameter from the form data, constructs a JSON payload,
    and makes a POST request to the API's query endpoint.
    """
    try:
        # Retrieve the 'query' parameter from the form data.
        query_text = request.form.get("query")
        payload = {"query": query_text}
        
        # Send a POST request to the API query endpoint with the JSON payload.
        response = requests.post(f"{API_BASE_URL}/query", json=payload)
        
        # Return the JSON response received from the API.
        return jsonify(response.json())
    except Exception as e:
        # In case of an error, return an error message with a 500 status code.
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    """
    Entry point of the Flask application.
    The application will run on all network interfaces (0.0.0.0) on port 5003 in debug mode.
    """
    app.run(host="0.0.0.0", port=5003, debug=True)
