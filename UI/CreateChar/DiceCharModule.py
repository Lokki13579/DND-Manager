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
    valueChanged = pyqtSignal(str, int, int)

    def __init__(self, _name, _val, _add, lastpoints):
        super().__init__()
        self.name = _name
        self.value = _val
        self.modif = str(floor((_val + int(_add) - 10) / 2))
        if self.modif[0] not in "-+":
            self.modif = "+" + self.modif
        self.addiction = _add
        self.points = lastpoints
        self.setupUi()

    def pointsUpdate(self, value):
        self.points = value
        self.diceManager()

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
        self.charVal.setValue(self.value)
        self.charVal.lineEdit().setReadOnly(True)
        self.charVal.valueChanged.connect(self.emit_Signal)
        self.charVal.setSuffix(f"(+{self.addiction})")
        self.charVal.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.vertLayout.addWidget(self.charVal, 2)

        self.charModificator = QLabel(text=str(self.modif))
        self.charModificator.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.charModificator.setStyleSheet("""
            font-size: 28px;

        """)
        self.vertLayout.addWidget(self.charModificator, 3)

    def diceManager(self):
        past = self.value  # 8
        new = self.charVal.value()  # 9
        if self.points == 0:
            self.charVal.setMaximum(self.value)
        else:
            self.charVal.setMaximum(15)
        if new == past:
            return past

        if new > past:
            if new > 13 and self.points >= 2:
                self.points -= 2
            elif self.points >= 1:
                self.points -= 1
            past += 1
        else:
            if past > 13:
                self.points += 2
            else:
                self.points += 1
            past -= 1

        return past

    def randomDisp(self):
        _v = [randint(1, 6) for i in range(4)]
        _v.remove(min(_v))
        self.value = sum(_v)
        self.charVal.setValue(self.value)
        self.modifUpdate()
        self.charVal.setReadOnly(True)
        print(_v)

    def dataUpdate(self):
        self.value = self.diceManager()
        self.modifUpdate()

    def modifUpdate(self):
        self.modif = str(floor((self.value + int(self.addiction) - 10) / 2))
        if self.modif[0] not in "-+":
            self.modif = "+" + self.modif
        self.charModificator.setText(str(self.modif))

    def emit_Signal(self):
        self.dataUpdate()
        self.valueChanged.emit(self.name, self.value, self.points)
