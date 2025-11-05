from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal


class CellObj(QHBoxLayout):
    cell_changed = pyqtSignal(str, int)

    def __init__(self, level: int, count: int, max: int):
        super().__init__()
        self.level: str = level
        self.count: int = count
        self.max: int = int(max)
        self.setupUi()

    def setMax(self, max):
        self.max = max
        print(self.level, max)
        self.setCount(self.count)

    def setCount(self, count):
        self.count = count
        self.label.setText(
            f"{self.level}:{''.center(14 - len(str(self.level)) - len(str(self.count)) - 1)}{self.count}"
        )

    def setupUi(self):
        self.label = QLabel()
        self.addWidget(self.label)
        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.addCount)
        self.addWidget(self.addButton)
        self.redButton = QPushButton("Del")
        self.redButton.clicked.connect(self.removeCount)
        self.addWidget(self.redButton)

    def addCount(self):
        print(self.max)
        if int(self.count) == int(self.max):
            return
        self.count += 1
        self.setCount(self.count)
        self.cell_changed.emit(self.level, self.count)

    def removeCount(self):
        if self.count > 0:
            self.count -= 1
            self.setCount(self.count)
            self.cell_changed.emit(self.level, self.count)
