#!/bin/bash
set -e

trap "echo TRAPed signal" HUP INT QUIT TERM

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-ietf_guides.settings.prod}

/code/manage.py collectstatic --noinput
/code/manage.py migrate --noinput

cp /code/nginx/default /etc/nginx/sites-enabled/default
nginx

gunicorn \
  -c /code/gunicorn.conf.py \
  --bind unix:/run/gunicorn.sock \
  ${GUNICORN_EXTRA_ARGS} \
  ietf_guides.wsgi:application

echo "exited $0"
