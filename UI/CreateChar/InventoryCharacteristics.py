from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QScrollArea,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
import re


from OtherPyFiles.characterclass import Character, jsonLoad
from UI.CreateChar.invItem import InventoryItem, Item

files = ["drugs", "giant_bag", "magic_items", "poisons", "trinkets"]
itemsData = {}
for file in files:
    itemsData[file] = jsonLoad(f"JSONS/dnd_{file}.json")


class InventoryCharacteristics(QWidget):
    def __init__(self, character: Character):
        super().__init__()
        self.character: Character = character
        self.items = {}
        self.searching = {}

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
        self.LeftSide.addLayout(self.TableTitle)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.invWidget = QWidget()
        self.inventoryItems = QVBoxLayout(self.invWidget)
        self.scrollArea.setWidget(self.invWidget)
        self.LeftSide.addWidget(self.scrollArea)

        self.searchLayout = QHBoxLayout()
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Введите название предмета")
        self.searchBar.textChanged.connect(self.searchItems)
        self.searchLayout.addWidget(self.searchBar)

        icon = QIcon("resources/icons/add.png")
        self.searchAddButton = QPushButton("Добавить", icon=icon)
        self.searchAddButton.clicked.connect(self.addItem)
        self.searchLayout.addWidget(self.searchAddButton)

        self.searchLayout.addLayout(self.searchLayout)

        self.LeftSide.addLayout(self.searchLayout)

        self.mainLayout.addLayout(self.LeftSide, 12)

        self.RightSide = QVBoxLayout()

        self.searchResult = QTreeWidget()
        self.searchResult.setWordWrap(True)
        self.searchResult.setHeaderLabel("Предметы")
        self.searchResult.itemDoubleClicked.connect(self.itemSelected)

        self.searchItems("", {})
        self.RightSide.addWidget(self.searchResult, 3)

        self.mainLayout.addLayout(self.RightSide)

    def searchItems(self, text, _dict={}):
        self.searchResult.clear()
        pattern = r"(\(.*\))?([^(#\[][^#\[]*)?(\[\d*\])?"
        res = re.findall(pattern, text) + [("None", "None")]
        print(res[0])
        searchGroup, searchItem, trash = res[0]
        searchGroup = searchGroup.strip("()")
        searchItem = searchItem.strip()

        if searchGroup == "None" or searchGroup == "":
            for group, item in itemsData.items():
                header = QTreeWidgetItem(self.searchResult, [group])
                header.setExpanded(True)
                _dict[group] = header

                if group == "giant_bag":
                    self.giantAdd(item, searchItem, header, _dict)
                    continue
                for subitem in item:
                    if searchItem.lower() in subitem.lower():
                        child = QTreeWidgetItem(header, [subitem])
                        _dict[subitem] = child
            self.searchResult.expandAll()
            return _dict

        for name in itemsData.keys():
            if searchGroup.lower() in name.lower():
                header = QTreeWidgetItem(self.searchResult, [name])
                header.setExpanded(True)
                _dict[name] = header
                if name == "giant_bag":
                    self.giantAdd(itemsData[name], searchItem, header, _dict)
                    continue
                for item in itemsData.get(name, []):
                    if searchItem.lower() in item.lower():
                        child = QTreeWidgetItem(header, [item])
                        _dict[item] = child
        self.searchResult.expandAll()
        return _dict

    def giantAdd(self, item, searchItem, header, _dict):
        checked = False

        for giant, loot in item.items():
            if searchItem.lower() in giant.lower() or any(
                [searchItem.lower() in i.lower() for i in loot]
            ):
                if searchItem.lower() in giant.lower():
                    checked = True
                child = QTreeWidgetItem(header, [giant])
                _dict[giant] = child
                for subitem in loot:
                    if searchItem.lower() in subitem.lower() or checked:
                        child2 = QTreeWidgetItem(child, [subitem])
                        _dict[subitem] = child2

    def addItem(self):
        pattern = r"(\(.*\))?([^(#\[][^#\[]*)?(\[\d*\])?"
        res = re.findall(pattern, self.searchBar.text())
        itemName = res[0][1].strip()
        itemNumber = res[0][2]
        if itemNumber:
            itemNumber = int(itemNumber[1:-1])
        else:
            itemNumber = 1
        invItem = self.createObject(itemName, itemNumber)
        self.character.addItem(itemName, invItem)
        for i in self.items.values():
            self.inventoryItems.removeWidget(i)
        self.items[itemName] = invItem
        for it in self.items.values():
            self.inventoryItems.addWidget(it)
        print(self.character.Stats)

    def createObject(self, itemName, itemNumber):
        item = InventoryItem(Item(itemName, itemNumber))
        return item

    def itemSelected(self, index: QTreeWidgetItem):
        if index.text(0) in files:
            return
        self.searchBar.setText(
            index.text(0)
            + "[1] #введите количество в кв скобках по умолчанию 1. Например: [10]"
        )
