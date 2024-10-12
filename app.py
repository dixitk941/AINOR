import requests
from flask import Flask, render_template, request, jsonify
from AINOR import AINORAssistant
import re
import random
import logging
import json
import ast  # For analyzing Python code
import traceback  # To handle exceptions and generate traceback

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
    api_key = 'ab365baf6721be32e96687c938d415bc'  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.ok:
        weather_data = response.json()
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return f"{description} at {temp}°C"
    return "I'm unable to retrieve the weather information."

def analyze_code(code):
    try:
        tree = ast.parse(code)
        return "No syntax errors found."  # If the code parses without error
    except SyntaxError as e:
        return f"Syntax error: {e.msg} at line {e.lineno}, column {e.offset}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def generate_code(task):
    """Generate code snippets based on the given task."""
    if "calculate factorial" in task:
        return """def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Example usage
print(factorial(5))  # Output: 120"""
    
    elif "reverse a string" in task:
        return """def reverse_string(s):
    return s[::-1]

# Example usage
print(reverse_string("Hello"))  # Output: "olleH""""
    
    elif "check if a number is prime" in task:
        return """def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Example usage
print(is_prime(11))  # Output: True"""
    
    return "Sorry, I can't generate code for that task."

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
    # Check for code analysis request
    if command.startswith("analyze code"):
        code = command.replace("analyze code", "").strip()
        return analyze_code(code)
    
    # Check for code generation request
    if command.startswith("generate code for"):
        task = command.replace("generate code for", "").strip()
        return generate_code(task)

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
