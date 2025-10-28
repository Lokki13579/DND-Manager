from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QTreeWidget,
    QTreeWidgetItem,
)

from OtherPyFiles.characterclass import classData, racesData, jsonLoad


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
        self.comboAdder(self.classChoose, "JSONS/dnd_classes.json")
        self.classChoose.currentTextChanged.connect(self.on_class_changed)
        self.classLayout.addWidget(self.classChoose, 3)

        self.classSkillTree = QTreeWidget()
        self.classSkillTree.setStyleSheet("font-size: 18pt;")
        self.classSkillTree.setHeaderLabel("Особенности класса")
        self.classSkillTreeGroup = QTreeWidgetItem(self.classSkillTree, ["Умения"])
        self.skills = {}
        self.on_class_changed(self.classChoose.currentText())
        self.classLayout.addWidget(self.classSkillTree, 12)

        self.bgChoose = QComboBox()
        self.comboAdder(self.bgChoose, "JSONS/dnd_backgrounds.json")
        self.bgChoose.currentTextChanged.connect(self.on_bg_changed)
        self.classLayout.addWidget(self.bgChoose, 2)

        self.mainLayout.addLayout(self.classLayout)

        self.raceLayout = QVBoxLayout()

        self.raceTitle = QLabel(text="Выберите расу вашего персонажа")
        self.raceLayout.addWidget(self.raceTitle, 2)

        self.raceChoose = QComboBox()
        self.comboAdder(self.raceChoose, "JSONS/dnd_races.json")
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
        self.comboAdder(self.wvChoose, "JSONS/dnd_alingments.json")
        self.wvChoose.currentTextChanged.connect(self.on_wv_changed)
        self.raceLayout.addWidget(self.wvChoose, 2)

        self.mainLayout.addLayout(self.raceLayout)

    def on_class_changed(self, _class):
        self.character.setClass(_class)
        self.classSkillTree.clear()
        self.classSkillTreeGroup = QTreeWidgetItem(self.classSkillTree, ["Умения"])
        self.skillAdder(self.classSkillTreeGroup, classData, self.skills)
        self.classSkillTree.expandAll()

    def on_wv_changed(self, wv):
        self.character.Stats["worldview"] = wv

    def on_race_changed(self, race):
        self.character.setRace(race)
        self.raceParamsTree.clear()
        self.raceParamsTreeGroup = QTreeWidgetItem(
            self.raceParamsTree, [self.raceChoose.currentText()]
        )
        self.raceDataAdder(self.raceParamsTreeGroup, racesData, self.raceData)
        self.raceParamsTree.expandAll()

    def on_bg_changed(self, bg):
        self.character.Stats["background"] = bg

    def comboAdder(self, obj: QComboBox, path: str | dict):
        if type(path) == type(""):
            _info = jsonLoad(path)
        else:
            _info = path
        for _name in _info:
            obj.addItem(_name)

    def skillAdder(self, obj: QTreeWidgetItem, path: str | dict, _dict):
        if type(path) == type(""):
            _info = jsonLoad(path)
        else:
            _info = path
        self.skills = self.recursiveAddTreeItems(
            obj, self.character.Stats.get("skills")
        )

    def raceDataAdder(self, obj: QTreeWidgetItem, path, _dict):
        if type(path) == type(""):
            _info = jsonLoad(path)
        else:
            _info = path
        self.raceData = self.recursiveAddTreeItems(
            obj, _info.get(self.character.Stats.get("race"))
        )

    def recursiveAddTreeItems(
        self, parent: QTreeWidgetItem, value: str | int | dict | list, _dict={}
    ):
        if type(value) == type(1):
            value = str(value)
        if type(value) == type(list()):
            for _val in value:
                _dict[_val] = QTreeWidgetItem(parent, [_val])
        if type(value) == type(dict()):
            for _key, _val in value.items():
                _dict[_key] = QTreeWidgetItem(parent, [_key])
                _dict[_key].setHidden(False)
                _dict[_key + "_"] = self.recursiveAddTreeItems(_dict[_key], _val, _dict)
        if type(value) == type(str()):
            _dict[value] = QTreeWidgetItem(parent, [value])
        return _dict
