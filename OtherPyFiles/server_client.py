from pickle import OBJ
import threading
from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM
from typing import final

from PyQt6.QtCore import QObject, pyqtSignal

# Импорты из вашего кода
from OtherPyFiles.playerClass import Player, Character

dataSize = 1024 * 8


@final
class ServerClass(QObject):
    # Сигналы для обновления UI
    player_connected = pyqtSignal(object)  # Передаем объект Player
    player_data_updated = pyqtSignal(object, str)  # Сигнал об обновлении данных игрока
    _ip: str
    _port: int
    connectedClients: dict[object, Player]
    connectionSocket: socket

    def __init__(self):
        super().__init__()
        self._ip = ""
        self._port = 0
        self.connectedClients = {}
        self.connectionSocket = socket(AF_INET, SOCK_STREAM)

    def startServer(self, port: int, ip: str = gethostbyname(gethostname())):
        # ip = "100.78.201.38"
        print("trying to create to", ip, port)
        try:
            self.connectionSocket.bind((ip, port))
        except Exception as e:
            print(f"Error binding socket: {e}")
            return False
        self._ip = ip
        self._port = port
        self.connectionSocket.listen(5)
        waitToConnect = threading.Thread(target=self._waitConnecting)
        waitToConnect.daemon = True
        waitToConnect.start()
        return True

    def _waitConnecting(self):
        while True:
            try:
                conn, addr = self.connectionSocket.accept()
                player = Player(conn, addr, len(self.connectedClients.keys()) + 1)
                self.connectedClients[addr] = player

                # Отправляем сигнал о новом игроке
                self.player_connected.emit(player)

                messageInput = threading.Thread(
                    target=self._clientMessageGet, args=(player,)
                )
                messageInput.daemon = True
                messageInput.start()
            except Exception as e:
                print(f"Ошибка подключения: {e}")
                break

    def closeServer(self):
        try:
            self.connectionSocket.close()
        except:
            pass
        self.connectedClients = {}

    def sendToClient(self, connection, *args):
        data = [*args]
        try:
            print(f"sending {data}")
            connection.send(str(data).encode("utf-8"))
        except:
            pass

    def _clientMessageGet(self, player):
        while True:
            data = player.conn.recv(dataSize).decode("utf-8")
            if not data:
                continue
            print(data)
            data = eval(data)

            for d in data:
                print("D", d)
                match d:
                    case ["characterNameChanged", _name]:
                        player.character.setName(_name)
                        self.player_data_updated.emit(player, None)
                    case ["newStats", _stats]:
                        print("_STATS", _stats)
                        player.character.setStats(_stats)
                        self.player_data_updated.emit(player, None)
                    case ["newSpellCells", _spells]:
                        player.character.spellCells = _spells
                        self.player_data_updated.emit(player, None)
                    case ["newStatus", _status]:
                        player.character.status = _status
                        self.player_data_updated.emit(player, None)
                    case ["newLevel", _level]:
                        if _level == -1:
                            continue
                        player.character.setLevel(_level)
                        self.player_data_updated.emit(player, None)
                    case ["newExp", _exp]:
                        player.character.setXp(_exp)
                        self.player_data_updated.emit(player, "exp")
                        continue

                    case _:
                        break


@final
class Client(QObject):
    # Сигналы для клиента
    data_updated = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.character = Character()
        self.connectionSocket = socket()

    def connectToServer(self, ip=gethostbyname(gethostname()), port=4242):
        address = (ip, port)
        try:
            print(f"trying to connect to {address}")
            self.connectionSocket.connect(address)
            self.whenConnected()
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def listenCommands(self):
        while True:
            data = self.connectionSocket.recv(dataSize).decode("utf-8")
            if not data:
                continue
            print(data)
            data = eval(data)
            for d in data:
                match d:
                    case ["newStats", _stats]:
                        print("_STATS", _stats)
                        self.character.setStats(_stats)
                    case ["newSpellCells", _spells]:
                        self.character.spellCells = _spells
                    case ["newStatus", _status]:
                        self.character.status = _status
                        # Сигнализируем об обновлении данных
                self.data_updated.emit(self.character)

    def whenConnected(self):
        listen_thread = threading.Thread(target=self.listenCommands)
        listen_thread.daemon = True
        listen_thread.start()

    def sendToServer(self, *args: list[str | dict[str, object]]):
        """данные типа [title,data],[title,data]"""
        data: list[list[str | dict[str, object]]] = [*args]
        try:
            self.connectionSocket.send(str(data).encode("utf-8"))
        except Exception as e:
            print(f"Ошибка отправки данных: {e}")

    def disconnectFromServer(self):
        try:
            self.connectionSocket.close()
        except:
            pass
