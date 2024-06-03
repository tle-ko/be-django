#/bin/bash

REPOSITORY=$(dirname $(dirname $0))

cd $REPOSITORY/src
python manage.py runserver 0.0.0.0:80 --insecure > $REPOSITORY/.log 2>&1 &