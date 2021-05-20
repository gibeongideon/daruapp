from .base import *
import os
from decouple import config


SECRET_KEY = config('SECRET_KEY', default='zecredcode2021!')

DEBUG = False
ALLOWED_HOSTS = ['localhost', '198.XX.XX.XX.XX','dwinnings.com', 'www.dwinnings.com',]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],  # Set to empty string for default.
    }
}


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Celery
#CELERY_BROKER_URL = 'amqp://localhost:5672'

CELERY_BROKER_URL = 'redis://localhost:6379'
