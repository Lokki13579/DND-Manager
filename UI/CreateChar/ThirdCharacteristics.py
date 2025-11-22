from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QPushButton,
)


from OtherPyFiles.characterclass import Character
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
        self.randomizeButton.clicked.connect(self.randimize)
        self.TitleLayout.addWidget(self.randomizeButton, 4)

        self.mainLayout.addLayout(self.TitleLayout, 4)

        _statsList = [
            "Сила",
            "Ловкость",
            "Телосложение",
            "Харизма",
            "Интеллект",
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
                self.character.Stats.get("diceStats").get("addiction").get(st, 0),
                self.points,
            )
            self.diceObjects[st].newPoints.connect(self.updatePoints)
            self.diceObjects[st].valueChanged.connect(self.applyToCharacter)
            self.placeforDice.addWidget(self.diceObjects[st], i // 3, i % 3, 1, 1)

        self.mainLayout.addLayout(self.placeforDice, 12)

        self.mainLayout.addLayout(self.PointLayout)
        self.applyToCharacter()

    def updatePoints(self, newPoints):
        self.points = newPoints
        self.PointText.setText(str(self.points))
        self.pointDisp()

    def randimize(self):
        for obj in self.diceObjects.values():
            obj.randomize()
        self.randomizeButton.setDisabled(True)
        self.points = -1
        self.pointDisp()
        self.PointText.close()

    def on_race_change(self):
        self.addictionDisp()

    def addictionDisp(self):
        for obj in self.diceObjects.values():
            obj.setAddiction(
                self.character.Stats.get("diceStats").get("addiction").get(obj.name, 0)
            )

    def applyToCharacter(self):
        for obj in self.diceObjects.values():
            self.character.Stats.get("diceStats").get("main").get("value").update(
                {obj.name: obj.value}
            )
            self.character.Stats.get("diceStats").get("main").get("modif").update(
                {obj.name: obj.modif}
            )

    def pointDisp(self):
        for obj in self.diceObjects.values():
            obj.setPoints(self.points)
