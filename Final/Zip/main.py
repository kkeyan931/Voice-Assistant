import datetime
import subprocess
import webbrowser
from tkinter import *
from tkinter import messagebox
import os, sys, signal

import requests
from PyDictionary import PyDictionary
from PIL import ImageTk
import PIL.Image
import time

import speech_recognition as sr
import pyttsx3

import screen_brightness_control as sbc

from threading import Thread

from pyowm import OWM

import webAutomation
import playSongGui
import translatorGui
import webScrapping
import MailGui

from chatterbot import ChatBot

chatbot = ChatBot(
    "GUI Bot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation',
        }
    ],
    database_uri="sqlite:///database.sqlite3",
)

appdata_path = os.getenv('APPDATA')
pid = os.getpid()


def resource_path():
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    spriteFolderPath = os.path.join(CurrentPath, 'Assets/')
    path = os.path.join(spriteFolderPath)
    newPath = path.replace(os.sep, '/')
    return newPath


_path = resource_path()

ownerName = "Team12"
ownerDesignation = "Engineer"
Theme_Mode = 1  # 0=Light #1= Dark
ai_name = 'R.O.S.S'.lower()
data_update_check = 0

root = Tk()


# root.iconbitmap(_path+'Images/userI.ico')


def center_window(w=350, h=550):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()

    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


center_window(350, 550)

root.title("R.O.S.S User Registration")
root.resizable(0, 0)

r = IntVar()
Color_state = 0
Male_Check = IntVar()
Female_Check = IntVar()
userName_Var = StringVar()
userName_Var.set("Enter Your Name Here")
Gen = ""
stop_threads = False
status = "Stopped"

userFrame2 = Frame(root, bd=10, width=300, height=550, relief=FLAT)
userFrame2.pack(padx=10, pady=10)
firstAvatar_choosing_Frame = Frame(root)
Fake_L_3 = Label(firstAvatar_choosing_Frame, text=" ", font=('arial', 15))
Chouse_Avtar_LAbel = Label(firstAvatar_choosing_Frame, text="Choose Your Avatar", font=('arial', 15))
avatarContainer = Frame(firstAvatar_choosing_Frame, width=300, height=500)
SuccessfullyRegistered_Frame = Frame(root)

#
# def countDown():
#     addBtn.config(fg="black")
#     for k in range(10, 0, -1):
#         addBtn["text"] = "  Choose Avatar  " + "(" + str(k) + ")"
#         root.update()
#         time.sleep(0.94)
#     addBtn["text"] = "    Choose Avatar    "
#     addBtn.config(fg='white')




def typeit(widget, index, string):
    if len(string) > 0:
        widget.configure(state='normal')
        widget.insert(index, string[0])
        widget.configure(state='disabled')
    if len(string) > 1:
        index = widget.index("%s + 1 char" % index)

        widget.after(120, typeit, widget, index, string[1:])


Ross_Logo = PIL.Image.open(_path + 'Images/F.R.I.D.A.Y.jpg')
Ross_Logo = Ross_Logo.resize((200, 200))
Ross_Logo = ImageTk.PhotoImage(Ross_Logo)

Ro_Logo = Label(userFrame2, image=Ross_Logo)
Ro_Logo.pack()

Fake_L_1 = Label(userFrame2, text='                     \n ', font=('Arial Bold', 4))
Fake_L_1.pack()

text_Field = Text(userFrame2, font=('Fixedsys', 16), width=31, height=3)
text_Field.pack()

typeit(text_Field, "1.0", "Hello! I Am AKASH, I Am A\nVirtual Assistant")

Fake_L_2 = Label(userFrame2,
                 text='                     \n                          \n                 \n                ',
                 font=('Arial Bold', 120))
Fake_L_2.pack()


def on_name_input_click(event):
    if userName_Var.get() == "Enter Your Name Here":
        statusLbl.place(x=1000, y=1000)
        nameField.delete(0, "end")
        nameField.insert(0, '')
        nameField.config(fg='gray16')


def on_name_input_focusout(event):
    if userName_Var.get() != 'Enter Your Name Here':
        nameField.config(fg='gray16')
    if nameField.get() == '':
        userName_Var.set('Enter Your Name Here')
        nameField.config(fg='grey60')


nameLbl = Label(userFrame2, text='Name', font=('Arial Bold', 12))
nameLbl.place(x=20, y=300)
nameField = Entry(userFrame2, textvariable=userName_Var, bd=5, font=("Comic Sans MS", 9), width=25, relief=FLAT,
                  bg="pale turquoise", fg="gray60")
nameField.place(x=90, y=300)

nameField.bind('<FocusIn>', on_name_input_click)
nameField.bind('<FocusOut>', on_name_input_focusout)

genLbl = Label(userFrame2, text='Gender', font=('Arial Bold', 12))
genLbl.place(x=20, y=360)

