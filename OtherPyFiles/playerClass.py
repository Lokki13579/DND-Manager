try:
    from OtherPyFiles.characterclass import Character
except ModuleNotFoundError:
    from characterclass import Character


class Player:
    def __init__(self, connection, addr):
        self.conn = connection
        self.addr = addr
        self.character = Character()

    def getName(self):
        return self.character.name

    def getCharStats(self):
        return self.character.getStats()
