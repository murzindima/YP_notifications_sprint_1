#!/bin/bash
set -e

# Создаем базу и выполняем миграции
poetry run flask db upgrade

# Запускаем Flask-сервер
gunicorn -b 0.0.0.0:5000 app:app
