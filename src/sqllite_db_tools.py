import logging
import sqlite3

def init_db(db_name: str):
    user_name = 'Professional'
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')

        # Проверяем, есть ли уже такое имя
        cursor.execute('SELECT id FROM users WHERE name = ?', (user_name,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute('INSERT INTO users (name) VALUES (?)', (user_name,))
            logging.info(f"Пользователь {user_name} добавлен.")
        else:
            logging.info(f"Пользователь {user_name} уже есть в базе.")

def get_users(db_name: str):
    """Выполняет запрос SELECT и возвращает всех пользователей."""
    with sqlite3.connect(db_name) as conn:
        # Установка row_factory позволяет обращаться к полям по именам, а не только по индексам
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT id, name FROM users')
        rows = cursor.fetchall()

        return rows

def print_users(users):
    """Красиво печатает список пользователей."""
    logging.info("\n--- Список пользователей в БД ---")
    for user in users:
        logging.info(f"ID: {user['id']} | Имя: {user['name']}")
