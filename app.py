import os
import requests
import json
import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import logging

# Initialize Firebase Admin SDK
try:
    # Use credentials.json file if available
    cred = credentials.Certificate('credentials.json')
    firebase_admin.initialize_app(cred)
    print("Firebase initialized successfully with credentials.json")
except Exception as e:
    print(f"Error initializing Firebase with credentials.json: {str(e)}")
    print("Attempting to use default credentials...")
    try:
        # Use default credentials if running in production or cloud environment
        firebase_admin.initialize_app()
        print("Firebase initialized successfully with default credentials")
    except Exception as e:
        print(f"Error initializing Firebase with default credentials: {str(e)}")
        print("Please make sure you have valid Firebase credentials in credentials.json")
        # Continue without Firebase - the app will use local storage instead
        pass

# Get a reference to the Firestore database
try:
    db = firestore.client()
    firebase_available = True
except Exception as e:
    print(f"Error getting Firestore client: {str(e)}")
    print("Firebase functionality will be disabled")
    db = None
    firebase_available = False

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Maximum number of messages to maintain for context
MAX_CONTEXT_MESSAGES = 10

# Gemini API setup with environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Use the hardcoded key if environment variable is not set
if not GEMINI_API_KEY:
    GEMINI_API_KEY = "AIzaSyARdoeSSu7JuVwvBRzy-ORO8hm5PW4-0lU"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_user_conversation_history(user_id="default"):
    """Retrieve conversation history from Firebase for a specific user"""
    if not firebase_available:
        # Fallback to local file if Firebase is not available
        try:
            with open('ainor_chat_history.json', 'r') as f:
                return json.load(f).get('messages', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []
            
    try:
        # Query Firestore for chat history
        chat_history_ref = db.collection('chat_history').document(user_id)
        doc = chat_history_ref.get()
        
        if doc.exists:
            return doc.to_dict().get('messages', [])
        return []
    except Exception as e:
        logging.error(f"Error retrieving conversation history: {str(e)}")
        return []

def save_to_conversation_history(user_id="default", user_message="", ai_response=""):
    """Save conversation to Firebase"""
    timestamp = datetime.datetime.now().isoformat()
    
    if not firebase_available:
        # Fallback to local file if Firebase is not available
        try:
            try:
                with open('ainor_chat_history.json', 'r') as f:
                    data = json.load(f)
                    messages = data.get('messages', [])
            except (FileNotFoundError, json.JSONDecodeError):
                messages = []
                
            # Add new messages
            messages.append({
                "role": "user",
                "content": user_message,
                "timestamp": timestamp
            })
            
            messages.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": timestamp
            })
            
            # Keep only the most recent MAX_CONTEXT_MESSAGES messages
            if len(messages) > MAX_CONTEXT_MESSAGES * 2:
                messages = messages[-MAX_CONTEXT_MESSAGES*2:]
            
            with open('ainor_chat_history.json', 'w') as f:
                json.dump({'messages': messages, 'updated_at': timestamp}, f)
            return True
        except Exception as e:
            logging.error(f"Error saving conversation history to local file: {str(e)}")
            return False
    
    try:
        chat_history_ref = db.collection('chat_history').document(user_id)
        
        # Get existing messages or create a new array
        doc = chat_history_ref.get()
        
        if doc.exists:
            messages = doc.to_dict().get('messages', [])
        else:
            messages = []
        
        # Add new messages
        messages.append({
            "role": "user",
            "content": user_message,
            "timestamp": timestamp
        })
        
        messages.append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": timestamp
        })
        
        # Keep only the most recent MAX_CONTEXT_MESSAGES messages
        if len(messages) > MAX_CONTEXT_MESSAGES * 2:
            messages = messages[-MAX_CONTEXT_MESSAGES*2:]
        
        # Update Firestore
        chat_history_ref.set({
            'messages': messages,
            'updated_at': timestamp
        }, merge=True)
        
        return True
    except Exception as e:
        logging.error(f"Error saving conversation history: {str(e)}")
        return False

