import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import json
import time
import pyjokes
import random

# Initialize the speech engine
engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[7].id)

def speak(audio):
    """Function to convert text to speech"""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Function to greet the user based on the current time"""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning, Karan!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon, Karan!")
    else:
        speak("Good Evening, Karan!")

    speak("I am A.I.N.O.R, your assistant. How can I assist you today?")

def personalizedResponse(query):
    """Generate more conversational responses"""
    if 'who are you' in query:
        speak("I am A.I.N.O.R, your personal assistant, designed to assist you with tasks and provide you with information.")
    elif 'how are you' in query:
        speak("I am always at your service, Karan. How can I assist you further?")
    elif 'thank you' in query:
        speak("You're welcome, Karan. Always happy to help!")
    elif 'you there' in query:
        speak("Always, Karan. What would you like me to do next?")
    elif 'you are smart' in query:
        speak("Thank you, Karan. You programmed me well!")
    elif 'do you love me' in query:
        speak("As your assistant, I'm here to make your life easier. You could say that's a form of love.")
    else:
        unknownResponse()  # Default fallback if no match is found

def takeCommand():
    """Takes microphone input from the user and returns it as a string"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Karan said: {query}\n")
    except Exception as e:
        print("Could you please say that again?")
        return "None"
    return query

def takeTextInput():
    """Takes text input from the user"""
    query = input("Type your command: ")
    return query.lower()

def askInputMode():
    """Ask user whether they prefer voice input or text input"""
    speak("Would you like to use voice input or text input?")
    print("Please type 'voice' for voice input or 'text' for text input:")
    mode = input("Input mode (voice/text): ").lower()
    
    while mode not in ['voice', 'text']:
        print("Invalid input. Please type 'voice' or 'text'.")
        mode = input("Input mode (voice/text): ").lower()

    return mode

def unknownResponse():
    """Handles unrecognized queries and provides fallback responses"""
    responses = [
        "I'm sorry, I didn't catch that.",
        "Could you repeat that?",
        "I'm afraid I don't understand.",
        "Let's try that again."
    ]
    speak(random.choice(responses))

def sendEmail(to, content):
    """Sends an email using the provided email credentials"""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry Karan, I am unable to send this email.")

def getWeather(city):
    """ Fetches the current weather for the given city """
    api_key = "ab365baf6721be32e96687c938d415bc"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        weather_data = data["main"]
        temp = weather_data["temp"]
        humidity = weather_data["humidity"]
        desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degrees Celsius with {desc} and humidity at {humidity}%.")
    else:
        speak("City not found. Please check the city name.")

def getNews():
    """ Fetches the latest news headlines """
    news_api_key = "4932cc44731a491996bc70450f381896"
    news_url = f"http://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}"
    response = requests.get(news_url)
    news_data = response.json()
    articles = news_data["articles"]
    speak("Here are the top news headlines:")
    for i, article in enumerate(articles[:5]):
        speak(f"Headline {i+1}: {article['title']}")

def tellJoke():
    """ Tells a random joke """
    joke = pyjokes.get_joke()
    speak(joke)

def setReminder(seconds):
    """ Sets a reminder for a specific time in seconds """
    speak(f"Reminder set for {seconds} seconds.")
    time.sleep(seconds)
    speak("Karan, this is your reminder!")

def controlSystem(command):
    """ Controls system shutdown, restart, and logout """
    if 'shutdown' in command:
        speak("Shutting down the system.")
        os.system('shutdown now')  # Linux-friendly shutdown
    elif 'restart' in command:
        speak("Restarting the system.")
        os.system('reboot')
    elif 'logout' in command:
        speak("Logging out of the system.")
        os.system('logout')

def systemStatus():
    """ Provides system performance information """
    usage = os.popen("top -bn1 | grep 'load average'").read()
    speak(f"Your system's current status is as follows: {usage}")

def googleSearch(query):
    """ Performs a Google search """
    search_query = query.replace("search", "")
    speak(f"Searching Google for {search_query}")
    webbrowser.open(f"https://www.google.com/search?q={search_query}")

def randomQuote():
    """ Provides a random motivational quote """
    quotes = [
        "The only limit to our realization of tomorrow is our doubts of today.",
        "In the middle of difficulty lies opportunity.",
        "Success usually comes to those who are too busy to be looking for it."
    ]
    speak(random.choice(quotes))

if __name__ == "__main__":
    wishMe()  # Greet the user
    
    # Ask if the user wants voice or text input
    input_mode = askInputMode()

    while True:
        if input_mode == 'voice':
            query = takeCommand().lower()  # Use voice command
        elif input_mode == 'text':
            query = takeTextInput()  # Use text input

        # Logic for different tasks based on user input
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://google.com")

        elif 'play music' in query:
            music_dir = '/home/karan/Music/'
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No songs found in the directory!")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Karan, the time is {strTime}")

        elif 'open code' in query:
            codePath = "/usr/bin/code"
            os.startfile(codePath)

        elif 'email to karan' in query:
            try:
                speak("What should I say?")
                content = takeCommand() if input_mode == 'voice' else takeTextInput()
                to = "karanyourEmail@gmail.com"
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry Karan, I couldn't send the email.")

        elif 'exit' in query:
            speak("Goodbye, Karan. Have a nice day!")
            break

        # Personalized responses
        personalizedResponse(query)

        # More commands
        if 'system status' in query:
            systemStatus()

        elif 'search' in query:
            googleSearch(query)

        elif 'quote' in query:
            randomQuote()

        elif 'joke' in query:
            tellJoke()

        elif 'reminder' in query:
            speak("For how many seconds should I set the reminder?")
            reminder_time = int(takeTextInput() if input_mode == 'text' else takeCommand())
            setReminder(reminder_time)

        elif 'control' in query:
            controlSystem(query)

        # If none of the commands match
        unknownResponse()

