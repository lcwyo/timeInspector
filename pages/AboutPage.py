from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class AboutPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("About TimeInspector 2.0")
        layout.addWidget(label)
        self.setLayout(layout)
