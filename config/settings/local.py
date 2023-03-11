from .core import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["debug_toolbar",]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware",]

DOMAIN = config("LOCAL_DOMAIN")

INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("LOCAL_DB_NAME"),
        'USER': config("LOCAL_DB_USER"),
        'PASSWORD': config("LOCAL_DB_PASSWORD"),
        'HOST': config("LOCAL_DB_HOST"),
        'PORT': config("LOCAL_DB_PORT")
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("LOCAL_EMAIL_HOST")
EMAIL_HOST_USER = config("LOCAL_EMAIL_USER")
EMAIL_HOST_PASSWORD = config("LOCAL_EMAIL_PASSWORD")
EMAIL_PORT = config("LOCAL_EMAIL_PORT")
DEFAULT_FROM_EMAIL = config("LOCAL_EMAIL_FROM")


CELERY_BROKER_URL = config("LOCAL_CELERY_BROKER")

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
        "LOCATION": config("LOCAL_CACHE_DB_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}