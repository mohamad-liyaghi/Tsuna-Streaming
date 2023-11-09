from .core import *

from .core import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("TEST_DATABASE_HOST"),
        "PORT": config("TEST_DATABASE_PORT"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("TEST_REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}


# TODO: Add the fixture for not sending email and remove this
DOMAIN = "test-domain.com"

# Disable Throttling
for throttle in REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]:
    REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"][throttle] = "1000/second"
