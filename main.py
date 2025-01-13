import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QStackedWidget
from pages import MainPage, SettingsPage, HelpPage, AboutPage, KmfPage, LunchPage  # Importing from the pages module

class TimeInspector(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TimeInspector 2.0")
        self.setGeometry(100, 100, 380, 165)
        self.setFixedSize(380, 165)

        self.menu = self.menuBar()

        filemenu = self.menu.addMenu('File')
        filemenu.addAction('Settings', lambda: self.show_frame('Settings'))
        filemenu.addAction('Time Inspector 2.0', lambda: self.show_frame('Main'))
        filemenu.addAction('Lunch Inspector', lambda: self.show_frame('Lunch'))
        filemenu.addSeparator()
        filemenu.addAction('Exit', sys.exit)

        helpmenu = self.menu.addMenu('Help')
        helpmenu.addAction('Help', lambda: self.show_frame(HelpPage))
        helpmenu.addAction('About', lambda: self.show_frame(AboutPage))

        self.container = QStackedWidget()
        self.setCentralWidget(self.container)

        self.frames = {
            'Main': MainPage(self),
            'Settings': SettingsPage(self),
            'Help': HelpPage(self),
            'About': AboutPage(self),
            'Kmf': KmfPage(self),
            'Lunch': LunchPage(self),
        }

        for page in self.frames.values():
            self.container.addWidget(page)

        self.show_frame('Main')  # Default page is MainPage

    def show_frame(self, page_name):
        page = self.frames[page_name]
        self.container.setCurrentWidget(page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = TimeInspector()
    mainWin.show()
    sys.exit(app.exec_())