genMaleImg = PIL.Image.open(_path + 'Images/Male.png')
genMaleImg = genMaleImg.resize((35, 35))
genMaleImg = ImageTk.PhotoImage(genMaleImg)

genFemaleImg = PIL.Image.open(_path + 'Images/Female.png')
genFemaleImg = genFemaleImg.resize((35, 35))
genFemaleImg = ImageTk.PhotoImage(genFemaleImg)


def specChoice(V):
    global Gen, ownerDesignation
    if V == 1:
        Gen = "Male"
        ownerDesignation = "Sir"
        Female_Check.set(0)

    if V == 2:
        Gen = "Female"
        ownerDesignation = "Madam"
        Male_Check.set(0)


Malecheck_Btn = Checkbutton(userFrame2, cursor="hand2", variable=Male_Check, command=lambda: specChoice(1), onvalue=1,
                            offvalue=0, height=2, width=10)
Malecheck_Btn.place(x=85, y=353)

Male_Logo = Label(userFrame2, image=genMaleImg, bg="black")
Male_Logo.place(x=138, y=351)

Femalecheck_Btn = Checkbutton(userFrame2, cursor="hand2", variable=Female_Check, command=lambda: specChoice(2),
                              onvalue=1, offvalue=0, height=2, width=10)
Femalecheck_Btn.place(x=170, y=353)

Female_Logo = Label(userFrame2, image=genFemaleImg, bg="black")
Female_Logo.place(x=223, y=351)

Male_Logo = Label(userFrame2, image=genMaleImg, bg="black")
Male_Logo.place(x=138, y=351)


def Add_Face():
    global user_name, ownerName
    user_name = userName_Var.get()
    if user_name == '' or user_name == "Enter Your Name Here":
        statusLbl.place(x=91, y=470)

        statusLbl.config(bg="ivory2", fg="indian red", text="(Enter Your Name)")
    elif Male_Check.get() == 0 and Female_Check.get() == 0:
        statusLbl.place(x=87, y=470)

        statusLbl.config(bg="ivory2", fg="indian red", text="(Select Your Gender)")
    else:
        ownerName = user_name
        firstAvatar_choosing_Frame.place(x=30, y=0)


Light_ModeImg = PIL.Image.open(_path + 'Images/LightMode.png')
Light_ModeImg = Light_ModeImg.resize((22, 22))
Light_ModeImg = ImageTk.PhotoImage(Light_ModeImg)

Dark_ModeImg = PIL.Image.open(_path + 'Images/DarkMode.png')
Dark_ModeImg = Dark_ModeImg.resize((22, 22))
Dark_ModeImg = ImageTk.PhotoImage(Dark_ModeImg)

Dark_Mode_Button = Button(root, cursor="hand2", image=Dark_ModeImg, bd=2, padx=10)
Light_Mode_Button = Button(root, cursor="hand2", image=Light_ModeImg, bd=2, padx=10)

addBtn = Button(userFrame2, text='    Choose Avatar    ', font=('Arial Bold', 12), bg='#01933B', fg='white',
                command=Add_Face, relief=FLAT)
addBtn.place(x=75, y=430)

statusLbl = Label(userFrame2, text='', font=('Cooper Black', 9))

check_Img = PIL.Image.open(_path + 'Images/Check.png')
check_Img = check_Img.resize((72, 72))
check_Img = ImageTk.PhotoImage(check_Img)

avatarChoosen = 0

coordinates_List = [(50, 50), (0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)]


def selectAVATAR(avt=0):
    global avatarChoosen, ownerPhoto
    avatarChoosen = avt
    i = 1
    for avtr in (avtb1, avtb2, avtb3, avtb4, avtb5, avtb6, avtb7, avtb8):
        if i == avt:
            row, column = coordinates_List[i]
            # print(i)
            check_Label.grid(row=row, column=column, ipadx=25, ipady=10)
            avtr['state'] = 'disabled'
            userPIC['image'] = avtr['image']
            ownerPhoto = i
            usernameLbl.config(text=userName_Var.get())
        else:
            avtr['state'] = 'normal'
        i += 1


Fake_L_3.pack()
Chouse_Avtar_LAbel.place(x=52, y=10)
avatarContainer.pack(pady=10)

