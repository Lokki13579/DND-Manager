# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CreateolpSLq.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt6.QtCore import QCoreApplication, QSize, Qt

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGroupBox,
)


class Ui_CreateLobby(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)

        self.title = QLabel(self, text="Создание лобби")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(
            self.title, stretch=1, alignment=Qt.AlignmentFlag.AlignTop
        )

        self.portGroup = QGroupBox("Порт")
        self.mainLayout.addWidget(self.portGroup, stretch=4)

        self.portLayout = QVBoxLayout(self.portGroup)
        self.portEnter = QLineEdit(self)
        self.portEnter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.portEnter.setPlaceholderText("4242")
        self.portEnter.textChanged.connect(self.portControl)
        self.portLayout.addWidget(self.portEnter, 2, Qt.AlignmentFlag.AlignCenter)

        self.buttonWidget = QWidget(self)
        self.mainLayout.addWidget(self.buttonWidget, 4, Qt.AlignmentFlag.AlignBottom)
        self.buttonLayout = QHBoxLayout(self.buttonWidget)

        self.backButton = QPushButton(self, text="Назад")
        self.buttonLayout.addWidget(self.backButton)

        self.hostButton = QPushButton(self, text="Создать")
        self.buttonLayout.addWidget(self.hostButton)

    def getPort(self):
        try:
            return int(self.portEnter.text())
        except ValueError:
            return 4242

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
