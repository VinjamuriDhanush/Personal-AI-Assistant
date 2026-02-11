import pyttsx3
import speech_recognition as sr
import datetime
import google.generativeai as genai
import os
import time
import pyautogui

# ------------------ CONFIG ------------------


genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# TTS Setup
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Zira
engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)

import pyttsx3

def speak(text):
  #  print("\n🔊 SPEAK FUNCTION CALLED")
    print(f"Trying to speak: {text}\n")

    try:
        engine = pyttsx3.init()              # Reinitialize engine every time
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)  # 0 = David, 1 = Zira

        engine.setProperty("volume", 1.0)
        engine.setProperty("rate", 185)

        engine.say(text)
        engine.runAndWait()
        engine.stop()
     #   print("✅ Speech finished.\n")
    except Exception as e:
        print(f"❌ TTS ERROR: {e}")



# ------------------ LISTEN ------------------

def listen():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 200
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""

    try:
        query = recognizer.recognize_google(audio, language="en-IN")
        print(f"You said: {query}")
        return query.lower()

    except Exception:
        return ""

#              changing volume




# ------------------ GEMINI RESPONSE ------------------
import subprocess
import webbrowser

def execute_local_commands(command):

    # ----- OPEN APPLICATIONS -----
    apps = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "vs code": r"C:\Users\YOUR_USERNAME\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "spotify": r"C:\Users\YOUR_USERNAME\AppData\Roaming\Spotify\Spotify.exe",
        "calculator": "calc.exe",
        "notepad": "notepad.exe"
    }

    for app in apps:
        if app in command:
            try:
                subprocess.Popen(apps[app])
                speak(f"Opening {app}")
                return True
            except:
                speak(f"I can't find {app} on this system.")
                return True

    # ----- WEBSITES -----
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return True

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        return True

    if "search" in command:
        query = command.replace("search", "")
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return True
    #volume

    if "increase volume" in command:
        query = command.replace("increase volume","")
        speak(f"increasing volume {query}")
        pyautogui.press("volumeup")
        return True
    if "decrease volume" in command:
        query = command.replace("decrease volume","")
        speak(f"decreasing volume{query}")
        pyautogui.press("volumedown")
        return True
    if "mute" in command:
        speak("muting the system")
        pyautogui.press("volumemute")
        return True       
    if "greatest" in command:
        speak("Dhanush is the greatest of all time")
        return True
    
    # ----- PLAY MUSIC (LOCAL FOLDER) -----
    if "play music" in command:
        MUSIC_DIR = r"D:\Music"  # <--- change this to your folder
        try:
            songs = os.listdir(MUSIC_DIR)
            os.startfile(os.path.join(MUSIC_DIR, songs[0]))
            speak("Playing music")
        except:
            speak("Music folder not found")
        return True

    return False

def get_llm_response(query):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(query)
        speak(response.text.strip())

    except Exception as e:
        print("AI Error:", e)
        speak("There was an issue communicating with the AI.")

# ------------------ WAKE WORD LOOP ------------------

WAKE_WORD = "hey jarvis"

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Listening for wake word...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio, language="en-IN").lower()
    except:
        return ""


# ------------------ MAIN ------------------

if __name__ == "__main__":
    speak("Jarvis system initialized. Say 'Hey Jarvis' to activate me.")

    while True:
        text = listen_for_wake_word()

        if WAKE_WORD in text:
            speak("Yes, I am listening...")

            # ✅ Stay in listening mode until user ends it
            while True:
                command = listen()

                if not command:
                    continue
                if execute_local_commands(command):
                    continue

                # ✅ Local time
                if "time" in command:
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    speak(f"The time is {now}")
                    continue

                # ✅ Local date
                if "date" in command:
                    today = datetime.datetime.now().strftime("%A, %d %B %Y")
                    speak(f"Today is {today}")
                    continue

                # ✅ Exit listening mode only, not program
                if any(word in command for word in ["stop listening", "go back", "sleep"]):
                    speak("Going back to wake mode.")
                    break

                # ✅ Shutdown program
                if any(exit_word in command for exit_word in ["exit", "bye", "shutdown"]):
                    speak("System shutting down. Goodbye.")
                    exit()

                # ✅ Send everything else to Gemini AI
                get_llm_response(command)


