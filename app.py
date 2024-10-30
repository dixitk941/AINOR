import requests
from flask import Flask, render_template, request, jsonify
from AINOR import AINORAssistant
import re
import random
import logging
import json
import ast  # For analyzing Python code
import traceback  # To handle exceptions and generate traceback
from googlesearch import search  # Make sure to install this library if not already installed

# Initialize Flask app
app = Flask(__name__)

# Initialize AINOR Assistant object
obj = AINORAssistant()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load conversation file
with open('conversation.json') as f:
    conversation_data = json.load(f)

# Gemini API setup
GEMINI_API_KEY ="AIzaSyCh87P6IHCR2TVINidnDifeybL3CqC_flQ"
GEMINI_API_URL = "https://api.google.com/gemini/v1/models/gemini"

def call_gemini_api(prompt):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-1",
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.ok:
        return response.json().get("choices")[0].get("text").strip()
    else:
        logging.error(f"Gemini API error: {response.status_code} {response.text}")
        return "I'm having trouble connecting to the Gemini API."

# ======================================= ROUTES =====================================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json.get('command', '').lower()
    response = handle_command(command)
    return jsonify({'response': response})

# =================================== COMMAND HANDLER ================================================

def handle_command(command):
    # Directly call Gemini API for natural language processing
    if "analyze" in command or "generate" in command or "weather" in command:
        prompt = f"Respond to this command: {command}"
        return call_gemini_api(prompt)
    
    # Fall back to predefined responses for other commands
    for entry in conversation_data["commands"]:
        for pattern in entry["patterns"]:
            if pattern == "*" or re.search(pattern, command):
                if entry["category"] == "time":
                    time_c = get_time()
                    response = random.choice(entry["responses"]).replace("{time}", time_c)
                    return response

                elif entry["category"] == "date":
                    date = get_date()
                    response = random.choice(entry["responses"]).replace("{date}", date)
                    return response

                elif entry["category"] == "search_google":
                    query = command.replace('search google for', '').strip()
                    results = google_search(query)
                    if results:
                        response = random.choice(entry["responses"]).replace("{query}", query)
                        response += "".join([f"\n{index + 1}. {result}" for index, result in enumerate(results)])
                    else:
                        response = "No results found."
                    return response

                elif entry["category"] == "weather":
                    location = re.search(r'in (\w+)', command)
                    if location:
                        location_name = location.group(1)
                        weather_info = get_weather(location_name)
                        response = random.choice(entry["responses"]).replace("{location}", location_name).replace("{weather}", weather_info)
                        return response
                    else:
                        return "Please provide a location to check the weather."

                elif entry["category"] == "location_time":
                    location = re.search(r'in (\w+)', command)
                    if location:
                        location_name = location.group(1)
                        time_c = get_time(location_name)
                        response = random.choice(entry["responses"]).replace("{location}", location_name).replace("{time}", time_c)
                        return response
                    else:
                        return "Please provide a location to check the time."

                elif entry["category"] == "open_website":
                    domain = command.split(' ')[-1]
                    response = random.choice(entry["responses"]).replace("{site}", domain)
                    obj.website_opener(domain)
                    return response

                elif entry["category"] == "tasks":
                    return random.choice(entry["responses"])

                else:
                    return random.choice(entry["responses"])

    unknown_entry = next((entry for entry in conversation_data["commands"] if entry["category"] == "unknown_command"), None)
    if unknown_entry:
        return random.choice(unknown_entry["responses"])

# ===================================== MAIN EXECUTION ===============================================

if __name__ == '__main__':
    app.run(debug=True, port=5001)