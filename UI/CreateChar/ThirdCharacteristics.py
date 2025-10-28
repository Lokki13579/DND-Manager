from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QPushButton,
)


from OtherPyFiles.characterclass import Character, jsonLoad
from UI.CreateChar.DiceCharModule import DiceChar


class ThirdCharacteristics(QWidget):
    def __init__(self, _character):
        super().__init__()
        self.character: Character = _character
        self.points = 27
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.TitleLayout = QHBoxLayout()

        self.TitleText = QLabel(
            text="Здесь можно выбрать(либо нарандомить) характеристики для своего персонажа"
        )
        self.TitleText.setWordWrap(True)
        self.TitleLayout.addWidget(self.TitleText, 8)

        self.randomizeButton = QPushButton(text="Случайно")
        self.randomizeButton.clicked.connect(self.randomize)
        self.TitleLayout.addWidget(self.randomizeButton, 4)

        self.mainLayout.addLayout(self.TitleLayout, 4)

        _statsList = [
            "Сила",
            "Ловкость",
            "Телосложение",
            "Харизма",
            "Интелект",
            "Мудрость",
        ]
        self.placeforDice = QGridLayout()
        self.placeforDice.setSpacing(14)
        self.placeforDice.setContentsMargins(42, 20, 42, 20)
        self.diceObjects = {}

        self.PointLayout = QHBoxLayout()
        self.PointText = QLabel(text=str(self.points))
        self.PointLayout.addWidget(self.PointText, 1, Qt.AlignmentFlag.AlignCenter)

        for i, st in enumerate(_statsList):
            self.diceObjects[st] = DiceChar(
                st,
                8,
                self.character.Stats.get("diceStats").get("addiction").get(st, "0"),
                self.points,
            )
            self.diceObjects[st].valueChanged.connect(self.on_value_changed)
            self.diceObjects[st].emit_Signal()
            self.placeforDice.addWidget(self.diceObjects[st], i // 3, i % 3)

        self.mainLayout.addLayout(self.placeforDice, 12)

        self.mainLayout.addLayout(self.PointLayout)

    def randomize(self):
        for i in self.diceObjects.values():
            i.randomDisp()
        self.randomizeButton.setDisabled(True)
        self.PointText.setText("")

    def pointsDispencer(self, points):
        for i in self.diceObjects.values():
            i.pointsUpdate(points)

    def on_value_changed(self, name, value, newPoints):
        self.points = newPoints
        self.pointsDispencer(self.points)
        self.PointText.setText(str(self.points))

        self.character.setDice(name, value)
