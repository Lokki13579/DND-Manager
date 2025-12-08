from typing import override
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QLabel, QCheckBox, QGroupBox, QHBoxLayout


class Cell(QCheckBox):
    @override
    def setChecked(self, a0: bool) -> None:
        if self.isChecked == a0:
            return
        return super().setChecked(a0)


class Cells(QGroupBox):
    count_changed = pyqtSignal(int, int)

    def __init__(self, level, maxCount):
        super().__init__()
        self.cell_level = level
        self.cell_count: int = maxCount
        self.active_cells: int = maxCount
        self.cells: list[QCheckBox] = []
        self.setupUi()

    def setupUi(self):
        self.setTitle(str(self.cell_level))
        self.mainLayout = QHBoxLayout(self)
        for i in range(self.cell_count):
            cell = Cell()
            cell.setChecked(True)
            cell.stateChanged.connect(self.sendData)
            self.cells.append(cell)
            self.mainLayout.addWidget(cell)

    def setMaxCells(self, maxCount):
        self.cell_count = maxCount

    def sendData(self, state):
        self.active_cells = 0
        for i in self.cells:
            if i.isChecked():
                self.active_cells += 1
        self.count_changed.emit(self.cell_level, self.active_cells)

    def newMax(self):
        for i in self.cells:
            self.mainLayout.removeWidget(i)
            i.deleteLater()
        self.cells = []
        for i in range(self.cell_count):
            cell = Cell()
            cell.setChecked(i < self.active_cells)
            cell.stateChanged.connect(self.sendData)
            self.cells.append(cell)
            self.mainLayout.addWidget(cell)

    def setCellsCount(self, count):
        self.active_cells = count
        self.newMax()


class CellsContainer(QGroupBox):
    needToSend = pyqtSignal(object)

    def __init__(self, character):
        super().__init__()
        self.character = character
        self.max_spell_cells = character.stats.get("otherStats").get("ЯчейкиЗаклинаний")
        self.cells_info: dict[int, int] = character.spellCells
        self.cells = []
        self.setupUi()

    def setupUi(self):
        self.setTitle("Ячейки заклинаний")
        self.mainLayout = QGridLayout(self)
        self.createNewCells()

    def createNewCells(self):
        for i in self.cells:
            self.mainLayout.removeWidget(i)
            i.deleteLater()
        self.cells.clear()

        for level, count in self.max_spell_cells.items():
            cells = Cells(level, count)
            self.cells.append(cells)
            self.mainLayout.addWidget(cells, (level - 1) % 2, (level - 1) // 2)
        self.title = QLabel("Ячейки")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.title, 1, 4)

    def characterUpdate(self, char):
        self.character = char
        self.max_spell_cells = char.stats.get("otherStats").get("ЯчейкиЗаклинаний")
        self.cells_info = char.spellCells
        self.createNewCells()
        for i in self.cells:
            i.setMaxCells(self.max_spell_cells[i.cell_level])
            i.setCellsCount(self.cells_info[i.cell_level])
            i.count_changed.connect(self.sendData)

    def sendData(self, level, count):
        if self.cells_info[level] != count:
            self.cells_info[level] = count
            self.needToSend.emit("newSpellCells&" + str(self.cells_info))
