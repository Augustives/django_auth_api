import os

from celery import Celery
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

environment = os.environ.get("ENVIRONMENT", "local")

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"api.settings.{environment}",
)

app = Celery("api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
