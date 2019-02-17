import clock
import sys
import map
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
        self.add_footer()
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
        next_bus.setFont(QFont("Times", 42, QFont.Bold))
        next_bus.setText("<font color='white'>Next Bus: #20 in 15 minutes</font>")
        next_bus.move(int(self.screen.width() / 2) - 400, 11)

        weather = QLabel(top)
        weather.setFont(QFont("Times", 42, QFont.Bold))
        weather.setText("<font color='white'>-15°</font>")
        weather.move(self.screen.width() - 130, 11)
        self.layout.addWidget(top)

    def add_footer(self):
        bottom = QFrame()
        bottom.setStyleSheet("background-color: white;")
        bottom.setMinimumSize(200, 200)
        self.layout.addWidget(bottom)

    def add_web_widget(self):
        self.web_widget = map.WebPage("2350")
        self.layout.addWidget(self.web_widget)
        # self.layout.addStretch(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop = QApplication.desktop()
    app.setApplicationDisplayName("Calgary Transit Kiosk")
    main_window = MainWindow(desktop)
    main_window.showMaximized()
    sys.exit(app.exec_())  # only need one app, one running event loop
