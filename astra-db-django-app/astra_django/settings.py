import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%hjisw!0c0)bs&s9m#0e(#(=g54-#f+q2-d3+p%puk)0=5qrp#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'qa_app',
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

ROOT_URLCONF = 'astra_django.urls'

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

WSGI_APPLICATION = 'astra_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {

# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ASTRA_ARTIFACT_PATH = BASE_DIR / 'astra_artifacts'

# Retrieve environment variables
astra_db_secure_bundle = os.environ.get('ASTRA_DB_SECURE_BUNDLE')
astra_db_token_json = os.environ.get('ASTRA_DB_TOKEN_JSON')

# Check if the environment variables are set
if astra_db_secure_bundle is None:
    raise ValueError("The environment variable ASTRA_DB_SECURE_BUNDLE is not set.")
if astra_db_token_json is None:
    raise ValueError("The environment variable ASTRA_DB_TOKEN_JSON is not set.")

# Define paths using the environment variables
ASTRA_DB_SECURE_BUNDLE_PATH = ASTRA_ARTIFACT_PATH / astra_db_secure_bundle
ASTRA_DB_TOKEN_JSON_PATH = ASTRA_ARTIFACT_PATH / astra_db_token_json

ASTRA_DB_KEYSPACE = 'text_qa_keyspace'
ASTRA_DB_TABLE_NAME = 'text_qa_vectors'


CLOUD_CONFIG = {
  "secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH
}
    
ASTRA_DB_APPLICATION_TOKEN = astra_db_token_json

INSTALLED_APPS = ['django_cassandra_engine'] + INSTALLED_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': ASTRA_DB_KEYSPACE,
        'USER': 'token',
        'PASSWORD': ASTRA_DB_APPLICATION_TOKEN,
        'OPTIONS': {
            'connection': {
                'cloud': {
                    'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
                },
            }
        }
    }
}