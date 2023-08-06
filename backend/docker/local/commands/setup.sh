#!/bin/bash

echo "Apply database migrations"
python manage.py makemigrations && python manage.py migrate

echo "Running the server"
python manage.py runserver 0.0.0.0:8000