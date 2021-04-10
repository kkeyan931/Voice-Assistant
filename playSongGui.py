from tkinter import *
from tkinter import filedialog

import pygame
import os


class MusicPlayer:
    def __init__(self, root):
        filename = filedialog.askdirectory(title="Select a Folder")

        self.root = root

        self.root.title("MusicPlayer")

        self.root.geometry("1000x200+200+200")

        self.root.resizable(0, 0)

        pygame.init()

        pygame.mixer.init()

        self.track = StringVar()

        self.status = StringVar()

        trackframe = LabelFrame(self.root, text="Song Track", font=("Ariel", 15, "bold"), bg="white",
                                fg="black", bd=5, relief=GROOVE)
        trackframe.place(x=0, y=0, width=600, height=100)

        songtrack = Label(trackframe, textvariable=self.track, width=20, font=("Ariel", 18, "bold"),
                          fg="black").grid(row=0, column=0, padx=10, pady=5)

        trackstatus = Label(trackframe, textvariable=self.status, font=("Ariel", 18, "bold"),
                            fg="black").grid(row=0, column=1, padx=10, pady=5)

        buttonframe = LabelFrame(self.root, text="Control Panel", font=("Ariel", 15, "bold"), bg="white",
                                 fg="black", bd=5, relief=GROOVE)

        buttonframe.place(x=0, y=100, width=600, height=100)

        playbtn = Button(buttonframe, text="PLAYSONG", command=self.playsong, width=10, height=1,
                         font=("Ariel", 16, "bold"), activebackground="#3c9d9b", fg='#ffffff', bg="#32de97", bd=0).grid(
            row=0, column=0, padx=10,
            pady=5)

        playbtn = Button(buttonframe, text="PAUSE", command=self.pausesong, width=8, height=1,
                         font=("Ariel", 16, "bold"), activebackground="#3c9d9b", fg='#ffffff', bg="#32de97", bd=0).grid(
            row=0, column=1, padx=10,
            pady=5)

        playbtn = Button(buttonframe, text="UNPAUSE", command=self.unpausesong, width=10, height=1,
                         font=("Ariel", 16, "bold"), activebackground="#3c9d9b", fg='#ffffff', bg="#32de97", bd=0).grid(
            row=0, column=2, padx=10,
            pady=5)

        playbtn = Button(buttonframe, text="STOP", command=self.stopsong, width=3, height=1,
                         font=("Ariel", 16, "bold"), activebackground="#3c9d9b", fg='#ffffff', bg="#32de97", bd=0).grid(
            row=0, column=3, padx=10,
            pady=5)

        songsframe = LabelFrame(self.root, text="Song Playlist", font=("Ariel", 15, "bold"), bg="white",
                                fg="black", bd=5, relief=GROOVE)
        songsframe.place(x=600, y=0, width=400, height=200)

        scrol_y = Scrollbar(songsframe, orient=VERTICAL)

        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectbackground="blue", selectmode=SINGLE,
                                font=("Ariel", 12, "bold"), bg="white", fg="navyblue", bd=5, relief=GROOVE)

        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        os.chdir(filename)
        songtracks = os.listdir()
        for track in songtracks:
            self.playlist.insert(END, track)

    def playsong(self):
        self.track.set(self.playlist.get(ACTIVE))
        self.status.set("-Playing")
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        pygame.mixer.music.play()

    def stopsong(self):
        self.status.set("-Stopped")

        pygame.mixer.music.stop()

    def pausesong(self):
        self.status.set("-Paused")

        pygame.mixer.music.pause()

    def unpausesong(self):
        self.status.set("-Playing")

        pygame.mixer.music.unpause()
