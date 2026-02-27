import os
from email.utils import parseaddr
from .base import *  # noqa
# n.b., does _not_ import from .local

def _multiline_to_list(s):
    """Helper to split at newlines and convert to list"""
    return [item.strip() for item in s.split("\n") if item.strip()]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]
assert not SECRET_KEY.startswith(
    "django-insecure"
)  # be sure we didn't get the dev secret

HASHSALT = os.environ["HASHSALT"].strip()

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = int(os.environ["EMAIL_PORT"])
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "lead@guides.ietf.org")

_admins_str = os.environ.get("ADMINS", None)
if _admins_str is not None:
    ADMINS = [parseaddr(admin) for admin in _multiline_to_list(_admins_str)]
else:
    raise RuntimeError("ADMINS must be set")

# ALLOWED_HOSTS is a newline-separated list of allowed hosts
ALLOWED_HOSTS = _multiline_to_list(os.environ["ALLOWED_HOSTS"])

# CSRF_TRUSTED_ORIGINS is a newline-separated list of allowed hosts
CSRF_TRUSTED_ORIGINS = _multiline_to_list(os.environ["CSRF_TRUSTED_ORIGINS"])

DATABASES = {
    "default": {
        "NAME": os.environ["DB_NAME"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
        "ENGINE": "django.db.backends.mysql",
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASS"],
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "ssl_mode": os.environ.get("DB_SSLMODE", "PREFERRED"),
        },
    },
}

# When running behind CloudFlare, X-Forwarded-Proto=https indicates the incoming connection was
# secure. Use that to decide whether to use http or https as the scheme when constructing absolute
# URLs instead of looking at the request.
# https://docs.djangoproject.com/en/5.0/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
