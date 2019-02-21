from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Your local.py should contain the credentials needed to send email through your selected SMTP
# server. See <https://docs.djangoproject.com/en/2.1/topics/email/#obtaining-an-instance-of-an-email-backend>

