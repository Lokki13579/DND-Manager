from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from UI.PlayerCard import Ui_PlayerCard

class Ui_PlayerList(QWidget):
    def __init__(self, servobj):
        super().__init__()
        self.ServerObj = servobj
        self.playersTab = {}
        
        # Подключаем сигналы сервера к слотам
        self.ServerObj.player_connected.connect(self.add_player_tab)
        self.ServerObj.player_data_updated.connect(self.update_player_tab)
        
        self.setupUi()
    
    def add_player_tab(self, player):
        """Добавляет вкладку для нового игрока (вызывается через сигнал)"""
        # Проверяем, нет ли уже вкладки для этого игрока
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == player.character.name:
                return  # Вкладка уже существует
        
        player_card = Ui_PlayerCard(player.character)
        self.tabWidget.addTab(player_card, player.character.name)
        self.playersTab[player] = player_card
    
    def update_player_tab(self, player):
        """Обновляет вкладку игрока при изменении данных (вызывается через сигнал)"""
        if player in self.playersTab:
            # Обновляем данные в карточке игрока
            self.playersTab[player].update_character_data(player.character)
            
            # Обновляем название вкладки если изменилось имя
            for i in range(self.tabWidget.count()):
                if self.tabWidget.widget(i) == self.playersTab[player]:
                    self.tabWidget.setTabText(i, player.character.name)
                    break
    
    def setupUi(self):
        self.resize(720, 540)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)