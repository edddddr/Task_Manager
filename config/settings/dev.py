# config/settings/dev.py
from .base import *
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = True  # Enable debug mode
# ALLOWED_HOSTS = ['*']

# Development DB (could use SQLite for simplicity)
DATABASES = os.getenv('DB_NAME', 'task_manager_dev')
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Email backend for development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Add any dev-specific middleware or apps
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

sentry_sdk.init(
    dsn="",  # no sentry in dev
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.0,
    send_default_pii=False,
)