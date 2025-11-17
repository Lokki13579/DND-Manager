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
    case "Linux":
        spellDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_spells.db"
        classDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_classes.db"
    case "Darwin":
        spellDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_spells.db"
        classDataBase = f"{path.expanduser('~')}/Library/Application Support/DNDManager/dnd_classes.db"
    case _:
        spellDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_spells.db"
        classDataBase = f"{path.expanduser('~')}/.config/DNDManager/dnd_classes.db"


def create_database(name: str, *columns: str, file="DND.db"):
    DATABASE = sqlite3.connect(f"dataBase/DND.db")
    cursor = DATABASE.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(columns)})")
    DATABASE.commit()
    DATABASE.close()


class SpellHandler:
    def __init__(self):
        self.database = sqlite3.connect(f"{spellDataBase}")
        self.cursor = self.database.cursor()

    def add_spell(
        self,
        name: str,
        level: int,
        school: str,
        casting_time: str,
        distance: str,
        components: str,
        duration: str,
        classes,
        subclasses,
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
        self.database = sqlite3.connect(f"{classDataBase}")
        self.cursor = self.database.cursor()
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


if __name__ == "__main__":
    print(
        ClassInfoHandler().getClassInfo(
            "hp_dice", f"class_name='{input('Enter class name:')}'"
        )
    )
