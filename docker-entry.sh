#!/bin/bash
set -e

trap "echo TRAPed signal" HUP INT QUIT TERM

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-ietf_guides.settings.prod}

/code/manage.py collectstatic --noinput
/code/manage.py migrate --noinput

cp /code/nginx/default /etc/nginx/sites-enabled/default
cp /code/nginx/00logging.conf /etc/nginx/conf.d/00logging.conf

# Relay nginx's access log to our stdout. nginx runs unprivileged and so cannot
# reopen /dev/stdout, which belongs to root; it writes to this FIFO instead. The
# reader must exist before nginx opens the FIFO for writing, and opening it
# read-write (<>) keeps it from ever seeing EOF if nginx restarts.
cat <>/run/guides/access.log &

nginx

gunicorn \
  -c /code/gunicorn.conf.py \
  --bind unix:/run/guides/gunicorn.sock \
  ${GUNICORN_EXTRA_ARGS} \
  ietf_guides.wsgi:application

echo "exited $0"
