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

export DJANGO_SETTINGS_MODULE=ietf_guides.settings.prod

sudo -E -u wwwrun ./manage.py migrate

sudo -E -u wwwrun ./manage.py collectstatic --noinput

./manage.py runmodwsgi --port 8002 --user wwwrun --group www --access-log --server-root /code/mod_wsgi-express-8002 --log-directory /code/logs

echo "exited $0"
