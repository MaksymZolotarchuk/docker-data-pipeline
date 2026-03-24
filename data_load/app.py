import os
import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def get_db_connection():
    """Намагається підключитися до БД з механізмом повторних спроб (retry)."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("Змінна середовища DATABASE_URL не знайдена!")

    engine = create_engine(db_url)

    # Налаштування автоматичного очікування
    max_retries = 10
    retry_delay = 3  # секунди

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[Спроба {attempt}/{max_retries}] Підключення до бази даних...")
            # Тестове з'єднання
            with engine.connect() as conn:
                print("Успішно підключено до PostgreSQL!")
                return engine
        except OperationalError:
            print(f"База даних ще не готова. Очікування {retry_delay} сек...")
            time.sleep(retry_delay)

    raise ConnectionError("Не вдалося підключитися до бази даних після всіх спроб.")


def load_data():
    engine = get_db_connection()

    # Шлях до файлу. /app/data - це шлях ВСЕРЕДИНІ контейнера
    file_path = "/app/data/dataset.csv"

    print(f"Зчитування файлу {file_path}...")
    try:
        df = pd.read_csv(file_path)
        print(f"Зчитано {len(df)} рядків.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не знайдено. Перевірте налаштування томів у Docker Compose.")

    print("Завантаження даних у таблицю 'raw_data'...")
    # Записуємо дані в БД. if_exists='replace' перезапише таблицю при повторному запуску
    df.to_sql("raw_data", engine, if_exists="replace", index=False)
    print("Процес data_load успішно завершено!")


if __name__ == "__main__":
    load_data()
