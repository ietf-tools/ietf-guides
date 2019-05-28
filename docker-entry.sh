#!/bin/sh

trap "echo TRAPed signal" HUP INT QUIT TERM

if [ -n "${WWWRUN_UID}" ]; then
  usermod -u "${WWWRUN_UID}" wwwrun
fi

if [ -n "${WWW_GID}" ]; then
  groupmod -g "${WWW_GID}" www
fi

if [ -n "${WWWRUN_UID}" -o -n "${WWW_GID}" ]; then
  chown -R wwwrun:www /code
fi

sudo -E -u wwwrun ./manage.py migrate

./mod_wsgi-express-8002/apachectl start

echo "[hit enter key to exit] or run 'docker stop <container>'"
read

./mod_wsgi-express-8002/apachectl stop

echo "exited $0"
