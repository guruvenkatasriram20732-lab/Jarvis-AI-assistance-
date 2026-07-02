from multiprocessing.dummy.connection import Listener
import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import time
import os
import webbrowser
import pywhatkit
import wikipedia
import pyjokes
import datetime
import requests
import customtkinter as ctk
def start_gui():

    app = ctk.CTk()
    app.title("JARVIS AI")
    app.geometry("500x350")

    label = ctk.CTkLabel(app, text="JARVIS AI ASSISTANT", font=("Arial",25))
    label.pack(pady=40)

    start_button = ctk.CTkButton(app, text="Start Jarvis", command=run_jarvis)
    start_button.pack(pady=20)

    stop_button = ctk.CTkButton(app, text="Exit", command=app.destroy)
    stop_button.pack(pady=10)

    app.mainloop()
import pyautogui
def change_volume(level):

    if level == "up":
        for _ in range(5):
            pyautogui.press("volumeup")
        speak("Volume increased")

    elif level == "down":
        for _ in range(5):
            pyautogui.press("volumedown")
        speak("Volume decreased")

    elif level == "mute":
        pyautogui.press("volumemute")
        speak("Volume muted")

        

def get_weather(city):
    api_key = "2746b04c920c5ba15b095352d1ea1846"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        speak("Sorry boss, I could not find that city.")
        return

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    speak(f"The temperature in {city} is {temp} degree celsius with {desc}")
# Initialize pygame mixer
pygame.mixer.init()

# ------------------ SPEAK FUNCTION (MALE VOICE) ------------------ #

async def speak_async(text):
    filename = "voice.mp3"
    
    # Choose Male Voice Here
    communicate = edge_tts.Communicate(text, "en-GB-RyanNeural", rate="+20%")  
    await communicate.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
     time.sleep(0.1)

    pygame.mixer.music.unload()
    os.remove(filename)

def speak(text):
    print("Jarvis:", text)
    asyncio.run(speak_async(text))


# ------------------ LISTEN FUNCTION ------------------ #
listener = sr.Recognizer()
def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = listener.listen(source, timeout=3, phrase_time_limit=4)
        except sr.WaitTimeoutError:
            return ""

    try:
        command = listener.recognize_google(audio)
        command = command.lower()
        print("You:", command)
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Internet connection problem boss")
        return ""


# ------------------ MAIN JARVIS ------------------ #

def run_jarvis():
    speak("Hello Sriram, I am your Jarvis.")

    while True:
        command = take_command()

        if "play" in command:
            song = command.replace("play", "")
            speak("Playing " + song)
            pywhatkit.playonyt(song)

        elif "hello jarvis" in  command:
            speak("Hello boss.How can I help you?")


        elif "jarvis" in command:
            speak("Yes boss. what can I do for you?")

        elif "time" in command:
            time_now = datetime.datetime.now().strftime('%I:%M %p')
            speak("Current time is " + time_now)

        elif "who is" in command:
            person = command.replace("who is", "")
            info = wikipedia.summary(person, 1)
            speak(info)


        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open spotify" in command:
            speak("Opening Spotify")
            os.startfile(r"C:\Users\Sriram\OneDrive\Desktop\Spotify.lnk")
   
         
        elif "open notepad" in command:
            os.system("notepad")
            speak("Opening Notepad")  

        elif "volume up" in command:
         change_volume("up")

        elif "volume down" in command:
            change_volume("down")

        elif "mute volume" in command:
            change_volume("mute")

        elif "weather" in command or "temperature" in command:
           speak("Which city?")
           city = take_command()
           get_weather(city)

        elif "shutdown computer" in command:
           speak("Shutting down the computer")
           os.system("shutdown /s /t 1")

        elif "restart computer" in command:
            speak("Restarting computer")
            os.system("shutdown /r /t 1")  

        
        elif "exit" in command or "stop" in command or "leave" in command:
            speak("Goodbye boss")
            break    

        elif command != "":
            speak("I did not understand that command boss!")

               
# ------------------ START ------------------ #

if __name__ == "__main__":
    start_gui()