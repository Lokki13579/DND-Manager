from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QTreeWidget,
    QTreeWidgetItem,
)

from OtherPyFiles.characterclass import classData, racesData
from OtherPyFiles.dataBaseHandler import ClassInfoHandler, RaceInfoHandler


class SecondCharacteristics(QWidget):
    def __init__(self, _character):
        super().__init__()
        self.character = _character
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QHBoxLayout(self)

        self.classLayout = QVBoxLayout()

        self.classTitle = QLabel(text="Выберите класс вашего персонажа")
        self.classLayout.addWidget(self.classTitle, 2)

        self.classChoose = QComboBox()
        self.classChoose.currentTextChanged.connect(self.on_class_changed)
        self.classLayout.addWidget(self.classChoose, 3)

        self.classSkillTree = QTreeWidget()
        self.classSkillTree.setStyleSheet("font-size: 18pt;")
        self.classSkillTree.setHeaderLabel("Особенности класса")
        self.classSkillTreeGroup = QTreeWidgetItem(self.classSkillTree, ["Умения"])
        self.skills = {}
        self.classLayout.addWidget(self.classSkillTree, 12)

        self.bgChoose = QComboBox()
        self.bgChoose.currentTextChanged.connect(self.on_bg_changed)
        self.classLayout.addWidget(self.bgChoose, 2)

        self.mainLayout.addLayout(self.classLayout)

        self.raceLayout = QVBoxLayout()

        self.raceTitle = QLabel(text="Выберите расу вашего персонажа")
        self.raceLayout.addWidget(self.raceTitle, 2)

        self.raceChoose = QComboBox()
        self.raceChoose.currentTextChanged.connect(self.on_race_changed)
        self.raceLayout.addWidget(self.raceChoose, 3)

        self.raceParamsTree = QTreeWidget()
        self.raceParamsTree.setStyleSheet("font-size: 18pt;")
        self.raceParamsTree.setHeaderLabel("Особенности расы")
        self.raceParamsTreeGroup = QTreeWidgetItem(
            self.raceParamsTree, [self.raceChoose.currentText()]
        )
        self.raceData = {}
        self.on_race_changed(self.raceChoose.currentText())
        self.raceLayout.addWidget(self.raceParamsTree, 12)

        self.wvChoose = QComboBox()
        self.wvChoose.currentTextChanged.connect(self.on_wv_changed)
        self.raceLayout.addWidget(self.wvChoose, 2)

        self.mainLayout.addLayout(self.raceLayout)

    def on_class_changed(self, _class):
        print(_class)
        self.character.setClass(_class)
        self.classSkillTree.clear()
        self.classSkillTreeGroup = QTreeWidgetItem(self.classSkillTree, ["Умения"])
        self.classSkillTree.expandAll()

    def on_wv_changed(self, wv):
        self.character.stats["worldview"] = wv

    def on_race_changed(self, race):
        self.character.setRace(race)
        self.raceParamsTree.clear()
        self.raceParamsTreeGroup = QTreeWidgetItem(
            self.raceParamsTree, [self.raceChoose.currentText()]
        )
        self.raceParamsTree.expandAll()

    def on_bg_changed(self, bg):
        self.character.stats["background"] = bg
