#!/bin/sh

cat scripts/droptables.py | python manage.py shell
cd $HOME/liveswot-api
python manage.py makemigrations
python manage.py migrate
sh scripts/load-test-data.sh
python manage.py runserver