size = 92
avtr1 = PIL.Image.open(_path + 'Images/Avatar/UserFace1.png')
avtr1 = avtr1.resize((size, size))
avtr1 = ImageTk.PhotoImage(avtr1)
avtr2 = PIL.Image.open(_path + 'Images/Avatar/UserFace2.png')
avtr2 = avtr2.resize((size, size))
avtr2 = ImageTk.PhotoImage(avtr2)
avtr3 = PIL.Image.open(_path + 'Images/Avatar/UserFace3.png')
avtr3 = avtr3.resize((size, size))
avtr3 = ImageTk.PhotoImage(avtr3)
avtr4 = PIL.Image.open(_path + 'Images/Avatar/UserFace4.png')
avtr4 = avtr4.resize((size, size))
avtr4 = ImageTk.PhotoImage(avtr4)
avtr5 = PIL.Image.open(_path + 'Images/Avatar/UserFace5.png')
avtr5 = avtr5.resize((size, size))
avtr5 = ImageTk.PhotoImage(avtr5)
avtr6 = PIL.Image.open(_path + 'Images/Avatar/UserFace6.png')
avtr6 = avtr6.resize((size, size))
avtr6 = ImageTk.PhotoImage(avtr6)
avtr7 = PIL.Image.open(_path + 'Images/Avatar/UserFace7.png')
avtr7 = avtr7.resize((size, size))
avtr7 = ImageTk.PhotoImage(avtr7)
avtr8 = PIL.Image.open(_path + 'Images/Avatar/UserFace8.png')
avtr8 = avtr8.resize((size, size))
avtr8 = ImageTk.PhotoImage(avtr8)

avtb1 = Button(avatarContainer, cursor="hand2", image=avtr1, relief=FLAT, bd=0, command=lambda: selectAVATAR(1))
avtb1.grid(row=0, column=0, ipadx=25, ipady=10)

avtb2 = Button(avatarContainer, cursor="hand2", image=avtr2, relief=FLAT, bd=0, command=lambda: selectAVATAR(2))
avtb2.grid(row=0, column=1, ipadx=25, ipady=10)

avtb3 = Button(avatarContainer, cursor="hand2", image=avtr3, relief=FLAT, bd=0, command=lambda: selectAVATAR(3))
avtb3.grid(row=1, column=0, ipadx=25, ipady=10)

avtb4 = Button(avatarContainer, cursor="hand2", image=avtr4, relief=FLAT, bd=0, command=lambda: selectAVATAR(4))
avtb4.grid(row=1, column=1, ipadx=25, ipady=10)

avtb5 = Button(avatarContainer, cursor="hand2", image=avtr5, relief=FLAT, bd=0, command=lambda: selectAVATAR(5))
avtb5.grid(row=2, column=0, ipadx=25, ipady=10)

avtb6 = Button(avatarContainer, cursor="hand2", image=avtr6, relief=FLAT, bd=0, command=lambda: selectAVATAR(6))
avtb6.grid(row=2, column=1, ipadx=25, ipady=10)

avtb7 = Button(avatarContainer, cursor="hand2", image=avtr7, relief=FLAT, bd=0, command=lambda: selectAVATAR(7))
avtb7.grid(row=3, column=0, ipadx=25, ipady=10)

avtb8 = Button(avatarContainer, cursor="hand2", image=avtr8, relief=FLAT, bd=0, command=lambda: selectAVATAR(8))
avtb8.grid(row=3, column=1, ipadx=25, ipady=10)

check_Label = Label(avatarContainer, image=check_Img, bd=0)


def exit_Check(ar):
    if ar == 1:
        root.destroy()
    if ar == 2:
        ans = messagebox.askquestion("Exit!", "Are you want to exit?")
        if ans == "yes":
            root.destroy()
            sys.exit()


def SuccessfullyRegistered():
    if avatarChoosen != 0:
        Text = user_name
        Text_spilt = Text.split()
        Text_spilt1 = "Hi, " + (Text_spilt[0]) + "\nYou Are Ready To Use R.O.S.S"
        Wellcome_Label.config(text=Text_spilt1)
        SuccessfullyRegistered_Frame.place(x=3, y=0)


Button(firstAvatar_choosing_Frame, text='         Submit         ', font=('Arial Bold', 15), bg='#01933B', fg='white',
       bd=0, command=SuccessfullyRegistered, relief=FLAT).pack()

userPIC = Label(SuccessfullyRegistered_Frame, image=avtr1)
userPIC.pack(pady=(40, 10))
usernameLbl = Label(SuccessfullyRegistered_Frame, text=" ", font=('Arial Bold', 15))
usernameLbl.pack(pady=(0, 70))

Wellcome_Label = Label(SuccessfullyRegistered_Frame, font=('Arial Bold', 15), wraplength=300)
Wellcome_Label.pack(pady=10)

Fake_L_4 = Label(SuccessfullyRegistered_Frame, text="                ", font=('arial', 15), wraplength=350)
Fake_L_4.pack()

Wellcome_msg_Label = Label(SuccessfullyRegistered_Frame,
                           text="Click On 'Ok' Button To Start Conversation with\nR.O.S.S", font=('arial', 13),
                           wraplength=350)
Wellcome_msg_Label.pack()

LaunchBtn = Button(SuccessfullyRegistered_Frame, text='     OK     ', bg='#0475BB', fg='white', font=('Arial Bold', 18),
                   bd=0, command=lambda: exit_Check(1), relief=FLAT)
LaunchBtn.pack(pady=50)


