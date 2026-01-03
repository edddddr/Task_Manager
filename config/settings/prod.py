from .base import *
import os
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from decouple import config
from dotenv import load_dotenv
    

load_dotenv()

DEBUG = False

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1"
).split(",")

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600)
}


SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

sentry_sdk.init(
    dsn="https://6d0b9f6585106533cebbff123e907f26@o4510616778702848.ingest.us.sentry.io/4510616800854016",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False,
)
