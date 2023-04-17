from pathlib import Path
from decouple import Config, RepositoryEnv
import os, sys
from datetime import timedelta


DJANGO_SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")


if DJANGO_SETTINGS_MODULE == 'config.settings.local':
    config = Config(RepositoryEnv('.env.local'))

else:
    config = Config(RepositoryEnv('.env.prod'))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")
# default v1 application location
sys.path.insert(0, os.path.join(BASE_DIR, 'v1'))


LOCAL_APPS = [
    'v1.accounts.apps.AccountsConfig',
    'v1.memberships.apps.MembershipsConfig',

    'v1.channels.apps.ChannelsConfig',
    'v1.channel_admins.apps.ChannelAdminsConfig',
    'v1.channel_subscribers.apps.ChannelSubscribersConfig',

    'v1.videos.apps.VideosConfig',
    'v1.musics.apps.MusicsConfig',
    
    'v1.votes.apps.VotesConfig',
    'v1.comments.apps.CommentsConfig',
    'v1.viewers.apps.ViewersConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'django_filters',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

    # pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 15,
    
    # Filtering
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_THROTTLE_CLASSES': [
        'v1.accounts.throttling.AuthenticationThrottle',
        'v1.videos.throttling.VideoThrottle',
    ], 

    'DEFAULT_THROTTLE_RATES': {
        'authentication' : '5/minute',
        'video' : '40/minute',
    }
}

# Docs related to endpoints
SPECTACULAR_SETTINGS = {
    'TITLE': 'Tsuna Streaming',
    'DESCRIPTION': 'A Video streaming api',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,    
}


AUTH_USER_MODEL = "accounts.Account"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}