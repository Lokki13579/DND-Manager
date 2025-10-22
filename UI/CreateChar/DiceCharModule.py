
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, QSize,QRect
from PyQt6.QtWidgets import *

from math import floor


class DiceChar(QFrame):
    valueChanged = pyqtSignal(str,int)
    def __init__(self,_name,_val,_add):
        super().__init__()
        self.name = _name
        self.value = _val
        self.modif = str(floor((_val + int(_add) - 10) / 2))
        if self.modif[0] not in "-+":
            self.modif = "+" + self.modif
        self.addiction = _add
        self.setupUi()

    def setupUi(self):
        #self.setMaximumSize(QSize(200,120))
        self.setMinimumSize(QSize(200,120))
        self.MainGroup = QGroupBox(self,title=self.name)
        self.MainGroup.setMinimumSize(QSize(200,120))
        self.MainGroup.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.vertLayout = QVBoxLayout(self.MainGroup)

        self.charVal = QSpinBox()
        self.charVal.valueChanged.connect(self.emit_Signal)
        self.charVal.setValue(self.value)
        self.charVal.setSuffix(f"(+{self.addiction})")
        self.charVal.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.vertLayout.addWidget(self.charVal,2)

        self.charModificator = QLabel(text=str(self.modif))
        self.charModificator.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.charModificator.setStyleSheet("""
            font-size: 28px;

        """)
        self.vertLayout.addWidget(self.charModificator,3)
    def emit_Signal(self):
        self.valueChanged.emit(self.name,self.charVal.value())

