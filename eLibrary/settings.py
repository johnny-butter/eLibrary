"""
Django settings for eLibrary project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

# https://docs.newrelic.com/docs/agents/python-agent/installation/python-agent-advanced-integration#more_help
import newrelic.agent
newrelic.agent.initialize()

import os
import environ
import rollbar
from django.utils.translation import gettext_lazy as _
# https://stackoverflow.com/questions/59719175/
from django.core.management.utils import get_random_secret_key

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, []),
    SECRET_KEY=(str, get_random_secret_key()),
    API_END_POINT=(str, 'http://127.0.0.1:8000'),

    EMAIL_BACKEND=(str, ''),
    EMAIL_HOST=(str, ''),
    EMAIL_PORT=(str, ''),
    EMAIL_HOST_USER=(str, ''),
    EMAIL_HOST_PASSWORD=(str, ''),

    REDIS_URL=(str, 'redis://127.0.0.1:6379'),

    DB_ENGINE=(str, ''),
    DB_NAME=(str, ''),
    DB_USER=(str, ''),
    DB_PASSWORD=(str, ''),
    DB_HOST=(str, ''),
    DB_PORT=(str, ''),

    CACHE_BACKEND=(str, ''),
    CACHE_LOCATION=(str, ''),
    CACHE_OPTIONS=(dict, {}),

    BRAINTREE_MERCHANT_ID=(str, ''),
    BRAINTREE_PUBLIC_KEY=(str, ''),
    BRAINTREE_PRIVATE_KEY=(str, ''),

    ROLLBAR_ACCESS_TOKEN=(str, ''),
    ROLLBAR_ENV=(str, ''),
)

# reading .env file
environ.Env.read_env()

API_END_POINT = env('API_END_POINT')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRONTEND_BASE_DIR = BASE_DIR + '/frontend'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'werkzeug_debugger_runserver',
    'django_extensions',
    'debug_toolbar',
    'rest_framework',
    'api',
    'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ROOT_URLCONF = 'eLibrary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            FRONTEND_BASE_DIR + '/login_page/template',
            FRONTEND_BASE_DIR + '/book_list/template',
            FRONTEND_BASE_DIR + '/pay/template',
            BASE_DIR + '/chat/template',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eLibrary.wsgi.application'

ASGI_APPLICATION = 'eLibrary.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [f"{env('REDIS_URL')}/3"],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# db4free.net
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        # 'TEST': {
        #     'NAME': 'elibrary',
        # }
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# Custom User model
AUTH_USER_MODEL = 'api.User'

AUTHENTICATION_BACKENDS = [
    'shared.auth_backend.emailOrUsernameModelBackend',
    'shared.auth_backend.oauthModelBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('zh-tw', _('中文繁體')),
    ('zh-hant', _('中文繁體')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'i18n'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticFiles')

STATICFILES_DIRS = (
    os.path.join(FRONTEND_BASE_DIR, 'book_list/static/js/'),
    os.path.join(FRONTEND_BASE_DIR, 'book_list/static/css/'),
    os.path.join(FRONTEND_BASE_DIR, 'book_list/static/img/'),
    os.path.join(FRONTEND_BASE_DIR, 'login_page/static/js/'),
    os.path.join(FRONTEND_BASE_DIR, 'login_page/static/css/'),
    os.path.join(FRONTEND_BASE_DIR, 'login_page/static/img/'),
    os.path.join(FRONTEND_BASE_DIR, 'pay/static/js/'),
    os.path.join(BASE_DIR, 'chat/static/css/'),
    os.path.join(BASE_DIR, 'chat/static/img/'),
)

CACHES = {
    "default": {
        "BACKEND": env('CACHE_BACKEND'),
        "LOCATION": env('CACHE_LOCATION'),
        "OPTIONS": env('CACHE_OPTIONS'),
    }
}

# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 9,
    'ORDERING_PARAM': 'order',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'shared.jwt_validate.JWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'shared.error_code.exception_handler',
}

# for django-debug-toolbar using
INTERNAL_IPS = ('127.0.0.1', '192.168.43.118')

BRAINTREE_MERCHANT_ID = env('BRAINTREE_MERCHANT_ID')
BRAINTREE_PUBLIC_KEY = env('BRAINTREE_PUBLIC_KEY')
BRAINTREE_PRIVATE_KEY = env('BRAINTREE_PRIVATE_KEY')

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

CELERY_BROKER_URL = f"{env('REDIS_URL')}/1"
CELERY_RESULT_BACKEND = f"{env('REDIS_URL')}/2"
CELERY_RESULT_SERIALIZER = 'json'

if not DEBUG:
    ROLLBAR = {
        'access_token': env('ROLLBAR_ACCESS_TOKEN'),
        'environment': env('ROLLBAR_ENV'),
        'root': BASE_DIR,
    }
    rollbar.init(**ROLLBAR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        'json_fmt': {
            '()': 'json_log_formatter.JSONFormatter',
        },
    },
    'handlers': {
        'logFile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/debug.log',
            'formatter': 'simple'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'jsonLogFile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/app.log',
            'formatter': 'json_fmt',
        },
    },
    'loggers': {
        'api': {
            'handlers': ['jsonLogFile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['logFile'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
