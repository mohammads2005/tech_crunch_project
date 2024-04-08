import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tech_crunch_proj.settings")

# Creating a Celery instance
celery_app = Celery("tech_crunch_proj", broker=settings.CELERY_BROKER_URL)

# Every task module from Django app configs are loading here
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
