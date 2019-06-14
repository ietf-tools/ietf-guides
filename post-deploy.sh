#!/bin/sh

export DJANGO_SETTINGS_MODULE=ietf_guides.settings.prod

sudo -E -u wwwrun ./manage.py migrate
sudo -E -u wwwrun ./manage.py collectstatic --noinput
