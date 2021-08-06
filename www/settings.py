"""
Django settings for www project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r%a(gvrf8k)t!gy7dvg59od=9z&#8^!udgbt2$+mw07^*_iutc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    'django-web',
    'web',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'compressor',
    'es_user',
    'es_common',
    'kafka_example',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_vouch_proxy_auth.middleware.VouchProxyMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django_vouch_proxy_auth.backends.VouchProxyUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'www.urls'

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

WSGI_APPLICATION = 'www.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

def yesno(val):
    return val and str(val).lower()[0] in 'yt1'

# Use postgres if defined, otherwise fall back to safe

if yesno(os.getenv('DJANGO_POSTGRES')) and os.getenv('POSTGRES_DB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'postgres'),
            'HOST': os.getenv('POSTGRES_HOST', 'postgres'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
            'USER': os.getenv('POSTGRES_USER', 'es_django'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'es_django'),
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        },
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

VOUCH_PROXY_VALIDATE_ENDPOINT = 'http://vouch-proxy:9090/validate'
VOUCH_PROXY_VERIFY_SSL = False
VOUCH_PROXY_CREATE_UNKNOWN_USER = True
# VOUCH_PROXY_CACHE_TIMEOUT = 3600

# Redirect to user home after login by default
LOGIN_REDIRECT_URL = 'user-home'
# Django view name of the login page
LOGIN_URL = 'user-login'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Everything in UTC
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = Path(os.getenv("STATIC_ROOT", "/web-static"))

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging configuration
# https://docs.djangoproject.com/en/3.2/topics/logging/#configuring-logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
        'verbose': {
            'format': '[%(asctime)s] level=%(levelname)s name=%(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# Try to add prometheus monitoring (but only if running!)
try:
    if yesno(os.getenv('DJANGO_PROMETHEUS')):
        import django_prometheus  # NOQA
        INSTALLED_APPS += (
            'django_prometheus',
        )
        MIDDLEWARE = [
            'django_prometheus.middleware.PrometheusBeforeMiddleware',
        ] + MIDDLEWARE + [
            'django_prometheus.middleware.PrometheusAfterMiddleware',
        ]
        DATABASES['default']['ENGINE'] = 'django_prometheus.db.backends.postgresql'
        # Under gunicorn, we actually have multiple processes, so each one needs its own port
        PROMETHEUS_METRICS_EXPORT_PORT_RANGE = range(9000, 9004)
except Exception as e:
    print(e)
    pass


# Example app config
KAFKA_EXAMPLE_TOPIC = "test_provenance"

# CSS compilers

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# Open CORS headers
CORS_ALLOW_ALL_ORIGINS = True
