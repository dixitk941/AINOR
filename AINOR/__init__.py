from AINOR.features import date_time
from AINOR.features import weather
from AINOR.features import google_search

class AINORAssistant:
    def __init__(self):
        self.memory = {}

    def mic_input(self):
        """
        Fetch input from the user (this will be modified for web input in practice).
        return: user's input as text
        """
        command = input("Type your command: ")
        return command.lower()

    def tell_me_date(self):
        return date_time.date()

    def tell_time(self):
        return date_time.time()

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

    def search_anything_google(self, command):
        return google_search.google_search(command)

    def add_to_memory(self, command):
        """
        Adds an unknown command to memory after confirming with the user.
        :param command: str - The command that is unknown.
        """
        print("I don't recognize that command. Would you like to add it to memory? (yes/no)")
        if input().strip().lower() == 'yes':
            answer = input("What should I remember as the answer? ")
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
