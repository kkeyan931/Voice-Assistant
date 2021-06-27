from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from translate import Translator


class TranslatorClass:

    def __init__(self, root):
        self.Main_Bg_Color_Dark = "#12232e"
        self.Main_Text_Color_Dark = "#c9e6ff"

        self.root = root

        self.root.geometry("700x400")
        self.root.resizable(width=FALSE, height=FALSE)
        self.root.title("Translator")

        self.mainframe = LabelFrame(self.root, text="source language", font=("Ariel", 15, "bold"),
                                    bg=self.Main_Bg_Color_Dark,
                                    fg="white", bd=5, relief=GROOVE)
        self.mainframe.place(x=0, y=0, width=350, height=200)

        self.lan1 = StringVar(self.root)
        self.lan2 = StringVar(self.root)

        choices = {'English', 'Tamil', 'Hindi', 'Spanish', 'German'}
        self.lan1.set('English')
        self.lan2.set('Tamil')

        fontStyle = ("Ariel", 15)

        lan1menu = OptionMenu(self.mainframe, self.lan1, *choices,)
        lan1menu.config(width=30, font=('Helvetica', 12))
        Label(self.mainframe, text="Select a language", font=fontStyle, bg=self.Main_Bg_Color_Dark,
              fg="white").grid(row=0, column=0)
        lan1menu.grid(row=2, column=0)

        helv20 = tkfont.Font(family='Helvetica', size=20)
        menu1 = self.root.nametowidget(lan1menu.menuname)
        menu1.config(font=helv20)

        mainframe2 = LabelFrame(self.root, text="Destination language", font=("Ariel", 15, "bold"),
                                bg=self.Main_Bg_Color_Dark,
                                fg="white", bd=5, relief=GROOVE)

        mainframe2.place(x=350, y=0, width=350, height=200)

        lan2menu = OptionMenu(mainframe2, self.lan2, *choices)
        lan2menu.config(width=30, font=('Helvetica', 12))
        Label(mainframe2, text="Select a language", font=fontStyle, bg=self.Main_Bg_Color_Dark,
              fg="white").grid(row=0, column=0)
        lan2menu.grid(row=2, column=0)

        menu2 = self.root.nametowidget(lan2menu.menuname)
        menu2.config(font=helv20)

        # Text Box to take user input
        Label(self.mainframe, text="Enter text", bg=self.Main_Bg_Color_Dark,
              font=fontStyle, fg="white").grid(row=3, column=0)

        self.var = StringVar()
        var1 = StringVar()

        textbox = Entry(self.mainframe, bd=0, textvariable=self.var, bg="white", font=("Arial", 20)).grid(row=4,
                                                                                                          column=0)

        mainframe3 = LabelFrame(self.root, text="Output", font=("Ariel", 15, "bold"), fg="white",
                                bg=self.Main_Bg_Color_Dark, bd=5, relief=GROOVE)

        mainframe3.place(x=0, y=200, width=700, height=200)

        self.out = Text(mainframe3, font=("Ariel", 30), fg="white", bg=self.Main_Bg_Color_Dark, wrap=WORD,
                        height=200, width=400)

        self.out.config(state=DISABLED)

        b = Button(mainframe2, text="Translate", command=self.translateFun, width=10, height=1,
                   font=("Ariel", 16, "bold"), activebackground="#3c9d9b", fg='#ffffff', bg="#32de97", bd=0)

        self.out.grid(row=2, column=3)
        b.grid(row=5, column=0)

    def translateFun(self):
        translator = Translator(from_lang=self.lan1.get(), to_lang=self.lan2.get())
        mes = self.var.get()
        translation = translator.translate(mes)
        self.out.config(state=NORMAL)
        self.out.delete("1.0", 'end-1c')
        self.out.insert(END, translation)

