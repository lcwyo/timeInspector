from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
import time
from datetime import datetime, timedelta

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
