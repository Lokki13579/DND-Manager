from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtWidgets import (
    QFrame,
    QGroupBox,
    QSpinBox,
    QVBoxLayout,
    QLabel,
)

from math import floor
from random import randint


class DiceChar(QFrame):
    valueChanged = pyqtSignal()
    newPoints = pyqtSignal(int)

    def __init__(self, _name, _val, _add, lastpoints):
        super().__init__()
        self.name = _name
        self.value = _val

        self.modif = ""
        self.addiction = _add
        self.points = lastpoints
        self.setupUi()

    def setupUi(self):
        # self.setMaximumSize(QSize(200,120))
        self.setMinimumSize(QSize(200, 120))
        self.MainGroup = QGroupBox(self, title=self.name)
        self.MainGroup.setMinimumSize(QSize(200, 120))
        self.MainGroup.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.vertLayout = QVBoxLayout(self.MainGroup)

        self.charVal = QSpinBox()
        self.charVal.setMinimum(8)
        self.charVal.setMaximum(15)
        self.charVal.lineEdit().setReadOnly(True)
        self.charVal.valueChanged.connect(self.setValue)
        self.charVal.setSuffix(f"(+{self.addiction})")
        self.charVal.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.vertLayout.addWidget(self.charVal, 2)

        self.charModificator = QLabel(text=str(self.modif))
        self.charModificator.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.charModificator.setStyleSheet("""
            font-size: 28px;

        """)

        self.vertLayout.addWidget(self.charModificator, 3)
        self.modifUPD(self.value)

    def setPoints(self, points):
        self.points = points

    def setAddiction(self, addiction):
        self.addiction = addiction
        self.setValue(self.value)
        self.modifUPD(self.value)

    def setValue(self, value):
        def isValid(value, allPoints):
            return (
                (8 <= value <= 15)
                and (allPoints > 0 or self.value - value > 0)
                and allPoints > -1
            )

        def pointsReducer(self, toReduce):
            self.points += toReduce
            if self.points < 0:
                self.points -= toReduce
                self.newPoints.emit(self.points)
                return -1
            self.newPoints.emit(self.points)
            return self.points

        def pointsGetter(data):
            data = list(map(int, data.split("&")))
            m = 1
            if data[0] > 13 or data[1] > 13:
                m = 2

            return (data[0] - data[1]) * m

        if isValid(value, self.points):
            if pointsReducer(self, pointsGetter(f"{self.value}&{value}")) >= 0:
                self.value = value

        self.charVal.setValue(self.value)
        self.charVal.setSuffix(f" (+{self.addiction})")
        self.modifUPD(self.value)
        self.valueChanged.emit()

    def modifUPD(self, value):
        self.modif = str(floor((value + self.addiction - 10) / 2))
        if self.modif[0] != "-":
            self.modif = "+" + self.modif
        self.charModificator.setText(str(self.modif))

    def randomize(self):
        _vals = [randint(1, 6) for _ in range(4)]
        _vals.remove(min(_vals))
        self.setValue(sum(_vals))
