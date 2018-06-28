#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, os
from datetime import datetime, timedelta
from tkinter import ttk

try:
    # Python2
    import Tkinter as tk
    import tkFont as tkFont
    from Tkinter import tkMessageBox as messagebox
except ImportError:
    # Python3
    import tkinter as tk
    from tkinter import font as tkFont
    from tkinter import messagebox


def tick(time1=''):
    # get the current local time from the PC
    time2 = time.strftime('%H:%M')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        currentTime_Display.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    currentTime_Display.after(200, tick)


def callback(event=None):
    time_now = datetime.now().strftime('%H:%M')
    time2 = datetime.strptime(time_now, '%H:%M')

    if startTime_Entry.get() != "":
        time1 = datetime.strptime(startTime_Entry.get(), '%H:%M')
    else:
        time1 = datetime.strptime("8:00", '%H:%M')
        startTime_Entry.insert(0, "08:00")

    diff = time2 - time1

    timeOn_display_label.set(str(diff)[:-3])

    timeLeft = time_left(diff)
    timeLeft_display_label.set(str(timeLeft)[:-3])

    goHome_display_label.set(go_home(time1))

    if timeLeft >= timedelta(0):
        timeLeft_display_label.set(str(timeLeft)[:-3])
        timeLeft_display_text.set("Time left until clocking out")

    else:
        extraTime = (diff - timedelta(hours=8, minutes=50))
        timeLeft_display_label.set(str(extraTime)[:-3])
        timeLeft_display_text.set("Overtime earned")


def go_home(start):
    time = start + timedelta(hours=8, minutes=50)
    goHome_time = datetime.strftime(time, '%H:%M')
    return goHome_time


def close_window():
    mainWindow.destroy()


def time_left(difference):
    return timedelta(hours=8, minutes=50) - difference

def showAbout():
     messagebox.showinfo("About", "Created for fun and games by me")

def showHelp():
    messagebox.showinfo("Help...", "put in your start time and click enter")



if __name__ == '__main__':

    mainWindow = tk.Tk()

    mainWindow.title('Time Inspector')
    mainWindow.geometry('375x160')
    mainWindow.resizable(width=False, height=False)
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(family='Helvetica', size=10)

    menu = tk.Menu(mainWindow)
    mainWindow.config(menu=menu)

    filemenu = tk.Menu(menu)
    filemenu.add_command(label='Settings')
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=close_window)
    menu.add_cascade(label='File', menu=filemenu)

    about = tk.Menu(menu)
    about.add_cascade(label='Help...', command=showHelp)
    about.add_command(label='About', command=showAbout)
    menu.add_cascade(label='Help', menu=about)

    text_frame = tk.Frame(mainWindow,  bd=0, relief="groove")
    time_frame = tk.Frame(mainWindow, bd=0, relief="groove", padx=2)
    button_frame = tk.Frame(mainWindow, bd=0, relief="sunken")
    image_frame = tk.Frame(mainWindow, bd=0, relief="groove")

    text_frame.grid(row=1, column=0, sticky="ew")
    time_frame.grid(row=1, column=1, sticky="ew")
    button_frame.grid(row=6, column=0, columnspan=6)
    image_frame.grid(row=1, column=3, rowspan=6, sticky="ew")

    currentTime = tk.Label(text_frame, text='Current Time')
    currentTime_Display = tk.Label(time_frame)

    startTime_text = tk.Label(text_frame, text='Start Time')
    startTime_Entry = tk.Entry(time_frame, width=5)

    timeOn_display_label = tk.StringVar()
    timeOn_text = tk.Label(text_frame, text='Time on the clock')
    timeOn_display = tk.Label(time_frame, textvariable=timeOn_display_label)

    timeLeft_display_label = tk.StringVar()
    timeLeft_display_text = tk.StringVar()

    timeLeft_text = tk.Label(text_frame, textvariable=timeLeft_display_text)
    timeLeft_display_text.set('Time left until clocking out')
    timeLeft_display = tk.Label(time_frame, textvariable=timeLeft_display_label)

    goHome_display_label = tk.StringVar()
    goHome_text = tk.Label(text_frame, text='You can leave the building at')
    goHome_display = tk.Label(time_frame, textvariable=goHome_display_label)

    button = ttk.Button(button_frame, text="OK", command=callback)
    button_close = ttk.Button(button_frame, text="Close", command=close_window)

    mainWindow.bind('<Return>', callback)

    currentTime.grid(row=0, column=0, sticky='nw')
    currentTime_Display.grid(row=0, column=1, sticky='nw')

    startTime_text.grid(row=1, column=0, sticky='nw')
    startTime_Entry.grid(row=1, column=1, sticky='nw')

    timeOn_text.grid(row=2, column=0, sticky='nw')
    timeOn_display.grid(row=2, column=1, sticky='nw')

    timeLeft_text.grid(row=3, column=0, sticky='nw')
    timeLeft_display.grid(row=3, column=1, sticky='nw')

    goHome_text.grid(row=4, column=0, sticky='nw')
    goHome_display.grid(row=4, column=1, sticky='nw')

    button.grid(row=1, column=0, columnspan=2)
    button_close.grid(row=1, column=2, columnspan=2)

    # need to get the clock to be a ppm file
    if tk.TkVersion >= 8.6:
        extension = 'png'
    else:
        extension = 'ppm'

    photo = tk.PhotoImage(file="./res/ninja." + extension)
    image_label = tk.Label(image_frame, image=photo).pack(side='left')

    tick()
    mainWindow.mainloop()
