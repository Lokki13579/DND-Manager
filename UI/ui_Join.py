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
    QGroupBox,
)


class Ui_JoinToServer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.title = QLabel("Подключение к серверу")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.title, 1, Qt.AlignmentFlag.AlignTop)

        self.hostGroup = QGroupBox("Адрес сервера")
        self.hostLayout = QHBoxLayout(self.hostGroup)
        self.hostEnter = QLineEdit()
        self.hostEnter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hostEnter.setPlaceholderText("xxx.xxx.xxx.xxx")
        self.hostLayout.addWidget(self.hostEnter, 1, Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.hostGroup, 3)

        self.portGroup = QGroupBox("Порт")
        self.portLayout = QHBoxLayout(self.portGroup)
        self.portEnter = QLineEdit()
        self.portEnter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.portEnter.setPlaceholderText("4242")
        self.portLayout.addWidget(self.portEnter, 1, Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.portGroup, 3)

        self.buttonWidget = QWidget()
        self.buttonLayout = QHBoxLayout(self.buttonWidget)
        self.mainLayout.addWidget(self.buttonWidget, 2, Qt.AlignmentFlag.AlignBottom)

        self.backButton = QPushButton("Назад")
        self.buttonLayout.addWidget(self.backButton)

        self.connectButton = QPushButton("Подключиться")
        self.buttonLayout.addWidget(self.connectButton)

    def getHost(self):
        try:
            return self.hostEnter.text()
        except ValueError:
            return "localhost"

    def getPort(self):
        try:
            return int(self.portEnter.text())
        except ValueError:
            return 4242

    # setupUi
    def portControl(self):
        if not self.portEnter.text():
            return
        if self.portEnter.text()[-1] not in "0123456789":
            self.portEnter.setText(self.portEnter.text()[:-1])
            return
        if int(self.portEnter.text()) > 2**16 - 1:
            self.portEnter.setText(str(2**16 - 1))
        if int(self.portEnter.text()) < 0:
            self.portEnter.setText(str(0))
