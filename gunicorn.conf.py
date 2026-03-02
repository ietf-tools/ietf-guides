# Copyright The IETF Trust 2024-2026, All Rights Reserved
"""gunicorn configuration"""
import os

# Worker config. If values are not present in the environment, uses defaults
workers = int(os.environ.get("GUNICORN_WORKERS", "1"))
max_requests = int(os.environ.get("GUNICORN_MAX_REQUESTS", "0"))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "30"))

# Logging config.
loglevel = os.environ.get("GUNICORN_LOGLEVEL", "info")
capture_output = True  # redirect stdout/stderr to errlog
accesslog = "-"  # access log -> stdout

# Log as JSON on stdout (to distinguish from Django's logs on stderr)
#
# This is applied as an update to gunicorn's glogging.CONFIG_DEFAULTS.
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
            "qualname": "gunicorn.error",
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": False,
            "qualname": "gunicorn.access",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access_json",
            "stream": "ext://sys.stdout",
        },
    },
    "formatters": {
        "json": {
            "class": "ietf_guides.utils.log.JsonFormatter",
            "style": "{",
            "format": "{asctime}{levelname}{message}{name}{process}",
        },
        "access_json": {
            "class": "ietf_guides.utils.log.GunicornRequestJsonFormatter",
            "style": "{",
            "format": "{asctime}{levelname}{message}{name}{process}",
        },
    },
}
