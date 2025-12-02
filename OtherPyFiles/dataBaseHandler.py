from collections import defaultdict
import sqlite3
from platform import system
from os import path
from typing import final
from webbrowser import BackgroundBrowser


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
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_poisons.db",
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_drugs.db",
        )
        statusDataBase = (
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_statuses.db"
        )
        backgroundsDataBase = (
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_backgrounds.db"
        )
        alignmentDataBase = (
            f"{path.expanduser('~')}\\AppData\\Local\\DNDManager\\dnd_alignments.db"
        )
    case "Linux":
        spellDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_spells.db"
        classDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_classes.db"
        raceDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_races.db"
        levelDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_levels.db"
        statusDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_statuses.db"
        itemDataBase = (
            f"{path.expanduser('~')}/.config/DNDManager/dnd_magic_items.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_giant_bag.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_trinkets.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_poisons.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_drugs.db",
        )
        backgroundsDataBase = (
            f"{path.expanduser('~')}/.config/DNDManager/dnd_backgrounds.db"
        )
        alignmentDataBase = (
            f"{path.expanduser('~')}/.config/DNDManager/dnd_alignments.db"
        )
    case "Darwin":
        spellDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_spells.db"
        classDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_classes.db"
        raceDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_races.db"
        levelDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_levels.db"
        statusDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_statuses.db"
        itemDataBase = (
            f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_magic_items.db",
            f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_giant_bag.db",
            f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_trinkets.db",
            f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_poisons.db",
            f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_drugs.db",
        )
        backgroundsDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_backgrounds.db"
        alignmentDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_alignments.db"
    case _:
        spellDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_spells.db"
        classDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_classes.db"
        raceDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_races.db"
        levelDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_levels.db"
        statusDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_statuses.db"
        itemDataBase = (
            f"{path.expanduser('~')}/.config/DNDManager/dnd_magic_items.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_giant_bag.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_trinkets.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_poisons.db",
            f"{path.expanduser('~')}/.config/DNDManager/dnd_drugs.db",
        )
        backgroundsDataBase = (
            f"{path.expanduser('~')}/.config/DNDManager/dnd_backgrounds.db"
        )
        alignmentDataBase = (
            f"{path.expanduser('~')}/.config/DNDManager/dnd_alignments.db"
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
            "UPDATE Spells SET active = ? WHERE name = ?",
            (active, name),
        )
        self.database.commit()
        self.database.close()

    def getSpellInfo(self, selectingItems: str, filter: str = "1=1"):
        self.cursor.execute(
            f"SELECT {selectingItems} FROM Spells WHERE {filter} AND active=true"
        )
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()

        columns = list(map(lambda x: x[0], self.cursor.description))
        try:
            out = defaultdict(list)
            for key, val in result:
                out[key].append(val)
            return dict(out)
        except ValueError:
            try:
                out = {}
                for spell in result:
                    out[spell[0]] = dict(zip(columns, spell))
                return out
            except ValueError:
                return sorted(list(map(lambda x: x[0], list(set(result)))))

    def fullDeleteSpell(self, name: str):
        self.cursor.execute(
            "DELETE FROM Spells WHERE spell_name = ?",
            (name,),
        )
        self.database.commit()
        self.database.close()


@final
class ClassInfoHandler:
    def __init__(self):
        self.database: sqlite3.Connection
        self.cursor: sqlite3.Cursor

    def getClassInfo(self, selectingItems: str, filter: str = "1=1"):
        self.database = sqlite3.connect(f"{classDataBase}")
        self.cursor = self.database.cursor()
        self.cursor.execute(f"""SELECT {selectingItems}
        FROM classes c
        JOIN class_levels cl ON c.class_id = cl.class_id
        LEFT JOIN spell_slots ss ON cl.level_id = ss.level_id
        LEFT JOIN warlock_features wf ON cl.level_id = wf.level_id
        LEFT JOIN artificer_features af  ON cl.level_id = af.level_id
        LEFT JOIN class_specific_features csf ON cl.level_id = csf.level_id
        WHERE {filter}""")
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        try:
            return dict(result)
        except ValueError:
            return sorted(list(set(list(map(lambda x: x[0], result)))))


@final
class RaceInfoHandler:
    def __init__(self):
        self.database: sqlite3.Connection
        self.cursor: sqlite3.Cursor

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
            return sorted(list(set(list(map(lambda x: x[0], result)))))


@final
class LevelInfoHandler:
    def __init__(self):
        self.database: sqlite3.Connection
        self.cursor: sqlite3.Cursor

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
            return sorted(list(map(lambda x: x[0], result)))


@final
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
            match justAllTable:
                case 1:
                    request = f"""SELECT {selectingItems}
                                FROM items i
                                LEFT JOIN giants g ON i.giant_id = g.giant_id
                                WHERE 1=1"""
                case _:
                    request = f"""SELECT {selectingItems}
                                FROM items
                                WHERE 1=1"""

            self.cursor.execute(request)
            result = self.cursor.fetchall()
            self.database.commit()
            self.database.close()
            try:
                out = defaultdict(list)
                for key, val in result:
                    out[key].append(val)
                return dict(out)
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


@final
class StatusesHandler:
    def __init__(self):
        self.database: sqlite3.Connection
        self.cursor: sqlite3.Cursor

    def getStatuses(self):
        self.database = sqlite3.connect(f"{statusDataBase}")
        self.cursor = self.database.cursor()
        self.cursor.execute("SELECT status_name FROM statuses")
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        try:
            return dict(result)
        except ValueError:
            return sorted(list(map(lambda x: x[0], list(set(result)))))


@final
class AlignmentHandler:
    def __init__(self):
        self.database: sqlite3.Connection
        self.cursor: sqlite3.Cursor

    def getAlignments(self):
        self.database = sqlite3.connect(f"{alignmentDataBase}")
        self.cursor = self.database.cursor()
        self.cursor.execute("SELECT alignment_name FROM alignments")
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        try:
            return dict(result)
        except ValueError:
            return sorted(list(map(lambda x: x[0], list(set(result)))))


@final
class BackgroundHandler:
    def __init__(self):
        self.database: sqlite3.Connection
        self.cursor: sqlite3.Cursor

    def getBackgrounds(self):
        self.database = sqlite3.connect(f"{backgroundsDataBase}")
        self.cursor = self.database.cursor()
        self.cursor.execute("SELECT background_name FROM backgrounds")
        result = self.cursor.fetchall()
        self.database.commit()
        self.database.close()
        try:
            return dict(result)
        except ValueError:
            return sorted(list(map(lambda x: x[0], list(set(result)))))


if __name__ == "__main__":
    print(LevelInfoHandler().getLevelInfo("experience_to_next_level", "level_id>=2"))
