from flask import Flask, render_template, request, jsonify
from AINOR import AINORAssistant
import re
import os
import random
import sys
import logging
import requests
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

def match_pattern(command, patterns):
    """Utility function to match a command with any pattern."""
    for pattern in patterns:
        if re.search(pattern, command):
            return True
    return False

def handle_command(command):
    # Match greetings
    if match_pattern(command, conversation_data["greetings"]["patterns"]):
        response = random.choice(conversation_data["greetings"]["responses"])
        return response

    # Match "how are you" responses
    elif match_pattern(command, conversation_data["how_are_you"]["patterns"]):
        response = random.choice(conversation_data["how_are_you"]["responses"])
        return response

    # Match date
    elif match_pattern(command, conversation_data["date"]["patterns"]):
        date = get_date()
        response = random.choice(conversation_data["date"]["responses"]).replace("{date}", date)
        return response

    # Match time
    elif match_pattern(command, conversation_data["time"]["patterns"]):
        time_c = get_time()
        response = random.choice(conversation_data["time"]["responses"]).replace("{time}", time_c)
        return response

    # Match Google search
    elif match_pattern(command, conversation_data["search_google"]["patterns"]):
        query = command.replace('search google for', '').strip()
        results = google_search(query)
        
        if results:
            response = random.choice(conversation_data["search_google"]["responses"]).replace("{query}", query)
            response += "".join([f"\n{index + 1}. {result}" for index, result in enumerate(results)])
        else:
            response = "No results found."
        
        return response

    # Match farewell
    elif match_pattern(command, conversation_data["farewell"]["patterns"]):
        response = random.choice(conversation_data["farewell"]["responses"])
        sys.exit()

    # Unknown command
    else:
        response = random.choice(conversation_data["unknown_command"]["responses"])
        return response

# ===================================== MAIN EXECUTION ===============================================

if __name__ == '__main__':
    app.run(debug=True, port=5001)
