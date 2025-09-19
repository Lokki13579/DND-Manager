# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PlayerListswZkBn.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from server_client import ServerClass, Client
from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QFrame, QGroupBox, QSizePolicy,
    QTabWidget, QWidget, QVBoxLayout, QLabel)
from UI.PlayerCard import Ui_PlayerCard


class Ui_PlayerList(QWidget):
    def __init__(self, servobj):
        super().__init__()
        self.ServerObj : ServerClass = servobj
        self.playersTab = {}
        ServerClass().player_connected.connect(self.playerConnected)
        ServerClass().player_updated.connect(self.playerDataUpdated)
        
        self.setupUi()
    
    def playerDataUpdated(self,player):
        for pl in self.playersTab.values():
            pl.updateData(player.character)

    def playerConnected(self, player):
        player_card = Ui_PlayerCard(player.character)
        self.tabWidget.addTab(player_card, player.character.name)
        self.playersTab[player] = player_card

    def setupUi(self):
        self.resize(720, 540)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)