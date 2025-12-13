from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QTreeWidget,
    QTreeWidgetItem,
)

from OtherPyFiles.dataBaseHandler import (
    ClassInfoHandler,
    RaceInfoHandler,
    BackgroundHandler,
    AlignmentHandler,
)


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
        self.raceParamsTree.setHeaderLabels(["Особенности расы", "Значение"])
        self.raceParamsTree.setColumnWidth(0, 42 * 6 - 20)
        self.raceLayout.addWidget(self.raceParamsTree, 12)

        self.wvChoose = QComboBox()
        self.wvChoose.currentTextChanged.connect(self.on_wv_changed)
        self.raceLayout.addWidget(self.wvChoose, 2)

        self.mainLayout.addLayout(self.raceLayout)

        self.classComboAdder()
        self.racesComboAdder()
        self.backgroundsComboAdder()
        self.alignmentsComboAdder()

    def on_class_changed(self, _class):
        self.character.setClass(_class)
        self.classSkillTree.clear()
        self.classSkillTreeGroup = QTreeWidgetItem(self.classSkillTree, ["Умения"])
        for i in self.character.stats.get("skills"):
            QTreeWidgetItem(self.classSkillTreeGroup, [i])
        self.classSkillTree.expandAll()

    def on_wv_changed(self, wv):
        self.character.stats["worldview"] = wv

    def on_race_changed(self, race):
        self.character.setRace(race)
        self.raceParamsTree.clear()
        self.raceParamsTreeGroup = QTreeWidgetItem(
            self.raceParamsTree, [self.raceChoose.currentText(), ""]
        )
        QTreeWidgetItem(
            self.raceParamsTreeGroup, ["Скорость", self.character.stats.get("speed")]
        )
        addict = QTreeWidgetItem(self.raceParamsTreeGroup, ["Характеристики +", ""])
        for key, val in (
            self.character.stats.get("diceStats", {}).get("addiction", {}).items()
        ):
            QTreeWidgetItem(addict, [key, str(val)])
        self.raceParamsTree.expandAll()

    def on_bg_changed(self, bg):
        self.character.stats["background"] = bg

    def classComboAdder(self):
        for i in ClassInfoHandler().getClassInfo("class_name"):
            self.classChoose.addItem(i)

    def racesComboAdder(self):
        for i in RaceInfoHandler().getRaceInfo("race_name"):
            self.raceChoose.addItem(i)

    def backgroundsComboAdder(self):
        for i in BackgroundHandler().getBackgrounds():
            self.bgChoose.addItem(i)

    def alignmentsComboAdder(self):
        for i in AlignmentHandler().getAlignments():
            self.wvChoose.addItem(i)
