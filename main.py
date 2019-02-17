import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *


def _on_load_finished():
    print("Url Loaded")


class WebPage(QWebEngineView):
    def __init__(self, bus, direction, stop_num):
        QWebEngineView.__init__(self)
        self.current_url = ''
        self.load(QUrl("http://hastinfoweb.calgarytransit.com/hastinfoweb2/NextDepartures?StopFilterIdentifier=" + bus +
                       "~~" + direction + "&StopFilterType=RouteDirection&StopIdentifier=" + stop_num + "&IsEmbedded"
                                                                                                        "=true"))
        self.loadFinished.connect(_on_load_finished)
        self.page().runJavaScript("map.zoom")


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # Initialize the Main Window
        super(MainWindow, self).__init__(parent)
        self.create_menu()
        self.add_web_widget()
        self.show()

    def create_menu(self):
        """ Creates the Main Menu """
        self.main_menu = self.menuBar()
        self.main_menu_actions = {}

        self.file_menu = self.main_menu.addMenu("Example File Menu")
        self.file_menu.addAction(QAction("Testing Testing", self))

    def add_web_widget(self):
        self.web_widget = WebPage("8", "North", "2350")
        self.setCentralWidget(self.web_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())  # only need one app, one running event loop
