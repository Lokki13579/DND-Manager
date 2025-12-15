from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QGroupBox
from OtherPyFiles.dataBaseHandler import StatusesHandler


class Status(QPushButton):
    def __init__(self, status, isChecked=False):
        super().__init__(status)
        self.setCheckable(True)
        self.setChecked(isChecked)
        self.status = status


class StatusContainer(QGroupBox):
    needToSend = pyqtSignal(object)

    def __init__(self, character):
        super().__init__()
        self.character = character
        self.states = {}
        self.statuses = {}
        self.stateInit()
        self.setupUi()

    def stateInit(self):
        for status in StatusesHandler().getStatuses():
            self.states[status] = False

    def createStatusButtons(self):
        for i in self.statuses.values():
            self.mainLayout.removeWidget(i)
            i.deleteLater()
        self.statuses.clear()
        for status in StatusesHandler().getStatuses():
            self.statuses[status] = Status(status, self.states[status])
            self.statuses[status].clicked.connect(self.statusClicked)
        for status in self.statuses:
            self.mainLayout.addWidget(
                self.statuses[status],
                list(self.statuses.keys()).index(status) % 5,
                list(self.statuses.keys()).index(status) // 5,
            )

    def statusClicked(self):
        self.character.setState(self.sender().status, self.sender().isChecked())
        self.needToSend.emit(f"newStatus&{self.character.status}")

    def setupUi(self):
        self.setTitle("Эффекты")
        self.mainLayout = QGridLayout(self)
        self.createStatusButtons()

    def characterUpdate(self, character):
        self.character = character
        self.states = character.status
        self.createStatusButtons()
