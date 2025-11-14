import sqlite3


def create_database(name: str, *columns: str, file="DND.db"):
    DATABASE = sqlite3.connect(f"dataBase/{file}")
    cursor = DATABASE.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(columns)})")
    DATABASE.commit()
    DATABASE.close()


def insert_data(name, data):
    DATABASE = sqlite3.connect("DNDManager/OtherPyFiles/DND.db")
    cursor = DATABASE.cursor()
    cursor.execute(f"INSERT INTO {name} VALUES ({', '.join(['?'] * len(data))})", data)
    DATABASE.commit()
    DATABASE.close()


def insert_spell(
    name,
    level=None,
    school=None,
    casting_time=None,
    distance=None,
    components=None,
    duration=None,
    classes=None,
    subclasses=None,
    description=None,
    file="DND.db",
):
    DATABASE = sqlite3.connect(f"dataBase/{file}")
    cursor = DATABASE.cursor()
    cursor.execute(
        "INSERT INTO Spells VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
        ),
    )
    DATABASE.commit()
    DATABASE.close()


def insert_homebrew_spell(
    name,
    level=None,
    school=None,
    casting_time=None,
    distance=None,
    components=None,
    duration=None,
    classes=None,
    subclasses=None,
    description=None,
):
    DATABASE = sqlite3.connect("DNDManager/OtherPyFiles/Homebrew.db")
    cursor = DATABASE.cursor()
    cursor.execute(
        "INSERT INTO Spells VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
        ),
    )
    DATABASE.commit()
    DATABASE.close()


def update_data(name, whatUpdate: list[str]):
    DATABASE = sqlite3.connect("DNDManager/OtherPyFiles/DND.db")
    cursor = DATABASE.cursor()
    cursor.execute(f"UPDATE {name} SET {', '.join(whatUpdate)}")
    DATABASE.commit()
    DATABASE.close()


def delete_data(name, whatDelete: str):
    DATABASE = sqlite3.connect("DNDManager/OtherPyFiles/DND.db")
    cursor = DATABASE.cursor()
    cursor.execute(f"DELETE FROM {name} WHERE {whatDelete}")
    DATABASE.commit()
    DATABASE.close()


if __name__ == "__main__":
    create_database(
        "Spells",
        "Name TEXT",
        "Level INTEGER",
        "School TEXT",
        "Casting Time TEXT",
        "Distance TEXT",
        "Components TEXT",
        "Duration TEXT",
        "Classes TEXT",
        "Subclasses TEXT",
        "Description TEXT",
    )
    create_database(
        "Characters",
        "Name TEXT",
        "Level INTEGER",
        "Experience INTEGER",
        "MasterBonus INTEGER",
        "Class TEXT",
        "HpDice TEXT",
        "Skills TEXT",
        "Race TEXT",
        "Speed TEXT",
        "Background TEXT",
        "WorldView TEXT",
        "MaxHP INTEGER",
        "CurrentHP INTEGER",
        "TempHP INTEGER",
        "DiceStats TEXT",
        "Inventory TEXT",
        "Spells TEXT",
        "OtherStats TEXT",
    )
