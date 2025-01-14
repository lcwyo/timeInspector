# ./pages/LunchPage.py
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
import sys
from datetime import timedelta, datetime
from utils import (
    parse_time,  
    get_image_path,
    get_current_time,
    calculate_go_home_time_with_lunch,
    calculate_remaining_working_hours,
    calculate_time_worked_before_lunch
)


class LunchPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QGridLayout()

        self.currentTime = QLabel("Current Time")
        self.currentTime_Display = QLabel()

        self.startTime_text = QLabel("Start Time")
        self.startTime_Entry = QLineEdit()
        self.startTime_Entry.setFixedWidth(50)

        self.start_lunch_time_display_label = QLabel()
        self.start_lunch_time_text = QLabel("Start Lunch Time")
        self.start_lunch_entry = QLineEdit()
        self.start_lunch_entry.setFixedWidth(50)

        self.end_lunch_time_display_label = QLabel()
        self.end_lunch_time_text = QLabel("End Lunch Time")
        self.end_lunch_entry = QLineEdit()
        self.end_lunch_entry.setFixedWidth(50)

        self.goHome_display_label = QLabel()
        self.goHome_text = QLabel("You can leave the building at")

        self.lunchTime_display_label = QLabel()
        self.lunchBreak_text = QLabel("Lunch Break")

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

    def lunch_ti(self):
        
        try:
            # Retrieve the actual input times from the UI fields
            start_time_input = self.startTime_Entry.text()
            lunch_start_input = self.start_lunch_entry.text()
            lunch_end_input = self.end_lunch_entry.text()

            # Use parsed input values or fallback to default if not provided
            time1 = parse_time(start_time_input) or datetime.strptime("08:00", '%H:%M')
            lunch_start = parse_time(lunch_start_input) or datetime.strptime("12:00", '%H:%M')
            lunch_end = parse_time(lunch_end_input) or datetime.strptime("12:30", '%H:%M')

            # Debugging: Print parsed times
            print(f"Start Time: {time1.strftime('%H:%M')}, Lunch Start: {lunch_start.strftime('%H:%M')}, Lunch End: {lunch_end.strftime('%H:%M')}")

            # Ensure lunch start time is earlier than lunch end time
            if lunch_start >= lunch_end:
                self.show_error_message("Lunch start time must be earlier than lunch end time.")
                return

            # Calculate time worked before lunch
            worked_before_lunch = calculate_time_worked_before_lunch(time1, lunch_start)

            # Calculate lunch duration
            lunch_duration = lunch_end - lunch_start

            # Calculate remaining working hours
            remaining_working_hours = calculate_remaining_working_hours(worked_before_lunch, lunch_duration)

            # Calculate go-home time based on remaining work time
            go_home_time = calculate_go_home_time_with_lunch(remaining_working_hours, lunch_end)

            # Debugging: Print remaining working hours and go-home time
            print(f"Remaining Working Hours: {str(remaining_working_hours)[:-3]}, Go Home Time: {go_home_time}")
            """
            print(f"Lunch Duration: {str(lunch_duration)[:-3]}")
            print(f"Time Worked Before Lunch: {str(worked_before_lunch)[:-3]}")
            print(f"Time Left: {str(remaining_working_hours)[:-3]}")
            print(f"Go Home Time: {go_home_time}")
            print(f"start time: {str(time1)[:-3]}")
            print(f"lunch end {str(lunch_end)[:-3]}")
            """
            # Display results in the corresponding UI fields
            self.goHome_display_label.setText(go_home_time)
            self.lunchTime_display_label.setText(str(lunch_end - lunch_start)[:-3])

            # Update the input fields with the new default times after calculation
            self.startTime_Entry.setText(time1.strftime('%H:%M'))
            self.start_lunch_entry.setText(lunch_start.strftime('%H:%M'))
            self.end_lunch_entry.setText(lunch_end.strftime('%H:%M'))

        except ValueError as e:
            self.show_error_message(f"Error: {e}")


    def show_error_message(self, message: str):
        from PyQt5.QtWidgets import QMessageBox

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()
