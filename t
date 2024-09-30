import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests  # pip install requests
import json
import time
import pyjokes  # pip install pyjokes

# Initialize the speech engine
engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[7].id)

def speak(audio):
    """ Function to convert text to speech """
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """ Function to greet the user based on the current time """
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning, Karan!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon, Karan!")
    else:
        speak("Good Evening, Karan!")

    speak("I am A.I.N.O.R, your assistant. How can I assist you today?")

def takeCommand():
    """ Takes microphone input from the user and returns it as a string """
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

def sendEmail(to, content):
    """ Sends an email using the provided email credentials """
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

if __name__ == "__main__":
    wishMe()  # Greet the user
    
    while True:
        query = takeCommand().lower()

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
                content = takeCommand()
                to = "karanyourEmail@gmail.com"
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry Karan, I couldn't send the email.")

        elif 'weather' in query:
            speak("Which city?")
            city = takeCommand().lower()
            getWeather(city)

        elif 'news' in query:
            getNews()

        elif 'joke' in query:
            tellJoke()

        elif 'remind me in' in query:
            speak("For how many seconds?")
            seconds = int(takeCommand())
            setReminder(seconds)

        elif 'shutdown' in query or 'restart' in query or 'logout' in query:
            controlSystem(query)

        elif 'exit' in query:
            speak("Goodbye, Karan. Have a nice day!")
            break
