
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/message')
def get_message():
    response_data = {
        "message": "Hello from the Python backend! 🚀",
        "status": "success"
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
