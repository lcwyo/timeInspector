import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from pages import (
    MainPage,
    SettingsPage, 
    HelpPage, 
    AboutPage, 
    KmfPage, 
    LunchPage 
)  # Importing from the pages module

class TimeInspector(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TimeInspector 2.0")
        self.setGeometry(100, 100, 380, 165)
        self.setFixedSize(380, 165)

        self.menu = self.menuBar()

       # File Menu
        filemenu = self.menu.addMenu('File')

        # Adding menu actions
        filemenu.addAction('Settings', lambda: self.show_frame('Settings'))
        filemenu.addAction('Time Inspector 2.0', lambda: self.show_frame('Main'))
        filemenu.addAction('Lunch Inspector', lambda: self.show_frame('Lunch'))

        # Add separator between actions
        filemenu.addSeparator()

        # Exit action with proper exit handling
        exit_action = filemenu.addAction('Exit')
        exit_action.triggered.connect(self.close)  # Connect to the close method to exit the app

        # Add additional menus for other pages if needed (example)
        othermenu = self.menu.addMenu('Other')
        othermenu.addAction('A Page', lambda: self.show_frame('About'))  # Action for Kmf page


        # Help Menu
        helpmenu = self.menu.addMenu('Help')
        helpmenu.addAction('Help', lambda: self.show_frame('Help'))  # Corrected to 'Help'
        helpmenu.addAction('About', lambda: self.show_frame('About'))  # Corrected to 'About'

        

        self.container = QStackedWidget()
        self.setCentralWidget(self.container)

        # Ensure all pages are correctly added to frames dictionary
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

        # Default page is MainPage
        self.show_frame('Main')  

    def show_frame(self, page_name):
        """Show the page corresponding to the given page name"""
        if page_name in self.frames:
            page = self.frames[page_name]
            self.container.setCurrentWidget(page)
        else:
            print(f"Error: {page_name} not found in frames!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = TimeInspector()
    mainWin.show()
    sys.exit(app.exec_())
