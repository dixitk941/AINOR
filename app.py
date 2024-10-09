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

# Initialize Flask app
app = Flask(__name__)

# Initialize AINOR Assistant object
obj = AINORAssistant()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Global Variables
GREETINGS = ["hello AINOR", "AINOR", "wake up AINOR", "you there AINOR", "time to work AINOR", "hey AINOR", "ok AINOR", "are you there"]
GREETINGS_RES = ["Always there for you.", "I am ready.", "Your wish is my command.", "How can I help you?", "I am online and ready."]

# ===================================== HELPER FUNCTIONS ==============================================

def speak(text):
    obj.tts(text)

def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        greeting = "Good Morning"
    elif 12 < hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
    c_time = obj.tell_time()
    speak(f"{greeting}. Currently, it is {c_time}. I am AINOR, online and ready. How may I assist you?")

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

def handle_command(command):
    if re.search('search google for', command):
        # Extract search query
        query = command.replace('search google for', '').strip()
        logging.info(f"Searching Google for: {query}")  # Log the search query
        
        results = google_search(query)  # Perform Google search
        
        # Create a formatted response
        if results:
            response = "Here are the top search results:"
            for index, result in enumerate(results):
                response += f"\n{index + 1}. {result}"
        else:
            response = "No results found."
        
        speak(response)  # Speak the response
        return response  # Return the response
    # Other command handling...


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
    # Command: Tell date
    if re.search('date', command):
        date = obj.tell_me_date()
        speak(date)
        return date

    # Command: Tell time
    elif "time" in command:
        time_c = obj.tell_time()
        speak(f"The time is {time_c}")
        return f"The time is {time_c}"

    # Command: Greetings
    elif command in GREETINGS:
        response = random.choice(GREETINGS_RES)
        speak(response)
        return response

    # Command: Open a website
    elif re.search('open', command):
        domain = command.split(' ')[-1]
        obj.website_opener(domain)
        speak(f'Opening {domain}')
        return f'Opening {domain}'

    # Command: Launch an application
    elif re.search('launch', command):
        dict_app = {'firefox': "C://Program Files//Mozilla Firefox//firefox.exe"}
        app_name = command.split(' ', 1)[1]
        path = dict_app.get(app_name)
        if path:
            speak(f'Launching {app_name}')
            os.startfile(path)
            return f'Launched {app_name}'
        else:
            speak('Application not found.')
            return 'Application not found.'

    # Command: Search Google
    elif re.search('search google for', command):
            # Extract search query
            query = command.replace('search google for', '').strip()
            results = google_search(query)  # Perform Google search
            
            # Create a formatted response
            if results:
                response = "Here are the top search results:"
                for index, result in enumerate(results):
                    response += f"\n{index + 1}. {result}"
            else:
                response = "No results found."
            
            speak(response)  # Speak the response
            return response  # Return the response
    # Command: Exit or say goodbye
    elif "goodbye" in command or "offline" in command or "bye" in command:
        speak("Going offline. It was nice working with you!")
        sys.exit()

    else:
        response = "I'm sorry, I didn't understand that command."
        speak(response)
        return response

# ===================================== MAIN EXECUTION ===============================================

if __name__ == '__main__':
    app.run(debug=True, port=5001)
