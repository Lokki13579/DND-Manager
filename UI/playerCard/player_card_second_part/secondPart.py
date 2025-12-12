from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
)

from .spellCellsPart import CellsContainer
from .statusPart import StatusContainer
from .addictButtonPart import AddictButtonPart


class SecondHorizontalPart(QWidget):
    needToSend = pyqtSignal(object)

    def __init__(self, character):
        super().__init__()
        self.character = character
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QHBoxLayout(self)
        self.statuses_container = StatusContainer(self.character)
        self.statuses_container.needToSend.connect(self.needToSend.emit)

        self.addict_button_part = AddictButtonPart(self.character)
        self.addict_button_part.needToSend.connect(self.needToSend.emit)
        self.mainLayout.addWidget(self.statuses_container)
        self.mainLayout.addWidget(self.addict_button_part)

    def characterUpdate(self, character):
        self.character = character
        self.cells_container.characterUpdate(character)


class secondChars(QWidget):
    needToSend = pyqtSignal(object)

    def __init__(self, character):
        super().__init__()
        self.character = character
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.cells_container = CellsContainer(self.character)
        self.cells_container.needToSend.connect(self.needToSend.emit)
        self.mainLayout.addWidget(self.cells_container, 1)

        self.second_horizontal_part = SecondHorizontalPart(self.character)
        self.second_horizontal_part.needToSend.connect(self.needToSend.emit)
        self.mainLayout.addWidget(self.second_horizontal_part, 2)

    def characterUpdate(self, character):
        self.character = character
        self.cells_container.characterUpdate(character)
