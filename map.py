from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *


class WebPage(QWebEngineView):

    def on_load_finished(self):
        print(self.page().runJavaScript('document.getElementsByClassName("RoutePublicIdentifier")[0].innerHTML'))
        print("Url Loaded")

    def __init__(self, stop_num):
        QWebEngineView.__init__(self)
        self.stop_num = stop_num
        self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)

        self.load(QUrl(
            "http://hastinfoweb.calgarytransit.com/hastinfoweb2/NextDepartures?StopIdentifier=" + stop_num + "&IsEmbedded=true"))
