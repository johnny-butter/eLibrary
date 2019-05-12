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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ot$(m)ky4w_$(*wt#ia*%y_!^1=*%3)i*gre6(m!0ifdyuzj7j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',
    'authApi',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
        'DIRS': [BASE_DIR + '/loginPage/template',
                 BASE_DIR + '/eLibrary/template', ],
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

WSGI_APPLICATION = 'eLibrary.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# db4free.net
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'elibrary',
        'USER': 'root',
        'PASSWORD': '5566rock',
        'HOST': '192.168.43.39',
        'PORT': '3306',
        # 'TEST': {
        #     # 'NAME': 'elibrary',
        # }
    }
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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


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

# Configure the authentication in Django Rest Framework to be JWT
# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

# Configure the JWTs to expire after 1 hour, and allow users to refresh near-expiration tokens
# https://getblimp.github.io/django-rest-framework-jwt/
# JWT_AUTH = {
#     # If the secret is wrong, it will raise a jwt.DecodeError telling you as such. You can still get at the payload by setting the JWT_VERIFY to False.
#     'JWT_VERIFY': True,

#     # You can turn off expiration time verification by setting JWT_VERIFY_EXPIRATION to False.
#     # If set to False, JWTs will last forever meaning a leaked token could be used by an attacker indefinitely.
#     'JWT_VERIFY_EXPIRATION': True,

#     # This is an instance of Python's datetime.timedelta. This will be added to datetime.utcnow() to set the expiration time.
#     # Default is datetime.timedelta(seconds=300)(5 minutes).
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=600),

#     'JWT_ALLOW_REFRESH': True,
#     'JWT_AUTH_HEADER_PREFIX': 'JWT',
# }

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),

    'AUTH_HEADER_TYPES': ('Bearer', 'JWT',),
}

INTERNAL_IPS = ('127.0.0.1', '192.168.43.118')
