from .settings import *  # NOQA

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kairly',
        'USER': 'root',
        'PASSWORD': '',
        'CONN_MAX_AGE': None,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
}
