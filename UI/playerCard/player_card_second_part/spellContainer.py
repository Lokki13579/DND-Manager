from PyQt6.QtWidgets import QGroupBox, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

from UI.playerCard.cellObj import CellObj


class spellGroup(QGroupBox):
    sbmChanged = pyqtSignal(object)

    def __init__(self, character):
        super().__init__()
        self.character = character
        self.spellCellsObj = {}

        self.setupUi()

    def setupUi(self):
        self.setTitle("Заклинания")
        self.mainLayout = QVBoxLayout(self)
        self.spellCellsInit()

    def spellCellsInit(self):
        for level, count in self.character.spellCells.items():
            self.spellCellsObj[level] = CellObj(
                level,
                count,
                self.character.stats.get("otherStats", {})
                .get("ЯчейкиЗаклинаний", {})
                .get(level, 0),
            )
            self.spellCellsObj[level].cell_changed.connect(self.on_cell_changed)

    def setNewCharacter(self, character):
        self.character = character
        for level, count in self.character.spellCells.items():
            self.spellCellsObj[level].setMax(
                self.character.stats.get("otherStats", {})
                .get("ЯчейкиЗаклинаний", {})
                .get(level, 0)
            )
        self.spellCellsUpdate()

    def on_cell_changed(self, level, count):
        self.character.spellCells[level] = count
        self.sbmChanged.emit(None)

    def spellCellsUpdate(self):
        for level, count in self.character.spellCells.items():
            self.spellCellsObj[level].setCount(count)
            self.mainLayout.addLayout(self.spellCellsObj[level])