def call_gemini_api(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    
    # Get user ID and load conversation history
    user_id = session.get('user_id', 'default')
    conversation_history = get_user_conversation_history(user_id)
    
    # Improve prompt to encourage code formatting with proper markdown
    if any(keyword in prompt.lower() for keyword in ["code", "function", "program", "script", "write"]):
        prompt = f"{prompt}\n\nPlease format any code with proper markdown code blocks using triple backticks."
    
    # Build conversation messages with history
    messages = []
    
    # Add previous conversation history for context
    for message in conversation_history:
        role = "user" if message["role"] == "user" else "model"
        messages.append({
            "role": role,
            "parts": [{"text": message["content"]}]
        })
    
    # Add current prompt
    messages.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })
    
    data = {
        "contents": messages,
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 8192,
        }
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
            
            # Log the whole response for debugging
            logging.info(f"Gemini API raw response: {response_json}")
            
            # Extract the text response
            candidates = response_json.get("candidates", [])
            if not candidates:
                return "No response generated by AI."
                
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            
            if not parts:
                return "Empty response from AI."
                
            gemini_response = parts[0].get("text", "").strip()
            
            if not gemini_response:
                return "The AI returned an empty response. Please try again."
            
            # Save to Firebase
            user_id = session.get('user_id', 'default')
            save_to_conversation_history(user_id, prompt, gemini_response)
            
            return gemini_response
        except Exception as e:
            logging.error(f"Error processing Gemini API response: {str(e)}")
            logging.error(f"Response data: {response.text}")
            return f"Error processing AI response: {str(e)}"
    else:
        logging.error(f"Gemini API error: {response.status_code} {response.text}")
        return "I'm having trouble connecting to the Gemini API."

# Function to initialize conversation history from Firebase
@app.route('/')
def index():
    # Initialize user session if needed
    if 'user_id' not in session:
        session['user_id'] = str(datetime.datetime.now().timestamp())
    
    return render_template('index.html')

@app.route('/coding')
def coding():
    # Initialize user session if needed
    if 'user_id' not in session:
        session['user_id'] = str(datetime.datetime.now().timestamp())
    
    return render_template('coding.html')

# Add login route
@app.route('/login')
def login():
    return render_template('Login.html')

# Add this route to handle direct requests to /Login.html
@app.route('/Login.html')
def login_html():
    return redirect(url_for('login'))

# Optional: add logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json.get('command', '').lower()
    user_id = session.get('user_id', 'default')
    
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
        "who is your originator"
    ]:
        response = "I was created by NeoCodeNex, Karan Dixit, and the talented Team Google."
        # Update conversation history for continuity
        save_to_conversation_history(user_id, command, response)
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
        "your name"
    ]:
        response = "My name is AINOR, which stands for Artificial Intelligence Natural Optimization Resource."
        # Update conversation history for continuity
        save_to_conversation_history(user_id, command, response)
    elif command == "clear conversation" or command == "clear context" or command == "forget conversation":
        # Clear Firebase conversation history
        if firebase_available:
            try:
                db.collection('chat_history').document(user_id).set({
                    'messages': [],
                    'updated_at': datetime.datetime.now().isoformat()
                })
            except Exception as e:
                logging.error(f"Error clearing conversation history: {str(e)}")
        else:
            # Clear local file if Firebase is not available
            try:
                with open('ainor_chat_history.json', 'w') as f:
                    json.dump({'messages': [], 'updated_at': datetime.datetime.now().isoformat()}, f)
            except Exception as e:
                logging.error(f"Error clearing local conversation history: {str(e)}")
        
        response = "Conversation history has been cleared."
    elif command == "show conversation history" or command == "show chat history":
        # Return the last few conversation exchanges from Firebase
        user_history = get_user_conversation_history(user_id)
        
        if user_history:
            history_text = "Here's our recent conversation:\n\n"
            for i in range(0, len(user_history), 2):
                if i+1 < len(user_history):
                    history_text += f"You: {user_history[i]['content']}\n"
                    history_text += f"AINOR: {user_history[i+1]['content']}\n\n"
            response = history_text
        else:
            response = "We haven't had any conversation yet."
    else:
        response = call_gemini_api(command)
    
    return jsonify({'response': response})

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    user_id = session.get('user_id', 'default')
    history = get_user_conversation_history(user_id)
    
    # Format history for frontend
    formatted_history = []
    for i in range(0, len(history), 2):
        if i+1 < len(history):
            entry = {
                "user": history[i]["content"],
                "assistant": history[i+1]["content"],
                "timestamp": history[i]["timestamp"]
            }
            formatted_history.append(entry)
    
    return jsonify(formatted_history)

# Set up Firebase auth route to store user ID in session
@app.route('/set_user_id', methods=['POST'])
def set_user_id():
    user_id = request.json.get('uid')
    if user_id:
        session['user_id'] = user_id
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "No user ID provided"}), 400

# Only needed for local development
if __name__ == '__main__':
    app.run(debug=True)