from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QTreeView,
    QWidget,
    QLabel,
    QLineEdit,
    QListWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
)
import re


from OtherPyFiles.characterclass import Character, jsonLoad

files = ["drugs", "giant_bag", "magic_items", "poisons", "trinkets"]
itemsData = {}
for file in files:
    itemsData[file] = jsonLoad(f"JSONS/dnd_{file}.json")


class InventoryCharacteristics(QWidget):
    def __init__(self):
        super().__init__()
        self.character: Character
        self.items = []
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

        self.inventoryItems = QListWidget()
        self.LeftSide.addWidget(self.inventoryItems)

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Введите название предмета")
        self.searchBar.textChanged.connect(self.searchItems)

        self.LeftSide.addWidget(self.searchBar)

        self.mainLayout.addLayout(self.LeftSide)

        self.RightSide = QVBoxLayout()

        self.searchResult = QTreeWidget()
        self.searchResult.setWordWrap(True)
        self.searchResult.setHeaderLabels(["Предметы"])
        self.searchResult.doubleClicked.connect(self.itemSelected)

        self.searchItems("", {})
        self.RightSide.addWidget(self.searchResult)

        self.mainLayout.addLayout(self.RightSide)

    def searchItems(self, text, _dict={}):
        self.searchResult.clear()
        pattern = r"(\(.*\))?([^\(]?.*[^\)])?"
        res = re.findall(pattern, text) + [("None", "None")]
        searchGroup, searchItem = res[0]
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

    def itemSelected(self, index):
        print(index)
