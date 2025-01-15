# ./pages/LunchPage.py
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
import sys
from datetime import datetime, timedelta
from utils import (
    parse_time,
    get_image_path,
    get_current_time,
    calculate_go_home_time_with_lunch,
    calculate_remaining_working_hours,
    calculate_time_worked_before_lunch
)


DEFAULT_START_TIME = "08:00"
DEFAULT_LUNCH_START = "12:00"
DEFAULT_LUNCH_END = "12:30"


class LunchPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Reference to main application for status bar updates

        layout = QGridLayout()

        self.currentTime = QLabel("Current Time")
        self.currentTime_Display = QLabel()

        self.startTime_text = QLabel("Start Time")
        self.startTime_Entry = QLineEdit()
        self.startTime_Entry.setFixedWidth(50)

        self.start_lunch_time_text = QLabel("Start Lunch Time")
        self.start_lunch_entry = QLineEdit()
        self.start_lunch_entry.setFixedWidth(50)

        self.end_lunch_time_text = QLabel("End Lunch Time")
        self.end_lunch_entry = QLineEdit()
        self.end_lunch_entry.setFixedWidth(50)

        self.lunchBreak_text = QLabel("Lunch Break")
        self.lunchTime_display_label = QLabel()

        self.goHome_text = QLabel("You can leave the building at")
        self.goHome_display_label = QLabel()

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
        layout.addWidget(self.lunchBreak_text, 4, 0)
        layout.addWidget(self.lunchTime_display_label, 4, 1)
        layout.addWidget(self.goHome_text, 5, 0)
        layout.addWidget(self.goHome_display_label, 5, 1)
        layout.addWidget(button_ok, 6, 0)
        layout.addWidget(button_close, 6, 1)

        self.photo = QLabel()
        inspector = get_image_path("inspector.png")
        pixmap = QPixmap(inspector)
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo, 0, 2, 6, 1)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(200)

    def update_current_time(self):
        current_time = get_current_time()
        self.currentTime_Display.setText(current_time)

    def get_or_default(self, entry: QLineEdit, default_time: str) -> datetime:
        """Parse time from input or use the default if empty or invalid."""
        time_input = entry.text().strip()
        return parse_time(time_input) or datetime.strptime(default_time, '%H:%M')

    def lunch_ti(self):
        try:
            # Retrieve parsed or default times
            start_time = self.get_or_default(self.startTime_Entry, DEFAULT_START_TIME)
            lunch_start = self.get_or_default(self.start_lunch_entry, DEFAULT_LUNCH_START)
            lunch_end = self.get_or_default(self.end_lunch_entry, DEFAULT_LUNCH_END)

            # Validate lunch time order
            if lunch_start >= lunch_end:
                raise ValueError("Lunch start time must be earlier than lunch end time.")

            # Perform calculations
            worked_before_lunch = calculate_time_worked_before_lunch(start_time, lunch_start)
            lunch_duration = lunch_end - lunch_start
            remaining_working_hours = calculate_remaining_working_hours(worked_before_lunch, lunch_duration)
            go_home_time = calculate_go_home_time_with_lunch(remaining_working_hours, lunch_end)

            # Update UI fields
            self.lunchTime_display_label.setText(str(lunch_duration)[:-3])
            self.goHome_display_label.setText(go_home_time)

            # Update status bar
            self.parent.update_status_bar(
                f"Lunch Duration: {str(lunch_duration)[:-3]}, Go Home Time: {go_home_time}"
            )

            # Update input fields with defaults for user clarity
            self.startTime_Entry.setText(start_time.strftime('%H:%M'))
            self.start_lunch_entry.setText(lunch_start.strftime('%H:%M'))
            self.end_lunch_entry.setText(lunch_end.strftime('%H:%M'))

        except ValueError as e:
            self.show_error_message(str(e))

    def show_error_message(self, message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
