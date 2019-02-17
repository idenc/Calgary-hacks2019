import clock
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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
    def __init__(self, screen, parent=None):
        # Initialize the Main Window
        super(MainWindow, self).__init__(parent)
        self.screen = QDesktopWidget.screenGeometry(screen)
        self.create_layout()
        self.add_head()
        self.add_web_widget()
        self.add_bottom()
        self.setLayout(self.layout)
        self.show()


    def create_layout(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

    def add_head(self):
        top = QFrame()
        top.setFrameShape(QFrame.WinPanel)
        top.setFrameShadow(QFrame.Raised)
        top.setMinimumSize(100, 100)
        top.setStyleSheet("background-color: red;")

        clk = clock.Clock(parent=top)
        clk.setFrameShape(QFrame.NoFrame)
        clk.setStyleSheet("background-color:none; color: white;")
        clk.move(-75, -75)
        clk.setMinimumWidth(250)
        clk.setMinimumHeight(250)

        weather = QLabel(top)
        weather.setFont(QFont("Times", 42, QFont.Bold))
        #weather.setMinimumHeight(50)
        #weather.setMinimumWidth(180)
        weather.setText("<font color='white'>-15°</font>")
        weather.move(self.screen.width() - 130, 11)
        self.layout.addWidget(top)

    def emergency_button(self):
        print("Emergency")

    def add_bottom(self):
        bot = QFrame()
        bot.setFrameShape(QFrame.WinPanel)
        bot.setFrameShadow(QFrame.Raised)
        bot.setMinimumSize(100, 150)
        bot.setStyleSheet("background-color: red;")

        self.layout.addWidget(bot)
        self.layout.addStretch(1)

        emer_button = QPushButton('Request Help')
        emer_button.clicked.connect(self.emergency_button)
        self.layout.addWidget(emer_button)
        self.layout.addStretch(1)

    def add_web_widget(self):
        self.web_widget = WebPage("8", "North", "2350")
        self.layout.addWidget(self.web_widget)
        self.layout.addStretch(1)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop = QApplication.desktop()
    app.setApplicationDisplayName("Calgary Transit Kiosk")
    main_window = MainWindow(desktop)
    main_window.showMaximized()
    sys.exit(app.exec_())  # only need one app, one running event loop
