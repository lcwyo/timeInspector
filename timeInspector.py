#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Comic Sans", 18)


class TimeInspector(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="./res/logo.ico")
        tk.Tk.wm_title(self, "TimeInspector 2.0")
        tk.Tk.geometry(self, '375x160')
        tk.Tk.resizable(self, width=False, height=False)

        menu = tk.Menu(self)
        self.config(menu=menu)

        filemenu = tk.Menu(menu)
        filemenu.add_command(label='Settings', command=lambda: self.show_frame(AboutPage))
        filemenu.add_command(label='Time Inspector 2.0', command=lambda: self.show_frame(MainPage))
        filemenu.add_command(label='Pizza Inspector', command=lambda: self.show_frame(MainPage))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menu.add_cascade(label='File', menu=filemenu)

        about = tk.Menu(menu)
        about.add_cascade(label='Help', command=lambda: self.show_frame(HelpPage))
        about.add_command(label='About', command=lambda: self.show_frame(AboutPage))
        menu.add_cascade(label='Help', menu=about)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, AboutPage, MainPage, HelpPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=1, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Time Inspector", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=2)

        if tk.TkVersion >= 8.6:
            extension = 'png'
        else:
            extension = 'ppm'

        self.photo = tk.PhotoImage(file="./res/ninja." + extension)
        image_label = tk.Label(self, image=self.photo)
        image_label.grid(row=1, column=0)

        self.button_frame = tk.Frame(self, bd=0, relief="sunken", padx=15)
        self.button_frame.grid(row=1, column=2)

        button1 = ttk.Button(self.button_frame, text="Start TimeInspector", width=18,
                             command=lambda: controller.show_frame(MainPage))

        button2 = ttk.Button(self.button_frame, text="About TimeInspector", width=18,
                             command=lambda: controller.show_frame(AboutPage))

        button3 = ttk.Button(self.button_frame, text="Nevermind", width=18,
                             command=quit)
        button1.grid(row=0, column=0)
        button2.grid(row=1, column=0)
        button3.grid(row=2, column=0)


class HelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="""Time Inspector was made \nso that I wouldn't be late""")
        self.label.pack(pady=10, padx=10)

        self.photo = tk.PhotoImage(file="./res/kmf.png")
        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.pack(side='left')

        self.button2 = ttk.Button(self, text="TimeInspector",
                                  command=lambda: controller.show_frame(MainPage))
        self.button2.pack()

        self.button3 = ttk.Button(self, text="About",
                                  command=lambda: controller.show_frame(AboutPage))
        self.button3.pack()


class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="""Time Inspector was made \nso that I wouldn't be late""")
        self.label.grid(row=0, column=1, pady=10, padx=10)

        self.photo = tk.PhotoImage(file="./res/bell.png")
        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.grid(row=0, column=0, pady=10, padx=10)



class MainPage(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        text_frame = tk.Frame(self, bd=0, relief="groove")
        time_frame = tk.Frame(self, bd=0, relief="groove", padx=2)
        button_frame = tk.Frame(self, bd=0, relief="sunken", bg="white")
        image_frame = tk.Frame(self, bd=0, relief="groove")

        text_frame.grid(row=1, column=0, sticky="ew")
        time_frame.grid(row=1, column=1, sticky="ew")
        button_frame.grid(row=6, column=0, columnspan=6, padx=2)
        image_frame.grid(row=1, column=3, rowspan=6, sticky="ew")

        self.currentTime = tk.Label(text_frame, text='Current Time')
        self.currentTime_Display = tk.Label(time_frame)

        startTime_text = tk.Label(text_frame, text='Start Time')
        self.startTime_Entry = tk.Entry(time_frame, width=5)

        self.timeOn_display_label = tk.StringVar()
        timeOn_text = tk.Label(text_frame, text='Time on the clock')
        timeOn_display = tk.Label(time_frame, textvariable=self.timeOn_display_label)

        self.timeLeft_display_label = tk.StringVar()
        self.timeLeft_display_text = tk.StringVar()

        timeLeft_text = tk.Label(text_frame, textvariable=self.timeLeft_display_text)
        self.timeLeft_display_text.set('Time left until clocking out')
        timeLeft_display = tk.Label(time_frame, textvariable=self.timeLeft_display_label)

        self.goHome_display_label = tk.StringVar()
        goHome_text = tk.Label(text_frame, text='You can leave the building at')
        goHome_display = tk.Label(time_frame, textvariable=self.goHome_display_label)

        button = ttk.Button(button_frame, text="OK", command=self.callback)
        button_close = ttk.Button(button_frame, text="Close", command=quit)

        self.bind('<Return>', self.callback)

        self.currentTime.grid(row=0, column=0, sticky='nw')
        self.currentTime_Display.grid(row=0, column=1, sticky='nw')

        startTime_text.grid(row=1, column=0, sticky='nw')
        self.startTime_Entry.grid(row=1, column=1, sticky='nw')

        timeOn_text.grid(row=2, column=0, sticky='nw')
        timeOn_display.grid(row=2, column=1, sticky='nw')

        timeLeft_text.grid(row=3, column=0, sticky='nw')
        timeLeft_display.grid(row=3, column=1, sticky='nw')

        goHome_text.grid(row=4, column=0, sticky='nw')
        goHome_display.grid(row=4, column=1, sticky='nw')

        button.grid(row=1, column=0, columnspan=2)
        button_close.grid(row=1, column=2, columnspan=2)
        self.tick()

        if tk.TkVersion >= 8.6:
            self.extension = 'png'
        else:
            self.extension = 'ppm'

        self.photo = tk.PhotoImage(file="./res/ninja." + self.extension)
        self.image_label = tk.Label(image_frame, image=self.photo)
        self.image_label.pack(side='right')

    def tick(self, time1=''):
        self.time1 = time1
        # get the current local time from the PC
        self.time2 = time.strftime('%H:%M')
        # if time string has changed, update it
        if self.time2 != self.time1:
            self.time1 = self.time2
            self.currentTime_Display.config(text=self.time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        self.currentTime_Display.after(200, self.tick)

    def callback(self, event=None):
        time_now = datetime.now().strftime('%H:%M')
        time2 = datetime.strptime(time_now, '%H:%M')

        if self.startTime_Entry.get() != "":
            time1 = datetime.strptime(self.startTime_Entry.get(), '%H:%M')
        else:
            time1 = datetime.strptime("8:00", '%H:%M')
            self.startTime_Entry.insert(0, "08:00")

        diff = time2 - time1

        self.timeOn_display_label.set(str(diff)[:-3])

        timeLeft = time_left(diff)
        self.timeLeft_display_label.set(str(timeLeft)[:-3])

        self.goHome_display_label.set(go_home(time1))

        if timeLeft >= timedelta(0):
            self.timeLeft_display_label.set(str(timeLeft)[:-3])
            self.timeLeft_display_text.set("Time left until clocking out")

        else:
            extraTime = (diff - timedelta(hours=8, minutes=50))
            self.timeLeft_display_label.set(str(extraTime)[:-3])
            self.timeLeft_display_text.set("Overtime earned")


def go_home(start):
    time = start + timedelta(hours=8, minutes=50)
    goHome_time = datetime.strftime(time, '%H:%M')
    return goHome_time


def time_left(difference):
    return timedelta(hours=8, minutes=50) - difference


if __name__ == "__main__":
    app = TimeInspector()
    app.mainloop()
