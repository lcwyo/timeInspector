from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton

class SettingsPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QGridLayout()
        # UI setup here...
        self.setLayout(layout)
