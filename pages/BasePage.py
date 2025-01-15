from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QTimer

class BasePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(200)

    def create_current_time_display(self):
        """Creates and returns the current time label and display widget."""
        self.currentTime_label = QLabel("Current Time")  # Assign to instance
        self.currentTime_Display = QLabel()  # Assign to instance
        return self.currentTime_label, self.currentTime_Display

    def create_start_time_input(self, default_time="8:00"):
        """Creates and returns the start time label and input field."""
        start_time_label = QLabel("Start Time")
        start_time_input = QLineEdit(default_time)
        start_time_input.setFixedWidth(50)
        return start_time_label, start_time_input

    def create_ok_button(self, callback):
        """Creates and returns the OK button."""
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(callback)
        return ok_button

    def update_current_time(self):
        """Override in subclass to update the current time display."""
        pass

