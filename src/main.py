import logging
import sys
import os
from dotenv import load_dotenv
from mytools import print_2_similarity
from datetime import datetime

logging.basicConfig(level=logging.INFO)

load_dotenv()

def main() -> None:
    try:
        md: float = print_2_similarity("первый", "второй")
        print(md)
        sk = os.environ.get("SECRET_KEY", "Not found")
        print(sk)

        with open("z_key.txt", "w", encoding="utf-8") as f:
            f.write(f"{datetime.now()}\nSECRET_KEY: {sk}")

    except KeyboardInterrupt:
        logging.info("🛑 Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        logging.exception(f"❌ Критическая ошибка выполнения: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()