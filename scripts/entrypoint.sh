#!/bin/bash

pip install --no-cache-dir -r requirements.txt

./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic --noinput

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL..."
    while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

exec "$@"