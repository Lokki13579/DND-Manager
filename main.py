import sys
from menus import *
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget,QWidget)

from UI.MainMenu import Ui_MainMenu
from UI.ui_Create import Ui_CreateLobby
from UI.ui_Join import Ui_JoinToServer
from UI.CharactersList import Ui_CharsList
from UI.ui_PlayerList import Ui_PlayerList



class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DND Manager")
        self.setGeometry(100,100,720,540)

        self.stackedW = QStackedWidget()

        self.setCentralWidget(self.stackedW)
        self.MainMenu = Ui_MainMenu()

        self.MainMenu.CreateButton.clicked.connect(self.showCreateMenu)
        self.MainMenu.JoinButton.clicked.connect(self.showJoinMenu)
        self.MainMenu.CharListButton.clicked.connect(self.showCharListMenu)
        self.MainMenu.QuitButton.clicked.connect(lambda: quit())

        self.CreateMenu = Ui_CreateLobby()
        print(self.CreateMenu.PortEnter.text())
        self.CreateMenu.HostButton.clicked.connect(lambda host: self.startServer(int(self.CreateMenu.PortEnter.text())))
        self.CreateMenu.BackButton.clicked.connect(self.showMainMenu)

        self.JoinMenu = Ui_JoinToServer()
        self.JoinMenu.ConnectButton.clicked.connect(lambda connect: self.connectToServer(self.JoinMenu.AddressEnter.text(), int(self.JoinMenu.PortEnter.text())))
        self.JoinMenu.BackButton.clicked.connect(self.showMainMenu)

        self.CharacterListMenu = Ui_CharsList()
        self.CharacterListMenu.BackButton.clicked.connect(self.showMainMenu)
        
        self.PlayerListMenu = Ui_PlayerList(ServerOBJ)
        


        self.stackedW.addWidget(self.MainMenu)
        self.stackedW.addWidget(self.CreateMenu)
        self.stackedW.addWidget(self.JoinMenu)
        self.stackedW.addWidget(self.CharacterListMenu)
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
    def showPlayerListMenu(self):
        self.stackedW.setCurrentIndex(4)
    def startServer(self,_port):
        ServerOBJ._startServer(_port)
        self.showPlayerListMenu()
    def connectToServer(self, _ip, _port):
        print((_ip,_port))
        ClientOBJ._connectToServer(_ip, _port)
        self.showCharListMenu()
def applicationset(_argv):
    app = QApplication(_argv)
    app.setStyle("Fusion")
    return app

if __name__ == "__main__":
    app = applicationset(sys.argv)
    mainwin = MainWin()
    mainwin.show()
    sys.exit(app.exec())
