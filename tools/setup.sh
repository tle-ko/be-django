#/bin/bash

REPOSITORY=$(dirname $(dirname $0))

cd $REPOSITORY/src
python manage.py shell < $REPOSITORY/tools/db/setup_db.py
