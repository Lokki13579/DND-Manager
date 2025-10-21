#!/home/artem/python/bin/python

import sys
from server_client import *
from PyQt6.QtWidgets import (QApplication, QMainWindow, QStackedWidget,QWidget)

from UI.MainMenu import Ui_MainMenu
from UI.ui_Create import Ui_CreateLobby
from UI.ui_Join import Ui_JoinToServer
from UI.CharactersList import Ui_CharsList
from UI.ui_PlayerList import Ui_PlayerList
from UI.ClientLobby import Ui_Lobby
from UI.CreateChar import Ui_MainList as Ui_CreateChar
ServerOBJ = ServerClass()
ClientOBJ = Client()
class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
    
        self.MenusNumbers = {
                "Main": 0,
                "CreateLobby": 1,
                "JoinMenu":2,
                "ClientLobby":3,
                "CharList":4,
                "CharCreate":5,
                "PlayerList":6,


                }
        
        self.setWindowTitle("DND Manager")
        self.setGeometry(100,100,720,540)
        self.setStyleSheet("font-family: '3270 Nerd Font'; font-size: 24px;")

        self.stackedW = QStackedWidget()

        self.setCentralWidget(self.stackedW)
        self.MainMenu = Ui_MainMenu()

        self.MainMenu.CreateButton.clicked.connect(self.showCreateMenu)
        self.MainMenu.JoinButton.clicked.connect(self.showJoinMenu)
        self.MainMenu.CharListButton.clicked.connect(self.showCharListMenu)
        self.MainMenu.QuitButton.clicked.connect(lambda: quit())
        self.stackedW.addWidget(self.MainMenu)
        
        self.CreateMenu = Ui_CreateLobby()
        self.CreateMenu.HostButton.clicked.connect(lambda host: self.startServer(int(self.CreateMenu.PortEnter.text())))
        self.CreateMenu.BackButton.clicked.connect(self.showMainMenu)
        self.stackedW.addWidget(self.CreateMenu)

        self.JoinMenu = Ui_JoinToServer()
        self.JoinMenu.ConnectButton.clicked.connect(lambda connect: self.connectToServer(self.JoinMenu.AddressEnter.text(), int(self.JoinMenu.PortEnter.text())))
        self.JoinMenu.BackButton.clicked.connect(self.showMainMenu)
        self.stackedW.addWidget(self.JoinMenu)

        self.ClientLobby = Ui_Lobby(ClientOBJ)
        self.stackedW.addWidget(self.ClientLobby)

        self.CharacterListMenu = Ui_CharsList(ClientOBJ)
        self.CharacterListMenu.CreateNewCharButton.clicked.connect(self.showCharCreateMenu)
        self.CharacterListMenu.BackButton.clicked.connect(self.showMainMenu)
        self.stackedW.addWidget(self.CharacterListMenu)
        
        self.CharCreateMenu = Ui_CreateChar()
        self.CharCreateMenu.BackButton.clicked.connect(self.showCharListMenu)
        self.stackedW.addWidget(self.CharCreateMenu)

        self.PlayerListMenu = Ui_PlayerList(ServerOBJ)
        self.stackedW.addWidget(self.PlayerListMenu)
        


        self.stackedW.setCurrentIndex(0)
        
    def showMainMenu(self):
        self.stackedW.setCurrentIndex(self.MenusNumbers.get("Main",0))
    def showCreateMenu(self):
        self.stackedW.setCurrentIndex(self.MenusNumbers.get("CreateLobby",0))
    def showJoinMenu(self):
        self.stackedW.setCurrentIndex(self.MenusNumbers.get("JoinMenu",0))
    def showCharListMenu(self):
        self.stackedW.setCurrentIndex(self.MenusNumbers.get("CharList",0))
    def showPlayerListMenu(self):
        self.stackedW.setCurrentIndex(self.MenusNumbers.get("PlayerList",0))
    def showClientLobby(self):
        self.stackedW.setCurrentIndex(self.MenusNumbers.get("ClientLobby",0))
    def showCharCreateMenu(self):
        self.stackedW.setCurrentIndex(self.MenusNumbers.get("CharCreate",0))
    def startServer(self,_port):
        ServerOBJ._startServer(_port)
        self.showPlayerListMenu()
    def connectToServer(self, _ip, _port):
        ClientOBJ._connectToServer(_ip, _port)
        self.showClientLobby()
style = ""
with open("style.css","r",encoding="utf-8") as file:
    style = file.read()
def applicationset(_argv):
    app = QApplication(_argv)
    # app.setStyle("Fusion")
    app.setStyleSheet(style)
    return app

if __name__ == "__main__":
    app = applicationset(sys.argv)
    mainwin = MainWin()
    mainwin.show()
    ex = app.exec()
    if ex == 0: ServerOBJ._closeServer()
    sys.exit(ex)
