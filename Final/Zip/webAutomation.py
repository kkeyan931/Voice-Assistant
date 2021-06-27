import rpa as r

from selenium import webdriver
import time



def urlSnap():
    r.init(visual_automation=True)
    r.url('https://www.google.com')
    r.type("q", "CEG[enter]")
    print(r.read('result-stats'))
    r.snap('page', 'results.png')


def hackerrank():
    r.init(visual_automation=True)
    r.url("https://www.hackerrank.com/dashboard")
    r.dclick(".login.pull-right.btn.btn-dark.btn-default.mmT")
    r.dclick("input-1")
    userName = r.ask("Enter the User Name")
    r.type("input-1", userName)

    password = r.ask("Enter the password")

    r.type("input-2", password + "[enter]")


def faceBook():
    r.init(visual_automation=True)
    r.url("https://www.facebook.com")
    r.dclick("email")
    userName = r.ask("Enter the User Name")
    r.type("email", userName)

    password = r.ask("Enter the password")

    r.type("pass", password + "[enter]")


def youtube():
    r.init(visual_automation=True)
    r.url("https://www.youtube.com/")
    r.dclick("img")


def acoe():
    r.init(visual_automation=True)
    r.url("https://acoe.annauniv.edu/rusa/login/student")
    # rollNo = r.ask("enter roll number")
    r.type("input", "2018103549")

    r.type("password", "Amiami@143[enter]")

    r.dclick("login")


def fillForm():
    driver = webdriver.Chrome()

    driver.get(
        'https://docs.google.com/forms/d/e/1FAIpQLSd8RGl4Z3EDQilXK2XDdRDvX5nd04vxRG0kI-RoqgyWNLsbMA/viewform?usp=sf_link')

    time.sleep(1)

    datas = [
        ['karthikeyan', 'kkeyan931@gmail.com', '8220578186',
         'Ariyalur', 'nothing']
    ]

    for data in datas:

        count = 0

        textboxes = driver.find_elements_by_class_name(
            "quantumWizTextinputPaperinputInput")

        textareaboxes = driver.find_elements_by_class_name(
            "quantumWizTextinputPapertextareaInput")

        for value in textboxes:
            value.send_keys(data[count])
            count += 1

        for value in textareaboxes:
            value.send_keys(data[count])
            count += 1

        submit = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
        submit.click()

        another_response = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        another_response.click()

        time.sleep(10)
