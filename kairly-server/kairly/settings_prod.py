from .settings import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'store4.rosti.cz',
        'NAME': 'kairly_2_265101',
        'USER': 'kairly_2_265101',
        'PASSWORD': 'RV3by6&#qg8@',
        'CONN_MAX_AGE': 570,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
}

ALLOWED_HOSTS = [
    'kairly-2648.rostiapp.cz',
    'kairly.honzamikula.cz/'
]

STATICFILES_DIRS = (
    '/srv/kairly/kairly-client/dist/static',
)

TEMPLATES[0]['DIRS'] = (
    '/srv/kairly/kairly-client/dist',
)