def change_color_fun(col):
    global Theme_Mode
    Main_Bg_Color_Light = "#dff3ff"
    Main_Text_Color_Light = "#303E54"
    Main_Bg_Color_Dark = "#333333"
    Main_Text_Color_Dark = "#c9e6ff"
    if col == 0:
        Light_Mode_Button.place(x=1000, y=1000)
        Dark_Mode_Button.place(x=312, y=512)
        root.config(bg=Main_Bg_Color_Light)
        Ro_Logo.config(bg="#42b8ff")
        Fake_L_1.config(bg=Main_Bg_Color_Light, fg=Main_Bg_Color_Light)
        Fake_L_2.config(bg=Main_Bg_Color_Light, fg=Main_Bg_Color_Light)
        Fake_L_3.config(bg=Main_Bg_Color_Light, fg=Main_Bg_Color_Light)
        Fake_L_4.config(bg=Main_Bg_Color_Light, fg=Main_Bg_Color_Light)
        text_Field.config(bg="azure3", fg="#0e5d0e")
        nameLbl.config(fg=Main_Text_Color_Light, bg=Main_Bg_Color_Light)
        genLbl.config(fg=Main_Text_Color_Light, bg=Main_Bg_Color_Light)
        # nameField.config(bg="pale turquoise",fg="gray60")
        Malecheck_Btn.config(bg=Main_Bg_Color_Light, activebackground=Main_Bg_Color_Light)
        Male_Logo.config(bg=Main_Bg_Color_Light)
        Femalecheck_Btn.config(bg=Main_Bg_Color_Light, activebackground=Main_Bg_Color_Light)
        Female_Logo.config(bg=Main_Bg_Color_Light)
        userFrame2.config(bg=Main_Bg_Color_Light)
        statusLbl.config(bg=Main_Bg_Color_Light)
        firstAvatar_choosing_Frame.config(bg=Main_Bg_Color_Light)
        avatarContainer.config(bg=Main_Bg_Color_Light)
        Chouse_Avtar_LAbel.config(bg="lavender", fg="#303E54")
        check_Label.config(bg=Main_Bg_Color_Light)
        avtb1.config(bg=Main_Bg_Color_Light, activebackground=Main_Bg_Color_Light)
        avtb2.config(bg=Main_Bg_Color_Light, activebackground=Main_Bg_Color_Light)
        avtb3.config(bg=Main_Bg_Color_Light, activebackground=Main_Bg_Color_Light)
        avtb4.config(bg=Main_Bg_Color_Light, activebackground=Main_Bg_Color_Light)
        avtb5.config(bg=Main_Bg_Color_Light, activebackground=Main_Bg_Color_Light)
        avtb6.config(bg=Main_Bg_Color_Light, activebackground=Main_Bg_Color_Light)
        avtb7.config(bg=Main_Bg_Color_Light, activebackground=Main_Bg_Color_Light)
        avtb8.config(bg=Main_Bg_Color_Light, activebackground=Main_Bg_Color_Light)
        SuccessfullyRegistered_Frame.config(bg=Main_Bg_Color_Light)
        Wellcome_msg_Label.config(bg=Main_Bg_Color_Light, fg='#515255')
        Wellcome_Label.config(bg=Main_Bg_Color_Light, fg='#303E54')
        userPIC.config(bg=Main_Bg_Color_Light)
        usernameLbl.config(bg=Main_Bg_Color_Light, fg='#367470')
        Theme_Mode = 0
    if col == 1:  # Black Color
        Dark_Mode_Button.place(x=1000, y=1000)
        Light_Mode_Button.place(x=312, y=512)
        root.config(bg=Main_Bg_Color_Dark)
        Ro_Logo.config(bg="grey70")
        Fake_L_1.config(bg=Main_Bg_Color_Dark, fg=Main_Bg_Color_Dark)
        Fake_L_2.config(bg=Main_Bg_Color_Dark, fg=Main_Bg_Color_Dark)
        Fake_L_3.config(bg=Main_Bg_Color_Dark, fg=Main_Bg_Color_Dark)
        Fake_L_4.config(bg=Main_Bg_Color_Dark, fg=Main_Bg_Color_Dark)
        text_Field.config(bg="#141414", fg="green")
        nameLbl.config(fg=Main_Text_Color_Dark, bg=Main_Bg_Color_Dark)
        genLbl.config(fg=Main_Text_Color_Dark, bg=Main_Bg_Color_Dark)

        Malecheck_Btn.config(bg=Main_Bg_Color_Dark, activebackground=Main_Bg_Color_Dark)
        Male_Logo.config(bg=Main_Bg_Color_Dark)
        Femalecheck_Btn.config(bg=Main_Bg_Color_Dark, activebackground=Main_Bg_Color_Dark)
        Female_Logo.config(bg=Main_Bg_Color_Dark)
        userFrame2.config(bg=Main_Bg_Color_Dark)
        statusLbl.config(bg=Main_Bg_Color_Dark)
        firstAvatar_choosing_Frame.config(bg=Main_Bg_Color_Dark)
        avatarContainer.config(bg=Main_Bg_Color_Dark)
        Chouse_Avtar_LAbel.config(bg="light slate gray", fg="old lace")
        check_Label.config(bg=Main_Bg_Color_Dark)
        avtb1.config(bg=Main_Bg_Color_Dark, activebackground=Main_Bg_Color_Dark)
        avtb2.config(bg=Main_Bg_Color_Dark, activebackground=Main_Bg_Color_Dark)
        avtb3.config(bg=Main_Bg_Color_Dark, activebackground=Main_Bg_Color_Dark)
        avtb4.config(bg=Main_Bg_Color_Dark, activebackground=Main_Bg_Color_Dark)
        avtb5.config(bg=Main_Bg_Color_Dark, activebackground=Main_Bg_Color_Dark)
        avtb6.config(bg=Main_Bg_Color_Dark, activebackground=Main_Bg_Color_Dark)
        avtb7.config(bg=Main_Bg_Color_Dark, activebackground=Main_Bg_Color_Dark)
        avtb8.config(bg=Main_Bg_Color_Dark, activebackground=Main_Bg_Color_Dark)
        SuccessfullyRegistered_Frame.config(bg=Main_Bg_Color_Dark)
        Wellcome_msg_Label.config(bg=Main_Bg_Color_Dark, fg="snow3")
        Wellcome_Label.config(bg=Main_Bg_Color_Dark, fg="#5f9ea0")
        userPIC.config(bg=Main_Bg_Color_Dark)
        usernameLbl.config(bg=Main_Bg_Color_Dark, fg="#85AD4F")
        Theme_Mode = 1


