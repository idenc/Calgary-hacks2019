from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
from google.transit import gtfs_realtime_pb2
import urllib.request


def get_info(stop_num):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.request.urlopen(
        'https://data.calgary.ca/api/views/gs4m-mdc2/files/6fca47cc-ecc1-4eb1-84d5-a966ab1e8cf7?filename=tripupdates.pb')
    feed.ParseFromString(response.read())
    for entity in feed.entity:
        print(entity)


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

        command1 = """
        function eventFire(el, etype){
          if (el.fireEvent) {
            el.fireEvent('on' + etype);
          } else {
            var evObj = document.createEvent('Events');
            evObj.initEvent(etype, true, false);
            el.dispatchEvent(evObj);
          }
        };
        """
        command2 = """
        var i;
        for (i = 0; i < 4; i++) { 
            document.getElementsByClassName("gm-control-active")[1].click()
        }
        """
        self.page().runJavaScript('document.getElementsByClassName("gm-control-active")[1].click()')
        print("Url Loaded")

    def __init__(self, stop_num):
        QWebEngineView.__init__(self)
        self.stop_num = stop_num
        self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)

        self.load(QUrl(
            "http://hastinfoweb.calgarytransit.com/hastinfoweb2/NextDepartures?StopIdentifier=" + stop_num + "&IsEmbedded=true"))
        # self.loadFinished.connect(self.on_load_finished)
