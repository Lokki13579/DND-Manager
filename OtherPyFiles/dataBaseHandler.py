import sqlite3
from platform import system
from os import path

match system():
    case "Windows":
        spellsDataBase = (
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_spells.db"
        )
        classDataBase = (
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_classes.db"
        )
        raceDataBase = (
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_races.db"
        )
        levelDataBase = (
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_levels.db"
        )
        itemDataBase = (
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_magic_items.db",
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_giant_bag.db",
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_trinkets.db",
        )
    case "Linux":
        spellDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_spells.db"
        classDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_classes.db"
        raceDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_races.db"
        levelDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_levels.db"
        itemDataBase = (
            f"{path.expanduser('~')}/.config/DNDManager/dnd_magic_items.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_giant_bag.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_trinkets.db",
        )
    case "Darwin":
        spellDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_spells.db"
        classDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_classes.db"
        raceDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_races.db"
        levelDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_levels.db"
        itemDataBase = (
            f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_magic_items.db",
            f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_giant_bag.db",
            f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_trinkets.db",
        )
    case _:
        spellDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_spells.db"
        classDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_classes.db"
        raceDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_races.db"
        levelDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_levels.db"
        itemDataBase = (
            f"{path.expanduser('~')}/.config/DNDManager/dnd_magic_items.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_giant_bag.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_trinkets.db",
        )


def create_database(name: str, *columns: str, file="DND.db"):
    DATABASE = sqlite3.connect(f"dataBase/DND.db")
    cursor = DATABASE.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(columns)})")
    DATABASE.commit()
    DATABASE.close()


class SpellHandler:
    def __init__(self):
        self.database: sqlite3.Connection = sqlite3.connect(f"{spellDataBase}")
        self.cursor: sqlite3.Cursor = self.database.cursor()

    def add_spell(
        self,
        name: str,
        level: int,
        school: str,
        casting_time: str,
        distance: str,
        components: str,
        duration: str,
        classes: list[str],
        subclasses: list[str],
        description: str,
    ):
        self.cursor.execute(
            "INSERT INTO Spells VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                name,
                level,
                school,
                casting_time,
                distance,
                components,
                duration,
                classes,
                subclasses,
                description,
                True,
            ),
        )
        self.database.commit()
        self.database.close()

    def setSpellActive(self, name: str, active: bool):
        self.cursor.execute(
            "UPDATE Spells SET Active = ? WHERE Name = ?",
            (active, name),
        )
        self.database.commit()
        self.database.close()

    def getSpellInfo(self, selectingItems: str, filter: str | None = None):
        if filter:
            self.cursor.execute(
                f"SELECT {selectingItems} FROM Spells WHERE Active = ? AND {filter}",
                (True,),
            )
        else:
            self.cursor.execute(
                f"SELECT {selectingItems} FROM Spells WHERE Active=true"
            )
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        return result

    def fullDeleteSpell(self, name: str):
        self.cursor.execute(
            "DELETE FROM Spells WHERE Name = ?",
            (name,),
        )
        self.database.commit()
        self.database.close()


class ClassInfoHandler:
    def __init__(self):
        self.database: sqlite3.Connection = sqlite3.connect(f"{classDataBase}")
        self.cursor: sqlite3.Cursor = self.database.cursor()
        self.database.close()

    def getClassInfo(self, selectingItems: str, filter: str = "1=1"):
        self.database = sqlite3.connect(f"{classDataBase}")
        self.cursor = self.database.cursor()
        self.cursor.execute(f"""SELECT {selectingItems}
        FROM classes c
        JOIN class_levels cl ON c.class_id = cl.class_id
        LEFT JOIN spell_slots ss ON cl.level_id = ss.level_id
        WHERE {filter}""")
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        try:
            return dict(result)
        except ValueError:
            return sorted(list(map(lambda x: x[0], list(set(result)))))


