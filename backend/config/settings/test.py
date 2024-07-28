from .core import *

from .core import *

DEBUG = True
ALLOWED_HOSTS = ["*"]


DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
  }
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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]


DOMAIN = "test-domain.com"

# Disable Throttling
for throttle in REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]:
    REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"][throttle] = "1000/second"
