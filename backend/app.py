# backend/app.py

from flask import Flask, jsonify

# Initialize the Flask application
app = Flask(__name__)

@app.route('/api/message')
def get_message():
    """
    This is an API endpoint. When a request is made to /api/message,
    this function will be executed.
    """
    # Create a Python dictionary for our response.
    response_data = {
        "message": "Hello from the Python backend! 🚀",
        "status": "success"
    }
    # Flask's jsonify function converts the dictionary to a JSON response.
    return jsonify(response_data)

# This block is not strictly necessary when using Gunicorn,
# but it's good practice for local development without Docker.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
