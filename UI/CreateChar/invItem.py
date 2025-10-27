
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class invItem(QFrame):
    def __init__(self,index,name,count = 1):
        super().__init__()
        self.index = index
        self.name = name
        self.count
    def setupUi(self):
        self.setMaximumHeight(48)

        self.mainLayout = QHBoxLayout(self)

        self.indexArea = QLabel()
        self.mainLayout.addWidget(self.indexArea)

        self.nameArea = QLabel()
        self.mainLayout.addWidget()
        

        add_icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.addButton = QPushButton(icon=add_icon)
        self.mainLayout.addWidget(self.addButton)


        reduce_icon = QIcon("")
        self.reduceButton = QPushButton(icon=reduce_icon)
        self.mainLayout.addWidget(self.reduceButton)


