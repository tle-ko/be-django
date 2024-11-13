#!/bin/bash
./manage.py migrate
./manage.py collectstatic --noinput

uwsgi --http :8000 --home /venv/ --chdir /app/ -w config.wsgi
