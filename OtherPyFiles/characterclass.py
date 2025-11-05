import json
import platform
import os
import math
from math import floor
from random import randint

match platform.system():
    case "Windows":
        charPath = f"{os.path.expanduser('~')}\\AppData\\Local\\DNDManager\\AllCharacterData.json"
    case "Linux":
        charPath = f"{os.path.expanduser('~')}/.config/DNDManager/AllCharacterData.json"
    case "Darwin":
        charPath = f"{os.path.expanduser('~')}/Library/Application Support/DNDManager/AllCharacterData.json"
    case _:
        charPath = f"{os.path.expanduser('~')}/.config/DNDManager/AllCharacterData.json"


def jsonLoad(path=charPath):
    """Безопасная загрузка JSON файлов с обработкой ошибок"""
    try:
        with open(path, "r", encoding="utf-8") as file:
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


def statusesGet(path="JSONS/dnd_statuses.json"):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
        return {}
    except json.JSONDecodeError:
        print(f"Ошибка формата JSON в файле: {path}")
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

characterPath = "/home/artem/.config/DNDManager/AllCharacterData.json"


class Character:
    def __init__(self, name="Выбирается", stats=None):
        def statusesInit():
            statuses_data = jsonLoad("JSONS/dnd_statuses.json")
            status_keys = list(statuses_data)[:15]
            self.status = dict(
                zip(status_keys, [False for _ in range(len(status_keys))])
            )

        self.name = name
        if stats:
            self.setStats(stats)
            statusesInit()

            return
        self.Stats = {}

        self.setClass("Бард")
        self.setRace("Ааракокра")
        self.setLevel(1)
        self.setXp(0)
        self.Stats["worldview"] = "Нейтральный"
        self.Stats["background"] = "Артист"
        self.healthInit()
        self.setMaxHealth(max([1, self.getFirstLevMaxHp()]))
        self.Stats["inventory"] = {}
        self.Stats["spells"] = {}
        self.Stats["spells"]["readySpells"] = {}
        self.Stats["spells"]["allSpells"] = {}
        for i in range(10):
            self.Stats["spells"]["allSpells"][str(i)] = []
        statusesInit()
        # Безопасная загрузка maxExp

    def addItem(
        self,
        item: str = "Абракадабрус",
        obj=object,
    ):
        obj.item.deletingItem.connect(self.removeItem)
        self.Stats["inventory"][item] = obj.item.count

    def addSpell(self, spellItem):
        spellItem.spell.deletingSpell.connect(self.removeSpell)
        self.Stats["spells"]["allSpells"][spellItem.spell.level].append(
            spellItem.spell.name
        )

    def removeSpell(self, spellName, spellLevel):
        self.Stats["spells"]["allSpells"][spellLevel].remove(spellName)

    def removeItem(self, item: str):
        self.Stats["inventory"].pop(item)

    def reduceItem(self, item: str, count=1):
        self.Stats["inventory"][item].reduce(count)

    def increaseItem(self, item: str, count=1):
        self.Stats["inventory"][item].add(count)

    def setName(self, newName):
        self.name = newName

    def setLevel(self, value):
        if value == -1:
            return
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
        self.otherStatsReset()
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
        self.Stats["mainChar"] = classData.get(_class).get("mainChar", "").split("?")

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
        self.Stats["diceStats"]["main"]["value"] = {}
        self.Stats["diceStats"]["main"]["modif"] = {}
        self.Stats["diceStats"]["addiction"] = {}

    def setDice(self, name, value, modif):
        self.Stats["diceStats"]["main"]["value"][name] = value
        self.Stats["diceStats"]["main"]["modif"][name] = modif

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

    def getNextLevelExp(self):
        levels_data = jsonLoad("JSONS/dnd_levels.json")
        current_level = self.Stats.get("level", 0)
        next_level_data = levels_data.get(str(current_level + 1), {})
        next_level_exp = next_level_data.get("experience", float("inf"))
        return next_level_exp

    def getExpTo20Level(self):
        levels_data = jsonLoad("JSONS/dnd_levels.json")
        current_level = self.Stats.get("level", 1)
        exp_to_20 = 0
        for i in range(current_level + 1, 21):
            next_level_exp = levels_data.get(str(i), {}).get("experience", float("inf"))
            exp_to_20 += next_level_exp
        return exp_to_20

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
        except:
            pass

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

    def fullHeal(self):
        self.Stats["health"]["main"]["val"] = self.getMaxHp()

    def heal(self, amount):
        self.Stats["health"]["main"]["val"] += amount

    def randomHeal(self):
        self.Stats["health"]["main"]["val"] += randint(
            1, int(self.Stats.get("hpDice", 1))
        )

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
        self.otherStatsReset()
        self.initSpellCell()
        self.expReset(self.Stats.get("level", 1))

    def initSpellCell(self):
        try:
            other_stats = self.Stats.get("otherStats", {})
            max_cells = other_stats.get("ЯчейкиЗаклинаний", {})

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
            data = jsonLoad()
            data[self.name] = self.Stats

            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
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
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения JSON: {e}")


class CharLoader:
    def __init__(self):
        self.allCharacters = {}

    def CharClassDispencer(self):
        try:
            characters_data = jsonLoad()
            for charName, charData in characters_data.items():
                char = Character()
                char.setName(charName)
                char.setStats(charData)
                self.allCharacters[charName] = char
        except Exception as e:
            print(f"Ошибка загрузки персонажей: {e}")
        return self.allCharacters


if __name__ == "__main__":
    character = Character()
    character.invMan("add")
