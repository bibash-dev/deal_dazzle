import os
from decouple import config
from .base import *


DEBUG = False

ADMINS = [
    ('Bibash B', 'admin@dealdazzle.com'),
]

ALLOWED_HOSTS = ['*']

# Database settings
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config('POSTGRES_DB'),
        "USER": config('POSTGRES_USER'),
        "PASSWORD": config('POSTGRES_PASSWORD'),
        "HOST": config('POSTGRES_HOST'),
        "PORT": config('POSTGRES_PORT', cast=int),
    }
}

# Security
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True



# Celery configuration
CELERY_BROKER_URL = f'amqp://{config('RABBITMQ_USER')}:{config('RABBITMQ_PASSWORD')}@rabbitmq:5672//'

# Redis configuration
REDIS_HOST = config('REDIS_HOST', default='redis')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_DB = config('REDIS_DB', default=1, cast=int)
