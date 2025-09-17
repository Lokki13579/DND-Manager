

from PyQt6.QtCore import QCoreApplication, QMetaObject, QRect
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

class Ui_MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200,360)
        self.setGeometry(QRect(0,0,200,360))
        self.Buttons = QVBoxLayout(self)
        self.Buttons.setGeometry(QRect(0,0,200,360))
        self.Buttons.setObjectName("AllButtons")
        
        self.CreateButton = QPushButton("Создать")

        self.JoinButton = QPushButton("Подключиться")
        
        self.CharListButton = QPushButton("Список Персонажей")
        
        self.QuitButton = QPushButton("Выйти")



        self.Buttons.addWidget(self.CreateButton)
        self.Buttons.addWidget(self.JoinButton)
        self.Buttons.addWidget(self.CharListButton)
        self.Buttons.addWidget(self.QuitButton)
        