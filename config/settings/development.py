from .core import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["debug_toolbar",]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware",]

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