from flask import Flask, render_template, request, jsonify
from AINOR import AINORAssistant
import re
import os
import random
import sys
import logging
import requests
from bs4 import BeautifulSoup
from googlesearch import search  # Import the googlesearch library
import datetime
import json  # To handle the conversation file

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

def get_time():
    return obj.tell_time()

def get_date():
    return obj.tell_me_date()

def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    c_time = obj.tell_time()
    return f"{greeting}. Currently, it is {c_time}. I am AINOR, online and ready. How may I assist you?"

def google_search(query):
    results = []
    try:
        # Perform Google search
        for j in search(query, num_results=5):  # Get the top 5 results
            results.append(j)
        if not results:  # Check if results are empty
            raise Exception("No results found.")
    except Exception as e:
        logging.error(f"Error during Google search: {e}")
        return []  # Return empty list on error
    return results

# ======================================= ROUTES =====================================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json.get('command', '').lower()  # Safely access JSON data
    response = handle_command(command)
    return jsonify({'response': response})

# =================================== COMMAND HANDLER ================================================

def handle_command(command):
    # Greetings handling
    if re.search(r'\b(hello|hi|hey|namaste|hola)\b', command):
        response = random.choice(conversation_data["greetings"]["hello"])
        return response

    # How are you response
    elif re.search(r'how are you', command):
        response = random.choice(conversation_data["greetings"]["how_are_you"])
        return response

    # Command: Tell date
    elif re.search('date', command):
        date = get_date()
        response = random.choice(conversation_data["date"]).replace("{date}", date)
        return response

    # Command: Tell time
    elif "time" in command:
        time_c = get_time()
        response = random.choice(conversation_data["time"]).replace("{time}", time_c)
        return response

    # Command: Open a website
    elif re.search('open', command):
        domain = command.split(' ')[-1]
        obj.website_opener(domain)
        return f'Opening {domain}'

    # Command: Search Google
    elif re.search('search google for', command):
        query = command.replace('search google for', '').strip()
        results = google_search(query)
        
        if results:
            response = random.choice(conversation_data["search_google"]).replace("{query}", query)
            response += "".join([f"\n{index + 1}. {result}" for index, result in enumerate(results)])
        else:
            response = "No results found."
        
        return response

    # Command: Exit or say goodbye
    elif re.search(r'\b(goodbye|bye|offline)\b', command):
        response = random.choice(conversation_data["farewell"])
        sys.exit()

    # Unknown command
    else:
        response = random.choice(conversation_data["unknown_command"])
        return response

# ===================================== MAIN EXECUTION ===============================================

if __name__ == '__main__':
    app.run(debug=True, port=5001)
