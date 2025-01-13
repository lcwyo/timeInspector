from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtWidgets import QMessageBox
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from datetime import datetime, timedelta
from utils import parse_time, calculate_time_difference, calculate_go_home_time, get_time_left, get_image_path, validate_time_input, get_current_time, get_default_time 


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
        inspector = get_image_path("inspector.png")
        pixmap = QPixmap(inspector)
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo, 0, 2, 6, 1)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(200)

    def tick(self):
        current_time = datetime.now().strftime('%H:%M')
        self.currentTime_Display.setText(current_time)

    def callback(self):
        # Get current time
        time_now = get_current_time()
        time2 = parse_time(time_now)

        # Check if start time is empty or invalid, set default time if so
        if self.startTime_Entry.text() != "":
            #time1 = parse_time(self.startTime_Entry.text())
            if not validate_time_input(self.startTime_Entry.text()):
                self.show_error_message("Invalid start time entered!")
                return
            else:
                time1 = parse_time(self.startTime_Entry.text())
        else:
            self.startTime_Entry.setText(get_default_time())  # Set the default time (08:00)
            time1 = parse_time(get_default_time())  # Default to "08:00"

        # Ensure time1 is valid (not None) before continuing
        if time1 is None:
            self.show_error_message("Invalid start time entered!")
            return

        # Calculate the time difference (timedelta)
        diff = calculate_time_difference(time1, time2)
        self.timeOn_display_label.setText(str(diff)[:-3])

        # Calculate the time left until clocking out (timedelta)
        time_left = get_time_left(diff)
        self.timeLeft_display_label.setText(str(time_left)[:-3])

        # Calculate when the user can go home
        self.goHome_display_label.setText(calculate_go_home_time(time1))  # Use the updated function

        # Update labels based on whether time left is positive or negative
        if time_left >= timedelta(0):
            self.timeLeft_display_label.setText(str(time_left)[:-3])
            self.timeLeft_display_text.setText("Time left until clocking out")
        else:
            extra_time = (diff - timedelta(hours=7, minutes=50))
            self.timeLeft_display_label.setText(str(extra_time)[:-3])
            self.timeLeft_display_text.setText("Overtime earned")





    def go_home(self, start_time):
        """Calculate and return the 'go home' time."""
        go_home_time = calculate_go_home_time(start_time)
        return go_home_time




    def show_error_message(self, message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
