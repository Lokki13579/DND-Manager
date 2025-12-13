from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout

from OtherPyFiles.characterclass import Character


class LoreCharacteristics(QWidget):
    def __init__(self, character):
        super().__init__()
        self.character: Character = character
        self.lore = """"""
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.textEdit = QTextEdit()
        self.textEdit.textChanged.connect(self.onTextChanged)
        self.mainLayout.addWidget(self.textEdit)

    def onTextChanged(self):
        self.lore = self.textEdit.toPlainText()
        self.character.stats["lore"] = self.lore
