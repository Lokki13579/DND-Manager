import socket
import threading

from PyQt6.QtCore import QObject, pyqtSignal

try:
    from OtherPyFiles.playerClass import Player
    import OtherPyFiles.settings as settings
except ModuleNotFoundError:
    import settings
    from playerClass import Player

dataSize = 1024 * 8


class Server(QObject):
    new_client_connected = pyqtSignal(str)
    player_data_updated = pyqtSignal(Player, str)
    client_connected = pyqtSignal(tuple)
    client_disconnected = pyqtSignal(tuple)
    message_received = pyqtSignal(tuple, str)  # (address, message)

    def __init__(self):
        super().__init__()
        self.server_socket = None
        self.running = False
        self.clients = dict()
        self.players = dict()
        self.server_thread = None

    def start(self):
        """Запускает сервер в отдельном потоке"""
        if self.running:
            return True

        self.server_thread = threading.Thread(target=self._run, daemon=True)
        self.running = True
        self.server_thread.start()
        return True

    def _run(self):
        """Основной цикл сервера (запускается в отдельном потоке)"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((settings.HOST, settings.PORT))
            self.server_socket.listen(8)

            print(f"Server started on {settings.HOST}:{settings.PORT}")

            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"Connected {address}")
                    self.client_connected.emit(address)

                    # Запускаем обработчик клиента в отдельном потоке
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, address),
                        daemon=True,
                    )
                    if address[0] not in self.clients:
                        self.clients[address[0]] = {
                            "sockets": [],
                            "address": address,
                            "client_thread": client_thread,
                        }
                        self.players[address[0]] = Player(
                            self.clients[address[0]], address[0]
                        )
                        self.new_client_connected.emit(address[0])
                    client_thread.start()

                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"Accept error: {e}")

        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.closeServer()

    def _handle_client(self, client_socket, address):
        """Обрабатывает соединение с клиентом"""
        while self.running:
            try:
                data = client_socket.recv(dataSize)
                if not data:
                    continue

                message = data.decode(encoding=settings.ENCODING)
                print(f"Received from {address}: {message}")
                match message.split("&"):
                    case ["data_type", data]:
                        match data:
                            case "stats":
                                self.clients[address[0]]["sockets"].insert(
                                    0, client_socket
                                )
                            case "spells":
                                self.clients[address[0]]["sockets"].insert(
                                    1, client_socket
                                )
                            case "status":
                                self.clients[address[0]]["sockets"].insert(
                                    2, client_socket
                                )
                        # client_socket.send(data.encode(encoding=settings.ENCODING))
                    case ["char_name", name]:
                        self.players[address[0]].character.name = name
                        self.player_data_updated.emit(self.players[address[0]], "name")
                    case ["newStats", stats]:
                        self.players[address[0]].character.setStats(eval(stats))
                        self.player_data_updated.emit(self.players[address[0]], "stats")
                    case ["newSpells", spells]:
                        self.players[address[0]].character.spellCells = eval(spells)
                        self.player_data_updated.emit(
                            self.players[address[0]], "spells"
                        )
                    case ["newStatus", status]:
                        self.players[address[0]].character.status = eval(status)
                        self.player_data_updated.emit(
                            self.players[address[0]], "status"
                        )
                    case ["newLevel", level]:
                        self.players[address[0]].character.setLevel(int(level))
                        self.player_data_updated.emit(self.players[address[0]], "level")
                    case ["newExp", xp]:
                        self.players[address[0]].character.setXp(int(xp))
                        self.player_data_updated.emit(self.players[address[0]], "exp")
                    case _:
                        response = "Unknown command"

                # Отправляем сигнал в главный поток
                self.message_received.emit(address, message)

                # Эхо-ответ (можно заменить на свою логику)

            except socket.timeout:
                continue

        client_socket.close()
        self.client_disconnected.emit(address)
        print(f"Disconnected {address}")

    def send_to_client(self, address, socket_index, message):
        """Отправляет сообщение конкретному клиенту"""
        for client_address in self.clients:
            if client_address == address:
                try:
                    self.clients[address]["sockets"][socket_index].send(
                        message.encode(encoding=settings.ENCODING)
                    )
                except BrokenPipeError:
                    pass
                return True
        return False

    def broadcast(self, message):
        """Отправляет сообщение всем подключенным клиентам"""
        for client_socket, address, _ in self.clients:
            try:
                client_socket.send(message.encode(encoding=settings.ENCODING))
            except Exception as e:
                print(f"Broadcast error to {address}: {e}")

    def closeServer(self):
        """Корректно закрывает сервер"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        for address in self.clients:
            for client_socket in self.clients[address]["sockets"]:
                try:
                    client_socket.send(
                        "Server is closing".encode(encoding=settings.ENCODING)
                    )
                except:
                    pass
        self.clients.clear()


class Client(QObject):
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    message_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    data_updated = pyqtSignal(str, str)

    def __init__(self, data_type):
        super().__init__()
        self.client_socket = None
        self.connected_to_server = False
        self.receive_thread = None
        self.data_type = data_type

    def connect(self, host=None, port=None):
        """Подключается к серверу"""
        if self.connected_to_server:
            return True

        try:
            if host is None:
                host = settings.HOST
            if port is None:
                port = settings.PORT

            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            self.connected_to_server = True

            # Запускаем поток для приема сообщений
            self.send_message(f"data_type&{self.data_type}")
            self.receive_thread = threading.Thread(
                target=self._receive_messages, daemon=True
            )
            self.receive_thread.start()

            self.connected.emit()
            return True

        except Exception as e:
            self.error_occurred.emit(f"Connection error: {e}")
            return False

    def _receive_messages(self):
        """Принимает сообщения от сервера (в отдельном потоке)"""
        try:
            while self.connected_to_server:
                try:
                    data = self.client_socket.recv(dataSize)
                    if not data:
                        continue

                    message = data.decode(encoding=settings.ENCODING)
                    match message:
                        case "Server is closing":
                            self.disconnectFromServer()
                    # Отправляем сигнал в главный поток
                    self.message_received.emit(message)
                    self.data_updated.emit(*message.split("&"))

                    print(message)

                except socket.timeout:
                    continue
                except Exception as e:
                    if self.connected_to_server:
                        print(f"Receive error: {e}")
                    break

        except Exception as e:
            print(f"Receive thread error: {e}")
        finally:
            self.disconnectFromServer()

    def send_message(self, message):
        """Отправляет сообщение на сервер"""
        if not self.connected_to_server or not self.client_socket:
            self.error_occurred.emit("Not connected to server")
            return False

        try:
            self.client_socket.send(message.encode(encoding=settings.ENCODING))
            return True
        except Exception as e:
            self.error_occurred.emit(f"Send error: {e}")
            return False

    def disconnectFromServer(self):
        """Отключается от сервера"""
        self.connected_to_server = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
        self.disconnected.emit()


if __name__ == "__main__":
    # Простой тест
    def test_server():
        server = Server()
        server.start()
        input("Server running. Press Enter to stop...")
        server.closeServer()

    def test_client():
        client = Client(input())
        if client.connect():
            print("Connected to server")
        input()
        client.disconnectFromServer()

    choice = input("Enter 'server' or 'client': ")
    if choice == "server":
        test_server()
    elif choice == "client":
        test_client()
