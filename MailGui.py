import smtplib
from tkinter import *


class MailWindow:
    def __init__(self, root):

        self.signInWindow = root

        self.signInWindow.configure(bg="white")
        self.signInWindow.resizable(0, 0)

        self.signInWindow.title("Sign In")

        self.signInWindow.geometry("500x400")
        Label(self.signInWindow,
              text="E-mail", font=("Ariel", 30), bg="white").place(x=6, y=60)
        Label(self.signInWindow, text="Password", font=("Ariel", 30), bg="white").place(x=6, y=120)

        self.sendMailId = Entry(self.signInWindow, font=("Ariel", 25))
        self.sendMailId.place(x=180, y=65, width=280, height=35)

        self.password = Entry(self.signInWindow, font=("Ariel", 25),show="*")
        self.password.place(x=180, y=125, width=280, height=35)

        signInButton = Button(self.signInWindow, font=("Arial", 20, 'bold'), text="Sign In", width=12, height=5,
                            bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                            command=self.mailWindowGui)

        signInButton.place(x=180, y=300, height=90)
        
        
    def mailWindowGui(self):
        
        successMessage = StringVar()
        mailWindow = Toplevel(self.signInWindow)

        mailWindow.configure(bg="white")
        mailWindow.resizable(0, 0)

        mailWindow.title("Compose email")

        mailWindow.geometry("500x400")
        Label(mailWindow,
              text="To email", font=("Ariel", 30), bg="white").place(x=6, y=60)
        Label(mailWindow, text="Message", font=("Ariel", 30), bg="white").place(x=6, y=120)

        mailId = Entry(mailWindow, font=("Ariel", 25))
        mailId.place(x=180, y=65, width=280, height=32)

        message = Text(mailWindow, font=("Ariel", 30))
        message.place(x=180, y=125, width=280, height=150)

        sendButton = Button(mailWindow, font=("Arial", 20, 'bold'), text="Send", width=12, height=5,
                            bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                            command=lambda: self.mail(mailId, message, successMessage))

        sendButton.place(x=180, y=300, height=90)

        Label(mailWindow, textvariable=successMessage, font=("Arial", 15), fg="red").place(x=6, y=290)
        

    def mail(self,mailId, message, successMessage):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)

            s.ehlo()

            s.starttls()

            s.login(self.sendMailId.get(), self.password.get())

            s.sendmail(self.sendMailId.get(), mailId.get(), message.get("1.0", "end-1c").strip())

            s.close()
            successMessage.set("Mail sent success")
        except:
            successMessage.set("Mail sent failed")