class RaceInfoHandler:
    def __init__(self):
        self.database: sqlite3.Connection = sqlite3.connect(f"{raceDataBase}")
        self.cursor: sqlite3.Cursor = self.database.cursor()
        self.database.close()

    def getRaceInfo(self, selectingItems: str, filter: str = "1=1"):
        self.database = sqlite3.connect(f"{raceDataBase}")
        self.cursor = self.database.cursor()
        self.cursor.execute(f"""SELECT {selectingItems}
        FROM race_addictions ra
        JOIN races r ON ra.race_id = r.race_id
        JOIN characteristics c ON ra.char_id = c.char_id
        WHERE {filter}""")
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        try:
            return dict(result)
        except ValueError:
            return sorted(list(map(lambda x: x[0], list(set(result)))))


class LevelInfoHandler:
    def __init__(self):
        self.database: sqlite3.Connection = sqlite3.connect(f"{levelDataBase}")
        self.cursor: sqlite3.Cursor = self.database.cursor()
        self.database.close()

    def getLevelInfo(self, selectingItems: str, filter: str = "level_id=1"):
        self.database = sqlite3.connect(f"{levelDataBase}")
        self.cursor = self.database.cursor()
        self.cursor.execute(f"""SELECT {selectingItems}
        FROM levels l
        WHERE {filter}""")
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        try:
            return dict(result)
        except ValueError:
            return sorted(list(map(lambda x: x[0], list(set(result)))))


class ItemInfoHandler:
    def __init__(self):
        self.database: sqlite3.Connection
        self.cursor: sqlite3.Cursor

    def getItemInfo(
        self,
        selectingItems: str,
        filter: str = "item_id=1",
        justAllTable: int | None = None,
    ):
        if justAllTable != None:
            print(itemDataBase[justAllTable])
            self.database = sqlite3.connect(itemDataBase[justAllTable])
            self.cursor = self.database.cursor()
            self.cursor.execute(f"""SELECT {selectingItems}
            FROM items
            WHERE 1=1""")
            result = self.cursor.fetchall()
            self.database.commit()
            self.database.close()
            try:
                return dict(result)
            except ValueError:
                return sorted(list(map(lambda x: x[0], list(set(result)))))

        for itemDBPath in itemDataBase:
            self.database = sqlite3.connect(itemDBPath)
            self.cursor = self.database.cursor()
            try:
                self.cursor.execute(f"""SELECT {selectingItems}
            FROM items i
            WHERE {filter}""")
            except sqlite3.OperationalError:
                self.database.commit()
                self.database.close()
                continue
            result = self.cursor.fetchall()
            self.database.commit()
            self.database.close()
            try:
                return dict(result)
            except ValueError:
                return sorted(list(map(lambda x: x[0], list(set(result)))))


class StatusesHandler:
    def __init__(self):
        self.database = sqlite3.connect("JSONS/dnd_statuses.json")
        self.cursor = self.database.cursor()

    def getStatuses(self):
        self.cursor.execute("SELECT * FROM statuses")
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        try:
            return dict(result)
        except ValueError:
            return sorted(list(map(lambda x: x[0], list(set(result)))))


class AlignmentHandler:
    def __init__(self):
        self.database = sqlite3.connect("JSONS/dnd_alignments.json")
        self.cursor = self.database.cursor()

    def getAlignments(self):
        self.cursor.execute("SELECT * FROM alignments")
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        try:
            return dict(result)
        except ValueError:
            return sorted(list(map(lambda x: x[0], list(set(result)))))


class BackgroundHandler:
    def __init__(self):
        self.database = sqlite3.connect("JSONS/dnd_backgrounds.json")
        self.cursor = self.database.cursor()

    def getBackgrounds(self):
        self.cursor.execute("SELECT * FROM backgrounds")
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        try:
            return dict(result)
        except ValueError:
            return sorted(list(map(lambda x: x[0], list(set(result)))))


if __name__ == "__main__":
    print(ItemInfoHandler().getItemInfo("item_name", "giant_id=1"))
