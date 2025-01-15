from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from utils import (
    get_image_path,
   
)
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
        ninja = get_image_path("ninja.png")
        pixmap = QPixmap(ninja)
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo, 0, 3, 3, 1)

        self.setLayout(layout)
