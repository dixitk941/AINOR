import requests
from flask import Flask, render_template, request, jsonify
from AINOR import AINORAssistant
import re
import random
import sys
import logging
import json  # To handle the conversation file
import datetime

# Initialize Flask app
app = Flask(__name__)

# Initialize AINOR Assistant object
obj = AINORAssistant()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load conversation file
with open('conversation.json') as f:
    conversation_data = json.load(f)

# ===================================== HELPER FUNCTIONS ==============================================

def get_time(location=None):
    # If a location is provided, return the time for that location
    if location:
        response = requests.get(f"http://worldtimeapi.org/api/timezone/{location}")
        if response.ok:
            time_data = response.json()
            return time_data['datetime']
    return obj.tell_time()

def get_date():
    return obj.tell_me_date()

def google_search(query):
    results = []
    try:
        for j in search(query, num_results=5):
            results.append(j)
        if not results:
            raise Exception("No results found.")
    except Exception as e:
        logging.error(f"Error during Google search: {e}")
        return []
    return results

def get_weather(location):
    # Replace 'your_api_key' with your actual OpenWeatherMap API key
    api_key = 'your_api_key'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.ok:
        weather_data = response.json()
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return f"{description} at {temp}°C"
    return "I'm unable to retrieve the weather information."

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
