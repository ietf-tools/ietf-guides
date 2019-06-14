#!/bin/bash

rm -rf /code/mod_wsgi-express-8002/regeneration
DJANGO_SETTINGS_MODULE=ietf_guides.settings.prod ./manage.py runmodwsgi --setup-only --port 8002 --user wwwrun --group www --access-log --server-root /code/mod_wsgi-express-8002/regeneration --log-directory /code/logs
echo "This directory is for comparison only. It is not used by the running server. It was created by "$0" at " `date` > /code/mod_wsgi-express-8002/regeneration/README
