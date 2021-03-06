"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# Mode PROD or DEV
MODE = os.environ.get('SERVER_MODE', 'DEV')
print("Starting server in {m} Mode".format(m=MODE))

if MODE == 'PROD':
    # Database
    # https://docs.djangoproject.com/en/3.0/ref/settings/#databases
    __DATABASES = {
        'default' : {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'NAME': os.environ.get('DB_NAME', ''),
            'USER': os.environ.get('DB_USER', ''),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        }
    }
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    # CORS settings
    CORS_ORIGIN_ALLOW_ALL = False

    CORS_ALLOW_CREDENTIALS = True

    CORS_ORIGIN_REGEX_WHITELIST = [
        r"^https://\w+\.skyspace\.live$",
        r"^https://skyspace\.live$",
    ]

else:
    __DATABASES = {
        'default' : {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'NAME': os.environ.get('DB_NAME', ''),
            'USER': os.environ.get('DB_USER', ''),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        }
    }

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    # CORS settings
    CORS_ORIGIN_ALLOW_ALL = True

    CORS_ALLOW_CREDENTIALS = True

    
DATABASES = __DATABASES


ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'django_filters',
    'django_otp',

    'django_extensions',

    # local apps
    'space',
    'case',
    'user'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # """ uncomment below lines when you want to test in local"""
    # 'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'main.wsgi.application'


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

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'user.User'

"""Keeping it disabled for now as we don't have our User section working."""
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'resendotp': '1/min'
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': '20'
}


# Elasticsearch configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://18.193.106.215:9200'
    },
}


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f's3.us-east-2.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}'

AWS_RECORDING_BUCKET_NAME = os.environ.get('AWS_RECORDING_BUCKET_NAME')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_DEFAULT_ACL = 'public-read'
AWS_PUBLIC_MEDIA_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'main.storage_backends.PublicMediaStorage'



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=48),
    'USER_ID_FIELD': 'user_id'
}

APPEND_SLASH=False


#sendgrid email config
EMAIL_HOST = 'smtp.sendgrid.net'



EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY', )
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_FROM = os.environ.get('EMAIL_FROM')
EMAIL_BCC = os.environ.get('EMAIL_BCC')

#frontend url
FRONTEND_URL = os.environ.get('FRONTEND_URL')
#twilio configurations
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_FROM_PHONE_NUMBER = os.environ.get('TWILIO_FROM_PHONE_NUMBER')


SPACE_NAME = os.environ.get('SPACE_NAME', 'kenyacourts')
COMPANY_NAME = os.environ.get('COMPANY_NAME', 'Kenyacourts')
