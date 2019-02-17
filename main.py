from PyQt5.QtCore import QRect, Qt

import clock
import sys
import map
import pygame  # install as module
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


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
        next_bus.setText("<font color='white'>Next Bus: #20 in 15 minutes</font>")
        next_bus.move(int(self.screen.width() / 2) - 400, 25)

        weather = QLabel(top)
        weather.setFont(QFont("Sans-serif", 42, QFont.Bold))
        weather.setText("<font color='white'>-15°</font>")
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

        bus1_img = QPixmap('8.png')
        bus2_img = QPixmap('303.png')
        bus3_img = QPixmap('308.png')

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
