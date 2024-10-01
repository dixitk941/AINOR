import speech_recognition as sr
import pyttsx3

from AINOR.features import date_time
from AINOR.features import launch_app
from AINOR.features import website_open
from AINOR.features import weather
from AINOR.features import wikipedia
from AINOR.features import news
from AINOR.features import send_email
from AINOR.features import google_search
from AINOR.features import google_calendar
from AINOR.features import note
from AINOR.features import system_stats
from AINOR.features import loc

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

class AINORAssistant:
    def __init__(self):
        self.memory = {}

    def mic_input(self):
        """
        Fetch input from mic or fallback to text input if mic input fails.
        return: user's voice or text input as text if true, False if fail
        """
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening....")
                r.energy_threshold = 4000
                audio = r.listen(source)
            try:
                print("Recognizing...")
                command = r.recognize_google(audio, language='en-in').lower()
                print(f'You said: {command}')
                return command
            except sr.UnknownValueError:
                print("Could not understand audio. Would you like to type your command instead? (yes/no)")
                if input().strip().lower() == 'yes':
                    return input("Type your command: ")
                else:
                    print("Please try again.")
                    return self.mic_input()
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def tts(self, text):
        """
        Convert any text to speech
        :param text: text(String)
        :return: True/False (Play sound if True otherwise write exception to log and return  False)
        """
        try:
            engine.say(text)
            engine.runAndWait()
            engine.setProperty('rate', 175)
            return True
        except:
            t = "Sorry I couldn't understand and handle this input"
            print(t)
            return False

    def tell_me_date(self):
        return date_time.date()

    def tell_time(self):
        return date_time.time()

    def launch_any_app(self, path_of_app):
        """
        Launch any windows application 
        :param path_of_app: path of exe 
        :return: True is success and open the application, False if fail
        """
        return launch_app.launch_app(path_of_app)

    def website_opener(self, domain):
        """
        This will open website according to domain
        :param domain: any domain, example "youtube.com"
        :return: True if success, False if fail
        """
        return website_open.website_opener(domain)

    def weather(self, city):
        """
        Return weather
        :param city: Any city of this world
        :return: weather info as string if True, or False
        """
        try:
            res = weather.fetch_weather(city)
        except Exception as e:
            print(e)
            res = False
        return res

    def tell_me(self, topic):
        """
        Tells about anything from wikipedia
        :param topic: any string is valid options
        :return: First 500 character from wikipedia if True, False if fail
        """
        return wikipedia.tell_me_about(topic)

    def news(self):
        """
        Fetch top news of the day from google news
        :return: news list of string if True, False if fail
        """
        return news.get_news()
    
    def send_mail(self, sender_email, sender_password, receiver_email, msg):
        return send_email.mail(sender_email, sender_password, receiver_email, msg)

    def google_calendar_events(self, text):
        service = google_calendar.authenticate_google()
        date = google_calendar.get_date(text) 
        if date:
            return google_calendar.get_events(date, service)
        else:
            pass
    
    def search_anything_google(self, command):
        google_search.google_search(command)

    def take_note(self, text):
        note.note(text)
    
    def system_info(self):
        return system_stats.system_stats()

    def location(self, location):
        current_loc, target_loc, distance = loc.loc(location)
        return current_loc, target_loc, distance

    def my_location(self):
        city, state, country = loc.my_location()
        return city, state, country

    def add_to_memory(self, command):
        """
        Adds an unknown command to memory after confirming with the user.
        :param command: str - The command that is unknown.
        """
        print("I don't recognize that command. Would you like to add it to memory? (yes/no)")
        if input().strip().lower() == 'yes':
            answer = input("What should I remember as the answer? (type 'google' to search for it): ")
            if answer.strip().lower() == 'google':
                query = command
                # Implement Google search to fetch answer (placeholder logic)
                answer = "This is a placeholder for the answer fetched from Google."
            # Store the command and answer in memory
            self.memory[command] = answer
            print(f"Stored command '{command}' with answer '{answer}' in memory.")
        else:
            print("Command not added to memory.")

# Example Usage
if __name__ == "__main__":
    assistant = AINORAssistant()
    while True:
        command = assistant.mic_input()
        if command:
            # Here you can add command processing logic based on recognized commands.
            # If the command is not recognized:
            assistant.add_to_memory(command)
