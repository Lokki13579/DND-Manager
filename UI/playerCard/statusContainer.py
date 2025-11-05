from PyQt6.QtWidgets import QApplication, QGroupBox, QGridLayout, QMainWindow
import sys
from OtherPyFiles.characterclass import statusesGet
from UI.playerCard.statusObj import StatusObj


class StatusContainer(QGroupBox):
    def __init__(self, character=object):
        super().__init__()
        self.character = character
        self.statusObjects = {}
        self.setupUi()

    def setNewCharacter(self, char):
        self.character = char

    def setupUi(self):
        self.mainLayout = QGridLayout(self)
        self.statusInit()

    def statusInit(self):
        for _name in statusesGet("../../JSONS/dnd_statuses.json"):
            self.statusObjects[_name] = StatusObj(_name)
            try:
                self.statusObjects.get(_name).stateChanged.connect(
                    self.character.setState
                )
            except:
                pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow(app)
    window.setCentralWidget(StatusContainer())
    window.show()

    sys.exit(app.exec())
