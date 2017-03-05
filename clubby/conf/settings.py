"""
Django settings for cinema_clubby project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dsk)xe!$5mc$66qy5f_^shcah13@=la2&dl7#tvosda7%3tva@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
USE_HTTPS = False

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'profiles.User'

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.postgres",
    # 'django_extensions'
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    'oauth2_provider',
    'django_crontab',
    'import_export',
    'rangefilter',
    'django_smtp_ssl',
    'social.apps.django_app.default',
    'rest_framework_social_oauth2',
    'corsheaders',
]

LOCAL_APPS = [
     "profiles",
     "core",
     "external_api",
     "api"
]


INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'clubby.urls'

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

WSGI_APPLICATION = 'clubby.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'clubby',
        'USER': 'clubby',
        'PASSWORD': 'clubby',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '',
    }
}


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'statics')
#STATIC_ROOT = '/statics/'


STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static'),
)

#if DEBUG:
 #  STATIC_ROOT = os.path.join(BASE_DIR, '/statics')
#else:
 #  STATIC_ROOT = os.path.join(BASE_DIR, 'statics')



STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'compressor.finders.CompressorFinder',
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'




TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.request",
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
            'debug': True
        },
    },
]


OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'},
    'ACCESS_TOKEN_EXPIRE_SECONDS': 86400  # TODO: revert to 1 week once refresh token is implemented
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    )
}

AUTHENTICATION_BACKENDS = (
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',

    # Facebook OAuth2
    # 'social.backends.facebook.FacebookAppOAuth2',
    # 'social.backends.facebook.FacebookOAuth2',

    # google oAuth2
    # 'social.backends.google.GooglePlusAuth',
    'social.backends.google.GoogleOAuth2',
    # 'social.backends.google.GoogleOpenId',

    # twitter
    # 'social.backends.twitter.TwitterOAuth',

)


EMAIL_BACKEND='django_smtp_ssl.SSLEmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'jineshpaul89@gmail.com'
EMAIL_HOST_PASSWORD = 'jinbin1403'
DEFAULT_FROM_EMAIL = 'jineshpaul89@gmail.com'


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

CLIENT_ID = "zTfCegJvxFQE1yxb2ga7sXHPwptm0im78dmFP6AD"
CLIENT_SECRET = "IecZLwFOrOmncFgBXBst38DmY5UJhioVcUSbZvYE19Esr9zOBMaW0HnstnzRXYmKZGCQoixgyhEfXKl5xx97rnqrUkWxX13oGgOmWi3qYMjWyFQKo5l3ydytkwMHiWNj"


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


try:
    from .local_settings import *
    # you can add SITE_BASE_URL = "localhost:8000" in a file called local_settings.py
except:
    # Ideally this should be the base url of the site since there is no domain name its like this
    BASE_URL = "http://ec2-35-154-167-9.ap-south-1.compute.amazonaws.com/"
    SITE_BASE_URL = "http://ec2-35-154-167-9.ap-south-1.compute.amazonaws.com/"
    LOGIN_URL = "http://ec2-35-154-167-9.ap-south-1.compute.amazonaws.com/"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

