from PyQt6.QtCore import QObject, pyqtSignal 
from socket import *
from blinker import signal
import threading
from panels import *
from playerClass import *
from random import randint
from art import tprint
class ServerClass(QObject):
    player_connected = pyqtSignal(object)
    player_updated = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self._ip = None
        self._port = None
        self.connectedClients = {}
        self.sbmConnected = signal("sbmC")
    def _startServer(self,port=randint(4000,5000), ip = gethostbyname(gethostname())):
        self.S = socket(AF_INET,SOCK_STREAM)
        self.S.bind((ip,port))
        print(tprint(str(port)))
        self._ip = ip
        self._port = port
        self.S.listen(5)
        waitToConnect = threading.Thread(target=self._waitConnecting)
        waitToConnect.daemon = True
        waitToConnect.start()
    def _waitConnecting(self):
        while True:
            try:
                conn, addr = self.S.accept()
                player = Player(conn,addr,len(self.connectedClients.keys())+1)
                self.connectedClients[addr] = player

                self.player_connected.emit(player)
                messageInput = threading.Thread(target=self._clientMessageGet,args=(self.connectedClients[addr], ))
                messageInput.daemon = True
                messageInput.start()
            except:
                pass

    def _closeServer(self):
        self.S.close()
        self.connectedClients = {}
    def sendToClient(self,connection, *data):
        out = ""
        for i in data:
            out += str(i) + "&"
        try:
            connection.send(out.encode('utf-8'))
        except:
            pass


    def _clientMessageGet(self,player):
        self.sbmConnected.send()
        print("\nЧто-то изменилось, введите  -2, чтобы обновить")
        while True:
            try:
                data = player.conn.recv(2048).decode('utf-8').split("&")
                if not data:
                    continue
                match data[0]:
                    case "newData":
                        player.character.Stats = eval(data[1])
                        player.character.spellCells = eval(data[2])
                        player.character.status = eval(data[3])
                        self.player_updated.emit(player)
                    case "characterNameChanged":
                        player.character.setName(data[1])
                        self.sbmConnected.send()
                        self.player_updated.emit(player)
                    case _:
                        return
                print("\nЧто-то изменилось, введите  -2, чтобы обновить")
            except:
                pass
class Client(QObject):
    data_updated = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.character = Character()
    def _connectToServer(self,ip = gethostbyname(gethostname()),port = 4242):
        self.S = socket()
        address = (ip,port)
        try:
            self.S.connect(address)
            self.whenConnected()
        except:
            pass
    def listenCommands(self):
        while True:
            try:
                data = self.S.recv(2048).decode('utf-8')[:-1]
                if not data:
                    continue
                comm = data.split("&")
                match comm[0]:
                    case "newData":
                        self.character.Stats = eval(comm[1])
                        self.character.spellCells = eval(comm[2])
                        self.character.status = eval(comm[3])
                        self.data_updated.emit()
                print("\nЧто-то изменилось, введите  <Enter>, чтобы обновить")
            except:
                pass
    def whenConnected(self):
        listen = threading.Thread(target=self.listenCommands)
        listen.daemon = True
        listen.start()
    def sendToServer(self,*data):
        out = ""
        for i in data:
            out += str(i) + "&"
        try:
            self.S.send(str(out).encode('utf-8'))
        except:
            pass
    def _disconnect(self):
        try:
            self.S.close()
        except:
            pass

        
if __name__ == "__main__":
    match input("LLL - "):
        case "1":
            serv = ServerClass()
            serv._startServer()
        case "2":
            cl = Client()
            cl._connectToServer()
