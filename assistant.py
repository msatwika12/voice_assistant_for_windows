import requests
import wikipedia
import webbrowser
import pywhatkit as kit
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from random import choice
from time import sleep
import threading
import os
import smtplib
import cv2
from math import sqrt, pow, sin, cos, tan, radians

# Load configurations
USERNAME = config('USER', default="User")
BOTNAME = config('BOTNAME', default="Assistant")
NEWS_API_KEY = config("NEWS_API_KEY")
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
EMAIL = config("EMAIL", default="example@example.com")
PASSWORD = config("PASSWORD", default="password")

# Text-to-speech setup
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Offline jokes pool
offline_jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "What do you call fake spaghetti? An impasta!",
    "Why couldn't the bicycle stand up by itself? It was two-tired!"
]

# Functions
def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greet the user based on the time of day."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning {USERNAME}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {USERNAME}")
    elif 16 <= hour < 19:
        speak(f"Good Evening {USERNAME}")
    else:
        speak(f"Hello {USERNAME}")
    speak(f"I am Jawaris, Powered by Team 18. How may I assist you?")

def take_user_input():
    """Listen to the user's input and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return "none"

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    kit.search(query)

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+91{number}", message)

def get_latest_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get("articles", [])
    return [article["title"] for article in articles[:5]]

def get_weather_report(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric"
    data = requests.get(url).json()
    weather = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

def tell_a_joke():
    joke = choice(offline_jokes)
    speak(joke)
    print(joke)

def get_random_advice():
    return requests.get("https://api.adviceslip.com/advice").json()['slip']['advice']

def tell_time():
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")
    print(f"Time: {current_time}")

def tell_date():
    current_date = datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {current_date}")
    print(f"Date: {current_date}")

def solve_math(query):
    try:
        result = eval(query)
        speak(f"The result is {result}")
        print(f"Result: {result}")
    except Exception as e:
        speak("I couldn't calculate that. Please try again.")

def set_reminder(time_str, message):
    speak(f"Reminder set for {time_str}.")
    print(f"Reminder set: {time_str} - {message}")
    delay = (datetime.strptime(time_str, "%I:%M %p") - datetime.now()).total_seconds()
    threading.Timer(delay, lambda: speak(f"Reminder: {message}")).start()

def open_application(app_name):
    if "notepad" in app_name:
        os.system("notepad")
    elif "calculator" in app_name:
        os.system("calc")
    elif "whatsapp" in app_name:
        webbrowser.open("https://www.whatsapp.com/")  # Open WhatsApp in browser
        speak("Opening WhatsApp")
    elif "youtube" in app_name:
        webbrowser.open("https://www.youtube.com/")  # Open YouTube in browser
        speak("Opening YouTube")
    elif "spotify" in app_name:
        webbrowser.open("https://www.spotify.com/")  # Open Spotify in browser
        speak("Opening Spotify")
    elif "chat gpt" in app_name:
        webbrowser.open("https://www.chatgpt.com/")  # Open ChatGPT in browser
        speak("Opening ChatGPT")
    else:
        speak("Application not available.")


def saveNotes(content):
    filename = "notes.txt"
    with open(filename, "a") as file:
        file.write(content + "\n")
    print("Notes saved successfully.")

def captureImage():
    cap = cv2.VideoCapture(0)  # Initialize the VideoCapture object for the camera
    
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    ret, frame = cap.read()

    if ret:
        filename = 'captured_image.jpg'
        cv2.imwrite(filename, frame)
        print(f"Image captured and saved as {filename}")
        speak("Image captured and saved!")
    else:
        print("Error: Unable to capture image.")
        speak("Error: Unable to capture image.")

    cap.release()
    cv2.destroyAllWindows()
def performMathOperation(query):
    try:
        # Extract operation and numbers
        if "addition" in query:
            numbers = [float(num) for num in query.split() if num.replace('.', '', 1).isdigit()]
            result = sum(numbers)
            operation = " + ".join(map(str, numbers))
        elif "subtraction" in query:
            numbers = [float(num) for num in query.split() if num.replace('.', '', 1).isdigit()]
            result = numbers[0] - sum(numbers[1:])
            operation = " - ".join(map(str, numbers))
        elif "multiplication" in query:
            numbers = [float(num) for num in query.split() if num.replace('.', '', 1).isdigit()]
            result = 1
            for num in numbers:
                result *= num
            operation = " * ".join(map(str, numbers))
        elif "division" in query:
            numbers = [float(num) for num in query.split() if num.replace('.', '', 1).isdigit()]
            if len(numbers) < 2 or any(n == 0 for n in numbers[1:]):
                raise ZeroDivisionError("Cannot divide by zero")
            result = numbers[0]
            for num in numbers[1:]:
                result /= num
            operation = " / ".join(map(str, numbers))
        else:
            speak("Operation not recognized.")
            return

        speak(f"The result of {operation} is {result}")
        print(f"{operation} = {result}")

    except ZeroDivisionError:
        speak("Error: Division by zero is not allowed.")
        print("Error: Division by zero.")
    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")

def sendEmail(to, content):
    try:
        smtp_user = EMAIL  # Loaded from .env
        smtp_password = PASSWORD  # Loaded from .env

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to, content)
        server.close()
        speak("Email has been sent!")
    except smtplib.SMTPAuthenticationError:
        speak("Authentication failed. Please check your email and password or use an app-specific password.")
    except smtplib.SMTPException as e:
        speak(f"An error occurred while sending the email: {e}")
    except Exception as e:
        speak(f"An unexpected error occurred: {e}")

# Main program
if __name__ == "__main__":
    greet_user()
    while True:
        query = take_user_input()

        if "ip address" in query:
            ip = find_my_ip()
            speak(f"Your IP Address is {ip}")
            print(f"IP Address: {ip}")

        elif "wikipedia" in query:
            speak("What do you want to search on Wikipedia?")
            search_query = take_user_input()
            result = search_on_wikipedia(search_query)
            speak(result)
            print(result)

        elif "youtube" in query:
            speak("What should I play on YouTube?")
            video = take_user_input()
            play_on_youtube(video)

        elif "google" in query:
            speak("What should I search on Google?")
            search_query = take_user_input()
            search_on_google(search_query)

        elif "news" in query:
            news = get_latest_news()
            speak("Here are the top news headlines.")
            for headline in news:
                speak(headline)
                print(headline)

        elif "weather" in query:
            speak("Please tell me the city name.")
            city = take_user_input()
            weather, temp, feels_like = get_weather_report(city)
            speak(f"The weather in {city} is {weather}. The temperature is {temp}, feels like {feels_like}.")
            print(f"Weather: {weather}, Temp: {temp}, Feels Like: {feels_like}")

        elif "joke" in query:
            tell_a_joke()

        elif "advice" in query:
            advice = get_random_advice()
            speak(advice)
            print(advice)

        elif "time" in query:
            tell_time()

        elif "date" in query:
            tell_date()

        elif "reminder" in query:
            speak("What time should I set the reminder for?")
            time_str = take_user_input()
            speak("What should I remind you about?")
            message = take_user_input()
            set_reminder(time_str, message)

        elif "open" in query:
            speak("Which application should I open?")
            app_name = take_user_input()
            open_application(app_name)

        elif "math" in query:
            speak("What calculation should I perform?")
            math_query = take_user_input()
            solve_math(math_query)

        elif "save note" in query:
            speak("What would you like to note down?")
            note_content = take_user_input()
            saveNotes(note_content)

        elif "capture image" in query:
            captureImage()

        elif "send email" in query:
            speak("To which email address should I send the email?")
            recipient = take_user_input()
            speak("What should be the content of the email?")
            content = take_user_input()
            sendEmail(recipient, content)

        elif "addition" in query or "subtraction" in query or "multiplication" in query or "division" in query:
            performMathOperation(query)

        elif any(word in query for word in ["exit", "stop", "bye", "quit"]):
            speak("Goodbye! Have a great day!")
            break

    


