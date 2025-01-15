from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from utils import (
    get_image_path,
   
)

class AboutPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.label = QLabel("Time Inspector was made so that I wouldn't be late going home.\n\n© 2017 Lance Chatwell")
        layout.addWidget(self.label)

        self.photo = QLabel()
        ninja = get_image_path("ninja.png")
        pixmap = QPixmap(ninja)
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo)


        self.setLayout(layout)