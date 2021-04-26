from app import app
from flask import render_template


@app.route('/')  # Основная страница
def index():
    return render_template('index.html')


@app.errorhandler(404)  # Обработка ошибки 404
def page_404(ex):
    return render_template('404.html'), 404
