import re
import os
import random
import datetime
import requests
import sys
import urllib.parse
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
from AINOR import AINORAssistant
from AINOR.config import config

obj = AINORAssistant()

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello AINOR", "AINOR", "wake up AINOR", "you there AINOR", "time to work AINOR", "hey AINOR",
             "ok AINOR", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]

EMAIL_DIC = {
    'myself': 'dixitk941@gmail.com',
    # 'my official email': 'atharvaaingle@gmail.com',
    # 'my second email': 'mail.mentorconnect@gmail.com',
    'my official mail': 'neocodenex@gmail.com',
    'my second mail': 'dixitk941@gmail.com'
}

# Adding personal information
PERSONAL_INFO = {
    'name': 'Karan Dixit',
    'github': 'https://github.com/dixitk941',  # Replace with your GitHub username
    'linkedin': 'https://www.linkedin.com/in/karan-dixit21',  # Replace with your LinkedIn username
    'email': 'dixitk941@gmail.com',
    'skills': ['Python', 'React', 'JavaScript', 'Machine Learning'],  # Add more skills as needed
}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
# =======================================================================================================================================================


def speak(text):
    obj.tts(text)


app_id = config.wolframalpha_id


def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except Exception as e:
        speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
        return None


def startup():
    speak("Initializing AINOR")
    speak("Starting all systems applications")
    speak("Installing and checking all drivers")
    speak("Caliberating and examining all the core processors")
    speak("Checking the internet connection")
    speak("Wait a moment sir")
    speak("All drivers are up and running")
    speak("All systems have been activated")
    speak("Now I am online")
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am AINOR. Online and ready sir. Please tell me how may I help you")


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am AINOR. Online and ready sir. Please tell me how may I help you")


def add_to_memory(command):
    speak("I don't recognize that command. Would you like to add it to memory? (yes/no)")
    if input().strip().lower() == 'yes':
        answer = input("What should I remember as the answer? (type 'google' to search for it): ")
        if answer.strip().lower() == 'google':
            query = command
            # Implement Google search to fetch answer
            print(f"Searching for {query} on Google...")
            # Replace this with actual search and fetch logic
            # Example: answer = fetch_answer_from_google(query)
            answer = "This is a placeholder for the answer fetched from Google."
        # Store the command and answer in memory (you may want to implement persistent storage)
        print(f"Storing command '{command}' with answer '{answer}' in memory.")
        # Store in a dictionary or file as needed


def retrieve_personal_info(info_key):
    return PERSONAL_INFO.get(info_key, "Information not found.")


class MainThread:
    def __init__(self):
        pass

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        # startup()
        wish()

        while True:
            command = obj.mic_input()
            if command is None:
                continue

            # Command processing
            if re.search('date', command):
                date = obj.tell_date()
                speak(date)
            elif "time" in command:
                time_c = obj.tell_time()
                speak(f"The time is {time_c}")
            elif re.search('launch', command):
                dict_app = {
                    'chrome': 'C:/Program Files/Google/Chrome/Application/chrome.exe'
                }
                app = command.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    speak('Application path not found')
                else:
                    speak('Launching: ' + app + ' for you!')
                    obj.launch_any_app(path)
            elif command in GREETINGS:
                speak(random.choice(GREETINGS_RES))
            elif re.search('open', command):
                domain = command.split(' ')[-1]
                speak(f'Opening {domain}')
            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                speak(weather_res)
            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    wiki_res = obj.tell_me(topic)
                    speak(wiki_res)
                else:
                    speak("Sorry, I couldn't load your query. Please try again.")
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
                speak(f"Okay, playing {video} on YouTube")
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
                        speak("Email has been successfully sent")
                    else:
                        speak("I couldn't find the requested person's email.")
                except:
                    speak("Sorry, I couldn't send your email. Please try again.")
            elif "calculate" in command:
                question = command
                answer = computational_intelligence(question)
                speak(answer)
            elif "what is" in command or "who is" in command:
                question = command
                answer = computational_intelligence(question)
                speak(answer)
            elif "goodbye" in command or "offline" in command or "bye" in command:
                speak("Going offline. It was nice working with you.")
                sys.exit()
            elif "tell me about you" in command:
                info = retrieve_personal_info("name")
                speak(f"My name is {info}. You can find my GitHub profile at {PERSONAL_INFO['github']} and my LinkedIn profile at {PERSONAL_INFO['linkedin']}.")
            else:
                # If the command is unrecognized, ask if the user wants to add it to memory
                add_to_memory(command)

# Start A.I.N.O.R
if __name__ == "__main__":
    startExecution = MainThread()
    startExecution.run()
