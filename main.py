import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QStatusBar, QAction

from pages import MainPage, SettingsPage, HelpPage, AboutPage, KmfPage, LunchPage, WFHPage

logging.basicConfig(level=logging.ERROR)

class TimeInspector(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TimeInspector 2.0")
        self.setGeometry(100, 100, 600, 400)  # Adjusted size to accommodate tabs
        self.setMinimumSize(600, 400)

        self._createMenuBar()
        self._createStatusBar()

        # Create a QTabWidget to hold the pages
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Define pages to be added to the tabs
        self.frames = {
            'Main': MainPage(self),
            'Lunch': LunchPage(self),
            'WFH': WFHPage(self),  # New WFHPage added
        }

        # Add pages to the tab widget
        for tab_name, page in self.frames.items():
            self.tabs.addTab(page, tab_name)

        # Add additional pages like Settings, Help, About if needed
        self.settings_page = SettingsPage(self)
        self.help_page = HelpPage(self)
        self.about_page = AboutPage(self)
        self.kmf_page = KmfPage(self)

    def _createMenuBar(self):
        self.menuBar = self.menuBar()
        self.menuBar.setNativeMenuBar(False)

        # Inspector Menu (no longer needed, as pages are now tabs)
        inspectorMenu = self.menuBar.addMenu('Inspector')
        inspectorMenu.addAction('Time Inspector', lambda: self.tabs.setCurrentIndex(0))
        inspectorMenu.addAction('Lunch Inspector', lambda: self.tabs.setCurrentIndex(1))
        inspectorMenu.addAction('WFH Inspector', lambda: self.tabs.setCurrentIndex(2))

        # Settings Menu
        settingsMenu = self.menuBar.addMenu('Settings')
        settingsMenu.addAction('Settings', lambda: self.show_frame('Settings'))
        settingsMenu.addSeparator()
        exitAction = settingsMenu.addAction('Exit')
        exitAction.triggered.connect(QApplication.instance().quit)

        # Help Menu
        helpMenu = self.menuBar.addMenu('?')
        helpMenu.addAction('About', lambda: self.show_frame('About'))
        helpMenu.addAction('Help', lambda: self.show_frame('Help'))

    def _createStatusBar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready", 3000)

    def update_status_bar(self, message):
        """Update the status bar with a given message."""
        self.statusbar.showMessage(message, 3000)

    def show_frame(self, page_name):
        """Show the page corresponding to the given page name."""
        if page_name == 'Settings':
            self.settings_page.show()
        elif page_name == 'About':
            self.about_page.show()
        elif page_name == 'Help':
            self.help_page.show()
        else:
            logging.error(f"Page {page_name} not found!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = TimeInspector()
    mainWin.show()
    sys.exit(app.exec_())
