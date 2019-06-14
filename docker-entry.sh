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

if [ ! -f "ietf_guides/settings/local.py" ]; then
    echo "local.py not found. Exiting."
    exit 1
fi

if [ ! -d "mod_wsgi-express-8002" ]; then
    echo "mod_wsgi-express-8002 not found. Exiting."
    exit 1
fi

export DJANGO_SETTINGS_MODULE=ietf_guides.settings.prod

./mod_wsgi-express-8002/apachectl start

echo "Successfully started. [hit enter key to exit] or run 'docker stop <container>'"
read

./mod_wsgi-express-8002/apachectl stop

echo "exited $0"
