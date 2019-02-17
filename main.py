import clock
import sys
import PyQt5.uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *


class WebPage(QWebEngineView):
    def on_load_finished(self):
        self.page().runJavaScript(
            "document.getElementsByClassName('LocationInputAutoComplete ui-autocomplete-input')[0].value = '" + self.stop_num + "';")
        self.page().runJavaScript(
            "document.getElementsByClassName('LocationInputAutoComplete ui-autocomplete-input')[0].focus();")
        command = """
        function eventFire(el, etype){
          if (el.fireEvent) {
            el.fireEvent('on' + etype);
          } else {
            var evObj = document.createEvent('Events');
            evObj.initEvent(etype, true, false);
            el.dispatchEvent(evObj);
          }
        };
        eventFire(document.getElementById("TravelPlansMenuItem"), 'click');
        document.getElementsByClassName('LocationInputAutoComplete ui-autocomplete-input')[0].focus();
        eventFire(document.getElementById("TravelPlansMenuItem"), 'keydown');
        eventFire(document.getElementById("TravelPlansMenuItem"), 'keypress');
        """
        self.page().runJavaScript(command)
        print("Url Loaded")

    def __init__(self, bus, direction, stop_num):
        QWebEngineView.__init__(self)
        self.stop_num = stop_num
        self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)

        self.load(QUrl("http://hastinfoweb.calgarytransit.com/hastinfoweb2/NextDepartures?StopFilterIdentifier=" + bus +
                       "~~" + direction + "&StopFilterType=RouteDirection&StopIdentifier=" + stop_num + "&IsEmbedded"
                                                                                                        "=true"))
        self.loadFinished.connect(self.on_load_finished)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        # Initialize the Main Window
        super(MainWindow, self).__init__(parent)
        self.create_menu()
        self.add_web_widget()
        self.setLayout(self.layout)
        self.show()

    def create_menu(self):
        self.layout = QVBoxLayout()
        top = QWidget()
        top.setMinimumSize(400, 400)
        top.setStyleSheet("background-color: red;")
        clk = clock.Clock(parent=top)
        clk.setFrameShape(QFrame.NoFrame)
        clk.setStyleSheet("background-color:none; color: white;")

        self.layout.addWidget(top)
        self.layout.addWidget(clk)

    def add_web_widget(self):
        self.web_widget = WebPage("8", "North", "2350")
        self.layout.addWidget(self.web_widget)
        self.layout.addStretch(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Calgary Transit Kiosk")
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())  # only need one app, one running event loop
