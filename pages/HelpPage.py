from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class HelpPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("Help Page Content")
        layout.addWidget(label)
        self.setLayout(layout)
