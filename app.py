import os
import requests
from flask import Flask, render_template, request, jsonify
import json
import logging

app = Flask(__name__)

# Initialize a list to store all responses
all_responses = []

# Gemini API setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# Set up logging
logging.basicConfig(level=logging.INFO)

def call_gemini_api(prompt):
    if not GEMINI_API_KEY:
        logging.error("API key is missing. Set the GEMINI_API_KEY environment variable.")
        return "API key is missing. Please configure it properly."

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=data
        )
        response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful

        # Inspect response JSON structure
        response_json = response.json()
        print("API Response:", response_json)  # Debugging line to check response structure

        # Extract the relevant text based on the provided structure
        gemini_response = (
            response_json.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "No response text")
            .strip()
        )

        # Log the response
        log_response(prompt, gemini_response)

        return gemini_response

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return "An HTTP error occurred while connecting to the Gemini API."
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        return "A request error occurred while connecting to the Gemini API."
    except ValueError as json_err:
        logging.error(f"JSON decode error: {json_err}")
        return "Unexpected response format from Gemini API."
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        return "An unexpected error occurred."

# Function to log responses
def log_response(prompt, response_text):
    response_data = {"prompt": prompt, "response": response_text}
    all_responses.append(response_data)
    
    # Optionally, write responses to a JSON file for persistence (for local development only)
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
