import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget,QWidget)

from UI.MainMenu import Ui_MainMenu
from UI.ui_Create import Ui_CreateLobby
from UI.ui_Join import Ui_JoinToServer
from UI.ui_PlayerList import Ui_PlayerList


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DND Manager")
        self.setGeometry(100,100,640,480)

        self.stackedW = QStackedWidget()

        self.setCentralWidget(self.stackedW)
        self.MainMenu = Ui_MainMenu()

        self.MainMenu.CreateButton.clicked.connect(self.showCreateMenu)
        self.MainMenu.JoinButton.clicked.connect(self.showJoinMenu)
        self.MainMenu.CharListButton.clicked.connect(self.showCharListMenu)
        self.MainMenu.QuitButton.clicked.connect(lambda: quit())

        self.CreateMenu = Ui_CreateLobby()
        self.CreateMenu.BackButton.clicked.connect(self.showMainMenu)

        self.JoinMenu = Ui_JoinToServer()
        self.JoinMenu.BackButton.clicked.connect(self.showMainMenu)

        self.PlayerListMenu = Ui_PlayerList()
        


        self.stackedW.addWidget(self.MainMenu)
        self.stackedW.addWidget(self.CreateMenu)
        self.stackedW.addWidget(self.JoinMenu)
        self.stackedW.addWidget(self.PlayerListMenu)
        self.stackedW.setCurrentIndex(0)
        
    def showMainMenu(self):
        self.stackedW.setCurrentIndex(0)
    def showCreateMenu(self):
        self.stackedW.setCurrentIndex(1)
    def showJoinMenu(self):
        self.stackedW.setCurrentIndex(2)
    def showCharListMenu(self):
        self.stackedW.setCurrentIndex(3)
def applicationset(_argv):
    app = QApplication(_argv)
    app.setStyle("Fusion")
    return app

if __name__ == "__main__":
    app = applicationset(sys.argv)
    mainwin = MainWin()
    mainwin.show()
    sys.exit(app.exec())
