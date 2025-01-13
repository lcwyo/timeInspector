from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
import sys
import time
from datetime import datetime, timedelta

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
            lunch_start = datetime.strptime(self.start_lunch_entry.text(), '%H:%M')
        else:
            lunch_start = datetime.strptime("12:00", '%H:%M')

        if self.end_lunch_entry.text() != "":
            lunch_end = datetime.strptime(self.end_lunch_entry.text(), '%H:%M')
        else:
            lunch_end = datetime.strptime("12:30", '%H:%M')

        working_hours = time1 - lunch_start
        self.start_lunch_time_display_label.setText(str(working_hours)[:-3])

        go_home = self.go_home(time1)
        self.goHome_display_label.setText(go_home)

        self.end_lunch_time_display_label.setText(str(working_hours)[:-3])

    def go_home(self, start):
        time = start + timedelta(hours=8, minutes=50)
        goHome_time = datetime.strftime(time, '%H:%M')
        return goHome_time