Dark_Mode_Button.config(command=lambda: change_color_fun(1))
Light_Mode_Button.config(command=lambda: change_color_fun(0))


change_color_fun(1)

root.protocol("WM_DELETE_WINDOW", lambda: exit_Check(2))


class MainWindow():
    def __init__(self):
        Voice_start.start()
        mainwindow.mainloop()


chatBgColor = "red"

root.mainloop()

mainwindow = Tk()

EXIT_COMMANDS = ['bye', 'exit', 'quit', 'shut down', 'shutdown']

chatBgColor = '#12232e'
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'
botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"
KCS_IMG = Theme_Mode
voice_id = 0
ass_volume = 1
ass_voiceRate = 200


def center_window2(w=400, h=650):
    ws = mainwindow.winfo_screenwidth()
    hs = mainwindow.winfo_screenheight()
    # calculate position x, y
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)  # change hs/2 to hs/4 to left window up
    mainwindow.geometry('%dx%d+%d+%d' % (w, h, x, y))


center_window2(400, 650)

mainwindow.title("R.O.S.S")
mainwindow.resizable(0, 0)
# mainwindow.iconbitmap(_path+'Images/assistant2.ico')

n = StringVar(mainwindow)
n2 = StringVar(mainwindow)
themeValue = IntVar(mainwindow)
chatMode = 1

main_frame = Frame(mainwindow, bg=chatBgColor)
settings_frame = Frame(mainwindow, bg=background)
secondAvatar_choosing_Frame = Frame(mainwindow)
About_Frame = Frame(mainwindow, bg=background)

rock_P__Frame = Frame(mainwindow)

Fake_L_N1 = Label(secondAvatar_choosing_Frame, text=" ", font=('arial', 2))
Fake_L_N1.pack()
Chouse_Avtar_LAbel_2nd = Label(secondAvatar_choosing_Frame, text="Choose Your Avatar", font=('arial', 15))
avatarContainer_2nd = Frame(secondAvatar_choosing_Frame, width=300, height=500)

chat_frame = Frame(main_frame, width=380, height=551, bg=chatBgColor)
chat_frame.pack(padx=10)
chat_frame.pack_propagate(0)

bottomFrame1 = Frame(main_frame, bg='#dfdfdf', height=100)
bottomFrame1.pack(fill=X, side=BOTTOM)
VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
VoiceModeFrame.pack(fill=BOTH)
TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
TextModeFrame.pack(fill=BOTH)

TextModeFrame.pack_forget()


def attachTOframe(text, bot=False):
    if bot:
        botchat = Label(chat_frame, text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250,
                        font=('Montserrat', 12, 'bold'))
        botchat.pack(anchor='w', ipadx=5, ipady=5, pady=5)
    else:
        userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=250,
                         font=('Montserrat', 12, 'bold'))
        userchat.pack(anchor='e', ipadx=2, ipady=2, pady=5)


def clearChatScreen():
    for wid in chat_frame.winfo_children():
        wid.destroy()


img0, img1, img2, img3, img4 = None, None, None, None, None


