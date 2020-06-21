"""Import Modules"""
from random import randint
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter.filedialog import askdirectory

from pygame import mixer
import os
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk

"""Setup"""
root = tk.ThemedTk()
root.get_themes()
root.set_theme("arc")

statusbar = ttk.Label(root, text="Welcome to SoundPoP", relief=GROOVE, font="Times 14 italic")
statusbar.pack(side=BOTTOM, pady=10, )

menubar = Menu(root)
root.config(menu=menubar)
subMenu = Menu(menubar, tearoff=0)

playlist = []
index = 0


def onClosing():
    stopMusic()
    root.destroy()


def browseFile():
    global filepath
    filepath = filedialog.askopenfilename()
    add_to_playlist(filepath)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistBox.insert(index, filename)
    playlist.insert(index, filepath)
    index += 1


def massImport():
    global songlist
    folder = askdirectory()
    os.chdir(folder)
    for files in os.listdir(folder):
        if files.endswith(".mp3"):
            songlist = os.listdir()
            songlist.reverse()
    for files in os.listdir(folder):
        if files.endswith(".wav"):
            songlist = os.listdir()
            songlist.reverse()
    for item in songlist:
        pos = len(songlist)
        playlist.insert(pos, item)
        playlistBox.insert(pos, item)
        pos += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Mass Import", command=massImport)
subMenu.add_command(label="Exit", command=onClosing)


def aboutUs():
    tkinter.messagebox.showinfo("About SoundPoP", "This is a music player made using tkinter and pygame \nby Jayprakash Pathak")


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Info", menu=subMenu)
subMenu.add_command(label="About Us", command=aboutUs)

mixer.init()

root.title("SoundPoP")
root.iconbitmap(r"images\WindowIcon.ico")

leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=30)

playlistBox = Listbox(leftFrame)
playlistBox.pack()

addbtn = ttk.Button(leftFrame, text="+ Add", command=browseFile)
addbtn.pack(side=LEFT)


def delSong():
    selected_song = playlistBox.curselection()
    selected_song = int(selected_song[0])
    playlistBox.delete(selected_song)
    playlist.pop(selected_song)


delbtn = ttk.Button(leftFrame, text="   - Del", command=delSong)
delbtn.pack(side=RIGHT)

rightFrame = Frame(root)
rightFrame.pack(side=RIGHT)

topFrame = Frame(rightFrame)
topFrame.pack()

lengthlabel = ttk.Label(topFrame, text="Total Length: --:--", font="Arial 10 bold")
lengthlabel.pack(pady=5)

currentTimelabel = ttk.Label(topFrame, text="Time Remaining: --:--", relief=GROOVE, font="Arial 10 bold")
currentTimelabel.pack()


def showDetails(playIt):
    fileData = os.path.splitext(playIt)
    if fileData[1] == ".mp3":
        audio = MP3(playIt)
        totalLength = audio.info.length
    else:
        a = mixer.Sound(playIt)
        totalLength = a.get_length()

    mins, secs = divmod(totalLength, 60)
    mins = round(mins)
    secs = round(secs)
    timeFormat = "{:02d}:{:02d}".format(mins, secs)
    lengthlabel["text"] = "Total Length" + " " + timeFormat
    thread = threading.Thread(target=startCount, args=(totalLength,))
    thread.start()


