# config/settings/dev.py
import os

from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = True  # Enable debug mode
# ALLOWED_HOSTS = ['*']

# Development DB (could use SQLite for simplicity)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "task_manager_dev",  # The name of your database
        "USER": "postgres",  # The PostgreSQL username
        "PASSWORD": "password",  # The user's password
        "HOST": "localhost",  # Set to an IP address or hostname for remote databases
        "PORT": "5432",  # Set to the port number (defaults to 5432 if empty)
    }
}

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")


# Email backend for development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Add any dev-specific middleware or apps
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# sentry_sdk.init(
#     dsn="", # no sentry in dev
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=0.0,
#     send_default_pii=False,
# )
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}