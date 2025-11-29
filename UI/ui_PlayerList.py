from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from UI.playerCard.PlayerCard import Ui_PlayerCard


class Ui_PlayerList(QWidget):
    def __init__(self, servobj):
        super().__init__()
        self.ServerObj = servobj
        self.playersTab = {}

        # Подключаем сигналы сервера к слотам
        self.ServerObj.player_connected.connect(self.add_player_tab)
        self.ServerObj.player_data_updated.connect(self.update_player_tab)

        self.setupUi()

    def send(self):
        widget = self.tabWidget.currentWidget()
        for pl, plc in self.playersTab.items():
            if widget == plc:
                plc.updateData(pl.character)
                self.ServerObj.sendToClient(
                    pl.conn,
                    ["newStats", pl.character.stats],
                    ["newSpellCells", pl.character.spellCells],
                    ["newStatus", pl.character.status],
                )

    def add_player_tab(self, player):
        player_card = Ui_PlayerCard(player.character)
        self.tabWidget.addTab(player_card, player.character.name)
        player_card.needToSend.connect(self.send)
        self.playersTab[player] = player_card

    def update_player_tab(self, player, whatToUpdate):
        if player in self.playersTab:
            plObj = self.playersTab[player]

            match whatToUpdate:
                case "exp":
                    plObj.expUPD(
                        plObj.character.stats.get("experience"),
                        plObj.character.getNextLevelExp(),
                    )
                case _:
                    plObj.updateData(player.character)

    def setupUi(self):
        self.resize(720, 540)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)
