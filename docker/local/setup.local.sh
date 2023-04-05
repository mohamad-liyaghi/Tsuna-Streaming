#!/bin/bash

echo "Apply database migrations and runserver"
python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000