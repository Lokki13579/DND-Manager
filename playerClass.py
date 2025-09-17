from characterclass import *

class Player:
    def __init__(self,connection,addr,ID):
        self.conn = connection
        self.addr = addr
        self.ID = ID
        self.character = Character()
    def getName(self):
        return "&" + str(self.ID) + ". " + self.character.name + "\n"
    def getCharStats(self):
        return self.character.getStats()
