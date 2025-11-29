#!/home/artem/python/bin/python

import sys
from typing import final
from OtherPyFiles.server_client import ServerClass, Client
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QStackedLayout

from UI.MainMenu import Ui_MainMenu
from UI.ui_Create import Ui_CreateLobby
from UI.ui_Join import Ui_JoinToServer
from UI.CharactersList import Ui_CharsList
from UI.ui_PlayerList import Ui_PlayerList
from UI.ClientLobby import Ui_Lobby
from UI.CreateChar.CreateChar import Ui_MainList as Ui_CreateChar

ServerOBJ = ServerClass()
ClientOBJ = Client()


@final
class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DND Manager")
        self.setGeometry(100, 100, 720, 540)

        self.setStyleSheet("""
                           font-family: '3270 Nerd Font';
                           font-size: 24px;
                           """)

        self.stackedW = QStackedWidget()

        self.setCentralWidget(self.stackedW)
        self.MainMenu = Ui_MainMenu()

        self.MainMenu.CreateButton.clicked.connect(self.showCreateMenu)
        self.MainMenu.JoinButton.clicked.connect(self.showJoinMenu)
        self.MainMenu.CharListButton.clicked.connect(self.showCharListMenu)
        self.MainMenu.QuitButton.clicked.connect(lambda: quit())
        self.stackedW.addWidget(self.MainMenu)

        self.stackedW.setCurrentIndex(0)

    def showMainMenu(self):
        print(self.stackedW.children())
        for i in self.stackedW.children():
            if i == self.MainMenu or type(i) is QStackedLayout:
                continue
            self.stackedW.removeWidget(i)
            i.deleteLater()
        self.stackedW.setCurrentWidget(self.MainMenu)

    def showCreateMenu(self):
        self.initCreateMenu()
        self.stackedW.setCurrentWidget(self.CreateMenu)

    def showJoinMenu(self):
        self.initJoinMenu()
        self.stackedW.setCurrentWidget(self.JoinMenu)

    def showCharListMenu(self):
        self.initCharacterList()
        self.CharacterListMenu.characterFind()
        self.stackedW.setCurrentWidget(self.CharacterListMenu)

    def showPlayerListMenu(self):
        self.initPlayerListMenu()
        self.stackedW.setCurrentWidget(self.PlayerListMenu)

    def showClientLobby(self):
        self.initClientLobby()
        self.stackedW.setCurrentWidget(self.ClientLobby)
        self.ClientLobby.CharSelect.characterFind()

    def showCharCreateMenu(self):
        self.initCharCreateMenu()
        self.stackedW.setCurrentWidget(self.CharCreateMenu)

    def initCreateMenu(self):
        self.CreateMenu = Ui_CreateLobby()
        self.CreateMenu.BackButton.clicked.connect(self.showMainMenu)
        self.stackedW.addWidget(self.CreateMenu)

    def initJoinMenu(self):
        self.JoinMenu = Ui_JoinToServer()
        self.JoinMenu.BackButton.clicked.connect(self.showMainMenu)
        self.stackedW.addWidget(self.JoinMenu)

    def initClientLobby(self):
        self.ClientLobby = Ui_Lobby(ClientOBJ)
        self.stackedW.addWidget(self.ClientLobby)

    def initCharacterList(self):
        self.CharacterListMenu = Ui_CharsList(ClientOBJ)
        self.CharacterListMenu.createNewButton.clicked.connect(self.showCharCreateMenu)
        self.CharacterListMenu.BackButton.clicked.connect(self.showMainMenu)
        self.stackedW.addWidget(self.CharacterListMenu)

    def initCharCreateMenu(self):
        self.CharCreateMenu = Ui_CreateChar()
        self.CharCreateMenu.BackButton.clicked.connect(self.showCharListMenu)
        self.stackedW.addWidget(self.CharCreateMenu)

    def initPlayerListMenu(self):
        self.PlayerListMenu = Ui_PlayerList(ClientOBJ)
        self.stackedW.addWidget(self.PlayerListMenu)

    def startServer(self, _port):
        if ServerOBJ.startServer(_port):
            self.showPlayerListMenu()

    def connectToServer(self, _ip, _port):
        if ClientOBJ.connectToServer(port=_port):
            self.showClientLobby()


style = ""
with open("style.css", "r", encoding="utf-8") as file:
    style = file.read()


def applicationset(_argv):
    app = QApplication(_argv)
    # app.setStyle("Fusion")
    app.setStyleSheet(style)
    return app


if __name__ == "__main__":
    try:
        app = applicationset(sys.argv)
        mainwin = MainWin()
        mainwin.show()
        ex = app.exec()
    except KeyboardInterrupt:
        ServerOBJ.closeServer()
        ClientOBJ.disconnectFromServer()
        sys.exit(0)
