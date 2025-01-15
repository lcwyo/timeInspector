from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QApplication,
)
from PyQt5.QtCore import QTimer, Qt 
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from datetime import datetime
from utils.utils import parse_time, get_current_time, get_image_path
import sys


class WFHPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Reference to the main window
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        # Set spacing and margins for a cleaner layout
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Current Time Display
        self.current_time_label = QLabel("Current Time")
        self.current_time_display = QLabel()
        layout.addWidget(self.current_time_label, 0, 0)
        layout.addWidget(self.current_time_display, 0, 1)

        # Start Time Input
        self.start_time_label = QLabel("Start Time")
        self.start_time_input = QLineEdit()
        self.start_time_input.setPlaceholderText("08:00")  # Default placeholder
        layout.addWidget(self.start_time_label, 1, 0)
        layout.addWidget(self.start_time_input, 1, 1)

        # Time on the Clock Display
        self.time_on_clock_label = QLabel("Time on the clock")
        self.time_on_clock_display = QLabel()
        layout.addWidget(self.time_on_clock_label, 2, 0)
        layout.addWidget(self.time_on_clock_display, 2, 1)

        # OK Button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.calculate_time_on_clock)
        self.button_close = QPushButton("Close")
        self.button_close.clicked.connect(sys.exit)
        layout.addWidget(self.ok_button, 3, 0)
        layout.addWidget(self.button_close, 3, 1)

        # Image
        self.photo = QLabel()
        ninja = get_image_path("ninja.png")
        pixmap = QPixmap(ninja)
        self.photo.setPixmap(pixmap)
        self.photo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.photo, 0, 2, 3, 1)  # Span image across 3 rows

        # Add Spacer for better spacing between widgets
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer, 4, 0, 1, 2)

        # Set Layout
        self.setLayout(layout)

        # Timer to update current time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(1000)  # Update every second

    def update_current_time(self):
        current_time = get_current_time()  # Utility function from utils
        self.current_time_display.setText(current_time)

    def calculate_time_on_clock(self):
        try:
            # Retrieve Start Time
            start_time_input = self.start_time_input.text().strip()
            start_time = parse_time(start_time_input) if start_time_input else datetime.strptime("08:00", "%H:%M")

            # Get Current Time
            current_time = datetime.now()

            # Calculate Elapsed Time
            elapsed_time = current_time - start_time

            # Format Elapsed Time for Display and Clipboard
            elapsed_hours, remainder = divmod(elapsed_time.seconds, 3600)
            elapsed_minutes = remainder // 60
            elapsed_time_str = f"{elapsed_hours}:{elapsed_minutes:02d}"  # "HH:MM" format

            # Display Results
            self.time_on_clock_display.setText(elapsed_time_str)

            # Update Status Bar
            self.parent.update_status_bar(f"Elapsed Time: {elapsed_time_str}")

            # Copy to Clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(elapsed_time_str)

        except ValueError as e:
            self.parent.update_status_bar(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)
    layout.addWidget(WFHPage(parent=None))  # Standalone example
    window.show()
    sys.exit(app.exec_())
