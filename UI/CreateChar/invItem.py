
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class invItem(QFrame):
    def __init__(self,index,name,count = 1):
        super().__init__()
        self.index = index
        self.name = name
        self.count = count
    def setupUi(self):
        self.setMaximumHeight(48)

        self.mainLayout = QHBoxLayout(self)

        self.indexArea = QLabel()
        self.mainLayout.addWidget(self.indexArea)

        self.nameArea = QLabel()
        self.mainLayout.addWidget()
        

        add_icon = QIcon("resources/add_icon.32.png")
        self.addButton = QPushButton(icon=add_icon)
        self.mainLayout.addWidget(self.addButton)


        reduce_icon = QIcon("resources/remove_icon.32.png")
        self.reduceButton = QPushButton(icon=reduce_icon)
        self.mainLayout.addWidget(self.reduceButton)

        delete_icon = QIcon("resources/close_icon.32.png")
        self.deleteButton = QPushButton(icon=delete_icon)
        self.mainLayout.addWidget(self.deleteButton)

    def setTexts(self):
        self.indexArea.setText(f"{self.index}")
        self.nameArea.setText(f"{self.name} - ({self.count})")
        self.addButton.setText("")
        self.reduceButton.setText("")
        self.deleteButton.setText("")

