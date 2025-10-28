import re
from random import randint

from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QPushButton,
)


from OtherPyFiles.characterclass import Character
from UI.CreateChar.DiceCharModule import DiceChar


class HealthCharacteristics(QWidget):
    def __init__(self, initCharacter: Character, stat: DiceChar):
        super().__init__()
        self.varUpd(initCharacter, stat)
        self.setupUi()

    def classUpd(self, ch, st):
        self.varUpd(ch, st)

    def varUpd(self, character, stat):
        self.character: Character = character
        self.stat: DiceChar = stat
        self.dice = self.character.Stats.get("hpDice")
        self.levels = self.character.getLevel() - 1
        self.character.setMaxHealth(self.character.getFirstLevMaxHp())
        self.mid = int(int(self.dice[1:]) / 2 + 1)
        self.updateData()

    def updateData(self):
        try:
            self.info.setText(f"""Здесь ты можешь определить максимальное количество хитов для твоего персонажа
    Этот параметр определяет сколько ударов ты выдержишь.
    Задать его можно двумя способами
    1. Рандом. Кинуть кубик {self.dice} и прибавить к нему модификатор Телосложения
    2. Взять среднее значение +1 ({self.mid}) и прибавить к нему тот же модификатор""")

            self.CurrentVal.setText(
                "Текущее кол-во хитов - " + str(self.character.getMaxHp())
            )
            self.FirstVar.setTitle("Рандом")
            self.ManualTitle.setText("Я сам посчитаю. \n Моё количество хитов: ")
            self.RandomButton.setText("Рандомить хп")
            self.SecondVar.setTitle("Среднее")
            self.MidButton.setText(
                f"Выбрать среднее значение ({self.mid + int(self.stat.modif)})"
            )
        except:
            pass

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.info = QLabel()

        self.info.setWordWrap(True)
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.info)

        self.CurrentVal = QLabel(text=str(self.character.getMaxHp()))
        self.CurrentVal.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.mainLayout.addWidget(self.CurrentVal, 1, Qt.AlignmentFlag.AlignHCenter)

        self.selectingHealth = QHBoxLayout()
        self.FirstVar = QGroupBox()
        self.FirstLayout = QVBoxLayout(self.FirstVar)
        self.ManualThrow = QHBoxLayout()
        self.ManualTitle = QLabel()
        self.ManualTitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.ManualThrow.addWidget(self.ManualTitle, 5)

        self.ManualInput = QLineEdit()
        self.ManualInput.setValidator(CheckDice())
        self.ManualInput.textChanged.connect(self.manualHp)
        self.ManualThrow.addWidget(self.ManualInput, 2)

        self.FirstLayout.addLayout(self.ManualThrow)

        self.RandomThrow = QHBoxLayout()
        self.RandomButton = QPushButton()
        self.RandomButton.clicked.connect(self.randomHp)
        self.RandomThrow.addWidget(self.RandomButton, 6, Qt.AlignmentFlag.AlignHCenter)

        self.RandomText = QLabel(text="0")
        self.RandomText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.RandomThrow.addWidget(self.RandomText, 1, Qt.AlignmentFlag.AlignHCenter)

        self.FirstLayout.addLayout(self.RandomThrow)

        self.selectingHealth.addWidget(self.FirstVar)

        self.SecondVar = QGroupBox()
        self.SecondLayout = QVBoxLayout(self.SecondVar)

        self.MidButton = QPushButton()
        self.MidButton.clicked.connect(self.middleHp)
        self.SecondLayout.addWidget(self.MidButton)

        self.selectingHealth.addWidget(self.SecondVar)

        self.mainLayout.addLayout(self.selectingHealth)

    def randomHp(self):
        if self.levels >= 1:
            randomizedHp = max(
                [1, randint(1, int(self.dice[1:])) + int(self.stat.modif)]
            )
            self.RandomText.setText(str(randomizedHp))
            self.character.maxHealthUp(randomizedHp)
            self.updateData()
            self.levels -= 1
            if self.levels == 0:
                self.RandomButton.setText("это максимальные хиты")

    def middleHp(self):
        if self.levels >= 1:
            self.character.maxHealthUp(self.mid + int(self.stat.modif))
            self.updateData()
            self.levels -= 1
            if self.levels == 0:
                self.MidButton.setText("это максимальные хиты")

    def manualHp(self, text):
        self.character.setMaxHealth(text)
        self.updateData()


class CheckDice(QtGui.QValidator):
    def validate(self, a0, a1):
        pattern = re.compile("(440)|(4[0123]\d)|([123]\d\d)|(\d\d?)|")
        if a0 == "":
            return QtGui.QValidator.State.Acceptable, a0, a1
        if pattern.fullmatch(a0):
            return QtGui.QValidator.State.Acceptable, a0, a1
        else:
            return QtGui.QValidator.State.Invalid, a0, a1


if __name__ == "__main__":
    hch = HealthCharacteristics(Character(), DiceChar())
