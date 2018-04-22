#!/bin/sh

# this script assumes that all required environment vars are populated in /etc/liveswot-api-env-vars/ as independent files
# it also assumes that gunicorn and nginx are setup properly

# reload gunicorn settings
systemctl daemon-reload

#restart gunicorn
systemctl restart gunicorn

#restart nginx
systemctl restart nginx
