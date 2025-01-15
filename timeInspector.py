#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QStackedWidget, QWidget, QMenuBar, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer

class TimeInspector(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TimeInspector 2.0")
        self.setGeometry(100, 100, 380, 165)
        self.setFixedSize(380, 165)

        self.menu = self.menuBar()

        filemenu = self.menu.addMenu('File')
        filemenu.addAction('Settings', lambda: self.show_frame(SettingsPage))
        filemenu.addAction('Time Inspector 2.0', lambda: self.show_frame(MainPage))
        filemenu.addAction('Lunch Inspector', lambda: self.show_frame(LunchPage))
        filemenu.addSeparator()
        filemenu.addAction('Exit', sys.exit)

        helpmenu = self.menu.addMenu('Help')
        helpmenu.addAction('Help', lambda: self.show_frame(HelpPage))
        helpmenu.addAction('About', lambda: self.show_frame(AboutPage))

        self.container = QStackedWidget()
        self.setCentralWidget(self.container)

        self.frames = {}
        for F in (AboutPage, MainPage, HelpPage, KmfPage, SettingsPage, LunchPage):
            frame = F(self)
            self.frames[F] = frame
            self.container.addWidget(frame)

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        self.container.setCurrentWidget(frame)


class SettingsPage(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        layout = QGridLayout()

        self.label = QLabel("Time Inspector Settings")
        self.label.setStyleSheet("font-size: 14px; font-family: Comic Sans MS;")
        layout.addWidget(self.label, 0, 0, 1, 3)

        self.working_label = QLabel("Working time ")
        self.break_label = QLabel("Break time ")

        self.wt_entry = QLineEdit()
        self.wt_entry.setFixedWidth(30)
        self.bt_entry = QLineEdit()
        self.bt_entry.setFixedWidth(30)

        self.working_hours_label = QLabel(" (hours)")
        self.break_min_label = QLabel(" (min)")

        layout.addWidget(self.working_label, 1, 0)
        layout.addWidget(self.wt_entry, 1, 1)
        layout.addWidget(self.working_hours_label, 1, 2)

        layout.addWidget(self.break_label, 2, 0)
        layout.addWidget(self.bt_entry, 2, 1)
        layout.addWidget(self.break_min_label, 2, 2)

        self.wt_entry.setText("8")
        self.bt_entry.setText("50")

        self.button_ok = QPushButton('Save')
        self.button_reset = QPushButton('Reset')
        layout.addWidget(self.button_ok, 3, 1)
        layout.addWidget(self.button_reset, 3, 2)

        self.photo = QLabel()
        pixmap = QPixmap("./res/img/ninja.png")
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo, 0, 3, 3, 1)

        self.setLayout(layout)


class HelpPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.message = QLabel('Enter the time you clocked in the "start time" box & click ok.\n'
                              'TimeInspector will calculate the time you have left before you can clock out.\n'
                              'If you have overtime, it will display the overtime earned')
        self.message.setStyleSheet("font-size: 8px; font-family: Comic Sans MS;")
        layout.addWidget(self.message)

        self.photo = QLabel()
        pixmap = QPixmap("./res/img/kmf.png")
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo)

        self.button = QPushButton()
        self.button.setIcon(QIcon(pixmap))
        self.button.setFlat(True)
        self.button.clicked.connect(lambda: parent.show_frame(KmfPage))
        layout.addWidget(self.button)

        self.setLayout(layout)


class AboutPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label = QLabel("Time Inspector was made so that I wouldn't be late going home.\n\n© 2017 Lance Chatwell")
        layout.addWidget(self.label)

        self.photo = QLabel()
        pixmap = QPixmap("./res/img/ninja.png")
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo)

        self.setLayout(layout)


class KmfPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label = QLabel("This bell is here so that you don't have to sit high and dry.\n")
        self.label.setStyleSheet("font-size: 16px; font-family: Helvetica; font-weight: bold;")
        layout.addWidget(self.label)

        self.photo = QLabel()
        pixmap = QPixmap("./res/img/bell.png")
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo)

        self.setLayout(layout)


class MainPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QGridLayout()

        self.currentTime = QLabel('Current Time')
        self.currentTime_Display = QLabel()

        startTime_text = QLabel('Start Time')
        self.startTime_Entry = QLineEdit()
        self.startTime_Entry.setFixedWidth(50)

        self.timeOn_display_label = QLabel()
        timeOn_text = QLabel('Time on the clock')

        self.timeLeft_display_label = QLabel()
        self.timeLeft_display_text = QLabel('Time left until clocking out')

        self.goHome_display_label = QLabel()
        goHome_text = QLabel('You can leave the building at')

        button_ok = QPushButton("OK")
        button_ok.clicked.connect(self.callback)
        button_close = QPushButton("Close")
        button_close.clicked.connect(sys.exit)

        layout.addWidget(self.currentTime, 0, 0)
        layout.addWidget(self.currentTime_Display, 0, 1)

        layout.addWidget(startTime_text, 1, 0)
        layout.addWidget(self.startTime_Entry, 1, 1)

        layout.addWidget(timeOn_text, 2, 0)
        layout.addWidget(self.timeOn_display_label, 2, 1)

        layout.addWidget(self.timeLeft_display_text, 3, 0)
        layout.addWidget(self.timeLeft_display_label, 3, 1)

        layout.addWidget(goHome_text, 4, 0)
        layout.addWidget(self.goHome_display_label, 4, 1)

        layout.addWidget(button_ok, 5, 0)
        layout.addWidget(button_close, 5, 1)

        self.photo = QLabel()
        pixmap = QPixmap("./res/img/inspector.png")
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo, 0, 2, 6, 1)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(200)

    def tick(self):
        current_time = time.strftime('%H:%M')
        self.currentTime_Display.setText(current_time)

    def callback(self):
        time_now = datetime.now().strftime('%H:%M')
        time2 = datetime.strptime(time_now, '%H:%M')

        if self.startTime_Entry.text() != "":
            time1 = datetime.strptime(self.startTime_Entry.text(), '%H:%M')
        else:
            time1 = datetime.strptime("8:00", '%H:%M')
            self.startTime_Entry.setText("08:00")

        diff = time2 - time1

        self.timeOn_display_label.setText(str(diff)[:-3])

        timeLeft = self.time_left(diff)
        self.timeLeft_display_label.setText(str(timeLeft)[:-3])

        self.goHome_display_label.setText(self.go_home(time1))

        if timeLeft >= timedelta(0):
            self.timeLeft_display_label.setText(str(timeLeft)[:-3])
            self.timeLeft_display_text.setText("Time left until clocking out")
        else:
            extraTime = (diff - timedelta(hours=8, minutes=50))
            self.timeLeft_display_label.setText(str(extraTime)[:-3])
            self.timeLeft_display_text.setText("Overtime earned")

    def go_home(self, start):
        time = start + timedelta(hours=8, minutes=50)
        goHome_time = datetime.strftime(time, '%H:%M')
        return goHome_time

    def time_left(self, difference):
        return timedelta(hours=8, minutes=50) - difference


class LunchPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QGridLayout()

        self.currentTime = QLabel('Current Time')
        self.currentTime_Display = QLabel()

        self.startTime_text = QLabel('Start Time')
        self.startTime_Entry = QLineEdit()
        self.startTime_Entry.setFixedWidth(50)

        self.start_lunch_time_display_label = QLabel()
        self.start_lunch_time_text = QLabel('Start Lunch Time')
        self.start_lunch_entry = QLineEdit()
        self.start_lunch_entry.setFixedWidth(50)

        self.end_lunch_time_display_label = QLabel()
        self.end_lunch_time_text = QLabel('End Lunch Time')
        self.end_lunch_entry = QLineEdit()
        self.end_lunch_entry.setFixedWidth(50)

        self.goHome_display_label = QLabel()
        self.goHome_text = QLabel('You can leave the building at')

        button_ok = QPushButton("OK")
        button_ok.clicked.connect(self.lunch_ti)
        button_close = QPushButton("Close")
        button_close.clicked.connect(sys.exit)

        layout.addWidget(self.currentTime, 0, 0)
        layout.addWidget(self.currentTime_Display, 0, 1)

        layout.addWidget(self.startTime_text, 1, 0)
        layout.addWidget(self.startTime_Entry, 1, 1)

        layout.addWidget(self.start_lunch_time_text, 2, 0)
        layout.addWidget(self.start_lunch_entry, 2, 1)

        layout.addWidget(self.end_lunch_time_text, 3, 0)
        layout.addWidget(self.end_lunch_entry, 3, 1)

        layout.addWidget(self.goHome_text, 4, 0)
        layout.addWidget(self.goHome_display_label, 4, 1)

        layout.addWidget(button_ok, 5, 0)
        layout.addWidget(button_close, 5, 1)

        self.photo = QLabel()
        pixmap = QPixmap("./res/img/inspector.png")
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo, 0, 2, 6, 1)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(200)

    def tick(self):
        current_time = time.strftime('%H:%M')
        self.currentTime_Display.setText(current_time)

    def lunch_ti(self):
        time_now = datetime.now().strftime('%H:%M')

        if self.startTime_Entry.text() != "":
            time1 = datetime.strptime(self.startTime_Entry.text(), '%H:%M')
        else:
            time1 = datetime.strptime("8:00", '%H:%M')
            self.startTime_Entry.setText("08:00")

        if self.start_lunch_entry.text() != "":
            pTime1 = datetime.strptime(self.start_lunch_entry.text(), '%H:%M')
        else:
            pTime1 = datetime.strptime("12:00", '%H:%M')
            self.start_lunch_entry.setText("12:00")

        if self.end_lunch_entry.text() != "":
            pTime2 = datetime.strptime(self.end_lunch_entry.text(), '%H:%M')
        else:
            pTime2 = datetime.strptime("13:00", '%H:%M')
            self.end_lunch_entry.setText("13:00")

        diff = pTime2 - pTime1
        self.goHome_display_label.setText(self.lunch_go_home(time1, diff))

    def lunch_go_home(self, start, diff):
        working_lgth = 7  # hours
        break_lgth = 50  # minutes
        break_sec = timedelta(minutes=break_lgth).seconds
        if break_sec < diff.seconds:
            time = start + timedelta(hours=working_lgth, seconds=diff.seconds)
        else:
            time = start + timedelta(hours=working_lgth, minutes=break_lgth)
        goHome_time = datetime.strftime(time, '%H:%M')
        return goHome_time


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = TimeInspector()
    mainWin.show()
    sys.exit(app.exec_())