from PyQt6.QtWidgets import QGroupBox, QGridLayout
from PyQt6.QtCore import pyqtSignal
from OtherPyFiles.characterclass import statusesGet
from UI.playerCard.statusObj import StatusObj


class StatusContainer(QGroupBox):
    sbmChanged = pyqtSignal(object)

    def __init__(self, character=object):
        super().__init__()
        self.character = character
        self.statusObjects = {}
        self.setupUi()

    def setNewCharacter(self, char):
        self.character = char
        self.tryToApplyChar()
        self.statusShow()

    def statusShow(self):
        for i, obj in enumerate(self.statusObjects.values()):
            obj.setChecked(self.character.status.get(obj.name, False))
            self.mainLayout.addWidget(obj, i % 8, i // 8)

    def setupUi(self):
        self.setTitle("Эффекты")
        self.mainLayout = QGridLayout(self)
        self.statusInit()

    def statusInit(self):
        for _name in statusesGet("JSONS/dnd_statuses.json"):
            print(_name)
            self.statusObjects[_name] = StatusObj(_name)
        self.tryToApplyChar()

    def tryToApplyChar(self):
        try:
            for obj in self.statusObjects.values():
                obj.stateChanged.connect(self.statUpdate)
        except Exception as e:
            print(e)

    def statUpdate(self, data):
        self.character.setState(*data)
        self.sbmChanged.emit(None)
