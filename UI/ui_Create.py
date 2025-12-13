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
)


class Ui_CreateLobby(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.vertLayout = QVBoxLayout(self)
        self.resize(720, 540)

        self.Title = QLabel(self)
        self.Title.setObjectName("Title")
        self.Title.setMaximumSize(QSize(16777215, 40))
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vertLayout.addWidget(self.Title)

        self.PortLayout = QHBoxLayout(self)
        self.PortLayout.setObjectName("PortLayout")
        self.portName = QLabel()
        self.portName.setObjectName("portName")
        self.portName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.PortLayout.addWidget(self.portName)

        self.PortEnter = QLineEdit()
        self.PortEnter.setObjectName("PortEnter")
        self.PortEnter.setMinimumSize(QSize(0, 30))
        self.PortEnter.setMaximumSize(QSize(350, 30))
        self.PortEnter.setReadOnly(False)
        self.PortEnter.textChanged.connect(self.portControl)
        self.PortEnter.setFrame(True)
        self.PortEnter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.PortLayout.addWidget(self.PortEnter)

        self.vertLayout.addLayout(self.PortLayout)

        # self.AlertLayout = QWidget(self)
        # self.AlertLayout.setObjectName(u"AlertLayout")
        # self.AlertLayout.setMaximumSize(QSize(600, 70))
        # self.horizontalLayout_3 = QHBoxLayout(self.AlertLayout)
        # self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Alert = QLabel(self)
        self.Alert.setObjectName("Alert")
        self.Alert.setMaximumSize(QSize(16777215, 16777215))
        self.Alert.setStyleSheet("color: rgb(255, 39, 97);")
        self.Alert.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Alert.setWordWrap(True)
        self.Alert.setMargin(0)

        self.vertLayout.addWidget(self.Alert)

        self.ButtonsLayout = QHBoxLayout()
        self.ButtonsLayout.setObjectName("ButtonsLayout")
        self.BackButton = QPushButton()
        self.BackButton.setObjectName("BackButto")

        self.ButtonsLayout.addWidget(self.BackButton)

        self.HostButton = QPushButton()
        self.HostButton.setObjectName("HostButton")

        self.ButtonsLayout.addWidget(self.HostButton)

        self.vertLayout.addLayout(self.ButtonsLayout)

        self.retranslateUi(self)

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

    # setupUi

    def retranslateUi(self, CreateLobby):
        CreateLobby.setWindowTitle(
            QCoreApplication.translate("CreateLobby", "CreateLobby", None)
        )
        self.Title.setText(
            QCoreApplication.translate(
                "CreateLobby",
                "\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u0441\u0435\u0440\u0432\u0435\u0440\u0430",
                None,
            )
        )
        self.portName.setText(
            QCoreApplication.translate(
                "CreateLobby",
                ">--- \u041f\u043e\u0440\u0442 \u0421\u0435\u0440\u0432\u0435\u0440\u0430 ===>",
                None,
            )
        )
        self.PortEnter.setText(QCoreApplication.translate("CreateLobby", "4242", None))
        self.PortEnter.setPlaceholderText(
            QCoreApplication.translate("CreateLobby", "server port", None)
        )
        self.Alert.setText(
            QCoreApplication.translate(
                "CreateLobby",
                "\u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u044c \u043c\u043e\u0436\u0435\u0442 \u0442\u043e\u043b\u044c\u043a\u043e \u0413\u0435\u0439\u043c \u041c\u0430\u0441\u0442\u0435\u0440, \n \u0435\u0441\u043b\u0438 \u0442\u044b \u043a \u043d\u0438\u043c \u043e\u0442\u043d\u043e\u0441\u0438\u0448\u044c\u0441\u044f, \n \u0442\u043e \u0441\u043e\u0437\u0434\u0430\u0432\u0430\u0439 \u0441\u0435\u0440\u0432\u0435\u0440",
                None,
            )
        )
        self.BackButton.setText(
            QCoreApplication.translate(
                "CreateLobby", "\u041d\u0430\u0437\u0430\u0434", None
            )
        )
        self.HostButton.setText(
            QCoreApplication.translate(
                "CreateLobby", "\u0421\u043e\u0437\u0434\u0430\u0442\u044c", None
            )
        )

    # retranslateUi
