from chatterbot import ChatBot
import tkinter as tk
from tkinter import WORD, DISABLED, END, NORMAL
from chatterbot.trainers import ChatterBotCorpusTrainer

try:
    import ttk as ttk
    import ScrolledText
except ImportError:
    import tkinter.ttk as ttk
    import tkinter.scrolledtext as ScrolledText


class TkinterGUIExample(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.chatbot = ChatBot(
            "GUI Bot",
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            logic_adapters=[
                "chatterbot.logic.BestMatch",
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.TimeLogicAdapter'
            ],
            database_uri="sqlite:///database.sqlite3"
        )

        trainer = ChatterBotCorpusTrainer(self.chatbot)

        trainer.train(
            "chatterbot.corpus.english"
        )

        self.title("Chatterbot")
        self.geometry("700x900")
        self.resizable(0, 0)

        self.ChatLog = tk.Text(self, bd=0, bg="white", height="8", width="50", font=("Arial", 35), wrap=WORD)

        self.ChatLog.config(state=DISABLED)

        self.scrollbar = tk.Scrollbar(self, command=self.ChatLog.yview, cursor="heart")
        self.ChatLog['yscrollcommand'] = self.scrollbar.set

        self.SendButton = tk.Button(self, font=("Arial", 20, 'bold'), text="Send", width="12", height=5,
                                    bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                                    command=self.get_response)

        self.EntryBox = tk.Text(self, bd=0, bg="white", width="29", height="5", font=("Arial", 30), insertwidth=5)

        self.scrollbar.place(x=676, y=6, height=886)
        self.ChatLog.place(x=6, y=6, height=780, width=665)
        self.EntryBox.place(x=170, y=800, height=90, width=500)
        self.SendButton.place(x=6, y=800, height=90)

    def get_response(self):
        msg = self.EntryBox.get("1.0", 'end-1c').strip()
        self.EntryBox.delete("0.0", END)

        if msg != '':
            self.ChatLog.config(state=NORMAL)
            self.ChatLog.insert(END, "You: " + msg + '\n\n')
            self.ChatLog.config(foreground="#442265", font=("Verdana", 30))

            self.ChatLog.insert(END, "Bot: " + str(self.chatbot.get_response(msg).text) + '\n\n')

            self.ChatLog.config(state=DISABLED)
            self.ChatLog.yview(END)


gui_example = TkinterGUIExample()
gui_example.mainloop()
