from .core import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DOMAIN = config("LOCAL_DOMAIN")

INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _request: DEBUG}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT")
DEFAULT_FROM_EMAIL = config("EMAIL_FROM")


CELERY_BROKER_URL = config("CELERY_BROKER")

CELERY_BEAT_SCHEDULE = {
    "auto_delete_expired_tokens": {
        "task": "accounts.tasks.auto_delete_expired_tokens",
        "schedule": 15 * 60,
    },
    "auto_delete_deactive_users": {
        "task": "accounts.tasks.auto_delete_deactive_users",
        "schedule": 1 * 60,
    },
    "auto_delete_invalid_subscription": {
        "task": "memberships.tasks.auto_delete_invalid_subscription",
        "schedule": 1 * 60,
    },
    "insert_subscribers_into_db": {
        "task": "channel_subscribers.tasks.insert_subscriber_from_cache_into_db",
        "schedule": 1 * 60,
    },
    "delete_unsubscribed_from_db": {
        "task": "channel_subscribers.tasks.delete_unsubscribed_from_db",
        "schedule": 1 * 60,
    },
    "insert_vote_to_db": {
        "task": "votes.tasks.insert_vote_into_db",
        "schedule": 1 * 60,
    },
    "delete_unvoted_from_db": {
        "task": "votes.tasks.delete_unvoted_from_db",
        "schedule": 1 * 60,
    },
    "insert_viewer_to_db": {
        "task": "viewers.tasks.insert_viewer_into_db",
        "schedule": 1 * 60,
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
