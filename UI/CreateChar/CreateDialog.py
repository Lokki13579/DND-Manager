from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt6.QtCore import Qt


class CreateDialog(QDialog):
    def __init__(self, character):
        super().__init__()
        self.character = character
        self.setWindowTitle("Create Character")
        self.setFixedSize(400, 300)
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.Title = QLabel("Create Character")
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.Title)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.mainLayout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
