import os
import time
import json
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError


def get_engine_and_wait_for_table():
    """Підключається до БД і чекає, поки data_load створить таблицю raw_data."""
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)

    # Спочатку чекаємо саму БД
    while True:
        try:
            with engine.connect():
                break
        except OperationalError:
            print("Очікування бази даних...")
            time.sleep(3)

    # Потім чекаємо появи таблиці
    inspector = inspect(engine)
    while not inspector.has_table("raw_data"):
        print("Очікування таблиці 'raw_data' від модуля data_load...")
        time.sleep(3)

    return engine


def analyze_quality():
    print("Запуск модуля data_quality_analysis...")
    engine = get_engine_and_wait_for_table()

    print("Зчитування даних з БД...")
    df = pd.read_sql_table("raw_data", engine)

    # Формуємо звіт
    report = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),  # Кількість пропусків по колонках
        "total_duplicates": int(df.duplicated().sum()),  # Кількість дублікатів
        "data_types": df.dtypes.astype(str).to_dict()  # Типи даних
    }

    # Зберігаємо звіт у папку /app/reports (це буде наш спільний Docker Volume)
    os.makedirs("/app/reports", exist_ok=True)
    report_path = "/app/reports/quality_report.json"

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(f"Звіт про якість успішно збережено у {report_path}")


if __name__ == "__main__":
    analyze_quality()
