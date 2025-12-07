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


class SecondPart(QWidget):
    needToSend = pyqtSignal(object)

    def __init__(self, character):
        super().__init__()
        self.character = character
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout(self)

        self.cells_container = CellsContainer(self.character)
        self.cells_container.needToSend.connect(self.needToSend.emit)
        layout.addWidget(self.cells_container)

    def characterUpdate(self, character):
        self.character = character
        self.cells_container.characterUpdate(character)
