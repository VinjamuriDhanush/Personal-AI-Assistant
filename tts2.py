import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 180)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
for v in voices:
    print(v.id)

engine.say("This is a test voice output.")
engine.runAndWait()
