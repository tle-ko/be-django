#!/bin/bash
./manage.py migrate
./manage.py collectstatic --noinput

./manage.py runserver --insecure 0.0.0.0:8000