def showSingleImage(type, data=None):
    global img0, img1, img2, img3, img4
    try:
        img0 = ImageTk.PhotoImage(
            PIL.Image.open(_path + '/AppData/0.jpg').resize((90, 110), PIL.Image.ANTIALIAS))
    except:
        pass
    img1 = ImageTk.PhotoImage(PIL.Image.open(_path + 'Images/heads.jpg').resize((220, 200), PIL.Image.ANTIALIAS))
    img2 = ImageTk.PhotoImage(PIL.Image.open(_path + 'Images/tails.jpg').resize((220, 200), PIL.Image.ANTIALIAS))
    img4 = ImageTk.PhotoImage(PIL.Image.open(_path + 'Images/WeatherImage.png'))

    if type == "weather":
        weather = Frame(chat_frame)
        weather.pack(anchor='w')
        Label(weather, image=img4, bg=chatBgColor).pack()
        Label(weather, text=data[0], font=('Arial Bold', 45), fg='white', bg='#3F48CC').place(x=65, y=45)
        Label(weather, text=data[1], font=('Montserrat', 15), fg='white', bg='#3F48CC').place(x=78, y=110)
        Label(weather, text=data[2], font=('Montserrat', 10), fg='white', bg='#3F48CC').place(x=78, y=140)
        Label(weather, text=data[3], font=('Arial Bold', 12), fg='white', bg='#3F48CC').place(x=60, y=160)

    elif type == "wiki":
        Label(chat_frame, image=img0, bg='#EAEAEA').pack(anchor='w')
    elif type == "head":
        Label(chat_frame, image=img1, bg='#EAEAEA').pack(anchor='w')
    elif type == "tail":
        Label(chat_frame, image=img2, bg='#EAEAEA').pack(anchor='w')
    else:
        img3 = ImageTk.PhotoImage(
            PIL.Image.open(_path + 'Images/Dice/' + type + '.jpg').resize((200, 200), PIL.Image.ANTIALIAS))
        Label(chat_frame, image=img3, bg='#EAEAEA').pack(anchor='w')


def show_Chat_Frame():
    settings_frame.place(x=1000, y=1000)
    About_Frame.place(x=1000, y=1000)
    main_frame.place(x=0, y=0)


def changeChatMode():
    global chatMode
    if chatMode == 1:
        VoiceModeFrame.pack_forget()
        TextModeFrame.pack(fill=BOTH)
        UserField.focus()
        chatMode = 0
    else:
        TextModeFrame.pack_forget()
        VoiceModeFrame.pack(fill=BOTH)
        mainwindow.focus()
        chatMode = 1


def exit_conformation(v):
    if v == 1:
        ans = messagebox.askquestion("Exit!", "Are you want to exit?")
        if ans == "yes":
            mainwindow.destroy()
            os.kill(pid, signal.SIGTERM)
    if v == 2:
        mainwindow.destroy()
        os.kill(pid, signal.SIGTERM)
    # sys.exit()


def SuccessfullyRegistered_2nd():
    if avatarChoosen != 0:
        global ownerPhoto, userProfileImg, userIcon
        userProfileImg = ImageTk.PhotoImage(
            PIL.Image.open(_path + 'Images/Avatar/UserFace' + str(ownerPhoto) + ".png").resize((120, 120)))
        # userPhoto['image'] = userProfileImg
        userIcon = PhotoImage(file=_path + 'Images/Avatar/ChatIcons/a' + str(ownerPhoto) + ".png")
        secondAvatar_choosing_Frame.place(x=1000, y=1000)
        settings_frame.place(x=50, y=0)


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[voice_id].id)  # male
engine.setProperty('volume', ass_volume)


def speak(text, display=False, icon=False):
    AITaskStatusLbl['text'] = 'Speaking...'
    if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w', pady=0)
    if display: attachTOframe(text, True)
    engine.say(text[0:30])
    engine.runAndWait()


def record(clearChat=True, iconDisplay=True):
    AITaskStatusLbl['text'] = 'Listening...'
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        said = ""
        try:
            AITaskStatusLbl['text'] = 'Processing...'
            said = r.recognize_google(audio)
            # print(f"\nUser said: {said}")
            if clearChat:
                clearChatScreen()
            if iconDisplay: Label(chat_frame, image=userIcon,
                    bg=chatBgColor).pack(anchor='e', pady=0)
            attachTOframe(said)
        except Exception as e:

            if "connection failed" in str(e):
                speak("Your System is Offline...", True, True)
            return 'None'
    return said.lower()


def record2forkey(y, clearChat=True, iconDisplay=True):
    # print('\nListening...')
    AITaskStatusLbl['text'] = 'Listening...'
    r = y
    # audio = r
    said = r
    try:
        AITaskStatusLbl['text'] = 'Processing...'

        if clearChat:
            clearChatScreen()
        if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e', pady=0)
        attachTOframe(said)
    except Exception as e:

        if "connection failed" in str(e):
            speak("Your System is Offline...", True, True)
        return 'None'
    return said.lower()


