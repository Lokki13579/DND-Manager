from socket import *
from blinker import signal
import threading
from panels import *
from playerClass import *
class ServerClass:
    def __init__(self,port=4242):
        self._ip = gethostbyname(gethostname())
        self._port = port
        self.connectedClients = {}
        self.sbmConnected = signal("sbmC")
    def _startServer(self):
        self.S = socket(AF_INET,SOCK_STREAM)
        self.S.bind((self._ip,self._port))
        self.S.listen(5)
        waitToConnect = threading.Thread(target=self._waitConnecting)
        waitToConnect.start()
    def _waitConnecting(self):
        while True:
            conn, addr = self.S.accept()
            self.connectedClients[addr] = Player(conn,addr,len(self.connectedClients.keys())+1)
            messageInput = threading.Thread(target=self._clientMessageGet,args=(self.connectedClients[addr], ))
            messageInput.start()

    def _closeServer(self):
        self.S.close()
        self.connectedClients = {}
    def sendToClient(self,connection, *data):
        out = ""
        for i in data:
            out += str(i) + "&"
        connection.send(out.encode('utf-8'))
    def _clientMessageGet(self,player):
        print("\nЧто-то изменилось, введите  -2, чтобы обновить")
        while True:
            data = player.conn.recv(2048).decode('utf-8').split("&")
            if not data:
                continue
            match data[0]:
                case "newData":
                    player.character.Stats = eval(data[1])
                    player.character.spellCells = eval(data[2])
                    player.character.status = eval(data[3])
                case "characterNameChanged":
                    player.character.setName(data[1])
                    self.sbmConnected.send()
                case _:
                    return
            print("\nЧто-то изменилось, введите  -2, чтобы обновить")
class Client:
    def __init__(self,ip = gethostbyname(gethostname()),port = 4242):
        self._ip = ip
        self._port = port
        self.character = Character()
    def _connectToServer(self):
        self.S = socket()
        address = (self._ip,self._port)
        self.S.connect(address)
        self.whenConnected()
    def listenCommands(self):
        while True:
            data = self.S.recv(2048).decode('utf-8')[:-1]
            if not data:
                continue
            comm = data.split("&")
            match comm[0]:
                case "newData":
                    self.character.Stats = eval(comm[1])
                    self.character.spellCells = eval(comm[2])
                    self.character.status = eval(comm[3])
            print("\nЧто-то изменилось, введите  <Enter>, чтобы обновить")
    def whenConnected(self):
        threading.Thread(target=self.listenCommands).start()
    def sendToServer(self,*data):
        out = ""
        for i in data:
            out += str(i) + "&"
        self.S.send(str(out).encode('utf-8'))
    def _disconnect(self):
        self.S.close()

        
if __name__ == "__main__":
    match input("LLL - "):
        case "1":
            serv = ServerClass()
            serv._startServer()
        case "2":
            cl = Client()
            cl._connectToServer()
