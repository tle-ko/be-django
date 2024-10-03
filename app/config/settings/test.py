from django.conf import global_settings

from config.settings.base import *


GEMINI_API_KEY = 'INVALID_API_KEY'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1odep3cb9^%i11_pxm)l&i(hjk_k3+kii7o#_qbip-ubb)rlkc"

DEBUG = True

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "/logs"

FIXTURE_DIRS = [
    *global_settings.FIXTURE_DIRS,
    BASE_DIR / "fixtures",
]

BACKGROUND_TASK_AUTO_RUN = False
