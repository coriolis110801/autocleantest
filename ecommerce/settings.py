"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku
import mimetypes
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z+ksf@)0d^qojbh4rnp4b1to$hq&*tt(3bs$gf(3i267g$k9ln'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['auto-clean.herokuapp.com', 'http://127.0.0.1:8000', 'www.autosqueak.com,', 'autosqueak.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'store.apps.StoreConfig',

    'django_filters',
    'storages',
    # 'demo',
    'corsheaders',
    'captcha'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

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

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# postgres://kqzendpuwfvbcf:5033df3754758d8e4c5e0d85fbf2bde7040476433410d83341588fa84175e1a7@ec2-52-213-167-210.eu-west-1.compute.amazonaws.com:5432/dait0ccr22e706
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'demo_2', #Live_DB 下面的那个名字
        'HOST' : 'database-2.cqymlgd54l24.us-east-2.rds.amazonaws.com',  #亚马逊的数据库的url
        'PORT' : 5432,
        'USER' : 'coriolis123',   #亚马逊账户名称
        'PASSWORD' : 'Michaellie3'
    }
}

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/images/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8000',
    'http://localhost:8000'
)
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'xhr'
)


#S3 BUCKETS CONFIG

AWS_ACCESS_KEY_ID = 'AKIA4SOHMCJQR3PC67ND'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'auto-clean'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_ADDRESSING_STYLE = "virtual"
AWS_S3_REGION_NAME = "eu-west-2"

# EMail， 需要在谷歌上有个页面同意新的程序访问，然后10分钟之内就可以允许了： https://accounts.google.com/DisplayUnlockCaptcha
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lee@autosqueak.com'
EMAIL_HOST_PASSWORD = 'rfirdyzpvqbpucxo'
DEFAULT_FROM_EMAIL = 'lee@autosqueak.com'

# reCaptcha
RECAPTCHA_PUBLIC_KEY = '6LfV7VIcAAAAAEmznjWclkxmxi6XA8hLd3Cb7rT7'
RECAPTCHA_PRIVATE_KEY = '6LfV7VIcAAAAAOpznBASfYfc5bnVSH4glQlJhYKz'
# RECAPTCHA_DOMAIN = 'www.recaptcha.net'
# SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

django_heroku.settings(locals())