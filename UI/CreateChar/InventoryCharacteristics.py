from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
)


from OtherPyFiles.characterclass import Character, jsonLoad

files = ["drugs", "giant_bag", "magic_items", "poisons", "trinkets"]
itemsData = {}
for file in files:
    itemsData[file] = jsonLoad(f"JSONS/dnd_{file}.json")


class InventoryCharacteristics(QWidget):
    def __init__(self):
        self.character: Character
        self.items = []

        self.setupUi()

    def setupUi(self):
        self.mainLayout = QHBoxLayout(self)

        self.LeftSide = QVBoxLayout()

        self.TableTitle = QHBoxLayout()
        self.indexTitle = QLabel()
        self.nameTitle = QLabel()
        self.emptySlotsTitle = QLabel()

        self.TableTitle.addWidget(self.indexTitle)
        self.TableTitle.addWidget(self.nameTitle)
        self.TableTitle.addWidget(self.emptySlotsTitle)
