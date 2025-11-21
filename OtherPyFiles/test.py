import json
import sqlite3


def create_database_schema(conn):
    """Создает структуру таблиц в базе данных"""

    # Таблица классов
    conn.execute("""
        CREATE TABLE IF NOT EXISTS statuses (
            status_id INTEGER PRIMARY KEY AUTOINCREMENT,
            status_name TEXT UNIQUE NOT NULL
        )
    """)


def insert_races_data(conn, name: str):
    """Вставляет данные одной расы в базу"""

    # Вставляем основную расу
    cursor = conn.execute(
        "INSERT OR IGNORE INTO statuses (status_name) VALUES (?)",
        (name,),
    )


def main(file):
    with open(f"./JSONS/{file}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(f"dataBase/{file}.db")

    create_database_schema(conn)

    for name in data:
        print(f"Обрабатываю: {name}")
        insert_races_data(conn, name)

    conn.commit()
    print("База данных успешно создана!")

    stats = conn.execute("""
        SELECT COUNT(*) as count FROM statuses
    """).fetchone()
    print(f"Добавлено: {stats[0]}")

    conn.close()


if __name__ == "__main__":
    main(file="dnd_backgrounds")
    main(file="dnd_trinkets")
