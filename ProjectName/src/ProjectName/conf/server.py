import os
from django.utils.translation import ugettext_lazy as _

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
BASE_DIR = os.path.normpath(os.path.join(PROJECT_ROOT, os.pardir, os.pardir))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

########
# Urls #
########

ALLOWED_HOSTS = ['*']
ROOT_URLCONF = '<% project_name %>.conf.urls'
STATIC_URL = '/static/'

##########
# Assets #
##########

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
ASSET_VERSION = 0

###############
# Application #
###############

WSGI_APPLICATION = '<% project_name %>.wsgi.application'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'account',
    'ordered_model',
    'semanticuiform',

    '<% project_name %>',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
    'account.middleware.ExpiredPasswordMiddleware',
]

#########
# Sites #
#########

SITE_ID = int(os.environ.get('SITE_ID', 1))
SITE_NAME = '<% project_name|title %>'
SITE_DOMAIN = '<% project_name %>.com'

########################
# Internacionalization #
########################

LANGUAGES = [
    ('en', _('English')),
    ('pl', _('Polish')),
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#############
# Templates #
#############

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'account.context_processors.account',
            ],
        },
    },
]

#########
# Cache #
#########

CACHE_VERSION = 1
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

########
# User #
########

LOGIN_URL = 'account_login'
AUTH_USER_MODEL = '<% project_name %>.User'

ACCOUNT_PASSWORD_EXPIRY = 60 * 60 * 24 * 180
ACCOUNT_PASSWORD_USE_HISTORY = True

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_NAME = '<% project_name %>sid'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

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

#########
# Email #
#########

SERVER_EMAIL = 'root@localhost'
BOT_EMAIL = 'bot@localhost'
SCRAPER_BOT_EMAIL = 'scraperbot@localhost'

EMAIL_BACKEND = 'smtp'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'root'
EMAIL_HOST_PASSWORD = 'pass'
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = '[<% project_name|title %>] '

EMAIL_BACKEND_ALIASES = {
    'smtp': 'django.core.mail.backends.smtp.EmailBackend',
    'dummy': 'django.core.mail.backends.dummy.EmailBackend',
    'console': 'django.core.mail.backends.console.EmailBackend',
}

##############
# Web Server #
##############

<% project_name|upper %>_WEB_HOST = 'localhost'
<% project_name|upper %>_WEB_PORT = 80
<% project_name|upper %>_WEB_OPTIONS = {}

###########
# Project #
###########


###########
# Logging #
###########


########
# Dead #
########
DEAD = object()
SECRET_KEY = DEAD
