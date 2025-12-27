import logging
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
from odbc_tools import load_data_to_excel
from sqllite_db_tools import init_db, get_users, print_users

logging.basicConfig(level=logging.INFO)

load_dotenv()

def save_secret_to_file(file_path: str):
    """Получает секретный ключ и записывает его в файл с меткой времени."""
    secret_key = os.environ.get("SECRET_KEY", "Not found Secret Key")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{datetime.now()}\nSECRET_KEY: {secret_key}")

    return secret_key


def main() -> None:
    try:
        # 1. Работа с секретами и файлами
        sk = save_secret_to_file("z_key.txt")
        logging.info(f"Ключ: {sk}")

        # 2.
        db_file = 'example.db'
        init_db(db_file)
        users = get_users(db_file)
        print_users(users)

        # 3.
        load_data_to_excel("Products_Report.xlsx")

    except KeyboardInterrupt:
        logging.info("🛑 Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        logging.exception(f"❌ Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
