# Використовуємо полегшений офіційний образ Python
FROM python:3.10-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Спочатку копіюємо лише requirements, щоб закешувати шар встановлення залежностей
COPY requirements.txt .

# Встановлюємо бібліотеки без збереження кешу для оптимізації розміру
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код програми
COPY app.py .

# Команда для запуску скрипта
CMD ["python", "app.py"]
