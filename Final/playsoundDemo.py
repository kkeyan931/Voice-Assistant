import gtts
from playsound import playsound

t1 = gtts.gTTS("Welcome to javaTpoint")
t1.save("welcome.mp3")
playsound("welcome.mp3")