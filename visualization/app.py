import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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


def create_visualizations():
    print("Запуск модуля visualization...")
    engine = get_engine_and_wait_for_table()

    df = pd.read_sql_table("raw_data", engine)

    # Створюємо директорію для збереження графіків (це буде Docker Volume)
    os.makedirs("/app/plots", exist_ok=True)

    # Налаштування стилю графіків
    sns.set_theme(style="whitegrid")

    # Графік 1: Розподіл віку (Гістограма)
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="age", bins=5, kde=True, color="skyblue")
    plt.title("Розподіл віку користувачів")
    plt.xlabel("Вік")
    plt.ylabel("Кількість")
    plt.savefig("/app/plots/age_distribution.png", bbox_inches='tight')
    plt.close()
    print("Графік 1 (Розподіл віку) збережено.")

    # Графік 2: Середній бал за відділами (Bar chart)
    plt.figure(figsize=(8, 5))
    # Відкидаємо порожні значення відділів для чистоти графіка
    # Відкидаємо порожні значення для чистоти графіка
    df_clean = df.dropna(subset=['subscription_type', 'score'])
    sns.barplot(data=df_clean, x="subscription_type", y="score", errorbar=None, palette="viridis")
    plt.title("Середній бал по відділах")
    plt.xlabel("Відділ")
    plt.ylabel("Середній бал")
    plt.savefig("/app/plots/score_by_department.png", bbox_inches='tight')
    plt.close()
    print("Графік 2 (Середній бал) збережено.")


if __name__ == "__main__":
    create_visualizations()