def startCount(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeFormat = "{:02d}:{:02d}".format(mins, secs)
            currentTimelabel["text"] = "Time Remaining" + " " + timeFormat
            time.sleep(1)
            t -= 1


def playMusic():
    try:
        global paused
        global playIt
        global index
        if paused:
            mixer.music.unpause()
            statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
            paused = FALSE
        else:
            try:
                index += 1
                index = 0
                if len(playlist) >= 0:
                    playIt = playlist[index]
                    mixer.music.load(playIt)
                    mixer.music.play()
                    statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
                    showDetails(playIt)
            except:
                tkinter.messagebox.showerror("File Error",
                                             "SoundPoP Is Unable To Read The Files or Your Playlist Maybe Empty! Try Adding Songs")
    except NameError:
        tkinter.messagebox.showerror("File Error",
                                     "SoundPoP Is Unable To Read The Files or Your Playlist Maybe Empty! Try Adding Songs")


def stopMusic():
    mixer.music.stop()
    statusbar["text"] = "Stopped"


paused = FALSE


def pauseMusic():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar["text"] = "Paused"


def previousMusic():
    try:
        global paused
        global playIt
        global index
        index -= 1
        stopMusic()
        time.sleep(1)
        if paused:
            mixer.music.unpause()
            statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
            paused = FALSE
        if index == -1:
            index = len(playlist) - 1
            playIt = playlist[index]
            mixer.music.load(playIt)
            mixer.music.play()
            statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
            showDetails(playIt)
        playIt = playlist[index]
        mixer.music.load(playIt)
        mixer.music.play()
        statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
        showDetails(playIt)
    except IndexError:
        tkinter.messagebox.showerror("File Error",
                                     "SoundPoP Is Unable To Read The Files or Your Playlist Maybe Empty! Try Adding Songs")


def nextMusic():
    try:
        global paused
        global playIt
        global index
        index += 1
        stopMusic()
        time.sleep(1)
        if paused:
            mixer.music.unpause()
            statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
            paused = FALSE
        if index == len(playlist):
            index = -1
            playIt = playlist[index]
            mixer.music.load(playIt)
            mixer.music.play()
            statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
            showDetails(playIt)

        playIt = playlist[index]
        mixer.music.load(playIt)
        mixer.music.play()
        statusbar["text"] = "Playing" + " " + os.path.basename(playIt)
        showDetails(playIt)
    except IndexError:
        tkinter.messagebox.showerror("File Error",
                                 "SoundPoP Is Unable To Read The Files or Your Playlist Maybe Empty! Try Adding Songs")


def setVol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    return val


muted = FALSE


def muteMusic():
    global muted
    if muted:
        mixer.music.set_volume(0.5)
        scale.set(50)
        volumeBtn.configure(image=volumephoto)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        scale.set(0)
        volumeBtn.configure(image=mutephoto)
        muted = TRUE


middleFrame = Frame(rightFrame)
middleFrame.pack(padx=30, pady=30)

playphoto = PhotoImage(file="Images/Play.png")
playBtn = ttk.Button(middleFrame, image=playphoto, command=playMusic)
playBtn.grid(row=0, column=0, padx=10)

stopphoto = PhotoImage(file="Images/Stop.png")
stopBtn = ttk.Button(middleFrame, image=stopphoto, command=stopMusic)
stopBtn.grid(row=0, column=1, padx=10)

pausephoto = PhotoImage(file="Images/Pause.png")
pauseBtn = ttk.Button(middleFrame, image=pausephoto, command=pauseMusic)
pauseBtn.grid(row=0, column=2, padx=10)

bottomFrame = Frame(rightFrame)
bottomFrame.pack()

previousphoto = PhotoImage(file="Images/Previous.png")
previousBtn = ttk.Button(bottomFrame, image=previousphoto, command=previousMusic)
previousBtn.grid(row=0, column=0, padx=10)

nextphoto = PhotoImage(file="Images/Next.png")
nextBtn = ttk.Button(bottomFrame, image=nextphoto, command=nextMusic)
nextBtn.grid(row=0, column=1, padx=10)

mutephoto = PhotoImage(file="Images/Mute.png")
volumephoto = PhotoImage(file="Images/Volume.png")
volumeBtn = ttk.Button(bottomFrame, image=volumephoto, command=muteMusic)
volumeBtn.grid(row=0, column=2, padx=10)

scale = ttk.Scale(bottomFrame, from_=0, to_=100, orient=HORIZONTAL, command=setVol)
scale.set(50)
mixer.music.set_volume(0.5)
scale.grid(row=0, column=3, pady=15)

bottomleftFrame = Frame(leftFrame)
bottomleftFrame.pack(side=BOTTOM)

playlistLabel = ttk.Label(bottomleftFrame, text="Playlist", font="Arial 13 bold")
playlistLabel.grid(row=1, column=0, pady=10)

root.protocol("WM_DELETE_WINDOW", onClosing)
root.mainloop()
