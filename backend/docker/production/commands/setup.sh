#!/bin/bash

echo "Apply database migrations"
python manage.py makemigrations && python manage.py migrate

echo "Running the server"
gunicorn config.wsgi --bind 0.0.0.0:8000