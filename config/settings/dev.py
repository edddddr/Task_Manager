# config/settings/dev.py
from .base import *

DEBUG = True  # Enable debug mode
ALLOWED_HOSTS = ['*']

# Development DB (could use SQLite for simplicity)
DATABASES['default']['NAME'] = os.getenv('DB_NAME', 'task_manager_dev')

# Email backend for development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Add any dev-specific middleware or apps
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
