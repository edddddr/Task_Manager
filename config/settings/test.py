from .base import *

# Database for GitHub Actions (matches your YAML services)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Speed up tests by using a simple hasher
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Ensure tests don't try to send real emails
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
