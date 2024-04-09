# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    """
    Please implement the database as you wish,
    or if you want to use Django's default database use the commented settings below
    """
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}


# These are the default values I used for celery, you can change it if you want
CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_TIMEZONE = "Asia/Tehran"
CELERY_TASK_TIME_LIMIT = 1800
CELERY_RESULT_BACKEND = "django-db"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
