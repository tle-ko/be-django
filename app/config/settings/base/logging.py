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
            "format": "[{server_time}] {message}",
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
            "filters": ["require_debug_true"],
            'class': 'config.utils.FileAndStreamHandler',
            'filename': 'logs/console.log',
            "formatter": "standard",
        },
        "django.mail": {
            "level": "ERROR",
            "filters": ["require_debug_true"],
            'class': 'config.utils.FileAndStreamHandler',
            'filename': 'logs/django.mail.log',
        },
        "django.server": {
            "level": "INFO",
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/django.server.log',
            'when': 'D',
            "formatter": "django.server",
        },
        "problems": {
            "level": "INFO",
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/problems.log',
            'when': 'D',
            "formatter": "standard",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            'class': 'logging.FileHandler',
            'filename': 'logs/mail_admins.log',
        },
        "django.security.DisallowedHost": {
            "level": "INFO",
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/django.security.DisallowedHost.log',
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
        "problems": {
            "handlers": ["problems"],
            "level": "INFO",
        },
    },
}
