#!bin/sh
# dependency: `npm install -g nodemon`

nodemon --ext py --exec "cd $HOME/liveswot-api; python manage.py test"
