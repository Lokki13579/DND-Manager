from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM

from PyQt6.QtCore import QObject, pyqtSignal

# Импорты из вашего кода
from OtherPyFiles.playerClass import Player, Character

dataSize = 1024 * 8


class ServerClass(QObject): ...


class Client(QObject): ...
