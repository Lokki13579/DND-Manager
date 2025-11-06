from PyQt6.QtWidgets import QPushButton

from PyQt6.QtCore import pyqtSignal


class StatusObj(QPushButton):
    stateChanged = pyqtSignal(object)

    def __init__(self, name, st=False):
        super().__init__()
        self.name = name
        self.setText(name)
        self.setCheckable(True)
        self.setChecked(st)
        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        print(self.name)
        self.stateChanged.emit((self.name, self.isChecked()))
