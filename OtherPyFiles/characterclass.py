from ast import Constant
import json
import platform
import os
import math
from math import floor
import OtherPyFiles.dataBaseHandler as dbHandler


CHARACTERISTICS = {
    "STR": "Сила",
    "DEX": "Ловкость",
    "CON": "Телосложение",
    "INT": "Интеллект",
    "WIS": "Мудрость",
    "CHA": "Харизма",
}

match platform.system():
    case "Windows":
        charPath = f"{os.path.expanduser('~')}\\AppData\\Local\\DNDManager\\AllCharacterData.json"
    case "Linux":
        charPath = f"{os.path.expanduser('~')}/.config/DNDManager/AllCharacterData.json"
    case "Darwin":
        charPath = f"{os.path.expanduser('~')}/Library/Application Support/DNDManager/AllCharacterData.json"
    case _:
        charPath = f"{os.path.expanduser('~')}/.config/DNDManager/AllCharacterData.json"


classData = dbHandler.ClassInfoHandler()
racesData = dbHandler.RaceInfoHandler()


class Character:
    def __init__(self, name: str = "Выбирается", stats: dict[str, object] = {}):
        def statusesInit():
            statuses_data: dict[str, object] | list[object]
            statuses_data = dbHandler.StatusesHandler().getStatuses()
            status_keys = list(statuses_data)[:15]
            self.status = dict(
                zip(status_keys, [False for _ in range(len(status_keys))])
            )

            return

        self.name: str = name
        self.stats = stats or {}
        self.status = {}
        self.spellCells = {}

        self.setClass("Бард")
        self.setRace("Ааракокра")
        self.setLevel(1)
        self.setXp(0)
        self.stats["worldview"] = "Нейтральный"
        self.stats["background"] = "Артист"
        self.healthInit()
        self.setMaxHealth(max(1, self.getFirstLevMaxHp()))
        self.stats["inventory"] = {}
        self.stats["spells"] = {}
        self.stats["spells"]["readySpells"] = {}
        self.stats["spells"]["allSpells"] = {}
        for i in range(10):
            self.stats["spells"]["allSpells"][i] = []
        statusesInit()
        # Безопасная загрузка maxExp

    def addItem(
        self,
        item: str = "Абракадабрус",
        obj: object = object,
    ):
        obj.item.deletingItem.connect(self.removeItem)
        self.stats["inventory"][item] = obj.item.count

    def addSpell(self, spellItem):
        spellItem.spell.deletingSpell.connect(self.removeSpell)
        print(self.stats)
        self.stats["spells"]["allSpells"][spellItem.spell.spell_level].append(
            spellItem.spell.spell_name
        )

    def removeSpell(self, spellName, spellLevel):
        self.stats["spells"]["allSpells"][spellLevel].remove(spellName)

    def removeItem(self, item: str):
        self.stats["inventory"].pop(item)

    def reduceItem(self, item: str, count=1):
        self.stats["inventory"][item].reduce(count)

    def increaseItem(self, item: str, count=1):
        self.stats["inventory"][item].add(count)

    def setName(self, newName):
        self.name = newName

    def setLevel(self, value):
        if value == -1:
            return
        if isinstance(value, str) and value[0] in "+-":
            self.stats["level"] += int(value)
        else:
            self.stats["level"] = int(value)

        if int(value) == 1:
            try:
                self.setMaxHealth(self.getFirstLevMaxHp())
            except:
                pass

        self.expReset(self.stats["level"])
        self.BMReset(self.stats["level"])
        self.skillReset(self.stats.get("class", ""), self.stats["level"])
        self.otherStatsReset()
        self.initSpellCell()

    def setXp(self, value):
        if isinstance(value, str) and value[0] in "+-":
            self.stats["experience"] += int(value)
        else:
            self.stats["experience"] = int(value)

        self.expReset(self.stats.get("level", 0))
        self.initSpellCell()

    def setClass(self, _class):
        print(self.name)
        self.stats["class"] = _class
        print(f"Class set to {_class}")
        self.stats["hpDice"] = classData.getClassInfo(
            "hp_dice", f"class_name='{_class}' AND level={self.stats.get('level', 1)}"
        )[0][0]
        print(self.stats["hpDice"])
        self.stats["mainChar"] = classData.getClassInfo(
            "main_characteristic", f"class_name='{_class}'"
        )[0]

        try:
            self.setMaxHealth(self.getFirstLevMaxHp())
        except:
            pass

        self.skillReset(_class, self.stats.get("level", 1))

    def healthInit(self):
        self.stats["health"] = {}
        self.stats["health"]["main"] = {"max": 0, "val": 0}
        self.stats["health"]["temp"] = 0

    def getFirstLevMaxHp(self):
        diceSt = self.stats.get("diceStats", {})
        print(self.stats.get("hpDice"))
        return int(self.stats.get("hpDice", "d6")[1:]) + floor(
            (
                diceSt.get("main", {}).get(
                    "Телосложение", int(self.stats.get("hpDice", "d6")[1:])
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
        self.stats["health"]["main"]["max"] = maxHealth

    def maxHealthUp(self, newMaxHealth: int):
        self.stats["health"]["main"]["max"] += newMaxHealth

    def setHealth(self, hp):
        self.stats["health"]["main"]["val"] = hp

    def setTempHp(self, tempHp):
        self.stats["health"]["temp"] = tempHp

    def setRace(self, race):
        self.stats["race"] = race
        self.stats["speed"] = racesData.getRaceInfo(
            "speed", "race_name=" + f"'{race.strip()}'"
        )

        self.diceInit()
        self.stats["diceStats"]["addiction"] = racesData.getRaceInfo(
            "char_name,increase", "race_name='Ааракокра'"
        )

    def diceInit(self):
        if self.stats.get("diceStats", {}) != {}:
            return
        self.stats["diceStats"] = {}
        self.stats["diceStats"]["main"] = {}
        self.stats["diceStats"]["main"]["value"] = {}
        self.stats["diceStats"]["main"]["modif"] = {}
        self.stats["diceStats"]["addiction"] = {}

    def setDice(self, name, value, modif):
        self.stats["diceStats"]["main"]["value"][name] = value
        self.stats["diceStats"]["main"]["modif"][name] = modif

    def skillReset(self, cl, newLevel):
        self.stats["skills"] = []
        if not cl:
            return

        try:
            for _level in range(int(newLevel), 0, -1):
                skills = classData.getClassInfo("features", f"class_name='{cl}'")
                if skills:
                    self.stats["skills"] += skills.split(", ")
            while "0" in self.stats["skills"]:
                self.stats["skills"].remove("0")
        except:
            self.stats["skills"] = []

    def BMReset(self, newLevel):
        try:
            self.stats["masterBonus"] = dbHandler.LevelInfoHandler().getLevelInfo(
                "master_bonus", f"level_id='{newLevel}'"
            )
        except:
            self.stats["masterBonus"] = ""

    def getNextLevelExp(self):
        return dbHandler.LevelInfoHandler().getLevelInfo(
            "experience_to_next_level", f"level_id={self.stats.get('level', 1)}"
        )

    def expReset(self, newLevel):
        try:
            levels_data = charLoad("JSONS/dnd_levels.json")
            current_level = self.stats.get("level", 0)
            current_exp = self.stats.get("experience", 0)
            while True:
                next_level_data = levels_data.get(str(current_level + 1), {})
                next_level_exp = next_level_data.get("experience", float("inf"))
                if current_exp >= next_level_exp and next_level_exp > 0:
                    current_exp -= next_level_exp
                    current_level += 1
                else:
                    break

            self.stats["level"] = current_level
            self.stats["experience"] = current_exp
            next_level_data = levels_data.get(str(current_level + 1), {})
        except:
            pass

    def getLevel(self):
        return self.stats.get("level", 1)

    def getStats(self):
        out = ""
        for k, v in self.stats.items():
            out += "&" + k.center(15, "-") + "\n" + str(v).center(15) + "\n"
        return out

    def getMaxHp(self):
        return self.stats.get("health", {}).get("main", {}).get("max", 0)

    def getHp(self):
        return self.stats.get("health", {}).get("main", {}).get("val", 0)

    def fullHeal(self):
        self.stats["health"]["main"]["val"] = self.getMaxHp()

    def heal(self, amount):
        self.stats["health"]["main"]["val"] += amount

    def randomHeal(self):
        self.stats["health"]["main"]["val"] += randint(
            1, int(self.stats.get("hpDice", 1))
        )

    def invMan(self, action, item=None):
        # Упрощенная версия для избежания ошибок
        print(f"Управление инвентарем: {action} {item}")

    def otherStatsReset(self):
        otherSt = {}
        try:
            for feature, value in dbHandler.ClassInfoHandler.getClassInfo(
                "feature_name,feature_value",
                f"class_name='{self.stats.get('class')}' AND level={self.stats.get('level')}",
            ):
                otherSt[feature] = value

            if "formula" in class_data:
                formula = class_data["formula"].split(" ") + ["1"]
                dice_stat = self.stats.get("diceStats", {}).get(formula[0], 10)
                other_stat = self.stats.get(formula[1], 0)
                otherSt["Известные заклинания"] = max(
                    1,
                    math.floor((int(dice_stat) - 10) / 2)
                    + math.floor(int(other_stat) / int(formula[2])),
                )

        except Exception as e:
            print(f"Ошибка в otherStatsReset: {e}")

        self.stats["otherStats"] = otherSt

    def setState(self, statName, statChecked):
        self.status.update({statName: statChecked})
        print(f"State updated: {statName} = {statChecked}")

    def setStats(self, st):
        self.stats = st
        self.otherStatsReset()
        self.initSpellCell()
        self.expReset(self.stats.get("level", 1))

    def initSpellCell(self):
        try:
            other_stats = self.stats.get("otherStats", {})
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
            max_cells = self.stats.get("otherStats", {}).get("MaxspellCells", {})
            if max_cells:
                max_cell_value = int(max_cells.get(key, 0))
            else:
                max_cell_value = int(
                    self.stats.get("otherStats", {}).get("Ячейки заклинаний", 0)
                )

            if max_cell_value < self.spellCells[key]:
                self.spellCells[key] = max_cell_value
            elif self.spellCells[key] < 0:
                self.spellCells[key] = 0
        except:
            # Защита от ошибок
            if self.spellCells[key] < 0:
                self.spellCells[key] = 0

    def charLoad(self):
        with open(charPath, "r", encoding="utf-8") as file:
            return json.load(file)

    def charSave(self, path=charPath):
        try:
            data = self.charLoad()
            data[self.name] = self.stats

            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"Персонаж {self.name} сохранен")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def jsonCharDelete(self):
        try:
            oldData = self.charLoad()
            if self.name in oldData:
                oldData.pop(self.name)
                self.jsonSave(oldData)
        except Exception as e:
            print(f"Ошибка удаления персонажа: {e}")

    def jsonSave(self, data, path=charPath):
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения JSON: {e}")


class CharLoader:
    def __init__(self):
        self.allCharacters = {}

    def charLoad(self):
        with open(charPath, "r", encoding="utf-8") as file:
            return json.load(file)

    def CharClassDispencer(self):
        try:
            characters_data = self.charLoad()
            print("char_data", characters_data)
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
