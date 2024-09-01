from config.settings.base.core import BASE_DIR


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "standard": {
            "()": "config.utils.ColorlessServerFormatter",
            "format": "[{server_time}] [{name}] [{levelname}] {message}",
            "style": "{",
        },
        "django.server": {
            "()": "config.utils.ColorlessServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR / 'logs/django/console.log',
            'when': 'D',
            "formatter": "standard",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django/mail_admins.log',
        },
        "django.mail": {
            "level": "ERROR",
            'class': 'config.utils.FileAndStreamHandler',
            'filename': BASE_DIR / 'logs/django/mail.log',
        },
        "django.server": {
            "level": "INFO",
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR / 'logs/django/server.log',
            'when': 'D',
            "formatter": "django.server",
        },
        "django.security.DisallowedHost": {
            "level": "INFO",
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR / 'logs/django/security.DisallowedHost.log',
            'when': 'D',
            "formatter": "standard",
        },
        "background_task": {
            "level": "INFO",
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR / 'logs/app/background_task/.log',
            'when': 'D',
            "formatter": "standard",
        },
        "boj": {
            "level": "INFO",
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR / 'logs/app/boj/.log',
            'when': 'D',
            "formatter": "standard",
        },
        "problems": {
            "level": "INFO",
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR / 'logs/app/problems/.log',
            'when': 'D',
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['django.security.DisallowedHost'],
            "level": "DEBUG",
            'propagate': False,
        },
        "background_task": {
            "handlers": ["background_task"],
            "level": "INFO",
        },
        "boj": {
            "handlers": ["boj"],
            "level": "INFO",
        },
        "problems": {
            "handlers": ["problems"],
            "level": "INFO",
        },
    },
}
