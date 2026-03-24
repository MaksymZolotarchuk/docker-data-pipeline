import os
import time
import json
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import OperationalError


def get_engine_and_wait_for_table():
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)

    while True:
        try:
            with engine.connect():
                break
        except OperationalError:
            time.sleep(3)

    inspector = inspect(engine)
    while not inspector.has_table("raw_data"):
        time.sleep(3)

    return engine


def research_data():
    print("Запуск модуля data_research...")
    engine = get_engine_and_wait_for_table()

    df = pd.read_sql_table("raw_data", engine)

    # Обчислюємо базові статистики за допомогою методу describe()
    # Це дасть нам count, mean, std, min, 25%, 50%, 75%, max для числових колонок
    stats_df = df.describe()

    # Перетворюємо DataFrame у словник для збереження в JSON
    research_report = stats_df.to_dict()

    os.makedirs("/app/reports", exist_ok=True)
    report_path = "/app/reports/research_report.json"

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(research_report, f, indent=4, ensure_ascii=False)

    print(f"Звіт з дослідження успішно збережено у {report_path}")


if __name__ == "__main__":
    research_data()
