#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk

LARGE_FONT=("Verdana", 12)

class TimeInspector(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="logo.ico")
        tk.Tk.wm_title(self, "TimeInspector 2.0")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, AboutPage, MainPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=1, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page for the TimeInspector", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        if tk.TkVersion >= 8.6:
            extension = 'png'
        else:
            extension = 'ppm'

        photo = tk.PhotoImage(file="./ninja." + extension)
        image_label = tk.Label(self, image=photo)
        image_label.pack(side='left')

        button1 = ttk.Button(self, text="Start TimeInspector",
                            command=lambda: controller.show_frame(MainPage))
        button1.pack()

        print(image_label)

class AboutPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="About Page of the TimeInspector", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button2 = ttk.Button(self, text="go to main page",
                            command=lambda: controller.show_frame(MainPage))
        button2.pack()

        button3 = ttk.Button(self, text="back to home",
                            command=lambda: controller.show_frame(StartPage))
        button3.pack()

class MainPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        text_frame = tk.Frame(self,  bd=0, relief="groove")
        time_frame = tk.Frame(self, bd=0, relief="groove", padx=2)
        button_frame = tk.Frame(self, bd=0, relief="sunken")
        image_frame = tk.Frame(self, bd=0, relief="groove")

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
        button_close = ttk.Button(button_frame, text="Close", command=quit)

        self.bind('<Return>', callback)

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

        if tk.TkVersion >= 8.6:
            extension = 'png'
        else:
            extension = 'ppm'

        photo = tk.PhotoImage(file="./ninja." + extension)
        image_label = tk.Label(image_frame, image=photo).pack(side='left')


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


def time_left(difference):
    return timedelta(hours=8, minutes=50) - difference

if __name__ == "__main__":
    app = TimeInspector()
    app.mainloop()
