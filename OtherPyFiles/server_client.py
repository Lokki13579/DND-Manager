import threading
from random import randint
from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM

from PyQt6.QtCore import QObject, pyqtSignal

# Импорты из вашего кода
from OtherPyFiles.playerClass import Player, Character


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

    def sendToClient(self, connection, *data):
        out = ""
        for i in data:
            out += str(i) + "&"
        try:
            connection.send(out.encode("utf-8"))
        except:
            pass

    def _clientMessageGet(self, player):
        while True:
            try:
                data = player.conn.recv(4096).decode("utf-8").split("&")
                if not data or not data[0]:
                    continue
                print(data)
                match data[0]:
                    case "newData":
                        player.character.setStats(eval(data[1]))
                        player.character.spellCells = eval(data[2])
                        player.character.status = eval(data[3])
                        player.character.expReset(
                            player.character.Stats.get("level", 1)
                        )
                        print("Data Uptained and signal emitted")
                        # Отправляем сигнал об обновлении данных
                        print(player.character.Stats)
                        self.player_data_updated.emit(player)
                    case "characterNameChanged":
                        player.character.setName(data[1])
                        # Отправляем сигнал об обновлении имени
                        self.player_data_updated.emit(player)
                    case _:
                        break
                print("\nЧто-то изменилось, введите -2, чтобы обновить")
            except Exception as e:
                print(f"Ошибка получения данных: {e}")
                break


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
            try:
                data = self.S.recv(4096).decode("utf-8")[:-1]
                if not data:
                    continue
                comm = data.split("&")
                match comm[0]:
                    case "newData":
                        self.character.setStats(eval(comm[1]))
                        self.character.spellCells = eval(comm[2])
                        self.character.status = eval(comm[3])
                        # Сигнализируем об обновлении данных
                        self.data_updated.emit(self.character)
                print("\nЧто-то изменилось, введите <Enter>, чтобы обновить")
            except Exception as e:
                print(f"Ошибка получения данных: {e}")
                break

    def whenConnected(self):
        listen_thread = threading.Thread(target=self.listenCommands)
        listen_thread.daemon = True
        listen_thread.start()

    def sendToServer(self, *data):
        out = ""
        for i in data:
            out += str(i) + "&"
        try:
            print(out)
            self.S.send(str(out).encode("utf-8"))
        except Exception as e:
            print(f"Ошибка отправки данных: {e}")

    def _disconnect(self):
        try:
            self.S.close()
        except:
            pass
