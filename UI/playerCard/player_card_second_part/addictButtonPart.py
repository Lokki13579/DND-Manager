from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
    QSpinBox,
    QGridLayout,
)

from UI.CreateChar.InventoryCharacteristics import InventoryCharacteristics as InvChar
from UI.CreateChar.SpellsCharacteristics import SpellsCharacteristics as SpellsChar


class DiceDialog(QDialog):
    closed = pyqtSignal()

    def __init__(self, parent, character):
        super().__init__(parent)
        self.character = character
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        elements = []
        charDiceStats = self.character.stats.get("diceStats", {})
        print(charDiceStats)
        for type, value in charDiceStats.get("main", {}).get("value", {}).items():
            elements.append(
                QLabel(
                    f"{type}: {value + charDiceStats.get('addiction', {}).get(type, 0)}"
                )
            )
            self.mainLayout.addWidget(elements[-1])
        exitButton = QPushButton("Закрыть")
        exitButton.clicked.connect(lambda: (self.closed.emit(None), self.close()))
        self.mainLayout.addWidget(exitButton)


class HealthDialog(QDialog):
    closed = pyqtSignal(object)

    def __init__(self, parent, character):
        super().__init__(parent)
        self.character = character
        self.hpInfo = character.stats.get("health", {})
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.maxInit()
        self.currentInit()
        self.tempInit()
        self.exitInit()

    def maxInit(self):
        self.maxGroup = QGroupBox("Максимум")
        self.maxLayout = QVBoxLayout(self.maxGroup)
        self.maxSpinBox = QSpinBox()
        self.maxSpinBox.setMinimum(1)
        self.maxSpinBox.setValue(self.hpInfo.get("main", {}).get("max", 1))
        self.maxSpinBox.valueChanged.connect(self.onMaxValueChanged)
        self.maxLayout.addWidget(self.maxSpinBox)
        self.mainLayout.addWidget(self.maxGroup)

    def currentInit(self):
        self.currentGroup = QGroupBox("Текущее")
        self.currentLayout = QVBoxLayout(self.currentGroup)
        self.currentSpinBox = QSpinBox()
        self.currentSpinBox.setMinimum(0)
        self.currentSpinBox.setMaximum(self.maxSpinBox.value())

        self.currentSpinBox.setValue(self.hpInfo.get("main", {}).get("val", 1))
        self.currentSpinBox.valueChanged.connect(self.onCurrentValueChanged)
        self.currentLayout.addWidget(self.currentSpinBox)
        self.mainLayout.addWidget(self.currentGroup)

    def tempInit(self):
        self.tempGroup = QGroupBox("Временное")
        self.tempLayout = QVBoxLayout(self.tempGroup)
        self.tempSpinBox = QSpinBox()
        self.tempSpinBox.setMinimum(0)
        self.tempSpinBox.setValue(self.hpInfo.get("temp", 0))
        self.tempSpinBox.valueChanged.connect(self.onTempValueChanged)
        self.tempLayout.addWidget(self.tempSpinBox)
        self.mainLayout.addWidget(self.tempGroup)

    def exitInit(self):
        self.exitButton = QPushButton("Закрыть")
        self.exitButton.clicked.connect(
            lambda: (
                self.close(),
                self.closed.emit("newStats&" + str(self.character.stats)),
            ),
        )
        self.mainLayout.addWidget(self.exitButton)

    def onMaxValueChanged(self):
        self.currentSpinBox.setMaximum(self.maxSpinBox.value())
        self.character.setMaxHealth(self.maxSpinBox.value())

    def onCurrentValueChanged(self):
        self.character.setHealth(self.currentSpinBox.value())

    def onTempValueChanged(self):
        self.character.setTempHp(self.tempSpinBox.value())


class InventoryDialog(QDialog):
    closed = pyqtSignal(str)

    def __init__(self, parent, character):
        super().__init__(parent)
        self.character = character
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.invInit()
        self.exitInit()

    def invInit(self):
        self.invObject = InvChar(self.character)
        self.mainLayout.addWidget(self.invObject)

    def exitInit(self):
        self.exitButton = QPushButton("Закрыть")
        self.exitButton.clicked.connect(
            lambda: (
                self.close(),
                self.closed.emit("newStats&" + str(self.character.stats)),
            ),
        )
        self.mainLayout.addWidget(self.exitButton)


class SpellDialog(QDialog):
    closed = pyqtSignal(str)

    def __init__(self, parent, character):
        super().__init__(parent)
        self.character = character
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.spellInit()
        self.exitInit()

    def spellInit(self):
        self.spellObject = SpellsChar(self.character)
        self.mainLayout.addWidget(self.spellObject)

    def exitInit(self):
        self.exitButton = QPushButton("Закрыть")
        self.exitButton.clicked.connect(
            lambda: (
                self.close(),
                self.closed.emit("newStats&" + str(self.character.stats)),
            ),
        )
        self.mainLayout.addWidget(self.exitButton)


class CommonButton(QPushButton):
    def __init__(self, text, linkToDialog, character, parent):
        super().__init__(text)
        self.character = character
        self.linkToDialog = linkToDialog
        self.parent = parent
        self.clicked.connect(self.onClicked)

    def setCharacter(self, character):
        self.character = character

    def onClicked(self):
        dialog = self.linkToDialog(self.parent, self.character)
        dialog.closed.connect(self.whenDialogClosed)
        dialog.show()

    def whenDialogClosed(self, data):
        self.parent.needToSend.emit(data)


class AddictButtonPart(QGroupBox):
    needToSend = pyqtSignal(object)

    def __init__(self, character):
        super().__init__()
        self.character = character
        self.diceButton, self.healthButton, self.invButton, self.spellButton = (
            None,
            None,
            None,
            None,
        )
        self.setupUi()

    def characterUpdate(self, character):
        self.character = character
        self.diceButton.setCharacter(self.character)
        self.healthButton.setCharacter(self.character)
        self.invButton.setCharacter(self.character)
        self.spellButton.setCharacter(self.character)

    def setupUi(self):
        self.mainLayout = QGridLayout(self)
        self.diceButton = CommonButton(
            "Просмотр дайсов", DiceDialog, self.character, self
        )
        self.healthButton = CommonButton(
            "Изменение здоровья", HealthDialog, self.character, self
        )
        self.invButton = CommonButton(
            "Инвентарь", InventoryDialog, self.character, self
        )
        self.spellButton = CommonButton(
            "Изменение заклинаний", SpellDialog, self.character, self
        )
        self.mainLayout.addWidget(self.diceButton, 0, 0)
        self.mainLayout.addWidget(self.healthButton, 0, 1)
        self.mainLayout.addWidget(self.invButton, 1, 0)
        self.mainLayout.addWidget(self.spellButton, 1, 1)
