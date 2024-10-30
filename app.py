import requests
from flask import Flask, render_template, request, jsonify
import json
import logging
import re

app = Flask(__name__)

# Gemini API setup
GEMINI_API_KEY = "AIzaSyCh87P6IHCR2TVINidnDifeybL3CqC_flQ"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

def call_gemini_api(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": {
            "text": prompt
        }
    }
    
    # Send the API request
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=data
    )

    if response.ok:
        try:
            response_json = response.json()
            logging.debug(f"API Response: {response_json}")  # Log the full response for debugging
            
            gemini_response = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response text").strip()
            
            return gemini_response
        except (KeyError, IndexError) as e:
            logging.error(f"Unexpected response format from Gemini API: {e}")
            return "Unexpected response format from Gemini API."
    else:
        logging.error(f"Gemini API error: {response.status_code} {response.text}")
        return "I'm having trouble connecting to the Gemini API."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json.get('command', '').lower()
    response = call_gemini_api(command)
    
    # Extract text and code from response
    code_snippet = None
    response_text = response
    code_match = re.search(r"'''([\s\S]*?)'''", response_text)

    if code_match:
        # Extract code snippet
        code_snippet = code_match.group(1)
        # Remove code snippet from response text
        response_text = response_text.replace(code_match.group(0), '').strip()

    return jsonify({'response': response_text, 'code': code_snippet})

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, port=5001)