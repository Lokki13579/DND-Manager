#!/home/artem/python/bin/python

import sys
from typing import final
from OtherPyFiles.server_client import ServerClass, Client
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

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

        self.CreateMenu = Ui_CreateLobby()
        self.CreateMenu.HostButton.clicked.connect(
            lambda: self.startServer(int(self.CreateMenu.PortEnter.text()))
        )
        self.CreateMenu.BackButton.clicked.connect(self.showMainMenu)
        self.stackedW.addWidget(self.CreateMenu)

        self.JoinMenu = Ui_JoinToServer()
        self.JoinMenu.ConnectButton.clicked.connect(
            lambda: self.connectToServer(
                self.JoinMenu.AddressEnter.text(), int(self.JoinMenu.PortEnter.text())
            )
        )
        self.JoinMenu.BackButton.clicked.connect(self.showMainMenu)
        self.stackedW.addWidget(self.JoinMenu)

        self.ClientLobby = Ui_Lobby(ClientOBJ)
        self.stackedW.addWidget(self.ClientLobby)

        self.CharacterListMenu = Ui_CharsList(ClientOBJ)
        self.CharacterListMenu.createNewButton.clicked.connect(self.showCharCreateMenu)
        self.CharacterListMenu.BackButton.clicked.connect(self.showMainMenu)
        self.stackedW.addWidget(self.CharacterListMenu)

        self.CharCreateMenu = Ui_CreateChar()
        self.CharCreateMenu.BackButton.clicked.connect(self.showCharListMenu)
        self.stackedW.addWidget(self.CharCreateMenu)

        self.PlayerListMenu = Ui_PlayerList(ServerOBJ)
        self.stackedW.addWidget(self.PlayerListMenu)

        self.stackedW.setCurrentIndex(0)

    def showMainMenu(self):
        self.stackedW.setCurrentWidget(self.MainMenu)

    def showCreateMenu(self):
        self.stackedW.setCurrentWidget(self.CreateMenu)

    def showJoinMenu(self):
        self.stackedW.setCurrentWidget(self.JoinMenu)

    def showCharListMenu(self):
        self.CharacterListMenu.characterFind()
        self.stackedW.setCurrentWidget(self.CharacterListMenu)

    def showPlayerListMenu(self):
        self.stackedW.setCurrentWidget(self.PlayerListMenu)

    def showClientLobby(self):
        self.stackedW.setCurrentWidget(self.ClientLobby)
        self.ClientLobby.CharSelect.characterFind()

    def showCharCreateMenu(self):
        self.stackedW.removeWidget(self.CharCreateMenu)
        self.CharCreateMenu = Ui_CreateChar()
        self.CharCreateMenu.BackButton.clicked.connect(self.showCharListMenu)
        self.stackedW.addWidget(self.CharCreateMenu)
        self.stackedW.setCurrentWidget(self.CharCreateMenu)

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
    app = applicationset(sys.argv)
    mainwin = MainWin()
    mainwin.show()
    ex = app.exec()
    if ex == 0:
        ServerOBJ.closeServer()
        ClientOBJ.disconnectFromServer()
    sys.exit(ex)
