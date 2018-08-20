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
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    },
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': ['localhost:6379'],
        'TIMEOUT': 120,
        'OPTIONS': {
            'DB': 5,
        },
    }
}

TWITTER_CONSUMER_KEY = 'vYuzgkErlgcU8hLSDG0yS8gry'
TWITTER_CONSUMER_SECRET = 'U0hVZVDahNoC4r9imOPkyKLQCJE343h2YK6OcD5s47RD2tSUYK'
TWITTER_ACCESS_TOKEN_KEY = '321647013-HGaOJzhg6hfrNYfWGj1NsV6ufNLgNb2fdUbeNi2j'
TWITTER_ACCESS_TOKEN_SECRET = 'CchNp5KVcuzatUNzVZOZMOMh716CNTDoSsTGBTJg7XOhZ'
