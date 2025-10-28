import json
import os
import math
import sys
from math import floor
from PyQt6.QtCore import pyqtSignal


def get_resource_path(relative_path):
    """Получаем правильный путь к ресурсам в exe"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)


def jsonLoad(path="/home/artem/.config/DNDManager/AllCharacterData.json"):
    """Безопасная загрузка JSON файлов с обработкой ошибок"""
    try:
        full_path = get_resource_path(path)
        with open(full_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка формата JSON в файле: {path}")
        return {}
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return {}


classData = jsonLoad("JSONS/dnd_classes.json")
racesData = jsonLoad("JSONS/dnd_races.json")
Stats = {
    "class": "Ааракокра",
    "race": "Бард",
    "level": 1,
    "experience": 0,
    "speed": "30",
    "worldview": "Нейтральный",
    "background": "Артист",
    "masterBonus": "+2",
    "skills": "",
    "diceStats": "",
    "inventory": "",
    "spells": "",
    "otherData": {
        "learnedSpells": 0,
        "learnedFocuses": 0,
        "spellCells": {"1": 0, "2": 0, "3": 0},
    },
    "lore": "",
}

characterPath = "AllCharacterData.json"


class Character:
    sthgChanged = pyqtSignal(str)

    def __init__(self, name="Выбирается", stats=None):
        if stats is None:
            stats = {}
        self.name = name
        self.spellCells = {}
        self.setStats(stats)
        self.setClass("Бард")
        self.setRace("Ааракокра")
        self.setLevel(1)
        self.setXp(0)
        self.healthInit()
        self.setMaxHealth(max([1, self.getFirstLevMaxHp()]))
        self.Stats["inventory"] = []

        # Безопасная загрузка maxExp
        try:
            levels_data = jsonLoad("JSONS/dnd_levels.json")
            current_level = self.Stats.get("level", 0)
            next_level_data = levels_data.get(str(current_level + 1), {})
            self.maxExp = next_level_data.get("experience", 300)
        except:
            self.maxExp = 300

        # Безопасная загрузка статусов
        try:
            statuses_data = jsonLoad("JSONS/dnd_statuses.json")
            if isinstance(statuses_data, dict):
                status_keys = list(statuses_data.keys())[:15]
            else:
                # Стандартные статусы по умолчанию
                status_keys = [
                    "Poisoned",
                    "Blinded",
                    "Frightened",
                    "Grappled",
                    "Incapacitated",
                    "Invisible",
                    "Paralyzed",
                    "Petrified",
                    "Exhaustion",
                    "Deafened",
                    "Stunned",
                    "Unconscious",
                    "Charmed",
                    "Restrained",
                    "Prone",
                ]
            self.status = dict(
                zip(status_keys, [False for _ in range(len(status_keys))])
            )
        except:
            # Резервные статусы
            default_statuses = [
                "Poisoned",
                "Blinded",
                "Frightened",
                "Grappled",
                "Incapacitated",
            ]
            self.status = dict(
                zip(default_statuses, [False for _ in range(len(default_statuses))])
            )

    def setName(self, newName):
        self.name = newName

    def setLevel(self, value):
        if isinstance(value, str) and value[0] in "+-":
            self.Stats["level"] += int(value)
        else:
            self.Stats["level"] = int(value)

        if int(value) == 1:
            try:
                self.setMaxHealth(self.getFirstLevMaxHp())
            except:
                pass

        self.expReset(self.Stats["level"])
        self.BMReset(self.Stats["level"])
        self.skillReset(self.Stats.get("class", ""), self.Stats["level"])
        self.initSpellCell()

    def setXp(self, value):
        if isinstance(value, str) and value[0] in "+-":
            self.Stats["experience"] += int(value)
        else:
            self.Stats["experience"] = int(value)

        self.expReset(self.Stats.get("level", 0))
        self.initSpellCell()

    def setClass(self, _class):
        self.Stats["class"] = _class
        self.Stats["hpDice"] = classData.get(_class).get("hpDice")

        try:
            self.setMaxHealth(self.getFirstLevMaxHp())
        except:
            pass

        self.skillReset(_class, self.Stats.get("level", 1))

    def healthInit(self):
        self.Stats["health"] = {}
        self.Stats["health"]["main"] = {"max": 0, "val": 0}
        self.Stats["health"]["temp"] = 0

    def getFirstLevMaxHp(self):
        diceSt = self.Stats.get("diceStats", {})
        return int(self.Stats.get("hpDice")[1:]) + floor(
            (
                diceSt.get("main", {}).get(
                    "Телосложение", int(self.Stats.get("hpDice")[1:])
                )
                + diceSt.get("addiction", {}).get("Телосложение", 0)
                - 10
            )
            / 2
        )

    def setMaxHealth(self, maxHealth):
        if maxHealth == "":
            maxHealth = self.getFirstLevMaxHp()
        maxHealth = int(maxHealth)
        self.Stats["health"]["main"]["max"] = maxHealth

    def maxHealthUp(self, newMaxHealth: int):
        self.Stats["health"]["main"]["max"] += newMaxHealth

    def setHealth(self, hp):
        self.Stats["health"]["main"]["val"] = hp

    def setTempHp(self, tempHp):
        self.Stats["health"]["temp"] = tempHp

    def setRace(self, race):
        self.Stats["race"] = race
        self.Stats["speed"] = racesData.get(race).get("скорость", 30)

        self.diceInit()
        self.Stats["diceStats"]["addiction"] = racesData.get(race).get(
            "УвеличениеХарактеристик"
        )

    def diceInit(self):
        if self.Stats.get("diceStats", {}) != {}:
            return
        self.Stats["diceStats"] = {}
        self.Stats["diceStats"]["main"] = {}
        self.Stats["diceStats"]["addiction"] = {}

    def setDice(self, name, value):
        self.Stats["diceStats"]["main"][name] = value

    def skillReset(self, cl, newLevel):
        self.Stats["skills"] = []
        if not cl:
            return

        try:
            class_data = jsonLoad("JSONS/dnd_classes.json").get(cl, {})
            for _level in range(int(newLevel), 0, -1):
                level_data = class_data.get(str(_level), {})
                skills = level_data.get("Умения", "")
                if skills:
                    self.Stats["skills"] += skills.split(", ")
            while "0" in self.Stats["skills"]:
                self.Stats["skills"].remove("0")
        except:
            self.Stats["skills"] = []

    def BMReset(self, newLevel):
        try:
            levels_data = jsonLoad("JSONS/dnd_levels.json")
            self.Stats["masterBonus"] = levels_data.get(str(newLevel), {}).get("BM", "")
        except:
            self.Stats["masterBonus"] = ""

    def expReset(self, newLevel):
        try:
            levels_data = jsonLoad("JSONS/dnd_levels.json")
            current_level = self.Stats.get("level", 0)
            current_exp = self.Stats.get("experience", 0)
            while True:
                next_level_data = levels_data.get(str(current_level + 1), {})
                next_level_exp = next_level_data.get("experience", float("inf"))
                if current_exp >= next_level_exp and next_level_exp > 0:
                    current_exp -= next_level_exp
                    current_level += 1
                else:
                    break

            self.Stats["level"] = current_level
            self.Stats["experience"] = current_exp
            next_level_data = levels_data.get(str(current_level + 1), {})
            self.maxExp = next_level_data.get("experience", 300)
        except:
            self.maxExp = 300

    def getLevel(self):
        return self.Stats.get("level")

    def getStats(self):
        out = ""
        for k, v in self.Stats.items():
            out += "&" + k.center(15, "-") + "\n" + str(v).center(15) + "\n"
        return out

    def getMaxHp(self):
        return self.Stats.get("health", {}).get("main", {}).get("max", 0)

    def getHp(self):
        return self.Stats.get("health", {}).get("main", {}).get("val", 0)

    def invMan(self, action, item=None):
        # Упрощенная версия для избежания ошибок
        print(f"Управление инвентарем: {action} {item}")

    def otherStatsReset(self):
        otherSt = {}
        try:
            class_data = jsonLoad("JSONS/dnd_classes.json").get(
                self.Stats.get("class", ""), {}
            )
            level_data = class_data.get(str(self.Stats.get("level", 1)), {})

            for i in level_data:
                if i == "Умения":
                    continue
                if i == "DifferentSpellCells":
                    otherSt["MaxspellCells"] = {}
                    for spCell in level_data[i]:
                        cell_level = (
                            spCell[-1] if isinstance(spCell, str) and spCell else "1"
                        )
                        otherSt["MaxspellCells"][cell_level] = str(
                            level_data[i].get(spCell, 0)
                        )
                    continue
                if i == "Ячейки заклинаний" or i == "Уровень ячеек":
                    otherSt["MaxspellCells"] = {}
                    cell_level = level_data.get("Уровень ячеек", "1")
                    otherSt["MaxspellCells"][cell_level] = level_data.get(
                        "Ячейки заклинаний", 0
                    )
                    continue
                otherSt[i] = level_data[i]

            if "formula" in class_data:
                formula = class_data["formula"].split(" ") + ["1"]
                dice_stat = self.Stats.get("diceStats", {}).get(formula[0], 10)
                other_stat = self.Stats.get(formula[1], 0)
                otherSt["Известные заклинания"] = max(
                    1,
                    math.floor((int(dice_stat) - 10) / 2)
                    + math.floor(int(other_stat) / int(formula[2])),
                )

        except Exception as e:
            print(f"Ошибка в otherStatsReset: {e}")

        self.Stats["otherStats"] = otherSt

    def setStats(self, st):
        self.Stats = st
        self.initSpellCell()

    def initSpellCell(self):
        try:
            other_stats = self.Stats.get("otherStats", {})
            max_cells = other_stats.get("MaxspellCells", {})

            if max_cells:
                for key, val in max_cells.items():
                    self.spellCells[str(key)] = int(val)
            else:
                # Альтернативный способ получения ячеек
                cell_level = other_stats.get("Уровень ячеек", "1")
                cell_count = other_stats.get("Ячейки заклинаний", 0)
                self.spellCells[str(cell_level)] = int(cell_count)
        except:
            self.spellCells = {}

    def spellCellsCh(self, key, value):
        if not isinstance(value, str) or value[0] not in "+-":
            self.spellCells[key] = int(value)
        else:
            self.spellCells[key] += int(value)

        try:
            max_cells = self.Stats.get("otherStats", {}).get("MaxspellCells", {})
            if max_cells:
                max_cell_value = int(max_cells.get(key, 0))
            else:
                max_cell_value = int(
                    self.Stats.get("otherStats", {}).get("Ячейки заклинаний", 0)
                )

            if max_cell_value < self.spellCells[key]:
                self.spellCells[key] = max_cell_value
            elif self.spellCells[key] < 0:
                self.spellCells[key] = 0
        except:
            # Защита от ошибок
            if self.spellCells[key] < 0:
                self.spellCells[key] = 0

    def charSave(self, path=characterPath):
        try:
            data = jsonLoad(path)
            data[self.name] = self.Stats

            full_path = get_resource_path(path)
            with open(full_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            print(f"Персонаж {self.name} сохранен")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def jsonCharDelete(self):
        try:
            oldData = jsonLoad()
            if self.name in oldData:
                oldData.pop(self.name)
                self.jsonSave(oldData)
        except Exception as e:
            print(f"Ошибка удаления персонажа: {e}")

    def jsonSave(self, data, path=characterPath):
        try:
            full_path = get_resource_path(path)
            with open(full_path, "w", encoding="utf-8") as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Ошибка сохранения JSON: {e}")


class CharLoader:
    def __init__(self):
        self.allCharacters = {}

    def CharClassDispencer(self):
        try:
            characters_data = jsonLoad()
            for charName, charData in characters_data.items():
                char = Character(charName, charData)
                self.allCharacters[charName] = char
        except Exception as e:
            print(f"Ошибка загрузки персонажей: {e}")
        return self.allCharacters


if __name__ == "__main__":
    character = Character()
    character.invMan("add")
