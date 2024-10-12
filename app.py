from flask import Flask, render_template, request, jsonify
from AINOR import AINORAssistant
import re
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

def handle_command(command):
    for entry in conversation_data["commands"]:
        for pattern in entry["patterns"]:
            if pattern == "*" or re.search(pattern, command):
                # Handle special cases like time, date, and Google search
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
                elif entry["category"] == "open_website":
                    domain = command.split(' ')[-1]
                    response = random.choice(entry["responses"]).replace("{site}", domain)
                    obj.website_opener(domain)
                    return response
                else:
                    # Regular response
                    return random.choice(entry["responses"])

    # If no match is found, return a response from unknown_command
    unknown_entry = next((entry for entry in conversation_data["commands"] if entry["category"] == "unknown_command"), None)
    if unknown_entry:
        return random.choice(unknown_entry["responses"])

# ===================================== MAIN EXECUTION ===============================================

if __name__ == '__main__':
    app.run(debug=True, port=5001)
