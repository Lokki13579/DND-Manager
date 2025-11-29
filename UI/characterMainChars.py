from PyQt6.QtWidgets import (
    QDialog,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QLabel,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtCore import Qt

from UI.moreInfo import MoreInfoDialog


class CharMainChar(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.info = QVBoxLayout(self)
        self.titleBox = QHBoxLayout()
        self.nameLabel = QLabel()
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nameLabel.setText("Имя персонажа")

        self.levelLabel = QLabel()
        self.levelLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.levelLabel.setText("Уровень")

        self.titleBox.addWidget(self.nameLabel, 12)
        self.titleBox.addWidget(self.levelLabel, 3)
        self.info.addLayout(self.titleBox)

        self.classLabel = QLabel()
        self.classLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.classLabel.setText("Класс")
        self.info.addWidget(self.classLabel)

        self.raceLabel = QLabel()
        self.raceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.raceLabel.setText("Раса")
        self.info.addWidget(self.raceLabel)

        self.dicesLabel = QLabel()
        self.dicesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dicesLabel.setText("Параметры")
        self.info.addWidget(self.dicesLabel)

        self.skillsLabel = QLabel()
        self.skillsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.skillsLabel.setText("Навыки")
        self.info.addWidget(self.skillsLabel)

        self.moreInfoButton = QPushButton("Узнать больше")
        self.moreInfoButton.clicked.connect(self.showMoreInfo)
        self.info.addWidget(self.moreInfoButton)

        self.moreInfo = MoreInfoDialog()

    def showNewCharacter(self, character):
        self.showingCharacter = character
        self.nameLabel.setText(character.name)
        self.classLabel.setText("Класс: " + character.stats.get("class"))
        self.raceLabel.setText("Раса: " + character.stats.get("race"))
        self.levelLabel.setText(str("Уровень: " + str(character.stats.get("level"))))
        dStats = character.stats.get("diceStats")
        # телосложение (значение) (модификатор)
        dstatsToPrint = []
        for key, value in dStats.get("main", {}).get("value", {}).items():
            dstatsToPrint.append(
                f"{key}: {value + dStats.get('addiction', {}).get(key, 0)} - [{dStats.get('main', {}).get('modif', {}).get(key, '+0')}]"
            )
        self.dicesLabel.setText(str("Параметры:\n" + "\n".join(dstatsToPrint)))
        self.skillsLabel.setText(
            str("Умения:\n" + "\n".join(character.stats.get("skills")))
        )
        self.moreInfo = MoreInfoDialog()
        self.moreInfo.setNewCharacter(character)

    def showMoreInfo(self):
        self.moreInfo.show()
