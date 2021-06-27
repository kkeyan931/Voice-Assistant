import pyttsx3

text = "I will speak this text"

engine = pyttsx3.init()
engine.say(text)
engine.runAndWait()