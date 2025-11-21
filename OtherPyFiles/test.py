import json
import sqlite3


def create_database_schema(conn, file):
    """Создает структуру таблиц в базе данных"""

    # Таблица классов
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {file.replace("dnd_", "")} (
            level_id INTEGER PRIMARY KEY AUTOINCREMENT,
            experience TEXT NOT NULL,
            master_bonus TEXT NOT NULL
        )
    """)


def insert_races_data(conn, name: str, *value):
    """Вставляет данные одной расы в базу"""

    print(value)
    # Вставляем основную расу
    cursor = conn.execute(
        "INSERT OR IGNORE INTO levels (level_id, experience, master_bonus) VALUES (?, ?, ?)",
        (name, *value),
    )


def main(file):
    with open(f"./JSONS/{file}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(f"dataBase/{file}.db")

    create_database_schema(conn, file)

    for name, value in data.items():
        print(f"Обрабатываю: {name} - {value}")
        insert_races_data(conn, name, *list(value.values()))

    conn.commit()
    print("База данных успешно создана!")

    stats = conn.execute("""
        SELECT COUNT(*) as count FROM drugs
    """).fetchone()
    print(f"Добавлено: {stats[0]}")

    conn.close()


if __name__ == "__main__":
    main(file="dnd_levels")
