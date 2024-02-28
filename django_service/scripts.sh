#!/bin/bash
python manage.py migrate
python manage.py collectstatic --clear
cp -r /app/collected_static/. /backend_static/

gunicorn --bind 0.0.0.0:8000 core.wsgi
