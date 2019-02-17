from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtCore import QTimer, QTime


class Clock(QLCDNumber):

    def __init__(self, digits=8, parent=None):
        super(Clock, self).__init__(digits, parent)
        self.setSegmentStyle(QLCDNumber.Flat)

        self.timer = QTimer()
        self.timer.timeout.connect(self._update)

        self.timer.start(1000)

    def _update(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.display(text)
