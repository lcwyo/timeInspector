from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from utils import (
    get_image_path,
   
)

class KmfPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label = QLabel("This bell is here so that you don't have to sit high and dry.\n")
        self.label.setStyleSheet("font-size: 16px; font-family: Helvetica; font-weight: bold;")
        layout.addWidget(self.label)

        self.photo = QLabel()
        bell = get_image_path("bell.png")
        pixmap = QPixmap(bell)
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo)

        self.setLayout(layout)
