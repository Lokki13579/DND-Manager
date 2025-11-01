from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel
from PyQt6.QtCore import Qt
from math import floor


class MoreInfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("More Info")
        self.setStyleSheet("""
                           font-family: '3270 Nerd Font';
                           font-size: 20px;
                           """)
        self.setFixedSize(540, 720)
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout(self)
        self.updateWidgets()

    def updateWidgets(self, character=None):
        if not character:
            return
        self.widgets = {}
        self.widgets.update({"Title": QLabel("Больше информации")})
        self.widgets.get("Title").setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widgets.get("Title").setStyleSheet("font-size: 24px;color: #6b586b;")
        self.widgets.update({"Name": QLabel(f"Имя: {character.name}")})
        self.widgets.update(
            {
                "Level": QLabel(
                    f"Уровень: {character.Stats.get('level')} - ({character.Stats.get('experience')}/{character.getNextLevelExp()})"
                )
            }
        )
        # self.widgets.update(
        #    {"Experience": QLabel(f"Опыт: {character.Stats.get('experience')}")}
        # )
        self.widgets.update({"Class": QLabel(f"Класс: {character.Stats.get('class')}")})
        self.widgets.update(
            {
                "MainChar": QLabel(
                    f"Глав. характеристика: {character.Stats.get('mainChar')}"
                )
            }
        )
        self.widgets.update({"Race": QLabel(f"Раса: {character.Stats.get('race')}")})
        self.widgets.update(
            {"Speed": QLabel(f"Скорость: {character.Stats.get('speed')}")}
        )
        self.widgets.update(
            {"Worldview": QLabel(f"Видение мира: {character.Stats.get('worldview')}")}
        )
        self.widgets.update(
            {"Background": QLabel(f"Прошлое: {character.Stats.get('background')}")}
        )
        self.widgets.update(
            {
                "MasterBonus": QLabel(
                    f"Мастер бонус: {character.Stats.get('masterBonus')}"
                )
            }
        )
        self.widgets.update(
            {
                "HitPoints": QLabel(
                    f"Здоровье: {character.Stats.get('health', {}).get('main', {}).get('val', 0)}"
                )
            }
        )
        self.widgets.update(
            {
                "Inventory": QLabel(
                    f"Инвентарь:\n  {'\n  '.join(character.Stats.get('inventory', []))}"
                )
            }
        )

        _d = character.Stats.get("spells", {}).get("allSpells", {})
        self.widgets.update(
            {
                "Spells": QLabel(
                    f"Заклинания:\n  {'\n  '.join([i for k in _d for i in _d[k]])}"
                )
            }
        )
        self.widgets.update(
            {"Lore": QLabel(f"Лор: {character.Stats.get('lore', 'Неизвестен')}")}
        )

        self.widgetsInit()

    def widgetsInit(self):
        doneButton = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        doneButton.setCenterButtons(True)
        doneButton.accepted.connect(self.accept)
        self.layout.addWidget(doneButton, 0, 0)
        i = 0
        for key, widget in self.widgets.items():
            if key == "Title":
                self.layout.addWidget(
                    widget, 0, floor(len(list(self.widgets.keys())) / 8)
                )
                continue
            widget.setWordWrap(True)
            self.layout.addWidget(widget, (i % 8) + 1, i // 8)
            i += 1

    def setNewCharacter(self, character):
        self.updateWidgets(character)
