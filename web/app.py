import os
import json
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


def load_json_report(filepath):
    """Спроба завантажити JSON-звіт. Якщо його ще немає - повертає порожній словник."""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


@app.route('/')
def index():
    # Шляхи до файлів у спільному томі
    quality_report = load_json_report("/app/reports/quality_report.json")
    research_report = load_json_report("/app/reports/research_report.json")

    # Рендеримо HTML сторінку, передаючи їй дані
    return render_template('index.html',
                           quality=quality_report,
                           research=research_report)


# Спеціальний роут, щоб Flask міг віддавати картинки з папки /app/plots
@app.route('/plots/<filename>')
def get_plot(filename):
    return send_from_directory('/app/plots', filename)


if __name__ == "__main__":
    # Запуск сервера на всіх мережевих інтерфейсах (0.0.0.0), щоб він був доступний ззовні Docker
    app.run(host="0.0.0.0", port=5000)
