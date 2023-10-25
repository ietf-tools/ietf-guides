#!/bin/sh

trap "echo TRAPed signal" HUP INT QUIT TERM

if [ ! -f "/code/ietf_guides/settings/local.py" ]; then
    echo "local.py not found. Exiting."
    exit 1
fi


export DJANGO_SETTINGS_MODULE=ietf_guides.settings.prod

/code/manage.py collectstatic
/code/manage.py migrate

cp /code/nginx/default /etc/nginx/sites-enabled/default
nginx

gunicorn ietf_guides.wsgi:application --bind unix:/run/gunicorn.sock

echo "exited $0"
