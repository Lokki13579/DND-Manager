from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from UI.playerCard.PlayerCard import Ui_PlayerCard


class Ui_PlayerList(QWidget):
    def __init__(self, servobj):
        super().__init__()
        self.ServerObj = servobj
        self.playersTab = {}

        # Подключаем сигналы сервера к слотам
        self.ServerObj.new_client_connected.connect(self.add_player_tab)
        self.ServerObj.player_data_updated.connect(self.update_player_tab)

        self.setupUi()

    def send(self):
        widget = self.tabWidget.currentWidget()
        for pl, plc in self.playersTab.items():
            if widget == plc:
                plc.updateData(self.ServerObj.players[pl].character)
                self.ServerObj.send_to_client(
                    self.ServerObj.players[pl].addr,
                    0,
                    "stats&" + str(self.ServerObj.players[pl].character.stats),
                )
                self.ServerObj.send_to_client(
                    self.ServerObj.players[pl].addr,
                    1,
                    "spellCells&"
                    + str(self.ServerObj.players[pl].character.spellCells),
                )
                self.ServerObj.send_to_client(
                    self.ServerObj.players[pl].addr,
                    2,
                    "status&" + str(self.ServerObj.players[pl].character.status),
                )

    def add_player_tab(self, player):
        player_card = Ui_PlayerCard(self.ServerObj.players[player].character)
        self.tabWidget.addTab(
            player_card, self.ServerObj.players[player].character.name
        )
        player_card.needToSend.connect(self.send)
        self.playersTab[player] = player_card

    def update_player_tab(self, player, whatToUpdate):
        if player.addr in self.playersTab:
            plObj = self.playersTab[player.addr]

            match whatToUpdate:
                case "name":
                    self.tabWidget.setTabText(
                        self.tabWidget.indexOf(plObj),
                        self.ServerObj.players[player.addr].character.name,
                    )
                    plObj.NameUPD(self.ServerObj.players[player.addr].character.name)
                case "exp":
                    plObj.expUPD(
                        plObj.character.stats.get("experience"),
                        plObj.character.getNextLevelExp(),
                    )
                case _:
                    plObj.updateData(self.ServerObj.players[player.addr].character)

    def setupUi(self):
        self.resize(720, 540)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)
