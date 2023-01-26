from settings.core import *

DEBUG = True
ALLOWED_HOSTS = []

DOMAIN = config("PRODUCTION_DOMAIN")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("PRODUCTION_DB_NAME"),
        'USER': config("PRODUCTION_DB_USER"),
        'PASSWORD': config("PRODUCTION_DB_PASSWORD"),
        'HOST': config("PRODUCTION_DB_HOST"),
        'PORT': config("PRODUCTION_DB_PORT")
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("PRODUCTION_EMAIL_HOST")
EMAIL_HOST_USER = config("PRODUCTION_EMAIL_USER")
EMAIL_HOST_PASSWORD = config("PRODUCTION_EMAIL_PASSWORD")
EMAIL_PORT = config("PRODUCTION_EMAIL_PORT")
DEFAULT_FROM_EMAIL = config("PRODUCTION_EMAIL_FROM")


CELERY_BROKER_URL = config("PRODUCTION_CELERY_BROKER")

CELERY_BEAT_SCHEDULE = {
    "auto_delete_expired_tokens":{
        "task" : "accounts.tasks.auto_delete_expired_tokens",
        "schedule" : 15 * 60
    },
    "auto_delete_deactive_users":{
        "task" : "accounts.tasks.auto_delete_deactive_users",
        "schedule" : 1 * 60 * 60 * 24
    }, 
    "auto_delete_invalid_subscription":{
        "task" : "accounts.tasks.auto_delete_invalid_subscription",
        "schedule" : 1 * 60 * 60 * 24
    }, 

}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("PRODUCTION_CACHE_DB_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}