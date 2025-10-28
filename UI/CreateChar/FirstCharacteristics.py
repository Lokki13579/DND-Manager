from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QHBoxLayout,
    QGroupBox,
)

from OtherPyFiles.characterclass import jsonLoad


class FirstCharacteristics(QWidget):
    def __init__(self, _character):
        super().__init__()
        self.character = _character
        self.setupUi()

    def setupUi(self):
        self.verticalLayout = QVBoxLayout(self)

        self.Trash = QLabel(
            text="В этом меню можно создать нового персонажа, который будет учавствовать в приключениях, придуманных вашим гейммастером"
        )
        self.Trash.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Trash.setWordWrap(True)
        self.verticalLayout.addWidget(self.Trash, 2)

        self.PlayerNameTitle = QLabel(text="Имя вашего персонажа\n|\n\/")
        self.PlayerNameTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.PlayerNameTitle)

        self.NameInput = QLineEdit()
        self.NameInput.textChanged.connect(self.on_name_changed)
        self.NameInput.setPlaceholderText("Имя")
        self.verticalLayout.addWidget(self.NameInput, 2, Qt.AlignmentFlag.AlignHCenter)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()

        self.LevelBox = QGroupBox(title="Уровень")
        self.levelvbox = QVBoxLayout(self.LevelBox)
        self.levelRange = QLabel(text="Введите уровень от 1 до 20")
        self.levelvbox.addWidget(self.levelRange)
        self.LevelSelectBox = QSpinBox()
        self.levelvbox.addWidget(self.LevelSelectBox)
        self.LevelSelectBox.setValue(1)
        self.LevelSelectBox.setMinimum(1)
        self.LevelSelectBox.setMaximum(20)
        self.LevelSelectBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LevelSelectBox.valueChanged.connect(self.on_level_changed)
        self.horizontalLayout.addWidget(self.LevelBox)

        self.expBox = QGroupBox(title="Опыт")
        self.expvbox = QVBoxLayout(self.expBox)
        self.expRange = QLabel()
        self.expvbox.addWidget(self.expRange)
        self.expSelectBox = QSpinBox(self.expBox)
        self.expvbox.addWidget(self.expSelectBox)
        self.expSelectBox.setValue(0)
        self.expSelectBox.setMinimum(0)
        self.expSelectBox.valueChanged.connect(self.on_exp_changed)
        self.horizontalLayout.addWidget(self.expBox)
        self.expMan(self.LevelSelectBox.value())

        self.verticalLayout.addLayout(self.horizontalLayout, 1)

    def on_name_changed(self, text):
        width = self.NameInput.fontMetrics().horizontalAdvance(text) + 20
        self.NameInput.setMinimumWidth(width)
        self.character.setName(text)
        print(self.character.name, self.character.Stats)

    def on_level_changed(self, level):
        self.expMan(level)
        self.character.setLevel(level)
        print(self.character.name, self.character.Stats)

    def on_exp_changed(self, exp):
        self.character.setXp(exp)
        print(self.character.name, self.character.Stats)

    def expMan(self, _level):
        _maxXp = (
            jsonLoad("JSONS/dnd_levels.json")
            .get(str(_level + 1), 1)
            .get("experience", 0)
            - 1
        )
        self.expRange.setText(f"Введите опыт от 0 до {_maxXp}")
        self.expSelectBox.setMaximum(_maxXp)
