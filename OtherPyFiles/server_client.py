import asyncio
import socket
from PyQt6.QtCore import QObject, pyqtSignal

try:
    import OtherPyFiles.settings as settings
except ImportError:
    import settings
# from OtherPyFiles.playerClass import Player, Character

dataSize = 1024 * 8
asyncio.start_server


class Server(QObject):
    def __init__(self):
        super().__init__()
        self.server_socket = None
        self.running = False

    async def _run(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((settings.HOST, settings.PORT))
        self.server_socket.listen(8)
        self.server_socket.setblocking(False)

        self.running = True
        print(f"Server started on {settings.HOST}:{settings.PORT}")

        loop = asyncio.get_event_loop()

        while self.running:
            try:
                client, address = await loop.sock_accept(self.server_socket)
                print(f"Connected {address}")
                loop.create_task(self.handle_client(client, address))
            except Exception as e:
                print(f"Accept error: {e}")
                await asyncio.sleep(0.1)

    async def handle_client(self, client_socket: socket.socket, address: tuple) -> None:
        try:
            while self.running:
                try:
                    data = await asyncio.get_event_loop().sock_recv(client_socket, 1024)
                    if not data:
                        break
                    data = data.decode(encoding=settings.ENCODING)
                    print(f"Received from {address}: {data}")
                    # Эхо-ответ
                    response = f"ECHO: {data}"
                    await asyncio.get_event_loop().sock_sendall(
                        client_socket, response.encode(encoding=settings.ENCODING)
                    )
                except BlockingIOError:
                    await asyncio.sleep(0.1)
                except Exception as e:
                    print(f"Client handling error: {e}")
                    break
        finally:
            client_socket.close()
            print(f"Disconnected {address}")

    async def send_message(self, *data):
        try:
            await asyncio.get_event_loop().sock_sendall(
                self.client_socket, data.encode(encoding=settings.ENCODING)
            )
        except Exception as e:
            print(f"Error sending message: {e}")

    def closeServer(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()


class Client(QObject):
    character = None

    def __init__(self):
        super().__init__()
        self.client_socket = None
        self.connected = False
        self.character = None

    async def _run(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        await asyncio.get_event_loop().sock_connect(
            self.client_socket, (settings.HOST, settings.PORT)
        )
        self.connected = True
        print(f"Connected to server {settings.HOST}:{settings.PORT}")

    async def send_message(self, message: str) -> str:
        if not self.connected or not self.client_socket:
            raise ConnectionError("Not connected to server")

        await asyncio.get_event_loop().sock_sendall(
            self.client_socket, message.encode(encoding=settings.ENCODING)
        )

        response = await asyncio.get_event_loop().sock_recv(
            self.client_socket, dataSize
        )
        return response.decode(encoding=settings.ENCODING)

    def disconnectFromServer(self):
        self.connected = False
        if self.client_socket:
            self.client_socket.close()


if __name__ == "__main__":
    while True:
        match input():
            case "server":
                Server().start()
                break
            case "client":
                Client().connect()
                break
            case _:
                print("Invalid input")
