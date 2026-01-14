from .base import *
# Pull from environment, fallback to a dummy key if missing
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-test-key-only-for-ci")

# Ensure other settings (like SimpleJWT) can see it
SIGNING_KEY = SECRET_KEY 

print("SECRET_KEY: _______---------________----", SECRET_KEY)
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