def voiceMedium():
    while True:
        query = record()
        if query == 'None': continue
        if isContain(query, EXIT_COMMANDS):
            speak("Shutting down the System. Good Bye " + ownerDesignation + "!", True, True)
            exit_conformation(2)
            break
        else:
            main(query.lower())


def keyboardInput(e):
    user_input = UserField.get().lower()
    text = user_input
    if user_input != "":
        clearChatScreen()
        if isContain(user_input, EXIT_COMMANDS):
            speak("Shutting down the System. Good Bye " + ownerDesignation + "!", True, True)
            exit_conformation(2)
        else:
            Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e', pady=0)
            attachTOframe(user_input.capitalize())

            record2forkey(user_input)
            Thread(target=lambda: main(user_input)).start()
        UserField.delete(0, END)


def isContain(txt, lst):
    for word in lst:
        if word in txt:
            return True
    return False


# 1 Greetings

def greetings():
    day_time = int(time.strftime('%H'))

    if day_time < 12:
        greet = 'Hello Sir. Good morning'
    elif 12 <= day_time < 18:
        greet = 'Hello Sir. Good afternoon'
    else:
        greet = 'Hello Sir. Good evening'

    return greet


# 2 Open Website

def openWebsite(command):
    reg_ex = re.search('open (.+)', command)
    if reg_ex:
        domain = reg_ex.group(1)
        url = 'https://www.' + domain + ".com"
        webbrowser.open(url)
        return 'The website you have requested has been opened.'
    else:
        return "unable to open the website"


# 3 Jokes

def joke():
    res = requests.get(
        'https://icanhazdadjoke.com/',
        headers={"Accept": "application/json"})
    if res.status_code == requests.codes.ok:
        return str(res.json()['joke'])
    else:
        return 'oops!I ran out of jokes'


# 4 weather

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


# 5 Meaning

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


# 6 Time

def currentTime():
    now = datetime.datetime.now()
    return 'Current time is %d hours %d minutes' % (now.hour, now.minute)


# 7 Launch Application

def launch(command):
    reg_ex = re.search('launch (.*)', command)
    try:
        if reg_ex:
            app = reg_ex.group(1)
            os.popen(app)
            return "Application " + app + " opened"

    except:
        return "unable to open the application"


# 9 Mail Window GUI

def openMailWindow():
    try:
        mailWindow = Toplevel(mainwindow)
        MailGui.MailWindow(mailWindow)
        return "Mail Window opened"
    except:
        return "Not able to open Mail window"


# 10 Play Song GUI

def playSong():
    try:
        player = playSongGui.MusicPlayer()
        return "Music Player opened"
    except:
        return "Not able to open the Music Player"


# 11 Translate Window GUI

def translate():
    try:
        translator = Toplevel(mainwindow)
        translatorGui.TranslatorClass(translator)
        return "Translator Window opened"
    except:
        return "Not able to open the translator"


# 12 Control Brightness

def brightness(command):
    reg_ex = re.search('brightness (.*)', command)
    bright = reg_ex.group(1)

    try:
        bright = int(bright)

        if (bright <= 100) and (bright >= 0):
            sbc.set_brightness(bright)

        return "brightness adjusted"

    except ValueError:
        return "unable to adjust the brightness"


# 13 Control Volume

def volume(command):
    reg_ex = re.search('brightness (.*)', command)
    volume = reg_ex.group(1)

    try:
        volume = int(volume)
        if (volume <= 100) and (volume >= 0):
            subprocess.call(["amixer", "-D", "pulse", "sset", "Master", str(volume) + "%"])

        return "volume adjusted"

    except ValueError:
        return "unable to adjust the Volume"


# 14 Bluetooth Control

def bluetooth(command):
    try:
        if "on" in command:
            subprocess.call(["rfkill", "unblock", "bluetooth"])
        else:
            subprocess.call(["rfkill", "block", "bluetooth"])

    except:
        return "unable to connect bluetooth"


# 15 Web Automation

def automate(command):
    try:
        if "snap" in command:
            webAutomation.urlSnap()
        if "hack" in command:
            webAutomation.hackerrank()
        if "facebook" in command:
            webAutomation.faceBook()
        if "acoe" in command:
            webAutomation.acoe()
        if "form" in command:
            webAutomation.fillForm()
        return "opened"

    except:
        return "unable to automate"


