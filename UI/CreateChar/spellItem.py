from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QFrame
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal


class Spell(QWidget):
    deletingSpell = pyqtSignal(str, str)

    def __init__(
        self,
        spell_name,
        spell_level,
        school,
        components,
        casting_time,
        distance,
        duration,
        classes,
        subclasses,
        description,
        active,
    ):
        super().__init__()
        self.spell_name = spell_name
        self.spell_level = spell_level
        self.school = school
        self.components = components
        self.casting_time = casting_time
        self.distance = distance
        self.duration = duration
        self.classes = classes
        self.subclasses = subclasses
        self.description = description

    def delete(self):
        self.deletingSpell.emit(self.name, self.level)


class SpellListItem(QFrame):
    def __init__(self, spell):
        super().__init__()
        self.spell = spell
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QHBoxLayout(self)

        self.nameArea = QLabel()

        delete_icon = QIcon("resources/close_icon.32.png")
        self.deleteButton = QPushButton(icon=delete_icon)

        self.nameArea.setWordWrap(True)
        self.mainLayout.addWidget(self.nameArea, 24)

        self.deleteButton.clicked.connect(self.delete)
        self.mainLayout.addWidget(self.deleteButton, 3)
        self.setTexts()

    def delete(self):
        self.spell.delete()
        super().close()

    def setTexts(self):
        self.nameArea.setText(self.spell.spell_name)
        self.deleteButton.setText("")
