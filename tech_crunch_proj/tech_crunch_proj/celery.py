import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tech_crunch_proj.settings")

# Creating a Celery instance
celery_app = Celery("tech_crunch_proj", broker=settings.CELERY_BROKER_URL)

# Every task module from Django app configs are loading here
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# The schedule for celery beat to take action in this way
celery_app.conf.beat_schedule = {
    'scrape-remainig-daily-search-articles': {
        'task': 'techcrunch.tasks.scrape_daily_remaining_items',
        'schedule': 120,  # In Second
    },
    'scrape-remainig-keyword-search-articles': {
        'task': 'techcrunch.tasks.scrape_search_ramining_items',
        'schedule': 120,  # In Second
    },
}

# Now every celery task is auto-detected
celery_app.autodiscover_tasks()


# Commands to run for celery
# celery -A tech_crunch_proj worker -l INFO -P eventlet
# celery -A tech_crunch_proj beat --loglevel=INFO
