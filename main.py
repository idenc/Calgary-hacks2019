import clock
import sys
import map
import pygame  # install as module
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QRect
from darksky import forecast
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class MainWindow(QWidget):
    def __init__(self, screen, parent=None):
        # Initialize the Main Window
        super(MainWindow, self).__init__(parent)
        self.screen = QDesktopWidget.screenGeometry(screen)
        self.get_info()
        self.create_layout()
        self.add_head()
        self.add_web_widget()
        self.add_bottom()
        self.setLayout(self.layout)
        self.show()

    def get_info(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome('C:\Windows\chromedriver.exe', chrome_options=options)

        browser.get("https://hastinfoweb.calgarytransit.com/hastinfoweb2/NextDepartures?StopIdentifier=2350")
        browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
        delay = 10  # seconds
        try:
            wait = WebDriverWait(browser, 100)
            men_menu = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='NextPassingTimesSuggestions']")))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        x = browser.find_elements_by_class_name("RoutePublicIdentifier")

        y = browser.find_elements_by_class_name("NextPassingTimesTime")
        self.l = []
        i = 0
        for a in x:
            self.l.append((a.text, y[i].text))
            i += 6
        browser.close()

    def create_layout(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

    def add_head(self):
        top = QFrame()
        top.setFrameShape(QFrame.WinPanel)
        top.setFrameShadow(QFrame.Raised)
        top.setMaximumHeight(100)
        top.setStyleSheet("background-color: red;")

        clk = clock.Clock(parent=top)
        clk.setFrameShape(QFrame.NoFrame)
        clk.setStyleSheet("background-color:none; color: white;")
        clk.move(-75, -75)
        clk.setMinimumWidth(250)
        clk.setMinimumHeight(250)

        next_bus = QLabel(top)
        next_bus.setFont(QFont("Sans-serif", 42, QFont.Bold))
        bus = self.l[0][0]
        time = self.l[0][1]
        next_bus.setText("<font color='white'>Next Bus: " + bus + " in " + time + "</font>")
        next_bus.move(int(self.screen.width() / 2) - 400, 25)

        weather = QLabel(top)
        weather.setFont(QFont("Sans-serif", 42, QFont.Bold))
        w = forecast('c505a8dedfcf4bc235046f56138a67d9', 51.0253, -114.0499)
        temp = round(w['currently']['temperature'])
        weather.setText("<font color='white'>" + str(temp) + "°</font>")
        weather.move(self.screen.width() - 130, 25)
        self.layout.addWidget(top)

    def emergency_button(self):
        print("Emergency")
        pygame.init()
        pygame.mixer.init()
        sounda = pygame.mixer.Sound("siren.wav")
        sounda.play()

    def add_bottom(self):
        bot = QFrame()
        bot.setFrameShape(QFrame.WinPanel)
        bot.setFrameShadow(QFrame.Raised)
        bot.setMinimumSize(200, 200)
        bot.setStyleSheet("background-color: white;")

        la = QVBoxLayout(bot)

        self.add_bus(8, la)
        self.add_bus(303, la)
        self.add_bus(308, la)

        self.add_emer_button(bot)

        self.layout.addWidget(bot)

    def add_web_widget(self):
        self.web_widget = map.WebPage("2350")
        self.layout.addWidget(self.web_widget)

    def add_emer_button(self, bot):
        emer_button = QPushButton('Request Help')
        emer_button.clicked.connect(self.emergency_button)
        emer_button.setStyleSheet("color: white; background-color: red;")
        emer_button.setFixedHeight(100)
        emer_button.setFixedWidth(100)
        rect = QRect(0, 0, 100, 100)
        region = QRegion(rect, QRegion.Ellipse)
        emer_button.setMask(region)
        emer_button.setParent(bot)
        emer_button.move(900, 320)

    def add_bus(self, num, layout):
        bus_img = QPixmap(str(num) + '.png')

        bus = QLabel()
        bus.setPixmap(bus_img)
        bus.setFixedSize(bus_img.size())
        layout.addWidget(bus)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop = QApplication.desktop()
    app.setApplicationDisplayName("Calgary Transit Kiosk")
    main_window = MainWindow(desktop)
    main_window.showMaximized()
    sys.exit(app.exec_())  # only need one app, one running event loop
