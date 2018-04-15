#!/bin/sh

cd $HOME/liveswot-api
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
sh scripts/load-test-data.sh
python manage.py runserver
