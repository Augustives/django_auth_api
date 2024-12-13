from api.settings.base import *

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

CORS_ALLOW_ALL_ORIGINS = True

DEBUG = True

ALLOWED_HOSTS = ["*"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

STATIC_ROOT = "collected_static/"
MEDIA_ROOT = "media/"
