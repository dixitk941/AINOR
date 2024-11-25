import os
import requests
from flask import Flask, render_template, request, jsonify
import logging
import pyjokes

app = Flask(__name__)

# Initialize a list to store all responses (only in memory)
all_responses = []

# Gemini API setup with environment variable
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = "AIzaSyCh87P6IHCR2TVINidnDifeybL3CqC_flQ"
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
    
    # List of possible questions related to the creator, founder, and developer
    if command in [
        "who is your creator", 
        "who is your founder", 
        "who is your developer", 
        "tell me about your creator",
        "tell me about your founder",
        "who created you",
        "who developed you",
        "who made you",
        "who is responsible for your creation",
        "who is behind your development",
        "who designed you",
        "what team created you",
        "who built you",
        "who established you",
        "can you tell me your creator",
        "can you tell me about your developers",
        "who are your creators",
        "who is the team behind you",
        "who is your parent company",
        "who is your maker",
        "who is your architect",
        "who is your originator",
        "who is your creator?",
        "who is your founder?",
        "who is your developer?",
        "tell me about your creator?",
        "tell me about your founder?",
        "who created you?",
        "who developed you?",
        "who made you?",
        "who is responsible for your creation?",
        "who is behind your development?",
        "who designed you?",
        "what team created you?",
        "who built you?",
        "who established you?",
        "can you tell me your creator?",
        "can you tell me about your developers?",
        "who are your creators?",
        "who is the team behind you?",
        "who is your parent company?",
        "who is your maker?",
        "who is your architect?",
        "who is your originator?"
    ]:
        response = "I was created by NeoCodeNex, Karan Dixit, and the talented Team Google."
    elif command in [
        "what is your name", 
        "tell me your name", 
        "who are you", 
        "what's your full name",
        "do you have a name",
        "can you tell me your name",
        "what should I call you",
        "who am i talking to",
        "are you ainor",
        "your name",
        "what is your name?",
        "tell me your name?",
        "who are you?",
        "what's your full name?",
        "do you have a name?",
        "can you tell me your name?",
        "what should I call you?",
        "who am i talking to?",
        "are you ainor?",
        "your name?"
    ]:
        response = "My name is AINOR, which stands for Artificial Intelligence Natural Optimization Resource."
    elif command in [
        "what is the full form of ainor",
        "what's the full form of ainor",
        "what is ainor",
        "what does ainor stand for",
        "what is the full form of ainor?",
        "what's the full form of ainor?",
        "what is ainor?",
        "what does ainor stand for?"
    ]:
        response = "AINOR stands for Artificial Intelligence Natural Optimization Resource."
    elif "tell me a joke" in command:
        response = pyjokes.get_joke()
    else:
        response = call_gemini_api(command)
    
    return jsonify({'response': response})


# Only needed for local development
if __name__ == '__main__':
    app.run(debug=True)
