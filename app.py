import os
import requests
from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)

# Initialize a list to store all responses (only in memory)
all_responses = []

# Gemini API setup with environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

def call_gemini_api(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    if GEMINI_API_KEY is None:
        return "API key is not set."

    # Send the API request
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=data
    )

    if response.ok:
        try:
            # Inspect response JSON structure
            response_json = response.json()
            gemini_response = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response text").strip()
            
            # Log the response (only in memory)
            log_response(prompt, gemini_response)
            
            return gemini_response
        except (KeyError, IndexError):
            logging.error("Unexpected response format from Gemini API.")
            return "Unexpected response format from Gemini API."
    else:
        logging.error(f"Gemini API error: {response.status_code} {response.text}")
        return "I'm having trouble connecting to the Gemini API."

# Function to log responses (only in memory)
def log_response(prompt, response_text):
    response_data = {"prompt": prompt, "response": response_text}
    all_responses.append(response_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json.get('command', '').lower()
    response = call_gemini_api(command)
    return jsonify({'response': response})

# Only needed for local development
if __name__ == '__main__':
    app.run(debug=True)
