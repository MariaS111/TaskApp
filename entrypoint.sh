#!/bin/sh

python /usr/src/taskapi/manage.py makemigrations --noinput
python /usr/src/taskapi/manage.py migrate --noinput
python /usr/src/taskapi/manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
python /usr/src/taskapi/manage.py collectstatic --no-input
python /usr/src/taskapi/manage.py runserver 0.0.0.0:8000

