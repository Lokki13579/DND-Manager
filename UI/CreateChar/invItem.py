from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QPushButton


class Item(QObject):
    deletingItem = pyqtSignal(str)

    def __init__(self, name, count=1, index=0):
        super().__init__()
        self.name = name
        self.count = count
        self.index = index

    def add(self, count=1):
        if count <= 0:
            return "количество должно быть больше нуля"
        self.count += count

    def reduce(self, count=1):
        if count <= 0:
            return "количество должно быть больше нуля"
        self.count -= count
        if self.count == 0:
            self.deletingItem.emit(self.name)

    def delete(self):
        self.deletingItem.emit(self.name)


class InventoryItem(QFrame):
    def __init__(self, item=Item("Абракадабрус")):
        super().__init__()
        self.item = item
        self.item.deletingItem.connect(self.close)
        self.setupUi()
        self.setTexts()

    def setupUi(self):
        self.mainLayout = QHBoxLayout(self)

        self.nameArea = QLabel()

        add_icon = QIcon("resources/add_icon.32.png")
        self.addButton = QPushButton(icon=add_icon)

        reduce_icon = QIcon("resources/remove_icon.32.png")
        self.reduceButton = QPushButton(icon=reduce_icon)

        delete_icon = QIcon("resources/close_icon.32.png")
        self.deleteButton = QPushButton(icon=delete_icon)

        self.nameArea.setWordWrap(True)
        self.mainLayout.addWidget(self.nameArea, 24)

        self.addButton.clicked.connect(self.add)
        self.mainLayout.addWidget(self.addButton, 3)

        self.reduceButton.clicked.connect(self.reduce)
        self.mainLayout.addWidget(self.reduceButton, 3)

        self.deleteButton.clicked.connect(self.delete)
        self.mainLayout.addWidget(self.deleteButton, 3)

    def add(self):
        self.item.add()
        self.setTexts()

    def reduce(self):
        self.item.reduce()
        self.setTexts()

    def delete(self):
        self.item.delete()
        super().close()

    def setTexts(self):
        self.nameArea.setText(f"{self.item.name} - ({self.item.count})")
        self.addButton.setText("")
        self.reduceButton.setText("")
        self.deleteButton.setText("")
