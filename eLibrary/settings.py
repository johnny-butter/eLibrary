"""
Django settings for eLibrary project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import datetime
import environ
from django.utils.translation import gettext_lazy as _

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, '*'),
    SECRET_KEY=(str, 'ot$(m)ky4w_$(*wt#ia*%y_!^1=*%3)i*gre6(m!0ifdyuzj7j'),
    DB=(dict, {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'elibrary',
        'USER': 'root',
        'PASSWORD': '5566rock',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        # 'TEST': {
        #     'NAME': 'elibrary',
        # }
    }),
    CACHE=(dict, {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }),
    BRAINTREE_MERCHANT_ID=(str, '2yt4756q4gnf5yd7'),
    BRAINTREE_PUBLIC_KEY=(str, 'f6hwn45pfn3xzgk8'),
    BRAINTREE_PRIVATE_KEY=(str, '08e566b7112491b6aa8327229705e97c'),
    EMAIL_BACKEND=(str, 'django.core.mail.backends.console.EmailBackend'),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
    'werkzeug_debugger_runserver',
    'django_extensions',
    'debug_toolbar',
    'rest_framework',
    'authApi',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'eLibrary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/loginPage/template',
            BASE_DIR + '/eLibrary/template',
            BASE_DIR + '/pay/template',
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


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# db4free.net
DATABASES = {
    'default': env('DB')
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
AUTH_USER_MODEL = 'authApi.User'

AUTHENTICATION_BACKENDS = ['authApi.obtainJWT.emailOrUsernameModelBackend']

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
    os.path.join(BASE_DIR, 'locale'),
]

# LOCALE_PATHS[

# ]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticFiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'eLibrary/static/js/'),
    os.path.join(BASE_DIR, 'eLibrary/static/css/'),
    os.path.join(BASE_DIR, 'eLibrary/static/img/'),
    os.path.join(BASE_DIR, 'loginPage/static/js/'),
    os.path.join(BASE_DIR, 'loginPage/static/css/'),
    os.path.join(BASE_DIR, 'loginPage/static/img/'),
)

CACHES = {
    "default": env('CACHE')
}

# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'ORDERING_PARAM': 'order',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),

    'AUTH_HEADER_TYPES': ('Bearer', 'JWT',),
}

# for django-debug-toolbar using
INTERNAL_IPS = ('127.0.0.1', '192.168.43.118')

BRAINTREE_MERCHANT_ID = env('BRAINTREE_MERCHANT_ID')
BRAINTREE_PUBLIC_KEY = env('BRAINTREE_PUBLIC_KEY')
BRAINTREE_PRIVATE_KEY = env('BRAINTREE_PRIVATE_KEY')

EMAIL_BACKEND = env('EMAIL_BACKEND')

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
CELERY_RESULT_SERIALIZER = 'json'
