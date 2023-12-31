#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
python manage.py collectstatic --no-input
gunicorn TaskApp.wsgi:application --bind 0.0.0.0:8000


#python manage.py runserver 0.0.0.0:8000