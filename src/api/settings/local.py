from api.settings.base import *

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CORS_ALLOW_ALL_ORIGINS = True

DEBUG = True

ALLOWED_HOSTS = ["*"]

STATIC_ROOT = "collected_static/"
MEDIA_ROOT = "media/"
