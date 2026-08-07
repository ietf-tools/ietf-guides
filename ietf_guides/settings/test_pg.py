# Copyright The IETF Trust 2026, All Rights Reserved
from .base import *
from .local import *

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'test_guides'),
        'USER': os.environ.get('DB_USER', 'guides'),
        'PASSWORD': os.environ.get('DB_PASS', 'abcd1234'),
        'HOST': os.environ.get('DB_HOST', 'pgdb'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
