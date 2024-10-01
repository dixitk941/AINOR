from AINOR import AINORAssistant
import re
import os
import random
import datetime
import requests
import sys
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
from AINOR.config import config

obj = AINORAssistant()

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello AINOR", "AINOR", "wake up AINOR", "you there AINOR", "time to work AINOR", "hey AINOR",
             "ok AINOR", "are you there"]
GREETINGS_RES = ["always there for you sir", "I am ready sir", "your wish my command", "how can I help you sir?", "I am online and ready sir"]

EMAIL_DIC = {
    'myself': 'neocodenex@gmail.com',
    'my official email': 'neocodenex@gmail.com',
    'my second email': 'dixitk941@gmail.com',
}

app_id = config.wolframalpha_id


def speak(text):
    obj.tts(text)


def log_conversation(command, response):
    """Logs the command and response to a history file."""
    with open("conversation_history.txt", "a") as log_file:
        log_file.write(f"Command: {command}\nResponse: {response}\n\n")


def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry sir, I couldn't fetch your question's answer. Please try again.")
        return None

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    c_time = obj.tell_time()
    speak(f"Currently, it is {c_time}")
    speak("I am AINOR. Online and ready sir. Please tell me how may I help you")


class MainThread:
    def __init__(self):
        pass

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        startup()
        wish()

        while True:
            command = obj.mic_input()
            # Check if command is None and continue to next iteration if it is
            if command is None:
                continue  # You might also want to include a small delay here to avoid busy-waiting

            # Command processing
            response = ""

            if re.search('date', command):
                date = obj.tell_date()
                response = date
                speak(date)

            elif "time" in command:
                time_c = obj.tell_time()
                response = f"The time is {time_c}"
                speak(response)

            elif re.search('launch', command):
                dict_app = {
                    'chrome': 'C:/Program Files/Google/Chrome/Application/chrome.exe'
                }
                app = command.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    response = 'Application path not found'
                    speak(response)
                else:
                    response = f'Launching: {app} for you!'
                    speak(response)
                    obj.launch_any_app(path)

            elif command in GREETINGS:
                response = random.choice(GREETINGS_RES)
                speak(response)

            elif re.search('open', command):
                domain = command.split(' ')[-1]
                response = f'Opening {domain}'
                speak(response)

            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                response = weather_res
                speak(weather_res)

            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    wiki_res = obj.tell_me(topic)
                    response = wiki_res
                    speak(wiki_res)
                else:
                    response = "Sorry, I couldn't load your query. Please try again."
                    speak(response)

            elif "news" in command:
                # Implement news fetching functionality
                pass

            elif 'search google for' in command:
                # Implement Google search functionality
                pass
            
            elif "play music" in command:
                music_dir = "F://Songs//Imagine_Dragons"
                songs = os.listdir(music_dir)
                for song in songs:
                    os.startfile(os.path.join(music_dir, song))

            elif 'youtube' in command:
                video = command.split(' ')[1]
                response = f"Okay, playing {video} on YouTube"
                speak(response)
                pywhatkit.playonyt(video)

            elif "email" in command:
                sender_email = config.email
                sender_password = config.email_password
                try:
                    speak("Whom do you want to email?")
                    recipient = obj.mic_input()
                    receiver_email = EMAIL_DIC.get(recipient)
                    if receiver_email:
                        speak("What is the subject?")
                        subject = obj.mic_input()
                        speak("What should I say?")
                        message = obj.mic_input()
                        msg = f'Subject: {subject}\n\n{message}'
                        obj.send_mail(sender_email, sender_password, receiver_email, msg)
                        response = "Email has been successfully sent"
                        speak(response)
                    else:
                        response = "I couldn't find the requested person's email."
                        speak(response)
                except:
                    response = "Sorry, I couldn't send your email. Please try again."
                    speak(response)

            elif "calculate" in command:
                question = command
                answer = computational_intelligence(question)
                response = answer
                speak(answer)
            
            elif "what is" in command or "who is" in command:
                question = command
                answer = computational_intelligence(question)
                response = answer
                speak(answer)

            elif "goodbye" in command or "offline" in command or "bye" in command:
                response = "Going offline. It was nice working with you."
                speak(response)
                sys.exit()

            # Log the conversation history
            log_conversation(command, response)


# Start A.I.N.O.R
if __name__ == "__main__":
    startExecution = MainThread()
    startExecution.run()
