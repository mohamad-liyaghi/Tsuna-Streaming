from settings.core import *

DEBUG = True
ALLOWED_HOSTS = []

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