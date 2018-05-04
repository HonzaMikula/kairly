from .settings_dev import *  # NOQA

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'kairly',
        'USER': 'root',
        'PASSWORD': '',
        'CONN_MAX_AGE': None,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
}

MEDIA_SITE = 'http://localhost:8000'
