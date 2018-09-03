from .settings import *  # NOQA

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'store4.rosti.cz',
        'NAME': 'kairly_2_265101',
        'USER': 'kairly_2_265101',
        'PASSWORD': 'RV3by6&#qg8@',
        'CONN_MAX_AGE': 570,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
}

ALLOWED_HOSTS = [
    'kairly.com'
]

# STATICFILES_DIRS = (
#     '/srv/kairly/kairly-client/dist/static',
# )
#
# TEMPLATES[0]['DIRS'] = (
#     '/srv/kairly/kairly-client/dist',
# )

MEDIA_ROOT = '/srv/kairly/kairly-server/media'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

TWITTER_CONSUMER_KEY = 'vYuzgkErlgcU8hLSDG0yS8gry'
TWITTER_CONSUMER_SECRET = 'U0hVZVDahNoC4r9imOPkyKLQCJE343h2YK6OcD5s47RD2tSUYK'
TWITTER_ACCESS_TOKEN_KEY = '321647013-HGaOJzhg6hfrNYfWGj1NsV6ufNLgNb2fdUbeNi2j'
TWITTER_ACCESS_TOKEN_SECRET = 'CchNp5KVcuzatUNzVZOZMOMh716CNTDoSsTGBTJg7XOhZ'

GOOGLE_ANALYTICS_ID = 'UA-114180015-2'
