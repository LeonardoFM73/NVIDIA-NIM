from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__)
CORS(app)

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

def build_profile_prompt():
    with open("cv.json") as f:
        cv = json.load(f)

    # Formatkan profil ke string yang enak dibaca LLM
    text = f"""
Berikut adalah data portfolio Leonardo Fajar Mardika:

- Nama: {cv["name"]}
- Title: {cv["title"]}
- Pendidikan: {cv["education"]["degree"]} di {cv["education"]["university"]} ({cv["education"]["period"]}, GPA: {cv["education"]["gpa"]})

Keahlian Utama:
{', '.join(cv["skills"])}

Pengalaman Kerja:
"""
    for job in cv["work_experience"]:
        text += f"""
• {job["role"]} di {job["company"]}, {job["location"]} ({job["period"]})
  - {'; '.join(job["details"])}
"""

    text += f"""

Proyek Utama: {', '.join(cv["projects"])}

Hobi & Minat: {', '.join(cv["interests"])}
"""

    return text

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")

    profile_text = build_profile_prompt()

    system_content = f"""
Kamu adalah AI Assistant yang sangat fasih berbahasa Indonesia.
Tugasmu adalah menjawab semua pertanyaan umum yang diberikan dan juga pertanyaan tentang portfolio Leonardo Fajar Mardika berdasarkan data berikut:

{profile_text}

Jawablah dengan sopan, profesional, ringkas namun tetap detail sesuai data di atas.
"""

    payload = {
        "model": "nvidia/llama-3.3-nemotron-super-49b-v1",
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 4096,
        "temperature": 0.6
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NVIDIA_API_KEY}"
    }

    print("DEBUG - Sending to NVIDIA:", payload)
    print("DEBUG - With headers:", headers)

    response = requests.post(NVIDIA_URL, json=payload, headers=headers)
    print("DEBUG - NVIDIA returned:", response.status_code, response.text)

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
