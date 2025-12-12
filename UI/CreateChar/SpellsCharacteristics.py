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


from OtherPyFiles.characterclass import Character
from OtherPyFiles.dataBaseHandler import SpellHandler
from UI.CreateChar.spellItem import SpellListItem, Spell

files = ["spells"]


class SpellsCharacteristics(QWidget):
    def __init__(self, character: Character):
        super().__init__()
        self.character: Character = character
        self.spells = {}

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
        self.spWidget = QWidget()
        self.spellsContainer = QVBoxLayout(self.spWidget)
        self.scrollArea.setWidget(self.spWidget)
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
        for spellName in [
            j
            for i in self.character.stats.get("spells", {})
            .get("allSpells", {})
            .values()
            for j in i
        ]:
            spD = SpellHandler().getSpellInfo("*", f"spell_name='{spellName}'")
            spell = self.createObject(spD[spellName])
            self.spells[spellName] = spell
            self.spellsContainer.addWidget(spell)

    def searchItems(self, text, _dict={}):
        self.searchResult.clear()
        pattern = r"(\([0-9]\))?([^#\(\)]+)?"
        res = re.findall(pattern, text) + [("None", "None")]
        searchGroup, searchSpell = res[0]
        searchGroup = searchGroup.strip("()")
        searchSpell = searchSpell.strip()
        if searchGroup == "":
            for i in range(
                max(
                    list(
                        map(
                            int,
                            dict(
                                filter(
                                    lambda x: x[1] > 0,
                                    self.character.stats.get("otherStats")
                                    .get("ЯчейкиЗаклинаний")
                                    .items(),
                                )
                            ).keys(),
                        )
                    )
                )
                + 1
            ):
                header = QTreeWidgetItem(self.searchResult, [f"{i} уровень"])
                _dict[f"{i}"] = header
                for spell, classes in (
                    SpellHandler()
                    .getSpellInfo("spell_name,classes", f"spell_level={i}")
                    .items()
                ):
                    _class = self.character.stats.get("class").lower()
                    for cl in classes:
                        if _class in cl.lower():
                            break
                    else:
                        continue
                    if searchSpell.lower() in spell.lower():
                        item = QTreeWidgetItem(header, [spell])
                        _dict[spell] = item
            self.searchResult.expandAll()
        else:
            header = QTreeWidgetItem(self.searchResult, [f"{searchGroup} уровень"])
            _dict[searchGroup] = header
            for spell in SpellHandler().getSpellInfo(
                "spell_name", f"level={searchGroup}"
            ):
                if searchSpell.lower() in spell.lower():
                    item = QTreeWidgetItem(header, [spell])
                    _dict[spell] = item
            self.searchResult.expandAll()

    def addItem(self):
        pattern = r"(\([0-9]\))?([^#\(\)]+)?"
        res = re.findall(pattern, self.searchBar.text())
        spellName = res[0][1].strip()
        spD = SpellHandler().getSpellInfo("*", f"spell_name='{spellName}'")

        if not spD:
            self.searchBar.setText("Такого заклинания не существует")
            return
        spellItem = self.createObject(spD[spellName])
        self.character.addSpell(spellItem)
        for i in self.spells.values():
            self.spellsContainer.removeWidget(i)
        self.spells[spellName] = spellItem
        for it in self.spells.values():
            self.spellsContainer.addWidget(it)
        self.searchBar.setText("")

    def createObject(self, spellData):
        item = SpellListItem(Spell(**spellData))
        return item

    def itemSelected(self, index: QTreeWidgetItem):
        if index.text(0) in files:
            return
        self.searchBar.setText(index.text(0))
