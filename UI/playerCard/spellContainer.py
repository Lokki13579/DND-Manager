from PyQt6.QtWidgets import QGroupBox, QVBoxLayout


class spellGroup(QGroupBox):
    def __init__(self, character):
        super().__init__()
        self.character = character

        self.setupUi()

    def setupUi(self):
        self.setTitle("Заклинания")
        self.mainLayout = QVBoxLayout(self)
