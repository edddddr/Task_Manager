# config/settings/base.py
import os
from pathlib import Path
from decouple import config

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)

# APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'apps.users.apps.UsersConfig',
    'apps.tasks.apps.TasksConfig',
    'apps.projects.apps.ProjectsConfig',
    'apps.system.apps.SystemConfig',
    # "ratelimit",pip v3.11
]

##########################################
#    MIDDLEWARE                          #
##########################################

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]   

ROOT_URLCONF = 'config.urls'

##########################################
#     TEMPLATES                          #
##########################################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.-g',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]},
    },
]

##########################################
#       Database                         #
##########################################
# DATABASE (default placeholder)    
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'task_manager',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


##########################################
#       LOGGING                          #
##########################################
# LOGGING = {
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "structured",
#         },
#     },
#     "root": {
#         "handlers": ["console"],
#         "level": "INFO",
#     },
# }

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "structured": {
#             "format": (
#                 "%(asctime)s %(levelname)s %(name)s "
#                 "event=%(message)s "
#                 "user_id=%(user_id)s ip=%(ip)s success=%(success)s"
#             )
#         },
#     },

#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "structured",
#         },
#         "file": {
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "logs/app.log"),
#         },
#     },

#     "root": {
#         "handlers": ["console", "file"],
#         "level": "INFO",
#     },
# }


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(levelname)s %(name)s %(message)s %(asctime)s",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },

    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "task_manager": {   # your app namespace
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


##########################################
#       CACHES                           #
##########################################
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# Optional: Store user sessions in Redis for faster access
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


##########################################
#       Sentry                           #
##########################################
sentry_sdk.init(
    dsn="https://6d0b9f6585106533cebbff123e907f26@o4510616778702848.ingest.us.sentry.io/4510616800854016",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,  # lower in prod
    send_default_pii=False,
)

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
RATELIMIT_ENABLE = True

# Static files
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'
