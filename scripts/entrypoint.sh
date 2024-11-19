#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL..."
    while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

exec "$@"