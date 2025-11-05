import threading
from random import randint
from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM

from PyQt6.QtCore import QObject, pyqtSignal

# Импорты из вашего кода
from OtherPyFiles.playerClass import Player, Character

dataSize = 1024 * 8


class ServerClass(QObject):
    # Сигналы для обновления UI
    player_connected = pyqtSignal(object)  # Передаем объект Player
    player_data_updated = pyqtSignal(object)  # Сигнал об обновлении данных игрока

    def __init__(self):
        super().__init__()
        self._ip = None
        self._port = None
        self.connectedClients = {}

    def _startServer(self, port=randint(4000, 5000), ip=gethostbyname(gethostname())):
        self.S = socket(AF_INET, SOCK_STREAM)
        ip = "100.78.201.38"
        print("trying to create to", ip, port)
        try:
            self.S.bind((ip, port))
        except Exception as e:
            print(f"Error binding socket: {e}")
            return False
        self._ip = ip
        self._port = port
        self.S.listen(5)
        waitToConnect = threading.Thread(target=self._waitConnecting)
        waitToConnect.daemon = True
        waitToConnect.start()
        return True

    def _waitConnecting(self):
        while True:
            try:
                conn, addr = self.S.accept()
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

    def _closeServer(self):
        try:
            self.S.close()
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
            print(f"Getted{data}")
            if not data:
                continue
            data = eval(data)
            for d in data:
                print("D", d)
                match d:
                    case ["characterNameChanged", _name]:
                        player.character.setName(_name)
                        print("set Name")
                    case ["newStats", _stats]:
                        print("_STATS", _stats)
                        player.character.setStats(_stats)
                    case ["newSpellCells", _spells]:
                        player.character.spellCells = _spells
                    case ["newStatus", _status]:
                        player.character.status = _status
                    case _:
                        break
            self.player_data_updated.emit(player)


class Client(QObject):
    # Сигналы для клиента
    data_updated = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.character = Character()

    def _connectToServer(self, ip=gethostbyname(gethostname()), port=4242):
        self.S = socket()
        address = (ip, port)
        try:
            print(f"trying to connect to {address}")
            self.S.connect(address)
            self.whenConnected()
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def listenCommands(self):
        while True:
            data = self.S.recv(dataSize).decode("utf-8")
            print("Getted" + data)
            if not data:
                continue
            data = eval(data)
            for d in data:
                print("D", d)
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

    def sendToServer(self, *args):
        """данные типа [title,data],[title,data]"""
        data = [*args]
        print(data)
        try:
            self.S.send(str(data).encode("utf-8"))
        except Exception as e:
            print(f"Ошибка отправки данных: {e}")

    def _disconnect(self):
        try:
            self.S.close()
        except:
            pass
