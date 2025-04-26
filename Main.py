import os
from os import startfile
from pyautogui import click
from keyboard import press, press_and_release, write
import pyttsx3
import speech_recognition as sr
import webbrowser as web
import speedtest
import pywhatkit
import wikipedia
import requests
import time

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set to female voice

# Speak function to output audio
def Speak(audio):
    try:
        print(f": {audio}")
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in Speak function: {e}")

# Function to take voice command from microphone
def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(": Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print(": Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f": Your Command: {query}\n")
    except Exception as e:
        print(f"Error: {e}")
        return ""
    return query.lower()

# Function to take text input
def PromptCommand():
    command = input("Enter your command: ")
    return command.lower()

# Function to play YouTube video directly
def YouTubePlay(video):
    try:
        Speak(f"Playing {video} on YouTube.")
        pywhatkit.playonyt(video)
    except Exception as e:
        print(f"Error: {e}")
        Speak("Unable to play the video on YouTube.")

# Function to run speed test
def SpeedTest():
    try:
        Speak("Running a speed test, please wait...")
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        Speak(f"Your download speed is {download_speed:.2f} Mbps")
        Speak(f"Your upload speed is {upload_speed:.2f} Mbps")
    except Exception as e:
        print(f"Error: {e}")
        Speak("Unable to complete the speed test.")

# Function to fetch information from Wikipedia or Google
def About(query):
    query = query.replace("about", "").strip()
    Speak(f"Searching for {query}...")
    try:
        result = wikipedia.summary(query, sentences=2)
        Speak(f"According to Wikipedia: {result}")
        print(f"Wikipedia: {result}")
    except wikipedia.exceptions.DisambiguationError as e:
        Speak("There are multiple results for this query. Searching Google instead.")
        web.open(f"https://www.google.com/search?q={query}")
    except Exception as e:
        Speak("Couldn't find an answer on Wikipedia. Searching Google instead.")
        web.open(f"https://www.google.com/search?q={query}")

# Global variables for Mars images
mars_images = []
current_image_index = 0

# Function to fetch and display Mars images
def MarsImages():
    global mars_images, current_image_index
    try:
        nasa_api_key = "e1oGjomlWlhR2YmYIJIHEtbYjfmMTVgfbX95ZvQC"
        rover_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={nasa_api_key}"

        response = requests.get(rover_url)
        data = response.json()

        mars_images = [photo['img_src'] for photo in data['photos']]

        if len(mars_images) > 0:
            current_image_index = 0
            Speak("Displaying the first Mars image.")
            web.open(mars_images[current_image_index])
        else:
            Speak("No Mars-related images found at this time.")
    except Exception as e:
        Speak("Unable to fetch Mars images.")
        print(f"Error: {e}")

# Function to show the next Mars image
def NextMarsImage():
    global current_image_index
    if len(mars_images) > 0:
        current_image_index = (current_image_index + 1) % len(mars_images)
        Speak(f"Displaying the next Mars image.")
        web.open(mars_images[current_image_index])
    else:
        Speak("No Mars images available to display.")

# Function to send a WhatsApp message
def SendWhatsAppMessage(contact_name, message):
    try:
        Speak(f"Sending WhatsApp message to {contact_name}.")
        startfile("WhatsApp.exe")
        time.sleep(5)

        click(x=200, y=100)
        write(contact_name)
        time.sleep(2)
        press("enter")

        write(message)
        press("enter")
        Speak("Message successfully sent.")
    except Exception as e:
        Speak("Unable to send WhatsApp message.")
        print(f"Error: {e}")

# Function to make a WhatsApp call
def WhatsAppCall(contact_name):
    try:
        Speak(f"Calling {contact_name} on WhatsApp.")
        startfile("WhatsApp.exe")
        time.sleep(5)

        click(x=200, y=100)
        write(contact_name)
        time.sleep(2)
        press("enter")

        click(x=1000, y=100)
        Speak("Call successfully initiated.")
    except Exception as e:
        Speak("Unable to make WhatsApp call.")
        print(f"Error: {e}")

# Function to open WhatsApp chats
def ShowWhatsAppChats():
    try:
        Speak("Opening WhatsApp chats.")
        startfile("WhatsApp.exe")
        time.sleep(5)
        Speak("WhatsApp chats are now open.")
    except Exception as e:
        Speak("Unable to open WhatsApp chats.")
        print(f"Error: {e}")

# Main Task Execution Function
def TaskExe():
    Speak("Hello! I am EchoBot. Please choose an input mode: voice or text.")
    print(": Choose your input mode - (1) Voice Command (2) Text Command")
    mode = input(": Enter 1 for Voice or 2 for Text: ")

    while True:
        if mode == "1":
            query = TakeCommand()
        elif mode == "2":
            query = PromptCommand()
        else:
            Speak("Invalid choice. Defaulting to text input.")
            mode = "2"
            query = PromptCommand()

        if not query:
            Speak("Sorry, I didn't catch that. Please try again.")
            continue

        # Command Handling
        if 'youtube search' in query:
            query = query.replace("youtube search", "").strip()
            YouTubePlay(query)

        elif 'google search' in query:
            query = query.replace("google search", "").strip()
            Speak(f"Searching Google for {query}.")
            web.open(f"https://www.google.com/search?q={query}")

        elif 'speed test' in query:
            SpeedTest()

        elif 'mars images' in query:
            MarsImages()

        elif 'next' in query:
            NextMarsImage()

        elif 'about' in query:
            About(query)

        elif 'send whatsapp message' in query:
            Speak("Who do you want to send a message to?")
            contact = TakeCommand() if mode == "1" else PromptCommand()
            Speak("What message should I send?")
            message = TakeCommand() if mode == "1" else PromptCommand()
            SendWhatsAppMessage(contact, message)

        elif 'whatsapp call' in query:
            Speak("Who do you want to call?")
            contact = TakeCommand() if mode == "1" else PromptCommand()
            WhatsAppCall(contact)

        elif 'show chats' in query:
            ShowWhatsAppChats()

        elif 'exit' in query or 'quit' in query or 'bye' in query:
            Speak("Goodbye! Have a nice day.")
            break

# Start the task execution
TaskExe()