def main(text):
    response = ""

    # 1 Greetings

    if 'hello' in text:
        response = greetings()
        speak(response, True, False)
        return

    # 2 Open Website

    if "open" in text:
        response = openWebsite(text)
        speak(response, True, True)
        return

    # 3 Joke

    if "joke" in text:
        response = joke()
        speak(response, True, False)
        return

    # 4 weather

    if "weather" in text:
        response = weather(text)
        speak(response, True, False)
        return

    # 5 Meaning

    if "meaning" in text:
        response = meaning(text)
        speak(response, True, False)
        return

    # 6 Current Time

    if "time" in text:
        response = currentTime()
        speak(response, True, False)
        return

    if isContain(text, ['news']):
        speak('Getting the latest news...', True, True)
        headlines, headlineLinks = webScrapping.latestNews(2)
        for head in headlines: speak(head, True)
        return

    # 7 Launch Application

    if "launch" in text:
        response = launch(text)
        speak("Opening....", True, True)
        speak(response, True, False)
        return

    # 8 Wikipedia From WebScrapping

    if isContain(text, ['wiki', 'who is']):
        Thread(target=webScrapping.downloadImage, args=(text, 1,)).start()
        speak('Searching...', True, True)
        result = webScrapping.wikiResult(text)
        showSingleImage('wiki')
        speak(result, True)
        return

    # 9 Mail Window GUI

    if "mail" in text:
        response = openMailWindow()
        speak("Opening....", True, True)
        speak(response, True, False)
        return

    # 10 Play Song GUI

    if "song" in text:
        response = playSong()
        speak("Opening....", True, True)
        speak(response, True, False)
        return

    # 11 Translate Window GUI

    if "translate" in text:
        response = translate()
        speak("Opening....", True, True)
        speak(response, True, False)
        return

    # 12 brightness

    if "brightness" in text:
        response = brightness(text)
        speak(response, True, False)
        return

    # 13 Volume

    if "volume" in text:
        response = volume(text)
        speak(response, True, False)
        return

    # 14 Blutooth

    if "bluetooth" in text:
        response = bluetooth(text)
        speak(response, True, False)
        return

    # Web Automation

    if "automate" in text:
        response = automate(text)
        speak(response, True, False)
        return

        # Web Scrapping
    if "map" in text:
        response = webScrapping.maps(text)
        speak(response, True, False)
        return

    if "youtube" in text:
        response = webScrapping.youtube(text)
        speak(response, True, False)
        return

    if "whatsapp" in text:
        content = text.split(" ")
        response = webScrapping.sendWhatsapp(content[1], content[2,:])
        speak(response, True, False)
        return

    if "google" in text:
        content = text.split(" ")
        response = webScrapping.googleSearch(content[1])
        speak(response, True, False)
        return

    if "covid" in text:
        response = webScrapping.covid(text)
        speak(response,True,False)
        return

    #Chat Bot
    else:
        #response = "I can't understand you"
        response = chatbot.get_response(text).text
        speak(response, True, False)
        return


cblLightImg = PhotoImage(file=_path + 'Images/centralButton.png')
cblDarkImg = PhotoImage(file=_path + 'Images/centralButton1.png')
if KCS_IMG == 1:
    cblimage = cblDarkImg
else:
    cblimage = cblLightImg
cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
cbl.pack(pady=17)
AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG, font=('montserrat', 16))
AITaskStatusLbl.place(x=140, y=32)

# Settings Button
sphLight = PhotoImage(file=_path + 'Images/setting.png')
sphLight = sphLight.subsample(2, 2)
sphDark = PhotoImage(file=_path + 'Images/setting1.png')
sphDark = sphDark.subsample(2, 2)
if KCS_IMG == 1:
    sphimage = sphDark
else:
    sphimage = sphLight

kbphLight = PhotoImage(file=_path + 'Images/keyboard.png')
kbphLight = kbphLight.subsample(2, 2)
kbphDark = PhotoImage(file=_path + 'Images/keyboard1.png')
kbphDark = kbphDark.subsample(2, 2)
if KCS_IMG == 1:
    kbphimage = kbphDark
else:
    kbphimage = kbphLight
kbBtn = Button(VoiceModeFrame, image=kbphimage, height=30, width=30, bg='#dfdfdf', borderwidth=0,
               activebackground="#dfdfdf", command=changeChatMode)  # ,command=changeChatMode
kbBtn.place(x=25, y=30)

# Mic
micImg = PhotoImage(file=_path + 'Images/mic.png')
micImg = micImg.subsample(2, 2)
micBtn = Button(TextModeFrame, image=micImg, height=30, width=30, bg='#dfdfdf', borderwidth=0,
                activebackground="#dfdfdf", command=changeChatMode)  # , command=changeChatMode
micBtn.place(relx=1.0, y=30, x=-20, anchor="ne")

# Text Field
TextFieldImg = PhotoImage(file=_path + 'Images/textField.png')
UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
UserField.place(x=20, y=30)
UserField.insert(0, "Ask me anything...")
UserField.bind('<Return>', keyboardInput)

userIcon = PhotoImage(file=_path + "Images/Avatar/ChatIcons/a" + str(ownerPhoto) + ".png")
botIcon = PhotoImage(file=_path + "Images/assistant2.png")
botIcon = botIcon.subsample(2, 2)

show_Chat_Frame()
Voice_start = Thread(target=voiceMedium)
Voice_start.daemon = True

if __name__ == "__main__":
    window = MainWindow()
