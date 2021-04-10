import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
from gnewsclient import gnewsclient
import requests
from pyowm import OWM
import wikipedia
from PyDictionary import PyDictionary
import subprocess

import screen_brightness_control as sbc

import playSongGui
import translatorGui
import MailGui

from tkinter import *
from time import strftime


def greetings():
    day_time = int(strftime('%H'))

    greet = str()
    if day_time < 12:
        greet = 'Hello Sir. Good morning'
    elif 12 <= day_time < 18:
        greet = 'Hello Sir. Good afternoon'
    else:
        greet = 'Hello Sir. Good evening'

    return greet


def shutDown():
    base.destroy()


def openWebsite(command):
    reg_ex = re.search('open (.+)', command)
    if reg_ex:
        domain = reg_ex.group(1)
        url = 'https://www.' + domain + ".com"
        webbrowser.open(url)
        return 'The website you have requested has been opened.'
    else:
        return "unable to open the website"


def time():
    now = datetime.datetime.now()
    return 'Current time is %d hours %d minutes' % (now.hour, now.minute)


def news():
    try:
        client = gnewsclient.NewsClient(
            language="english", location="india", topic="business", max_results=3)
        news_list = client.get_news()
        return (news_list[0]["title"] + "\n" +
                news_list[1]["title"] + "\n" + news_list[2]["title"])
    except:
        return "unable to fetch the news"


def joke():
    res = requests.get(
        'https://icanhazdadjoke.com/',
        headers={"Accept": "application/json"})
    if res.status_code == requests.codes.ok:
        return str(res.json()['joke'])
    else:
        return 'oops!I ran out of jokes'


def weather(command):
    reg_ex = re.search('weather in (.*)', command)
    try:
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM('ab0d5e80e8dafb2cb81fa9e82431c1fa')
            mgr = owm.weather_manager()
            obs = mgr.weather_at_place(city)
            w = obs.weather
            k = w.detailed_status
            x = w.temperature(unit='celsius')
            return (
                    'Current weather in %s is %s The maximum temperature is %0.2f and the minimum temperature is '
                    '%0.2f degree celcius ' % (
                        city, k, x['temp_max'], x['temp_min']))
    except:
        return "unable to fetch the weather"


def meaning(command):
    dictionary = PyDictionary()
    reg_ex = re.search('meaning of (.*)', command)

    try:
        if reg_ex:
            word = reg_ex.group(1)
            res = dictionary.synonym(word)
            return res[0]

    except:
        return "unable to find the meaning"


def launch(command):
    reg_ex = re.search('launch (.*)', command)
    try:
        if reg_ex:
            app = reg_ex.group(1)
            os.popen(app)
            return "Application " + app + " opened"

    except:
        return "unable to open the application"


def wiki(command):
    reg_ex = re.search('tell me about (.*)', command)

    topic = reg_ex.group(1)
    try:
        return wikipedia.summary(topic,sentences=1)
    except Exception:
        for new_topic in wikipedia.search(topic,results=10):
            try:
                return wikipedia.summary(new_topic,sentences=1)
            except Exception:
                pass
    return "I don't know about " + topic


def openMailWindow():
    try:
        mailWindow = Toplevel(base)
        MailGui.MailWindow(mailWindow)
        return "Mail Window opened"
    except:
        return "Not able to open Mail window"



def playSong():
    try:
        musicPlayer = Toplevel(base)
        playSongGui.MusicPlayer(musicPlayer)
        return "Music Player opened"
    except:
        return "Not able to open the Music Player"


def translate():
    try:
        translator = Toplevel(base)
        translatorGui.TranslatorClass(translator)
        return "Translator Window opened"
    except:
        return "Not able to open the translator"


def brightness(command):
    valid = False

    while not valid:
        bright = input('What Brightness? > ')

        try:
            bright = int(bright)

            if (bright <= 100) and (bright >= 0):
                sbc.set_brightness(bright)
                valid = True

        except ValueError:
            pass

    return "brightness adjusted"


def volume(command):
    valid = False

    while not valid:
        volume = input('What volume? > ')

        try:
            volume = int(volume)
            if (volume <= 100) and (volume >= 0):
                subprocess.call(["amixer", "-D", "pulse", "sset", "Master", str(volume) + "%"])
                valid = True

        except ValueError:
            pass

    return "volume adjusted"


def bluetooth(command):
    try:
        if "on" in command:
            subprocess.call(["rfkill", "unblock", "bluetooth"])
        else:
            subprocess.call(["rfkill", "block", "bluetooth"])

    except:
        return "unable to connect bluetooth"


def assistant(command):
    response = "I can't understand you"
    if 'hello' in command:
        response = greetings()
    elif "shut down" in command:
        shutDown()
    elif "open" in command:
        response = openWebsite(command)
    elif "time" in command:
        response = time()
    elif "news" in command:
        response = news()

    elif "joke" in command:
        response = joke()

    elif 'weather' in command:
        response = weather(command)

    elif "tell me about" in command:
        response = wiki(command)

    elif "meaning" in command:
        response = meaning(command)

    elif "launch" in command:
        response = launch(command)

    elif "mail" in command:
        response = openMailWindow()

    elif "song" in command:
        response = playSong()

    elif "translate" in command:
        response = translate()

    elif "brightness" in command:
        response = brightness(command)

    elif "volume" in command:
        response = volume(command)

    elif "bluetooth" in command:
        response = bluetooth(command)

    return response


def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 30))

        res = assistant(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


base = Tk()
base.title("Voice Assistant")
base.geometry("700x900")
base.resizable(width=FALSE, height=FALSE)

ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font=("Arial", 35), wrap=WORD)

ChatLog.config(state=DISABLED)

scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

SendButton = Button(base, font=("Arial", 20, 'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                    command=send)

EntryBox = Text(base, bd=0, bg="white", width="29", height="5", font=("Arial", 30), insertwidth=5)

scrollbar.place(x=676, y=6, height=886)
ChatLog.place(x=6, y=6, height=780, width=665)
EntryBox.place(x=170, y=800, height=90, width=500)
SendButton.place(x=6, y=800, height=90)

base.mainloop()
