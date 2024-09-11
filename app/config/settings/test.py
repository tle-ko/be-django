from config.settings.base.core import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1odep3cb9^%i11_pxm)l&i(hjk_k3+kii7o#_qbip-ubb)rlkc"

DEBUG = True

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "/logs"
