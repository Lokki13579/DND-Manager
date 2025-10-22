



from PyQt6 import QtCore, QtWidgets

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import *


from characterclass import *
from UI.CreateChar.DiceCharModule import *

class ThirdCharacteristics(QWidget):
    def __init__(self,_character):
        super().__init__()
        self.character : Character= _character
        self.setupUi()
    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.TitleLayout = QHBoxLayout()

        self.TitleText = QLabel(text="Здесь можно выбрать(либо нарандомить) характеристики для своего персонажа")
        self.TitleText.setWordWrap(True)
        self.TitleLayout.addWidget(self.TitleText,8)

        self.randomizeButton = QPushButton(text="Случайно")
        self.TitleLayout.addWidget(self.randomizeButton,4)

        self.mainLayout.addLayout(self.TitleLayout,4)

        _statsList = ["Сила","Ловкость","Телосложение","Харизма","Интелект","Мудрость"]
        self.placeforDice = QGridLayout()
        self.placeforDice.setSpacing(14)
        self.placeforDice.setContentsMargins(42,20,42,20)
        self.diceObjects = {}

        for i,st in enumerate(_statsList):
            self.diceObjects[st] = DiceChar(st,8,"0")
            self.diceObjects[st].valueChanged.connect(self.on_value_changed)
            self.diceObjects[st].emit_Signal()
            self.placeforDice.addWidget(self.diceObjects[st],i//3,i%3)

        self.mainLayout.addLayout(self.placeforDice,12)
    def on_value_changed(self,name, value):
        print(name,value)
        self.character.setDice(name,value)
        print(self.character.name, self.character.Stats)

