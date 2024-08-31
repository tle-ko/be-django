from config.settings.base import *


DEBUG = True

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "/logs"
