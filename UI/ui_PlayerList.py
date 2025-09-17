# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PlayerListswZkBn.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QFrame, QGroupBox, QSizePolicy,
    QTabWidget, QWidget)


class Ui_PlayerList(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
    def setupUi(self):
        
        self.resize(640, 480)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 30, 620, 420))
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab,"MainChars")

        self.retranslateUi()

        self.tabWidget.setCurrentIndex(0)


    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Frame", u"Main Chars", None))
    # retranslateUi

