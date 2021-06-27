import sys

import wikipedia
import webbrowser
import requests
from bs4 import BeautifulSoup

import urllib.request
import os

path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(path, 'Assets/AppData/')
path = path.replace(os.sep, '/')


class COVID:
    def __init__(self):
        self.total = 'Not Available'
        self.deaths = 'Not Available'
        self.recovered = 'Not Available'
        self.totalIndia = 'Not Available'
        self.deathsIndia = 'Not Available'
        self.recoveredIndia = 'Not Available'

    def covidUpdate(self):
        URL = 'https://www.worldometers.info/coronavirus/'
        result = requests.get(URL)
        src = result.content
        soup = BeautifulSoup(src, 'html.parser')

        temp = []
        divs = soup.find_all('div', class_='maincounter-number')
        for div in divs:
            temp.append(div.text.strip())
        self.total, self.deaths, self.recovered = temp[0], temp[1], temp[2]

    def covidUpdateIndia(self):
        URL = 'https://www.worldometers.info/coronavirus/country/india/'
        result = requests.get(URL)
        src = result.content
        soup = BeautifulSoup(src, 'html.parser')

        temp = []
        divs = soup.find_all('div', class_='maincounter-number')
        for div in divs:
            temp.append(div.text.strip())
        self.totalIndia, self.deathsIndia, self.recoveredIndia = temp[0], temp[1], temp[2]

    def totalCases(self, india_bool):
        if india_bool: return self.totalIndia
        return self.total

    def totalDeaths(self, india_bool):
        if india_bool: return self.deathsIndia
        return self.deaths

    def totalRecovery(self, india_bool):
        if india_bool: return self.recoveredIndia
        return self.recovered

    def symptoms(self):
        symt = ['1. Fever',
                '2. Coughing',
                '3. Shortness of breath',
                '4. Trouble breathing',
                '5. Fatigue',
                '6. Chills, sometimes with shaking',
                '7. Body aches',
                '8. Headache',
                '9. Sore throat',
                '10. Loss of smell or taste',
                '11. Nausea',
                '12. Diarrhea']
        return symt

    def prevention(self):
        prevention = ['1. Clean your hands often. Use soap and water, or an alcohol-based hand rub.',
                      '2. Maintain a safe distance from anyone who is coughing or sneezing.',
                      '3. Wear a mask when physical distancing is not possible.',
                      '4. Don’t touch your eyes, nose or mouth.',
                      '5. Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze.',
                      '6. Stay home if you feel unwell.',
                      '7. If you have a fever, cough and difficulty breathing, seek medical attention.']
        return prevention


def wikiResult(query):
    query = query.replace('wikipedia', '')
    query = query.replace('search', '')
    if len(query.split()) == 0: query = "wikipedia"
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception as e:
        return "Desired Result Not Found"


c = COVID()


def dataUpdate():
    c.covidUpdate()
    c.covidUpdateIndia()


### COVID ###
def covid(query):

    dataUpdate()
    if "india" in query:
        india_bool = True
    else:
        india_bool = False

    if "statistic" in query or 'report' in query:
        return ["Here are the statistics...",
                ["Total cases: " + c.totalCases(india_bool), "Total Recovery: " + c.totalRecovery(india_bool),
                 "Total Deaths: " + c.totalDeaths(india_bool)]]

    elif "symptom" in query:
        return ["Here are the Symptoms...", c.symptoms()]

    elif "prevent" in query or "measure" in query or "precaution" in query:
        return ["Here are the some of preventions from COVID-19:", c.prevention()]

    elif "recov" in query:
        return "Total Recovery is: " + c.totalRecovery(india_bool)

    elif "death" in query:
        return "Total Deaths are: " + c.totalDeaths(india_bool)

    else:
        return "Total Cases are: " + c.totalCases(india_bool)


def latestNews(news=5):
    URL = 'https://indianexpress.com/latest-news/'
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')

    headlineLinks = []
    headlines = []

    divs = soup.find_all('div', {'class': 'title'})

    count = 0
    for div in divs:
        count += 1
        if count > news:
            break
        a_tag = div.find('a')
        headlineLinks.append(a_tag.attrs['href'])
        headlines.append(a_tag.text)

    return headlines, headlineLinks


def maps(text):
    text = text.replace('maps', '')
    text = text.replace('map', '')
    text = text.replace('google', '')
    openWebsite('https://www.google.com/maps/place/' + text)
    return "maps opened"


def openWebsite(url='https://www.google.com/'):
    webbrowser.open(url)


def youtube(query):
    query = query.replace('youtube', '')
    result = urllib.parse.quote(query)
    # "https://www.youtube.com/results?search_query=" + query
    # webbrowser.open('https://www.youtube.com/watch?v=' + results[0]['id'])
    webbrowser.open("https://www.youtube.com/results?search_query=" + result)
    return "Showing Search Result For " + query


def googleSearch(query):
    if 'image' in query:
        query += "&tbm=isch"
    query = query.replace('images', '')
    query = query.replace('image', '')
    query = query.replace('search', '')
    query = query.replace('show', '')
    webbrowser.open("https://www.google.com/search?q=" + query)
    return "Here you go..."


def sendWhatsapp(phone_no='', message=''):
    phone_no = '+91' + str(phone_no)
    webbrowser.open('https://web.whatsapp.com/send?phone=' + phone_no + '&text=' + message)
    import time
    from pynput.keyboard import Key, Controller
    time.sleep(10)
    k = Controller()
    k.press(Key.enter)
    return "whatsapp opened"


def downloadImage(query, n=4):
    query = query.replace('images', '')
    query = query.replace('image', '')
    query = query.replace('search', '')
    query = query.replace('show', '')
    URL = "https://www.google.com/search?tbm=isch&q=" + query
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')
    imgTags = soup.find_all('img', class_='t0fcAb')

    if os.path.exists(path) == False:
        os.mkdir(path)

    count = 0
    for i in imgTags:
        if count == n: break
        try:
            urllib.request.urlretrieve(i['src'], (path + "/" + str(count) + '.jpg'))
            count += 1
        # print('Downloaded', count)
        except Exception as e:
            raise e
