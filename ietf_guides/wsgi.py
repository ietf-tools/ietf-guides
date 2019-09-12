"""
WSGI config for ietf_guides project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Virtualenv support
virtualenv_activation = os.path.join(path, "env", "bin", "activate_this.py")
if os.path.exists(virtualenv_activation):
    with open(virtualenv_activation) as f:
        code = compile(f.read(), virtualenv_activation, 'exec')
        exec(code, dict(__file__=virtualenv_activation))

if not path in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ietf_guides.settings.prod")

application = get_wsgi_application()
