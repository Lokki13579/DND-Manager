import json
import sqlite3
from typing import Dict, Any


def create_database_schema(conn):
    """Создает структуру таблиц в базе данных"""

    # Таблица классов
    conn.execute("""
        CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            race_name TEXT UNIQUE NOT NULL,
            speed TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS characteristics (
            char_id INTEGER PRIMARY KEY AUTOINCREMENT,
            char_name TEXT UNIQUE NOT NULL
        )
    """)

    # Таблица уровней классов
    conn.execute("""
        CREATE TABLE IF NOT EXISTS race_addictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            race_id INTEGER,
            char_id INTEGER,
            increase INTEGER,
            FOREIGN KEY (race_id) REFERENCES races (race_id),
            FOREIGN KEY (char_id) REFERENCES characteristics (char_id)
        )
    """)


def insert_races_data(conn, race_name: str, race_data: Dict[str, Any]):
    """Вставляет данные одной расы в базу"""

    # Вставляем основную расу
    cursor = conn.execute(
        "INSERT OR IGNORE INTO races (race_name, speed) VALUES (?, ?)",
        (race_name, race_data["скорость"]),
    )

    # Получаем ID расы
    race_id = cursor.lastrowid
    if race_id == 0:  # Если раса уже существует
        race_id = conn.execute(
            "SELECT race_id FROM races WHERE race_name = ?", (race_name,)
        ).fetchone()[0]

    CHARS = ["Сила", "Ловкость", "Телосложение", "Интеллект", "Мудрость", "Харизма"]
    for char in CHARS:
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO characteristics (char_name) VALUES (?)
        """,
            (char,),
        )
    for char_str, char_increase in race_data.get("УвеличениеХарактеристик", {}).items():
        print(char_str)
        char_id = conn.execute(
            "SELECT char_id FROM characteristics WHERE char_name = ?", (char_str,)
        ).fetchone()[0]
        cursor = conn.execute(
            """INSERT INTO race_addictions
               (race_id, char_id, increase)
               VALUES (?, ?, ?)""",
            (race_id, char_id, char_increase),
        )


def main():
    # Загружаем JSON данные
    with open("./JSONS/dnd_races.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Создаем базу данных
    conn = sqlite3.connect("dataBase/dnd_races.db")

    # Создаем схему
    create_database_schema(conn)

    # Вставляем данные для каждой расы
    for race_name, race_data in data.items():
        print(f"Обрабатываю расу: {race_name}")
        insert_races_data(conn, race_name, race_data)

    # Сохраняем изменения
    conn.commit()
    print("База данных успешно создана! Файл: dnd_races.db")

    # Показываем статистику
    stats = conn.execute("""
        SELECT COUNT(*) as race_count FROM races
    """).fetchone()
    print(f"Добавлено рас: {stats[0]}")

    conn.close()


if __name__ == "__main__":
    main()
