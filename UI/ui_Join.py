# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'JoinaHELIM.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt6.QtCore import (
    QCoreApplication,
    QSize,
    Qt,
)
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Ui_JoinToServer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.vertLayout = QVBoxLayout(self)

        self.Title = QLabel("Присоединиться к серверу")
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vertLayout.addWidget(self.Title)

        self.IPAddressLayout = QHBoxLayout()

        self.AddressName = QLabel("IP-адрес:")

        self.IPAddressLayout.addWidget(self.AddressName, 3)

        self.AddressEnter = QLineEdit()

        self.IPAddressLayout.addWidget(self.AddressEnter, 2)

        self.vertLayout.addLayout(self.IPAddressLayout)

        self.PortLayout = QHBoxLayout()
        self.PortName = QLabel("Порт:")

        self.PortLayout.addWidget(self.PortName, 3)

        self.PortEnter = QLineEdit()
        self.PortEnter.textChanged.connect(self.portControl)

        self.PortLayout.addWidget(self.PortEnter, 2)

        self.vertLayout.addLayout(self.PortLayout)

        self.ButtonsLayout = QHBoxLayout()
        self.ButtonsLayout.setObjectName("ButtonsLayout")
        self.BackButton = QPushButton("Назад")
        self.BackButton.setObjectName("BackButton")

        self.ButtonsLayout.addWidget(self.BackButton)

        self.ConnectButton = QPushButton("Подключиться")
        self.ConnectButton.setObjectName("ConnectButton")

        self.ButtonsLayout.addWidget(self.ConnectButton)

        self.vertLayout.addLayout(self.ButtonsLayout)

    # setupUi
    def portControl(self):
        if not self.PortEnter.text():
            return
        if self.PortEnter.text()[-1] not in "0123456789":
            self.PortEnter.setText(self.PortEnter.text()[:-1])
            return
        if int(self.PortEnter.text()) > 2**16 - 1:
            self.PortEnter.setText(str(2**16 - 1))
        if int(self.PortEnter.text()) < 0:
            self.PortEnter.setText(str(0))
