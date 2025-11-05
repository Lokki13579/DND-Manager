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
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_JoinToServer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.vertLayout = QVBoxLayout(self)
        self.resize(720, 540)

        self.Title = QLabel()
        self.Title.setObjectName("Title")
        self.Title.setMaximumSize(QSize(16777215, 40))
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vertLayout.addWidget(self.Title)

        self.IPAddressLayout = QHBoxLayout()
        self.IPAddressLayout.setObjectName("IPAddressLayout")

        self.AddressName = QLabel()
        self.AddressName.setObjectName("AddressName")
        self.AddressName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.IPAddressLayout.addWidget(self.AddressName)

        self.AddressEnter = QLineEdit()
        self.AddressEnter.setObjectName("AddressEnter")
        self.AddressEnter.setMinimumSize(QSize(0, 30))
        self.AddressEnter.setMaximumSize(QSize(350, 30))
        self.AddressEnter.setFrame(True)
        self.AddressEnter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.IPAddressLayout.addWidget(self.AddressEnter)

        self.vertLayout.addLayout(self.IPAddressLayout)

        self.PortLayout = QHBoxLayout()
        self.PortLayout.setObjectName("PortLayout")
        self.PortName = QLabel()
        self.PortName.setObjectName("PortName")
        self.PortName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.PortLayout.addWidget(self.PortName)

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
        self.BackButton.setObjectName("BackButton")

        self.ButtonsLayout.addWidget(self.BackButton)

        self.ConnectButton = QPushButton()
        self.ConnectButton.setObjectName("ConnectButton")

        self.ButtonsLayout.addWidget(self.ConnectButton)

        self.vertLayout.addLayout(self.ButtonsLayout)

        self.retranslateUi(self)

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

    def retranslateUi(self, JoinToServer):
        JoinToServer.setWindowTitle(
            QCoreApplication.translate("JoinToServer", "Form", None)
        )
        self.Title.setText(
            QCoreApplication.translate(
                "JoinToServer",
                "\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u043a \u0441\u0435\u0440\u0432\u0435\u0440\u0443",
                None,
            )
        )
        self.AddressName.setText(
            QCoreApplication.translate(
                "JoinToServer",
                ">--- \u0410\u0434\u0440\u0435\u0441 \u0421\u0435\u0440\u0432\u0435\u0440\u0430 ===>",
                None,
            )
        )
        self.AddressEnter.setText(
            QCoreApplication.translate("JoinToServer", "100.78.201.38", None)
        )
        self.AddressEnter.setPlaceholderText(
            QCoreApplication.translate("JoinToServer", "server address", None)
        )
        self.PortName.setText(
            QCoreApplication.translate(
                "JoinToServer",
                ">--- \u041f\u043e\u0440\u0442 \u0421\u0435\u0440\u0432\u0435\u0440\u0430 ===>",
                None,
            )
        )
        self.PortEnter.setText(QCoreApplication.translate("JoinToServer", "4242", None))
        self.PortEnter.setPlaceholderText(
            QCoreApplication.translate("JoinToServer", "server port", None)
        )
        self.Alert.setText(
            QCoreApplication.translate(
                "JoinToServer",
                "\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0430\u0435\u0448\u044c \u043a \u0441\u0435\u0440\u0432\u0435\u0440\u0443? \n \u0417\u0430\u0447\u0438\u0442 \u0442\u044b \u043f\u0440\u0438\u043a\u043b\u044e\u0447\u0435\u043d\u0435\u0446. \n \u0423\u0434\u0430\u0447\u043d\u043e\u0433\u043e \u043f\u0443\u0442\u0438",
                None,
            )
        )
        self.BackButton.setText(
            QCoreApplication.translate(
                "JoinToServer", "\u041d\u0430\u0437\u0430\u0434", None
            )
        )
        self.ConnectButton.setText(
            QCoreApplication.translate(
                "JoinToServer", "\u0417\u0430\u0439\u0442\u0438", None
            )
        )

    # retranslateUi
