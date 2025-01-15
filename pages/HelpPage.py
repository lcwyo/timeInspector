from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from utils import (
    get_image_path,
   
)

class HelpPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.message = QLabel('Enter the time you clocked in the "start time" box & click ok.\n'
                              'TimeInspector will calculate the time you have left before you can clock out.\n'
                              'If you have overtime, it will display the overtime earned')
        self.message.setStyleSheet("font-size: 12px; font-family: Arial;")
        layout.addWidget(self.message)

        self.photo = QLabel()
        kmf = get_image_path("kmf.png")
        pixmap = QPixmap(kmf)
        self.photo.setPixmap(pixmap)
        layout.addWidget(self.photo)

        
        self.button = QPushButton()
        self.button.setIcon(QIcon(pixmap))
        self.button.setFlat(True)
        layout.addWidget(self.button)

        self.setLayout(layout)
