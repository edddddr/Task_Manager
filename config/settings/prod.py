# config/settings/prod.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# Production database credentials
DATABASES['default']['NAME'] = os.getenv('DB_NAME', 'task_manager')
DATABASES['default']['USER'] = os.getenv('DB_USER')
DATABASES['default']['PASSWORD'] = os.getenv('DB_PASSWORD')
DATABASES['default']['HOST'] = os.getenv('DB_HOST', 'db')
DATABASES['default']['PORT'] = os.getenv('DB_PORT', 5432)

# Email backend for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
