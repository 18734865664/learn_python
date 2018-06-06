
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

import django_crontab.crontab
import djcelery
from celery import Celery, platforms

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'eot0n@m#@cpxmtd$dappr&=t1b@zehb%)rr2i8@&xx5wib8v*c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [u'*']

SESSION_COOKIE_AGE = 3600

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'pagination',
    'djcelery',
    'userauth',
    'saltminions',
    'libtools',
    'tasks',
    'dashboard',
    'codeupdates',
    'configspec',
    'workflow',
    'histrecord',
    'cms',
)

#AUTH_USER_MODEL = 'users.User'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'juziom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
#        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'juziom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'juziom',
        'USER': 'root',
        'PASSWORD': 'juziyule',
        'HOST': '192.168.10.156',
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# SaltStack API
SALT_API_URL = 'https://192.168.10.156:8888'
SALT_API_USER = 'saltapi'
SALT_API_PASSWD = 'juziyule'

# rsync
RSYNC_USER = 'synccode'
RSYNC_SERVER = '192.168.10.156'
RSYNC_PASSWD = '/etc/rsync.passwd'

CRONJOBS = (
    ('*/9 * * * *', 'libtools.cron.grains_scheduled_job'),
    ('*/10 * * * *', 'libtools.cron.minions_status_scheduled_job'),

)




platforms.C_FORCE_ROOT = True   # Running a worker with superuser privileges
djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
ELERYD_FORCE_EXECV=True
CELERY_ACKS_LATE=True
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC=False
CELERY_ACCEPT_CONTENT = ['json','pickle']
BROKER_HEARTBEAT=0
CELERYD_MAX_TASKS_PER_CHILD = 40

#MEDIA_ROOT = HERE
#MEDIA_URL = 'media'
