from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")

    payload = {
        "model": "nvidia/llama-3.3-nemotron-super-49b-v1",
        "messages": [
            {"role": "system", "content": "Berbicaralah dalam bahasa Indonesia dan jawablah tentang portfolio Leonardo Fajar Mardika."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 4096,
        "temperature": 0.6
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NVIDIA_API_KEY}"
    }

    response = requests.post(NVIDIA_URL, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
