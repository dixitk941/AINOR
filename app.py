import requests
from flask import Flask, render_template, request, jsonify
import json
import logging

app = Flask(__name__)

# Initialize a list to store all responses
all_responses = []

# Gemini API setup
GEMINI_API_KEY = "AIzaSyCh87P6IHCR2TVINidnDifeybL3CqC_flQ"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

def call_gemini_api(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
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
            print("API Response:", response_json)  # Debugging line to check response structure
            
            # Extract the relevant text based on the provided structure
            gemini_response = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response text").strip()
            
            # Log the response
            log_response(prompt, gemini_response)
            
            return gemini_response
        except (KeyError, IndexError):
            logging.error("Unexpected response format from Gemini API.")
            return "Unexpected response format from Gemini API."
    else:
        logging.error(f"Gemini API error: {response.status_code} {response.text}")
        return "I'm having trouble connecting to the Gemini API."


# Function to log responses
def log_response(prompt, response_text):
    response_data = {"prompt": prompt, "response": response_text}
    all_responses.append(response_data)
    
    # Optionally, write responses to a JSON file for persistence
    with open('gemini_responses.json', 'w') as file:
        json.dump(all_responses, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json.get('command', '').lower()
    response = call_gemini_api(command)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5001)